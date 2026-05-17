import numpy as np

def load_knowledge(file_path="trade_faq.txt"):
    with open(file_path,"r",encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def simple_retrieve(query,knowledge,top_k=2):
    """基于关键词匹配的简单检索（后续可换成 embedding + 相似度）"""
    query_words = set(query.lower().split())
    scored = []
    for idx ,para in enumerate(knowledge):
        para_words = set(para.lower().split())
        overlap = len(query_words&para_words)
        scored.append((overlap,idx,para))
    scored.sort(key=lambda x:x[0],reverse=True)
    return [para for _,_,para in scored[:top_k]]