import os
import json
import numpy as np
from pydub import AudioSegment

# 🔎 Força o Python a enxergar a pasta do FFmpeg
ffmpeg_dir = r"C:\ffmpeg\bin"
os.environ["PATH"] += os.pathsep + ffmpeg_dir

# Define manualmente os executáveis
AudioSegment.converter = os.path.join(ffmpeg_dir, "ffmpeg.exe")
AudioSegment.ffprobe   = os.path.join(ffmpeg_dir, "ffprobe.exe")

# -------------------------------
# Funções de métricas internas (busca)
# -------------------------------

def avg_similarity(scores):
    return np.mean(scores) if scores else 0

def min_similarity(scores):
    return np.min(scores) if scores else 0

def max_similarity(scores):
    return np.max(scores) if scores else 0

def std_similarity(scores):
    return np.std(scores) if scores else 0

# -------------------------------
# Funções de métricas de áudio (sinal)
# -------------------------------

def avaliar_audio_signal(file_path):
    if not os.path.exists(file_path):
        return None

    # Usa from_file com formato explícito
    audio = AudioSegment.from_file(file_path, format="mp3")

    # Duração em segundos
    duracao = len(audio) / 1000.0

    # Energia RMS normalizada
    energia_rms = audio.rms / 1000.0

    # Loudness médio em dBFS
    loudness = audio.dBFS

    # Proporção de silêncio (amplitude < -40 dBFS)
    silencio = 1 if audio.dBFS < -40 else 0

    return {
        "duracao_s": duracao,
        "energia_rms": energia_rms,
        "loudness_dbfs": loudness,
        "silencio": silencio
    }

# -------------------------------
# Avaliação automática
# -------------------------------

def avaliar_sistema(json_file, audio_dir="audio", output_file="avaliacao_resultados.txt"):
    with open(json_file, "r", encoding="utf-8") as f:
        dados = json.load(f)

    linhas_saida = []
    linhas_saida.append("=== Avaliação do Sistema ===\n")

    for query, frases in dados.items():
        scores = [f["score"] for f in frases]

        media = avg_similarity(scores)
        minimo = min_similarity(scores)
        maximo = max_similarity(scores)
        desvio = std_similarity(scores)

        duracoes, energias, loudnesses = [], [], []
        silencios = 0

        for item in frases:
            audio_file = item.get("audio_file")
            if audio_file:
                info = avaliar_audio_signal(audio_file)
                if info:
                    duracoes.append(info["duracao_s"])
                    energias.append(info["energia_rms"])
                    loudnesses.append(info["loudness_dbfs"])
                    silencios += info["silencio"]

        media_duracao = np.mean(duracoes) if duracoes else 0
        media_energia = np.mean(energias) if energias else 0
        media_loudness = np.mean(loudnesses) if loudnesses else 0
        taxa_silencio = silencios / len(frases) if frases else 0

        resultado = (
            f"\nConsulta: {query}\n"
            f"Similaridade média (busca): {media:.2f}\n"
            f"Score mínimo: {minimo:.2f}, máximo: {maximo:.2f}, desvio: {desvio:.2f}\n"
            f"Duração média dos áudios: {media_duracao:.2f} s\n"
            f"Energia RMS média: {media_energia:.2f}\n"
            f"Loudness médio: {media_loudness:.2f} dBFS\n"
            f"Taxa de silêncio: {taxa_silencio:.2f}\n"
        )

        print(resultado)
        linhas_saida.append(resultado)

    # Salva em arquivo TXT
    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(linhas_saida)

    print(f"\nResultados salvos em '{output_file}'")

# -------------------------------
# Executar avaliação
# -------------------------------

avaliar_sistema("resultados.json", audio_dir="audio", output_file="avaliacao_resultados.txt")
