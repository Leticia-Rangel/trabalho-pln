import pandas as pd
import random
import re

# Carrega sua base de embeddings
embeddings_df = pd.read_pickle("embeddings_batches/embeddings_all.pkl")

# Junta todas as legendas em um único texto
all_captions = " ".join(embeddings_df["caption"].astype(str).tolist())

# Quebra em palavras (removendo pontuação e deixando em minúsculo)
words = re.findall(r"\b\w+\b", all_captions.lower())

# Remove palavras muito curtas (ex.: "a", "an", "of") para ficar mais útil
words = [w for w in words if len(w) > 3]

# Seleciona 10 palavras aleatórias únicas
random_words = random.sample(list(set(words)), 10)

print("10 palavras aleatórias da base:")
for w in random_words:
    print("-", w)

# 🔎 Salva em um arquivo TXT
with open("palavras_aleatorias.txt", "w", encoding="utf-8") as f:
    for w in random_words:
        f.write(w + "\n")

print("\nAs palavras foram salvas em 'palavras_aleatorias.txt'")
