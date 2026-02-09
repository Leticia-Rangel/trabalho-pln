import os
from datasets import load_dataset
import pandas as pd
import re
from sentence_transformers import SentenceTransformer
import glob

# baixando a base de dados MSR-VTT
ds = load_dataset("friedrichor/MSR-VTT", "train_7k") 
    
# Converter o split "train" em DataFrame
df = pd.DataFrame(ds["train"])

def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[#\*\+\.\:\=\>\\\[\]]", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

df["clean_caption"] = df["caption"].apply(lambda caps: [normalize_text(c) for c in caps])

# Carrega o modelo Sentence-BERT
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_sentence_embedding(text, model):
    return model.encode(text)

# 🔹 Cria a pasta para salvar os embeddings
output_dir = "embeddings_batches"
os.makedirs(output_dir, exist_ok=True)

# Processa em lotes
batch_size = 1000
embeddings_full = []

for start in range(0, len(df), batch_size):
    end = start + batch_size
    batch = df.iloc[start:end]

    batch_embeddings = []
    for idx, caps in enumerate(batch["clean_caption"]):
        for c in caps:
            emb = get_sentence_embedding(c, model)
            batch_embeddings.append({
                "video_id": batch["video_id"].iloc[idx],
                "caption": c,
                "embedding": emb
            })

    # salva cada lote em arquivo separado dentro da pasta
    batch_df = pd.DataFrame(batch_embeddings)
    batch_df.to_pickle(os.path.join(output_dir, f"embeddings_batch_{start}_{end}.pkl"))

    print(f"Lote {start}-{end} processado e salvo em {output_dir}.")

# Carrega todos os lotes salvos e concatena
files = glob.glob(os.path.join(output_dir, "embeddings_batch_*.pkl"))
dfs = [pd.read_pickle(f) for f in files]
embeddings_df = pd.concat(dfs, ignore_index=True)

print(embeddings_df.shape)
