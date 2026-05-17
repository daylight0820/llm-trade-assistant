import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# 模型 ID
model_id = "gpt2-medium"

# 加载 tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token

# 加载模型
model = AutoModelForCausalLM.from_pretrained(model_id)

# 推理模式
model.eval()

# CPU
device = torch.device("cpu")
model.to(device)


def generate_text(
    prompt: str,
    max_new_tokens: int = 50,
    temperature: float = 0.7,
    top_p: float = 0.9,
    repetition_penalty: float = 1.1,
):
    """
    统一文本生成接口
    """

    # tokenize
    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    ).to(device)

    # 推理
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=temperature,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
        )

    # decode
    text = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return text