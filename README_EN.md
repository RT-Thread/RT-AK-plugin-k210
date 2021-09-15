中文: [Chinese](README.md)

<center><h1>The Plugin of RT-AK Platform: K210</h1></center> 

- [1. Introduction](#1.Introduction)
- [2. Structure of the Plugin K210](#2.Structure_of_the_Plugin_K210)
- [3. Parameter Explanation of the Plugin K210](#3.Parameter_Explanation_of_the_Plugin_K210)
- [4. Installation for the Plugin K210](#4.Installation_for_the_Plugin_K210)
- [5. Instruction for the Plugin K210 Command Line](#5.Instruction_for_the_Plugin_K210_Command_Line)
- [6. Compilation for the Embed Application Project](#6.Compilation_for_the_Embed_Application_Project)
- [7. Work flow on the K210 Platform](#7.Work_flow_on_the_K210_Platform)

## 1.Introduction

[![License](https://camo.githubusercontent.com/2a2157c971b7ae1deb8eb095799440551c33dcf61ea3d965d86b496a5a65df55/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4c6963656e73652d417061636865253230322e302d626c75652e737667)](https://github.com/pinxue/RT-AK/blob/main/LICENSE) [![img](https://camo.githubusercontent.com/12f51a23f724d8f12da5ad99e1f188e0e9c1db1d52d283134d9ad16384ca987c/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f506c7567696e2d4b3231302d627269676874677265656e)](https://github.com/RT-Thread/RT-AK-plugin-k210)

**This project shows one of the plugins of RT-AK platform**

This project uses the Kendryte K210 as the target hardware for AI application development on the RT-Thread RTOS. In order to deploy an AI model into the K210, the Kendryte NNCase tool is integrated into RT-AK. 

- Model storage types supported in K210

  - `TFLite`
  - `Caffe`
  - `ONNX`
  
- Model operator lists

  - [TFLite ops](./k_tools/tflite_ops.md)
  - [Caffe ops](./k_tools/caffe_ops.md)
  - [ONNX ops](./k_tools/onnx_ops.md)

- Tool-chains of the project

  - Cross compilation tool chain (For instance: Windows 10)

     [xpack-riscv-none-embed-gcc-8.3.0-1.2-win32-x64.zip](https://github.com/xpack-dev-tools/riscv-none-embed-gcc-xpack/releases/tag/v8.3.0-1.2) | `Version: v8.3.0-1.2`

  - Official tools
    - NNCase, which is located at `./k_tools`. it also can be downloaded from [here](https://github.com/kendryte/nncase/blob/master/docs/USAGE_ZH.md)

    - K-Flash can be downloaded from [here ](https://github.com/kendryte/kendryte-flash-windows/releases)

      > PS: [K-Flash for linux](https://github.com/kendryte/kflash.py)

- Quick start for the K210 of RT-AK platform
  - [Introduction of the quick start](./docs/Quick_start_with_RT-AK_K210.md)

## 2.Structure_of_the_Plugin_K210 

```shell
./
├── backend_plugin_k210                 # Model registration for the RT-AK Lib
│   ├── backend_k210_kpu.c
│   ├── backend_k210_kpu.h
│   └── readme.md
├── datasets                            # Dataset for AI model quantization
│   ├── mnist_datasets
│   └── readme.md
├── docs                                # docs for the K210 platform
│   ├── images
│   ├── Q&A.md
│   ├── Quick start for the K210 platform.md
│   └── version.md
├── generate_rt_ai_model_h.py
├── k210.c                              # rt_ai_<model_name>_model.c 
├── k_tools                             # docs and softwares of Kendryte 
│   ├── kendryte_datasheet_20180919020633.pdf
│   ├── kendryte_standalone_programming_guide_20190704110318_zh-Hans.pdf
│   ├── ncc
│   ├── ncc.exe                         
│   └── readme.md
├── plugin_k210_parser.py               # Inputs of the K210 platform
├── plugin_k210.py                      
└── README.md
```

## 3.Parameter_Explanation_of_the_Plugin_K210

$$
RT-AK Input parameters = （RT-AK basic parameters + K210 plugin parameters）
$$

- RT-AK basic parameters，[Link](https://github.com/RT-Thread/RT-AK/tree/main/RT-AK/rt_ai_tools#0x03-%E5%8F%82%E6%95%B0%E8%AF%B4%E6%98%8E)

- Introduction for input parameters of the K210 Platform，for more details: `plugin_k210_parser.py` 

| Parameter                    | Description                                                  |
| ---------------------------- | ------------------------------------------------------------ |
| --embed_gcc                  | Cross compilation tool chain，**not essential**.             |
| --ext_tools                  | Input path for `NNCase`，it is used to transform the original AI model to kmodel. Default is `./platforms/k210/k_tools` |
| **--inference_type**         | Inference type for AI model. If it is a `float` type, the AI model will not be quantized, and the KPU will not be used to  accelerate computation. Default is `uint8`. |
| --dataset                    | Dataset for AI model quantization. Default is `--inference-type`  = `uint8` |
| --dataset_format             | Dataset format of the model quantization. Default is `image`. For audio dataset, the default is `raw` |
| --weights_quantize_threshold | Threshold to control quantizing op or not according to it's weigths range, Default is 32.000000 |
| --output_quantize_threshold  | Threshold to control quantizing op or not according to it's output size, default is 1024 |
| --no_quantized_binary        | Don't quantize binary ops                                    |
| --dump_weights_range         | Dump weights range                                           |
| --input-type                 | Input type. Default is float or uint8, which is equal to inference type |
| **--clear**                  | Delete `convert_report.txt` ，Default is `False`             |

## 4.Installation_for_the_Plugin_K210

- It is not necessary to install the Plug-in K210 manually, but you need to clone the [`RT-AK`](https://github.com/RT-Thread/RT-AK) platform 

- Under the `RT-AK/rt_ai_tools`, it is only need to execute `python aitools.py --xxx` and make sure that `platform=K210`, then the plug-in will be downloaded automatically

## 5.Instruction_for_the_Plugin_K210_Command_Line

- Entering the `RT-AK/rt_ai_tools`, and typing the command as below
-  `your_project_path` is the `BSP` path of the `RT-Thread RTOS`. We provide a [`BSP`](http://117.143.63.254:9012/www/RT-AK/sdk-bsp-k210.zip), the `SDK` of the `k210` is `V0.5.6`

```bash
# no model quantization, --inference_type
$ python aitools.py --project=<your_project_path> --model=<your_model_path> --platform=k210  --inference_type=float

# no model quantization, set path for the cross compilation tool chain
$ python aitools.py --project=<your_project_path> --model=<your_model_path> --platform=k210 --embed_gcc=<your_RISCV-GNU-Compiler_path> --inference_type=float

# model quantization with uint8 type, accelerating computation with KPU, dataset format is image
$ python aitools.py --project=<your_project_path> --model=<your_model_path> --platform=k210 --embed_gcc=<your_RISCV-GNU-Compiler_path> --dataset=<your_val_dataset>

# model quantization with uint8 type, accelerating computation with KPU, dataset format is not image
$ python aitools.py --project=<your_project_path> --model=<your_model_path> --platform=k210 --embed_gcc=<your_RISCV-GNU-Compiler_path> --dataset=<your_val_dataset> --dataset_format=raw

# example
$ python aitools.py --project="D:\Project\k210_val" --model="./Models/facelandmark.tflite" --model_name=facelandmark --platform=k210 --embed_gcc="D:\Project\k210_third_tools\xpack-riscv-none-embed-gcc-8.3.0-1.2\bin" --dataset="./platforms/plugin_k210/datasets/images"
```

Other commands：

```shell
# set name of the transformed AI model --model_name Default is network
$ python aitools.py --project=<your_project_path> --model=<your_model_path> --model_name=<model_name> --platform=k210 --embed_gcc=<your_RISCV-GNU-Compiler_path> --dataset=<your_val_dataset> --clear

# clear convert_report.txt, --clear
$ python aitools.py --project=<your_project_path> --model=<your_model_path> --platform=k210 --embed_gcc=<your_RISCV-GNU-Compiler_path> --dataset=<your_val_dataset> --clear
```

## 6.Compilation_for_the_Embed_Application_Project

**Please prepare the cross compilation tool chain: xpack-riscv-none-embed-gcc-8.3.0-1.2**

setting the environment:

```shell
set RTT_EXEC_PATH=your_toolchains
# modify rtconfig.py, line 22 os.environ['RTT_EXEC_PATH'] = r'your_toolchains'
scons -j 6	
```

If it is compiled successfully,  `rtthread.elf` and `rtthread.bin` will be generated,  `rtthread.bin` can be downloaded into the k210 hardware

## 7.Work_flow_on_the_K210_Platform

- [x] Checking the validation of AI model 
- [x] AI model is transformed to the `kmodel` and saved at `project/applications` 
- [x] `kmodel` is transformed to hexadecimal type and saved at `project/applications` 
- [x] `rt_ai_<model_name>_model.h` is generated and saved at `project/applications` 
- [x] `rt_ai_<model_name>_model.c` is generated and saved at `project/applications` 
- [x] Setting the environment variable  `RTT_EXEC_PATH` into the project
- [x] Deleting the `convert_report.txt`

