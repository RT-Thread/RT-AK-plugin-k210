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
        self.project = opt.project
        self.model_path = opt.model
        self.platform = opt.platform
        self.rt_ai_example = opt.rt_ai_example

        self.ext_tools = opt.ext_tools
        self.embed_gcc = opt.embed_gcc
        self.dataset = opt.dataset
        self.convert_report = opt.convert_report
        self.model_types = opt.model_types
        self.flag = opt.flag
        self.network = opt.network

        kmodel_name = self.is_support_model_type(self.model_types, self.model_path)
        self.kmodel_name = opt.model_name if opt.model_name else kmodel_name


    def is_support_model_type(self, model_types, model):
        supported_model = model_types.split()
        model = Path(model)
        assert model.suffix[1:] in supported_model, f"The {model.name} is not surpported now!!!"

        logging.info(f"The model is {model.name}")
        return model.stem


    def excute_cmd(self, cmd):
        """ Returnning string after the command is executed """
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
        return p.read()


    def set_env(self, ncc_path):
        """ set ncc.exe path """
        assert Path(ncc_path).exists(), "No {} here".format(ncc_path)

        # set nncase env
        os.environ["PATH"] += (";" + ncc_path)

        # validate
        ncc_info = self.excute_cmd("ncc --version")
        ncc_info = ncc_info.decode("utf-8")
        if not ncc_info:
            raise Exception("Set nncase env wrong！！！")
        logging.info(f"ncc {str(ncc_info)}")

        return ncc_info


    def convert_kmodel(self, model, project, dataset, kmodel_name, convert_report):
        """ convert your model to kmodel"""
        model, project = Path(model), Path(project)

        assert model.exists(), FileNotFoundError("No model found, pls check the model path!!!")

        # kmodel path
        output_model = project / f"applications/{kmodel_name}.kmodel"

        convert_cmd = f"ncc compile {model} {output_model} -i {model.suffix[1:]} -t k210 " \
                      f"--inference-type uint8 --dataset {dataset}"
        cmd_out = self.excute_cmd(convert_cmd)

        with open(convert_report, "wb+") as f:
            f.write(cmd_out)

        logging.info("Convert model to kmodel successfully...")

        return output_model


    def hex_read_model(self, project, model):
        """ save model with hex """
        model_path = Path(project) / f"applications/{model}.kmodel"
        output_path = Path(model_path.parent)


        f = open(model_path, "rb")
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

        head = f"unsigned char {model_path.stem}_kmodel[] = {'{'}\n"
        tail = f"unsigned int {model_path.stem}_{model_path.suffix[1:]}_len = {count_bytes};\n"

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
        assert os.path.exists(embed_gcc), "No GNU Compiler Toolchain found???"

        rtconfig_py = os.path.join(project, "rtconfig.py")
        with open(rtconfig_py, "r+") as fr:
            lines = fr.readlines()

        set_embed_gcc_env = f"\nos.environ['RTT_EXEC_PATH'] = r'{embed_gcc}'\n"

        if set_embed_gcc_env in lines:
            logging.info("Don't set GNU Compiler Toolchain again...")
            return
        for index, line in enumerate(lines):
            if "RTT_EXEC_PATH" in line:
                lines = lines[:index - 1] + [set_embed_gcc_env] + lines[index:]
                break

        with open(rtconfig_py, "w+") as fw:
            fw.write("".join(lines))

        logging.info("Set GNU Compiler Toolchain successfully...")


    def run_plugin(self):
        # 1. set nncase env
        self.set_env(self.ext_tools)

        # # 2.1 convert model to kmodel
        # kmodel_path = self.convert_kmodel(self.model_path, self.project, self.dataset, self.kmodel_name, self.convert_report)

        # 2.2 save kmodel with hex
        self.hex_read_model(self.project, self.kmodel_name)


        # 3.1 generate rt_ai_<model_name>_model.h
        _ = generate_rt_ai_model_h.rt_ai_model_gen(self.convert_report, self.project, self.kmodel_name)

        # 3.2 laod rt_ai_<model_name>_model.c
        self.load_rt_ai_example(self.rt_ai_example, self.project, self.network, self.kmodel_name, self.platform)


        # 4. set GNU Compiler Toolchain
        self.set_gcc_path(self.project, self.embed_gcc)


        # 5. remove convert_report.txt or not
        if os.path.exists(self.convert_report) and self.flag:
            os.remove(self.convert_report)

        return True


if __name__ == "__main__":
    import shutil
    logging.getLogger().setLevel(logging.INFO)

    tmp_project = Path("tmp_cwd")
    app_path = tmp_project / "applications"
    config_path = "../../../examples/k210/rtconfig.py"


    if not app_path.exists():
        app_path.mkdir(parents=True)
    shutil.copy(config_path, tmp_project)

    class Opt():
        def __init__(self):
            self.project = r"tmp_cwd"
            self.model_path = "../../Model/facelandmark.tflite"
            self.platform = "k210"
            self.rt_ai_example = "../../Documents"
            self.model_name = "facelandmark"

            # k210
            self.embed_gcc = r"D:\Project\k210_third_tools\xpack-riscv-none-embed-gcc-8.3.0-1.2\bin"
            self.ext_tools = r"./k_tools"
            self.model_types = "tflite caffe onnx"
            self.convert_report = "./convert_report.txt"
            self.dataset = "./datasets/images"
            self.network = "facelandmark"
            self.flag = False

    opt = Opt()
    k210 = K210(opt)
    _ = k210.run_k210()
