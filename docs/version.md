<!--
 * @Author: lebhoryi@gmail.com
 * @Date: 2021-08-13 09:40:00
 * @LastEditors: lebhoryi@gmail.com
 * @LastEditTime: 2021-08-13 11:02:52
 * @Version: V0.0.1
 * @FilePath: /RT-AK/RT-AK/rt_ai_tools/platforms/plugin_k210/docs/version.md
 * @Description: 
-->
k210 版本跟踪

| Version | Date       | Description                                                  |
| ------- | ---------- | ------------------------------------------------------------ |
| V0.0.1  | 2021/04/10 | 新增非量化模型支持<br>新增量化数据集格式参数                 |
| V0.0.2  | 2021/04/12 | 修复单输出生成rt_ai_model.h 的 bug<br>重置 kmodel 路径，之前是 \<BSP>/applications, 现在是 plugin_k210<br>新增模型进度条显示 |
| V0.0.3 | 2021/06/01 |  embed_gcc 参数不是非必须，如果有，则将写入 rt_config.py 文件中，如果没有，则在编译的时候需要指定                                                            |
| V0.0.4  | 2021/06/03 | 新增 linux 支持                                              |
| V0.0.5 | 2021/06/03| 增加 `--weights-quantize-threshold`, `--output-quantize-threshold` and `--no-quantized-binary`，`--no_quantized_binary`, `--dump_weights_range`<br>`--dump_weights_range` 从可选择输入更改为指定输入，二选一 |
| V0.0.6 | 2021/06/16 | 新增`RT-AK之K210插件快速上手.md` <br>修改根目录的 `readme.md`，新增文件夹下面的 `readme.md` |
| V0.0.7 | 2021/06/17 | 新增 K210 NNCase 算子支持说明 |
| V0.0.8 | 2021/06/23 | 1. 新增 input-type 参数；<br>2. 新增 kmodel 生成失败的异常处理 |
| V0.0.9 | 2021/08/13 | 1.修复 linux ncc 没有执行权限<br>2. 新增 `--input-std` 和 `--input-mean` 参数 |
|  |  |  |

