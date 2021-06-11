<center><h1>RT-AK 之 K210</h1></center>

- [简介](# 简介)
- [目录结构](# 目录结构)
- [参数说明](# 参数说明)
- [运行](# 运行)
- [功能列表](# 功能列表)

## 简介

*本项目归属于 `RT-AK` 主项目中的一个子模块。*

*使用堪智 `K210` 原 厂插件进行开发，嘉楠科技*

- k210 SDK |  Version: v0.5.6

- 模型支持：TFLite、Caffe、ONNX

- 交叉编译工具链，下载地址： [xPack GNU RISC-V Embedded GCC](https://github.com/xpack-dev-tools/riscv-none-embed-gcc-xpack/releases/) | Version: v8.3.0-1.2

- K-Flash 烧录工具，下载地址：[windows上的kflash图形界面烧录软件](https://github.com/kendryte/kendryte-flash-windows/releases)

  > PS: [linux下python脚本烧录](https://github.com/kendryte/kflash.py)

## 目录结构

```shell
% tree k210                                                               ~/tmp
k210
├── backend_plugin_k210  			# 将模型信息注册到 RT-AK Lib 后端
│   ├── backend_k210_kpu.c
│   ├── backend_k210_kpu.h
│   └── readme.md
├── datasets
│   └── images 						# 用于模型量化的数据集
├── docs  							#k210 相关文档
│   └── k210.c  					# rt_ai_<model_name>_model.c 示例文件
├── generate_rt_ai_model_h.py  		# 生成 rt_ai_<model_name>_model.h
├── k_tools  						# k210 所使用的相关工具
│   └── ncc.exe  					# k210 模型转成 kmodel 模型工具
├── plugin_k210_parser.py  			# k210 参数
├── plugin_k210.py 					# k210 插件运行
└── README.md

5 directories, 9 files
```

## 参数说明

本插件使用的模型转换工具是 `NNCase`， 功能：将深度神经网络模型转成 `kmodel` 格式，[资料传送门](https://github.com/kendryte/nncase/blob/master/docs/USAGE_ZH.md)

> 详见 `plugin_k210_parser.py` 

| Parameter                    | Description                                                  |
| ---------------------------- | ------------------------------------------------------------ |
| --embed_gcc                  | 交叉编译工具链路径，**非必须**。如果有，则会更改 `rt_config.py` 文件，如果无指定，则需要在编译的时候指定该工具链路径 |
| --ext_tools                  | `NNCase` 路径，将模型转换为 `kmodel`，默认是 `./platforms/k210/k_tools` |
| **--inference_type**         | 是否将模型量化为整形，如果是 `float`，不量化，将不能使用 `KPU` 加速，默认是 `uint8` |
| --dataset                    | 模型量化过程中所需要用到的数据集，只需要在设置 `--inference-type` 为 `uint8` 时提供这个参数 |
| --dataset_format             | 用于指定量化校准集的格式。默认是 `image`，如果是音频之类的数据集，则需要设置为 `raw` |
| --weights_quantize_threshold | 控制是否量化 `conv2d` 和 `matmul weights` 的阈值。如果 `weights` 的范围大于这个阈值，`nncase` 将不会量化它 |
| --output_quantize_threshold  | 控制是否量化 `conv2d` 和 `matmul weights` 的阈值。如果输出的元素个数小于这个阈值，`nncase` 将不会量化它。 |
| --no_quantized_binary        | 禁用 `quantized binary` 算子，`nncase` 将总是使用 `float binary` 算子。 |
| --dump_weights_range         | 是一个调试选项。当它打开时 `ncc` 会打印出 `conv2d weights` 的范围。 |
| --rt_ai_example              | 存放`rt_ai_<model_name>_model.c` 示例文件，默认是 `./platforms/k210/docs` |
| --convert_report             | 模型转换成 `kmodel` 的日志输出，默认是 `./platforms/k210/convert_report.txt` |
| --model_types                | `RT-AK Tools` 所支持的模型类型，目前模型支持范围：`tflite、onnx、caffe` |
| --network                    | 在 `Documents` 中的模板文件的模型名，默认是 `facelandmark`   |
| --enable_rt_lib              | 在 `project/rtconfgi.h` 中打开宏定义 `RT_AI_USE_K210`，默认是 `RT_AI_USE_K210` |
| **--clear**                  | 是否需要删除 `convert_report.txt` ，默认 `False`             |

## 运行

> 目前耗时在 220s 左右，时间占用最长在 nncase 转换模型的过程中，耗时 200s 上下。

```bash
# 非量化，不使用 KPU 加速， --inference_type
$ python aitools.py --project=<your_project_path> --model=<your_model_path> --platform=k210  --inference_type=float

# 非量化，指定交叉编译工具链路径
$ python aitools.py --project=<your_project_path> --model=<your_model_path> --platform=k210 --embed_gcc=<your_RISCV-GNU-Compiler_path> --inference_type=float

# 量化为 uint8，使用 KPU 加速，量化数据集为图片
$ python aitools.py --project=<your_project_path> --model=<your_model_path> --platform=k210 --embed_gcc=<your_RISCV-GNU-Compiler_path> --dataset=<your_val_dataset>

# 量化为 uint8，使用 KPU 加速，量化数据集为音频之类非图片，--dataset_format
$ python aitools.py --project=<your_project_path> --model=<your_model_path> --platform=k210 --embed_gcc=<your_RISCV-GNU-Compiler_path> --dataset=<your_val_dataset> --dataset_format=raw

# 示例(量化模型，图片数据集)
$ python aitools.py --project="D:\Project\k210_val" --model="./Models/facelandmark.tflite" --model_name=facelandmark --platform=k210 --embed_gcc="D:\Project\k210_third_tools\xpack-riscv-none-embed-gcc-8.3.0-1.2\bin" --dataset="./platforms/plugin_k210/datasets/images"
```

![](https://gitee.com/lebhoryi/PicGoPictureBed/raw/master/img/20210223151447.png)

其他：

```shell
# 指定转换的模型名称，--model_name 默认为 network
$ python aitools.py --project=<your_project_path> --model=<your_model_path> --model_name=<model_name> --platform=k210 --embed_gcc=<your_RISCV-GNU-Compiler_path> --dataset=<your_val_dataset> --clear

# 不保存模型转换日志，--clear
$ python aitools.py --project=<your_project_path> --model=<your_model_path> --platform=k210 --embed_gcc=<your_RISCV-GNU-Compiler_path> --dataset=<your_val_dataset> --clear
```

## 项目工程编译

**需要准备好交叉编译工具链** | [下载](https://github.com/xpack-dev-tools/riscv-none-embed-gcc-xpack/releases/tag/v8.3.0-1.2)

设置编译环境：

```shell
set RTT_EXEC_PATH=your_toolchains
# 或者修改rtconfig.py 文件第22行，新增 os.environ['RTT_EXEC_PATH'] = r'your_toolchains'
scons -j 6	
```

如果编译正确无误，会产生rtthread.elf、rtthread.bin文件。

其中 rtthread.bin 需要烧写到设备中进行运行。

## 功能列表

- [x] 判断模型是否支持
- [x] 模型转换成 `kmodel` 模型，保存在 `project/applications` 
- [x] `kmodel` 模型转存为十六进制，保存在 `project/applications` 
- [x] 生成 `rt_ai_<model_name>_model.h` 文件，保存在 `project/applications` 
- [x] 生成 `rt_ai_<model_name>_model.c` 文件，保存在 `project/applications` 
- [x] 在 `project` 中写入 `RTT_EXEC_PATH` 环境变量
- [x] 判断是否删除 `convert_report.txt`
- [ ] ~~修改 `main.c`~~

### 3.1 Function1 - 判断模型是否支持

- 函数：`is_support_model_type(model_types, model)`
- 功能：判断模型类型是否支持
- input: (model_types, model)
- output: model name

### 3.2 Function2 - 转换 kmodel

- 函数：`convert_kmodel(model, project, dataset, kmodel_name, convert_report)`
- 功能：将输入模型转成 `kmodel` 模型，保存路径：`project/applications/<kmodel_name>.kmodel` ，并将运行日志保存为：`./platforms/k210/convert_report.txt`
- input: (model, project, dataset, kmodel_name, convert_report)
- output: 模型转换的输出日志

### 3.3 Function3 -  转存16进制

- 函数：`hex_read_model(self, project, model)`
- 功能：将 `kmodel` 模型转存为十六进制，`project/applications/<kmodel_name>_kmodel.c` 
- input: (project, model)

### 3.4 Function4 - 生成 rt_ai_model.h

- 函数：`rt_ai_model_gen(convert_report, project, model_name)`
- 功能：根据 `./platforms/k210/convert_report.txt` 生成 `rt_ai_<model_name>_model.h` 文件
- input: (convert_report, project, model_name)
- output: `rt_ai_<model_name>_model.h` 文件内容

### 3.5 Function5 - 生成 rt_ai_model.c

- 函数：`load_rt_ai_example(rt_ai_example, project, old_name, new_name, platform)`
- 功能：根据 `Documents/k210.c` 生成 `rt_ai_<model_name>_model.c` 文件
- input: (Documents_path, project, default_name, kmodel_name, platform)

### 3.6 Function6 - RTT_EXEC_PATH 环境变量

- 函数：`set_gcc_path(project, embed_gcc)`
- 功能：在 `project/rtthread.py` 文件的第十四行写入 `RTT_EXEC_PATH` 变量，这样就不用在 `env` 中手动指定路径了。
- input: (project, embed_gcc)

