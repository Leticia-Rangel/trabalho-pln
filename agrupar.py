import glob
import pandas as pd
import os

# Pasta onde os lotes foram salvos
output_dir = "embeddings_batches"

# Lista todos os arquivos de embeddings salvos dentro da pasta
files = glob.glob(os.path.join(output_dir, "embeddings_batch_*.pkl"))

# Carrega cada arquivo como DataFrame
dfs = [pd.read_pickle(f) for f in files]

# Junta tudo em um único DataFrame
embeddings_df = pd.concat(dfs, ignore_index=True)

print(embeddings_df.shape)   # número total de linhas
print(embeddings_df.head())  # primeiras linhas

# Salva tudo em um único arquivo final
embeddings_df.to_pickle(os.path.join(output_dir, "embeddings_all.pkl"))
