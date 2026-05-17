from fastapi import FastAPI, HTTPException
from retrieve import load_knowledge, simple_retrieve
from loguru import logger
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi import Request
from schemas import GenRequest                 # 定义请求体结构
from generation import generate_text, model_id, device



#创建 FastAPI 应用
app=FastAPI(
    title="LLM Trade Assistant",
    description="Local GPT-2 text generation API with sampling parameters",
    version="0.2.0",
)





# 在模型加载之后，API 定义之前，全局缓存知识库
KNOWLEDGE = load_knowledge()

# 创建限流器（根据客户端 IP 限制）
limiter=Limiter(key_func=get_remote_address,default_limits=["10/minute"])
app.state.limiter=limiter
app.add_exception_handler(429,_rate_limit_exceeded_handler)


# API 端点
@app.post("/generate")
@limiter.limit("10/minute")
async def generate(req: Request, request: GenRequest): # 必须有 req: Request
    # 记录请求开始
    logger.info(f"Received prompt : {request.prompt[:50]}...") # 只记前50字符，避免太长



    try:
        #prompt 长度限制
        if len(request.prompt)>1000:
            raise  HTTPException(status_code=400, detail="Prompt too long(max 1000 chars)")
        # max_new_tokens 限制
        if request.max_new_tokens > 200:
            raise HTTPException(
                status_code=400,
                detail="max_new_tokens too large"
            )
        # 检索相关上下文
        retrieved = simple_retrieve(
            request.prompt,
            KNOWLEDGE,
            top_k=2
        )
        context="\n".join(retrieved)

        enhanced_prompt=(
            f"Context:\n{context}\n\n"
            f"Question:{request.prompt}\n"
            f"Answer:"
        )

        text = generate_text(
            prompt=enhanced_prompt,
            max_new_tokens=request.max_new_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
            repetition_penalty=request.repetition_penalty,
        )

    # 将 token IDs 解码为字符串
        logger.success(f"Generated text: {len(text)} chars") # 成功日志
        return {"generated_text": text,"retrieved":retrieved}
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error:{e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model-info")
async def model_info():
    return {
        "model": model_id,
        "device": str(device),
        "model_type": "GPT-2 (causal LM)"
    }
@app.get("/health")
async def health():
    return {"status":"ok"}

