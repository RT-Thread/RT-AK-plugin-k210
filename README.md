## 2. 硬件平台2 - k210

- k210 SDK |  Version: v0.5.6

- 模型支持：TFLite、Caffe、ONNX

- 交叉编译工具链，下载地址： [xPack GNU RISC-V Embedded GCC](https://github.com/xpack-dev-tools/riscv-none-embed-gcc-xpack/releases/) | Version: v8.3.0-1.2

- K-Flash 烧录工具，下载地址：[windows上的kflash图形界面烧录软件](https://github.com/kendryte/kendryte-flash-windows/releases)

  > PS: [linux下python脚本烧录](https://github.com/kendryte/kflash.py)

### Part3：k210 参数

| Parameter           | Description                                                  |
| ------------------- | ------------------------------------------------------------ |
| --embed_gcc         | 交叉编译工具链路径，**需要用户指定**                         |
| **--ext_tools**     | `NNCase` 路径，将模型转换为 `kmodel`，默认是 `./platforms/k210/k_tools` |
| `--rt_ai_example`   | 存放`rt_ai_<model_name>_model.c` 示例文件，默认是 `./platforms/k210/docs` |
| **--dataset**       | 模型量化过程中所需要用到的数据集，**需要用户指定**           |
| --convert_report    | 模型转换成 `kmodel` 的日志输出，默认是 `./platforms/k210/convert_report.txt` |
| --model_types       | `RT-AK Tools` 所支持的模型类型，目前仅支持：tflite、onnx、caffe |
| --**network**       | 在 `Documents` 中的模板文件的模型名，默认是 `facelandmark`   |
| **--enable_rt_lib** | 在 `project/rtconfgi.h` 中打开宏定义 `RT_AI_USE_K210`，默认是 `RT_AI_USE_K210` |
| **--flag**          | 是否需要删除 `convert_report.txt` ，默认 `False`             |

## 

### Part2：k210

目前耗时在 220s 左右，时间占用最长在 nncase 转换模型的过程中，耗时 200s 上下。

1. 基础运行命令：

```shell
python aitools.py --project=<your_project_path> --model_path=<your_model_path> --platform=k210 --embed_gcc=<your_RISCV-GNU-Compiler_path> --dataset=<your_val_dataset>

# 示例
python aitools.py --project="D:\Project\k210_val" --model_path="./Model/facelandmark.tflite" --platform=k210 --embed_gcc="D:\Project\k210_third_tools\xpack-riscv-none-embed-gcc-8.3.0-1.2\bin" --dataset="./platforms/k210/datasets/images"
```

![](https://gitee.com/lebhoryi/PicGoPictureBed/raw/master/img/20210223151447.png)

2. 其他：

```shell
# 指定转换的模型名称，--model_name 默认为 network
python aitools.py --project=<your_project_path> --model_path=<your_model_path> --model_name=<model_name> --platform=k210 --embed_gcc=<your_RISCV-GNU-Compiler_path> --dataset=<your_val_dataset> --flag

# 不保存模型转换日志，--flag
python aitools.py --project=<your_project_path> --model_path=<your_model_path> --platform=k210 --embed_gcc=<your_RISCV-GNU-Compiler_path> --dataset=<your_val_dataset> --flag

# 指定 kmodel 名称，--kmodel_name
python aitools.py --project=<your_project_path> --model_path=<your_model_path> --platform=k210 --embed_gcc=<your_RISCV-GNU-Compiler_path> --dataset=<your_val_dataset> --kmodel_name=<new_model_name>
```

# 

## 3. k210

- [x] 判断模型是否支持
- [x] 模型转换成 `kmodel` 模型，保存在 `project/applications` 
- [x] `kmodel` 模型转存为十六进制，保存在 `project/applications` 
- [x] 生成 `rt_ai_<model_name>_model.h` 文件，保存在 `project/applications` 
- [x] 生成 `rt_ai_<model_name>_model.c` 文件，保存在 `project/applications` 
- [x] 在 `project` 中写入 `RTT_EXEC_PATH` 环境变量
- [x] 判断是否删除 `convert_report.txt`
- [ ] 修改 `main.c`

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

