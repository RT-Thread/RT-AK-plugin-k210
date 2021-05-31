# coding=utf-8
'''
@ Summary: how to use k210
@ Update:

@ file:    k210.py
@ version: 1.0.0

@ Author:  Lebhoryi@gmail.com
@ Date:    2021/2/5 11:44

@ Update:  Load rt_ai_<model_name>_model.c from Documents to projects/applications
            将会被移除，在稳定版
@ Date:    2021/02/23
'''
import os
import sys
import re
import logging
import subprocess
from pathlib import Path

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, '../../'))

from platforms.plugin_k210 import generate_rt_ai_model_h


class Plugin(object):
    def __init__(self, opt):
        # aitools base parsers
        self.project = opt.project
        self.model_path = opt.model
        self.platform = opt.platform

        # plugin_k210 parser
        self.embed_gcc = opt.embed_gcc
        self.ext_tools = opt.ext_tools
        self.inference_type = opt.inference_type
        self.dataset = opt.dataset
        self.dataset_format = opt.dataset_format
        self.rt_ai_example = opt.rt_ai_example
        self.convert_report = opt.convert_report
        self.model_types = opt.model_types
        self.network = opt.network
        self.clear = opt.clear

        kmodel_name = self.is_support_model_type(self.model_types, self.model_path)
        self.kmodel_name = opt.model_name if opt.model_name else kmodel_name
        self.kmodel_path = Path(__file__).parent / f"{self.kmodel_name}.kmodel"


    def is_support_model_type(self, model_types, model):
        supported_model = model_types.split()
        model = Path(model)
        assert model.suffix[1:] in supported_model, f"The {model.name} is not supported now!!!"

        logging.info(f"The model is {model.name}")
        return model.stem


    def excute_cmd(self, cmd, is_realtime=False):
        """ Returnning string after the command is executed """
        result = list()
        screenData = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        if is_realtime:
            while True:
                line = screenData.stdout.readline()
                line_str = line.decode('utf-8').strip()
                result.append(line_str)
                print(f"\t{line_str}")
                if line == b'' or subprocess.Popen.poll(screenData) == 0:
                    screenData.stdout.close()
                    break
        else:
            result.append(screenData.stdout.read())
            screenData.stdout.close()
        return result


    def set_env(self, ncc_path):
        """ set ncc.exe path """
        assert Path(ncc_path).exists(), "No {} here".format(ncc_path)

        # set nncase env
        os.environ["PATH"] += (";" + ncc_path)

        # validate
        ncc_info = self.excute_cmd("ncc --version")
        if not ncc_info:
            raise Exception("Set nncase env wrong！！！")
        logging.info(f"ncc {ncc_info[0]}...")

        return ncc_info


    def convert_kmodel(self, model, kmodel_path, inference_type, dataset, dataset_format,
                       convert_report):
        """ convert your model to kmodel"""
        model = Path(model)
        assert model.exists(), FileNotFoundError("No model found, pls check the model path!!!")

        # kmodel path
        base_cmd = f"ncc compile {model} {kmodel_path} -i {model.suffix[1:]} -t k210 " \
                   f"--inference-type " \
                   f"{inference_type}"
        convert_cmd = base_cmd if inference_type == "float" \
            else f"{base_cmd} --dataset {dataset} --dataset-format {dataset_format}"

        cmd_out = self.excute_cmd(convert_cmd, is_realtime=True)
        report = "\n".join(cmd_out)

        with open(convert_report, "w+") as f:
            f.write(report)

        logging.info("Convert model to kmodel successfully...")


    def hex_read_model(self, kmodel_path, project, model):
        """ save model with hex """
        output_path = Path(project) / "applications"

        f = open(kmodel_path, "rb")
        # lenth of bytes
        count_bytes = 0
        s = f.read(1)

        # save file contects, hexadecimal
        result = list()
        while s:
            byte = ord(s)
            count_bytes += 1
            result.append("0x%02x, " % (byte))
            if count_bytes % 12 == 0:
                result.append("\n")
            s = f.read(1)
        f.close()

        head = f"unsigned char {kmodel_path.stem}_kmodel[] = {'{'}\n"
        tail = f"unsigned int {kmodel_path.stem}_{kmodel_path.suffix[1:]}_len = {count_bytes};\n"

        result = [head] + result + ["};\n"] + [tail]

        # hex kmodel
        model_c = output_path / (f"{model}_kmodel.c")

        with model_c.open("w+") as fw:
            fw.write("".join(result))

        logging.info("Save hex kmodel successfully...")

        return result


    def update_network_name(self, info_file, new_example_file, default_name, model_name):
        """ replace old_name by new_name """
        # load file
        with info_file.open() as fr:
            lines = fr.read()

        if default_name != model_name:
            old_name_list = [default_name, default_name.upper()]
            new_name_list = [model_name, model_name.upper()]

            # replace file
            for i in range(len(old_name_list)):
                lines = re.sub(old_name_list[i], new_name_list[i], lines)

        # save new example file
        with new_example_file.open("w") as fw:
            fw.write(lines)

        return new_example_file


    def load_rt_ai_example(self, rt_ai_example, project, old_name, new_name, platform):
        """ load rt_ai_<model_name>_model.c from Documents"""
        rt_ai_example = Path(rt_ai_example)

        # k210.c
        k210_c_file = rt_ai_example / f"{platform}.c"

        # network info
        example_file = Path(project) / f"applications/rt_ai_{new_name}_model.c"

        if example_file.exists():
            example_file.unlink()
        self.update_network_name(k210_c_file, example_file, old_name, new_name)

        logging.info("Generate rt_ai_facelandmark_model.c successfully...")


    def set_gcc_path(self, project, embed_gcc):
        """ set GNU Compiler Toolchain """
        def clear_gcc_path(lines, index=0):
            while (index < len(lines)):
                if "os.environ['RTT_EXEC_PATH']" in lines[index]:
                    lines.remove(lines[index])
                    break
                index += 1
            return lines

        rtconfig_py = os.path.join(project, "rtconfig.py")
        with open(rtconfig_py, "r+") as fr:
            lines = fr.readlines()
        lines = clear_gcc_path(lines)
        if embed_gcc:
            assert os.path.exists(embed_gcc), "No GNU Compiler Toolchain found???"
            set_embed_gcc_env = f"os.environ['RTT_EXEC_PATH'] = r'{embed_gcc}'"

            for index, line in enumerate(lines):
                if "RTT_EXEC_PATH" in line:
                    lines = lines[:index - 1] + ["\n", set_embed_gcc_env, "\n"] + lines[index:]
                    break

        with open(rtconfig_py, "w+") as fw:
            fw.write("".join(lines))

        logging.info("Set GNU Compiler Toolchain successfully...")


    def run_plugin(self):
        # 1. set nncase env
        self.set_env(self.ext_tools)

        # 2.1 convert model to kmodel
        self.convert_kmodel(self.model_path, self.kmodel_path, self.inference_type, self.dataset,
                            self.dataset_format, self.convert_report)

        # 2.2 save kmodel with hex
        self.hex_read_model(self.kmodel_path, self.project, self.kmodel_name)


        # 3.1 generate rt_ai_<model_name>_model.h
        _ = generate_rt_ai_model_h.rt_ai_model_gen(self.convert_report, self.project, self.kmodel_name)

        # 3.2 laod rt_ai_<model_name>_model.c
        self.load_rt_ai_example(self.rt_ai_example, self.project, self.network, self.kmodel_name, self.platform)


        # 4. set GNU Compiler Toolchain
        self.set_gcc_path(self.project, self.embed_gcc)


        # 5. remove convert_report.txt or not
        if os.path.exists(self.convert_report) and self.clear:
            os.remove(self.convert_report)
            os.remove(self.kmodel_path)

        return True


if __name__ == "__main__":
    import shutil
    logging.getLogger().setLevel(logging.INFO)

    tmp_project = Path("tmp_cwd")
    app_path = tmp_project / "applications"
    config_path = "D:\Project\K210_Demo\PersonDetection\k210-person-template/rtconfig.py"


    if not app_path.exists():
        app_path.mkdir(parents=True)
    shutil.copy(config_path, tmp_project)

    class Opt():
        def __init__(self):
            self.project = r"tmp_cwd"
            self.model = "../../Model/facelandmark.tflite"
            self.platform = "k210"
            self.rt_ai_example = "../../Documents"
            self.model_name = "facelandmark"

            # k210
            self.embed_gcc = r"D:\Project\k210_third_tools\xpack-riscv-none-embed-gcc-8.3.0-1.2\bin"
            self.ext_tools = r"./k_tools"
            self.inference_type = "uint8"
            self.model_types = "tflite caffe onnx"
            self.dataset_format = "image"
            self.convert_report = "./convert_report.txt"
            self.dataset = "./datasets/images"
            self.network = "facelandmark"
            self.clear = False

    opt = Opt()
    k210 = Plugin(opt)
    _ = k210.run_plugin()
