# coding=utf-8
'''
@ Summary: 
@ Update:  

@ file:    generate_rt_ai_model_h.py
@ version: 1.0.0

@ Author:  Lebhoryi@gmail.com
@ Date:    2021/2/4 16:32
'''
import os
import sys
import logging
from pathlib import Path

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, '../../'))

from platforms.plugin_k210 import plugin_k210_parser


def multiple_inputs_and_outputs(rt_ai, inputs, num):
    """ add input num, default is one input output """
    # 1. copy raw input/output
    rt_ai *= num

    # 2. replace default index(1) with true index
    for i in range(1, num):
        rt_ai[2*i] = rt_ai[2*i].replace("1", str(i+1))
        rt_ai[2*i + 1] = rt_ai[2*i + 1].replace("1", str(i+1))

    return rt_ai


def handle_in_out(rt_ai_info, model_info, rt_ai_in_out, nncase_out):
    # the input/outpus numbers
    in_out_nums = len(nncase_out)

    # save rt ai total size bytes
    total_size = list()
    for index, key in enumerate(rt_ai_info.keys()):
        if index == 0:
            rt_ai_info[key] = f"{rt_ai_info[key]}({in_out_nums})\n\n"
            model_info.append(rt_ai_info[key])
        elif index == 1:
            for inputs_index in range(in_out_nums):
                rt_ai_in_out[2*inputs_index] = f"{rt_ai_in_out[2*inputs_index]}{nncase_out[inputs_index]}\n"
                rt_ai_in_out[2*inputs_index+1] = f"{rt_ai_in_out[2*inputs_index+1]}({nncase_out[inputs_index]} * 4)\n"
                model_info += [rt_ai_in_out[2*inputs_index], rt_ai_in_out[2*inputs_index+1]]
        elif index == 2:
            for inputs_index in range(in_out_nums):
                total_size.append(f"({nncase_out[inputs_index]} * 4)")
                rt_ai_info[key].append(f"\t({nncase_out[inputs_index]} * 4) ,\t\\\n")
            model_info += rt_ai_info[key]
            model_info.append("}\n\n")
        elif index == 3:
            total_size = "(" + " + ".join(total_size) + ")" if in_out_nums > 1 else total_size[0]

            model_info.append(f"{rt_ai_info[key]}{total_size}\n\n\n")

    return model_info


def get_io(line, io="output"):
    # N, C, H, W
    io_shape = line.strip().split()[-1]
    io_shape_list = io_shape.replace('x', ' * ')
    return f"({io_shape_list})"


def rt_ai_model_gen(convert_report, project, model_name):
    """ generate rt_ai_<model_name>_model.h """
    # work buffer
    work_buffer = 0

    # inputs & outputs from nncase
    inputs, outputs = list(), list()

    with open(convert_report, "r+") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if "Working memory usage" in line:
            work_buffer = line.strip().split()[-2]
        elif "INPUTS" in line:
            for j in range(i+1, len(lines)):
                if "OUTPUTS" in lines[j]:
                    break
                inputs.append(get_io(lines[j]))
        elif "OUTPUTS" in line:
            for j in range(i+1, len(lines)):
                if not lines[j]:
                    break
                outputs.append(get_io(lines[j]))

    inputs_num, outputs_num = len(inputs), len(outputs)

    # saved work_buffer/inputs/outputs
    parser_in_convert, rt_ai_info, model_name_upper = plugin_k210_parser.model_info(model_name, work_buffer)

    # rt ai input/output info
    rt_ai_input_info = rt_ai_info["input_info"]
    rt_ai_output_info = rt_ai_info["output_info"]

    # one or more inputs/outputs
    rt_ai_inputs = rt_ai_input_info["inputs"]
    rt_ai_outputs = rt_ai_output_info["outputs"]

    # save the new model info
    model_info = rt_ai_info["head_info"]

    if inputs_num > 1:
        rt_ai_inputs = multiple_inputs_and_outputs(rt_ai_inputs, inputs, inputs_num)

    if outputs_num > 1:
        rt_ai_outputs = multiple_inputs_and_outputs(rt_ai_outputs, outputs, outputs_num)

    model_info = handle_in_out(rt_ai_input_info, model_info, rt_ai_inputs, inputs)
    model_info = handle_in_out(rt_ai_output_info, model_info, rt_ai_outputs, outputs)

    model_info += rt_ai_info["tail_info"]

    # project/applications/<model>.h
    pro_app_model_h = Path(project) / f"applications/rt_ai_{model_name}_model.h"

    if pro_app_model_h.exists():  pro_app_model_h.unlink()

    with open(pro_app_model_h, "w+") as f:
        f.write("".join(model_info))

    logging.info(f"Generate rt_ai_{model_name}_model.h successfully...")

    return model_info


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    convert_info = ""
    tmp_project = Path("tmp_cwd")
    app_path = tmp_project / "applications"

    if not app_path.exists():
        app_path.mkdir(parents=True)

    report = "./convert_report.txt"
    _ = rt_ai_model_gen(report, tmp_project, "facelandmark")