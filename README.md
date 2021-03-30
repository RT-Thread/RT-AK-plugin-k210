func:

set_gcc()

修改 `rtconfig.py`，设定交叉编译工具链的路径

输入为 (rtconfig_path, gcc_path)

输出 None



func：

is_support_model_type()

验证模型类型是否在支持列表中 (tflite|caffe|onnx)

输入 (model_types, model)

输出 模型文件名



func:

run_k210()

运行k210

- sub_func

    convert_kmodel()

    设置ncc 的系统环境变量，用 nncase 把 `tflite` 转成 kmodel, cmd 运行结果保存为一个txt，然后模型另保存为16进制文件

    **量化需要数据集**

    input: (model, project, ncc_path, dataset, convert_report)

    output: cmd 运行结果

- sub_func

    rt_ai_model_gen()

    根据上一个函数的 cmd 运行保存的txt，生成 `rt_ai_<model_name>_model.h`， 另存为 project/applications 路径下

    输入：(convert_report, project, model_name)

    输出：模型信息

- sub_func：

    load_rt_ai_model_c() - 在update_info.py 中已经实现

    ~~把生成的rt_ai_<model_name>_model.c 加载到 project/applications 中~~

    > ~~做法：documents 中 rt_ai_facelandmark_model.c 中模型名变量替换~~

    ~~输入：(project_path, rt_ai_model_path)~~

    ~~输出：True~~
    
- ~~sub_func~~

    ~~rm_convert_report~~

    ~~如果flag 为真，那么删除 convert_report.txt 文件~~

    ~~input: (convert_report)~~

    ~~output: None~~



func:

set_gcc_path()

人为指定 RTT_EXEC_PATH 路径，即手动设置 k210 的交叉编译工具链，具体做法：

修改 project/rtconfig.py 中的第23行，增加设置 RTT_EXEC_PATH 的命令

![](https://gitee.com/lebhoryi/PicGoPictureBed/raw/master/img/20210220154318.png)

input: (project, embed_gcc_path)

output: None

---

**待定**

func:

修改main.c 中的各个模型的相关变量名

输入： (project, model_name)



