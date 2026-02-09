import os
import json
import pandas as pd
import numpy as np
from gtts import gTTS
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Carrega o DataFrame com todos os embeddings
embeddings_df = pd.read_pickle("embeddings_batches/embeddings_all.pkl")

# Carrega o modelo
model = SentenceTransformer("all-MiniLM-L6-v2")

def buscar_frases(query, embeddings_df, model, top_k=5):
    query_emb = model.encode(query).reshape(1, -1)
    all_embs = np.stack(embeddings_df["embedding"].values)
    sims = cosine_similarity(query_emb, all_embs)[0]
    top_idx = np.argsort(sims)[::-1][:top_k*2]  # pega mais para compensar duplicatas
    resultados = embeddings_df.iloc[top_idx][["caption", "video_id"]].copy()
    resultados["score"] = sims[top_idx]
    resultados = resultados.drop_duplicates(subset=["caption"]).head(top_k)
    return resultados

if __name__ == "__main__":
    json_file = "resultados.json"
    if os.path.exists(json_file):
        with open(json_file, "r", encoding="utf-8") as f:
            resultados_json = json.load(f)
    else:
        resultados_json = {}

    # Cria pasta de áudio se não existir
    audio_dir = "audio"
    os.makedirs(audio_dir, exist_ok=True)

    while True:
        query = input("\nDigite a palavra-chave (ou 'sair' para encerrar): ").strip().lower()
        if query == "sair":
            break

        resultados = buscar_frases(query, embeddings_df, model, top_k=5)

        frases_info = []
        for i, row in resultados.iterrows():
            frase = row["caption"]
            video_id = row["video_id"]
            score = round(float(row["score"]), 4)

            # 🔊 Gera áudio com gTTS e salva em pasta
            nome_arquivo = os.path.join(audio_dir, f"{query}_{i+1}.mp3")
            tts = gTTS(frase, lang="en")  # use 'pt' se quiser em português
            tts.save(nome_arquivo)
            print(f"Áudio salvo: {nome_arquivo}")

            # Junta texto + áudio no JSON
            frases_info.append({
                "caption": frase,
                "video_id": video_id,
                "score": score,
                "audio_file": nome_arquivo
            })

        # Atualiza JSON acumulativo
        resultados_json[query] = frases_info
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(resultados_json, f, ensure_ascii=False, indent=4)

        print(f"\nTop 5 frases relacionadas a '{query}':")
        for j, item in enumerate(frases_info, 1):
            print(f"{j}. {item['caption']} (video_id={item['video_id']}, score={item['score']}, áudio={item['audio_file']})")

        print(f"\nResultados atualizados em {json_file}")
