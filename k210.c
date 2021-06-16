#include <rt_ai.h>
#include <backend_k210_kpu.h>
#include <rt_ai_facelandmark_model.h>
#include <kpu.h>

extern unsigned char facelandmark_kmodel[];

/* based on k210 */
#define RT_AI_FACELANDMARK_INFO    {       \
    RT_AI_FACELANDMARK_IN_NUM,             \
    RT_AI_FACELANDMARK_OUT_NUM,            \
    RT_AI_FACELANDMARK_IN_SIZE_BYTES,      \
    RT_AI_FACELANDMARK_OUT_SIZE_BYTES,     \
    RT_AI_FACELANDMARK_WORK_BUFFER_BYTES,  \
    ALLOC_INPUT_BUFFER_FLAG                 \
}

#define RT_AI_FACELANDMARK_HANDLE  {         \
    .info   =     RT_AI_FACELANDMARK_INFO    \
}

#define RT_K210_AI_FACELANDMARK   {   \
    .parent         = RT_AI_FACELANDMARK_HANDLE,   \
    .model          = facelandmark_kmodel, \
    .dmac           = DMAC_CHANNEL5,        \
}

static struct k210_kpu rt_k210_ai_facelandmark = RT_K210_AI_FACELANDMARK;

static int rt_k210_ai_facelandmark_init(){
    rt_ai_register(RT_AI_T(&rt_k210_ai_facelandmark),RT_AI_FACELANDMARK_MODEL_NAME,0,backend_k210_kpu,&rt_k210_ai_facelandmark);
    return 0;
}

INIT_APP_EXPORT(rt_k210_ai_facelandmark_init);
