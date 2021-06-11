k210 版本跟踪

| Version | Date       | Description                                                  |
| ------- | ---------- | ------------------------------------------------------------ |
| V0.0.1  | 2021/04/10 | 新增非量化模型支持<br>新增量化数据集格式参数                 |
| V0.0.2  | 2021/04/12 | 修复单输出生成rt_ai_model.h 的 bug<br>重置 kmodel 路径，之前是 \<BSP>/applications, 现在是 plugin_k210<br>新增模型进度条显示 |
| V0.0.3 | 2021/06/01 |  embed_gcc 参数不是非必须，如果有，则将写入 rt_config.py 文件中，如果没有，则在编译的时候需要指定                                                            |
| V0.0.4  | 2021/06/03 | 新增 linux 支持                                              |
| V0.0.5 | 2021/06/03| 增加 `--weights-quantize-threshold`, `--output-quantize-threshold` and `--no-quantized-binary`，`--no_quantized_binary`, `--dump_weights_range`<br>`--dump_weights_range` 从可选择输入更改为指定输入，二选一 |

