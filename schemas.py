from pydantic import BaseModel

class GenRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 50
    temperature:float = 0.7
    top_p:float=0.9
    repetition_penalty:float=1.1