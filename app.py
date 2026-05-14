import torch
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer

# 1. 选择一个真正的生成式模型（GPT-2，约 500MB，CPU 可跑）
model_id = "gpt2-medium"

# 2. 加载分词器和模型（CPU 自动，无量化）
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token =tokenizer.eos_token


model = AutoModelForCausalLM.from_pretrained(model_id)

# 3. 确保模型在 CPU 上（你的电脑没有 GPU 或不想用 GPU）
device = torch.device("cpu")
model.to(device)

# 4. 创建 FastAPI 应用
app = FastAPI(title="GPT-2 Text Generation API")

# 5. 定义请求体结构
class GenRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 50

# 6. API 端点
@app.post("/generate")
async def generate(request: GenRequest):
    # 将文本转为 token IDs
    inputs = tokenizer(request.prompt, return_tensors="pt").to(device)
    # 生成文本
    outputs = model.generate(
        **inputs,
        max_new_tokens=request.max_new_tokens,
        do_sample=True,          # 随机采样，增加多样性
        temperature=1,
        top_p=0.9
    )
    # 将 token IDs 解码为字符串
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"generated_text": text}