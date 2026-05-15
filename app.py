import torch
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer

# 1. 选择一个真正的生成式模型（GPT-2，约 500MB，CPU 可跑）
model_id = "gpt2-medium"

# 2. 加载分词器和模型（CPU 自动，无量化）
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token =tokenizer.eos_token


model = AutoModelForCausalLM.from_pretrained(model_id)
model.eval()
# 3. 确保模型在 CPU 上（你的电脑没有 GPU 或不想用 GPU）
device = torch.device("cpu")
model.to(device)

# 4. 创建 FastAPI 应用
app=FastAPI(
    title="LLM Trade Assistant",
    description="Local GPT-2 text generation API with sampling parameters",
    version="0.2.0",
)


# 5. 定义请求体结构
class GenRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 50
    temperature:float = 0.7
    top_p:float=0.9
    repetition_penalty:float=1.1


# 6. API 端点
@app.post("/generate")
async def generate(request: GenRequest):
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
    # 将文本转为 token IDs
        inputs = tokenizer(request.prompt, return_tensors="pt").to(device)
    # 生成文本
        with torch.no_grad():
            outputs = model.generate(
                    **inputs,
                    max_new_tokens=request.max_new_tokens,
                    do_sample=True,          # 随机采样，增加多样性
                    temperature=request.temperature,
                    top_p=request.top_p,
                    repetition_penalty=request.repetition_penalty,
            )
    # 将 token IDs 解码为字符串
        text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {"generated_text": text}
    except HTTPException:
        raise

    except Exception as e:
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

