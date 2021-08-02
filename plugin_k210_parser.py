# coding=utf-8
'''
@ Summary: 
@ Update:  

@ file:    k210_parser.py
@ version: 1.0.0

@ Author:  Lebhoryi@gmail.com
@ Date:    2021/2/4 16:27
'''

def platform_parameters(parser):
    """ K210 platform parameters """
    parser.add_argument("--embed_gcc", type=str, default="",
                        help="The Kendryte RISC-V GNU Compiler Toolchain.")
    parser.add_argument("--ext_tools", type=str, default="./platforms/plugin_k210/k_tools",
                        help="NNcase excute file path. Convert tflite/onnx/caffe model to kmodel.")
    parser.add_argument("--inference_type", type=str, default="uint8", choices=["uint8", "float"],
                        help="inference type: e.g. float, uint8 default is uint8")
    parser.add_argument("--dataset", type=str, default="./platforms/plugin_k210/datasets/images",
                        help="calibration dataset, used in post quantization, only quantize used")
    parser.add_argument("--dataset_format", type=str, default="image",
                        help="The datset format: e.g. image, raw. Default is image, only quantize used")
    parser.add_argument("--weights_quantize_threshold", type=float, default=64.000000,
                        help="the threshold to control quantizing op or not according to it's weigths range")
    parser.add_argument("--output_quantize_threshold", type=int, default=1024,
                        help="the threshold to control quantizing op or not according to it's output size")
    parser.add_argument("--no_quantized_binary", action="store_true",
                        help="Disable quantized binary operator, nncase will always use float binary operator")
    parser.add_argument("--dump_weights_range", action="store_true",
                        help="Show conv2d weights range or not.")
    parser.add_argument("--input-type", type=str, default="",
                        help="input type: e.g. default, float, uint8, default means equal to inference type")
    parser.add_argument("--rt_ai_example", type=str, default="./platforms/plugin_k210",
                        help="Model & platform informations registered to RT-AK Lib, eg:stm32, k210.")
    parser.add_argument("--convert_report", type=str, default="./platforms/plugin_k210/convert_report.txt",
                        help="The report about nncase convert model to kmodel.")
    parser.add_argument("--model_types", type=str, default="tflite caffe onnx",
                        help="The supported model types, tflite|caffe|onnx")
    parser.add_argument("--network", type=str, default="facelandmark",
                        help="The model name in '<tools>/Documents/<stm32> files'")
    parser.add_argument("--enable_rt_lib", type=str, default="RT_AI_USE_K210",
                        help="Enabel RT-AK Lib using k210")
    parser.add_argument("--clear", action="store_true", help="Remove convert_report.txt or not.")
    return parser


def model_info(model_name, work_buffer):
    model_name_upper = model_name.upper()
    parser_in_convert = ["Working memory usage", "Input", "Identity"]

    rt_ai_info = {
        "head_info":[
            # the 5 head lines
            f"#ifndef __RT_AI_{model_name_upper}_MODEL_H\n",
            f"#define __RT_AI_{model_name_upper}_MODEL_H\n\n",
            "/* model info ... */\n\n",
            "// model name\n",
            f"#define RT_AI_{model_name_upper}_MODEL_NAME\t\t\t\"{model_name}\"\n\n",

            # activations and weights
            f"#define RT_AI_{model_name_upper}_WORK_BUFFER_BYTES\t({work_buffer})\n\n",
            f"#define AI_{model_name_upper}_DATA_WEIGHTS_SIZE\t\t(1493120) //unused\n\n",

            # alignment
            f"#define RT_AI_{model_name_upper}_BUFFER_ALIGNMENT\t\t(4)\n\n",
            ],

        # inputs info
        "input_info": {
            # input num
            "rt_ai_in_num": f"#define RT_AI_{model_name_upper}_IN_NUM\t\t\t\t",

            "inputs": [
                f"#define RT_AI_{model_name_upper}_IN_1_SIZE\t\t\t",
                f"#define RT_AI_{model_name_upper}_IN_1_SIZE_BYTES\t\t"
            ],

            "input_size": [f"#define RT_AI_{model_name_upper}_IN_SIZE_BYTES\t\t{'{'}\t\\\n", ],
            "total_input_size": f"#define RT_AI_{model_name_upper}_IN_TOTAL_SIZE_BYTES\t"
        },

        # output info
        "output_info":{
            # output num
            "rt_ai_out_num": f"#define RT_AI_{model_name_upper}_OUT_NUM\t\t\t\t",

            "outputs": [
                f"#define RT_AI_{model_name_upper}_OUT_1_SIZE\t\t\t",
                f"#define RT_AI_{model_name_upper}_OUT_1_SIZE_BYTES\t\t"
            ],

            "output_size": [f"#define RT_AI_{model_name_upper}_OUT_SIZE_BYTES\t\t{'{'}\t\\\n", ],
            "total_output_size": f"#define RT_AI_{model_name_upper}_OUT_TOTAL_SIZE_BYTES\t"
        },

        # tail info
        "tail_info": [
            # the last two lines
            f"\n#define RT_AI_{model_name_upper}_TOTAL_BUFFER_SIZE\t\t//unused\n\n",
            "#endif\t//end\n",
        ]
    }

    return parser_in_convert, rt_ai_info, model_name_upper
