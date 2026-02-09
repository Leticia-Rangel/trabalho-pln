import json
import subprocess

# Carrega JSON original
with open(r"C:\Users\letic\.cache\huggingface\hub\datasets--friedrichor--MSR-VTT\snapshots\c1af215a96934854f42683c19c51391aaee6f962\msrvtt_train_7k.json", "r", encoding="utf-8") as f:
    dataset_json = json.load(f)

videos_ativos = []
videos_inativos = []

def verificar_video(url):
    """
    Usa yt_dlp para verificar se o vídeo existe sem baixar nada.
    Retorna True se ativo, False se inativo.
    """
    try:
        result = subprocess.run(
            ["python", "-m", "yt_dlp", "--skip-download", "--print", "title", url],
            capture_output=True, text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            return True
        else:
            return False
    except Exception:
        return False

for item in dataset_json:
    url = item["url"]
    if verificar_video(url):
        print(f"Vídeo ativo: {url}")
        videos_ativos.append(item)   # mantém estrutura original
    else:
        print(f"Vídeo inativo: {url}")
        videos_inativos.append(item)

# Salva apenas os ativos
with open("msrvtt_active.json", "w", encoding="utf-8") as f:
    json.dump(videos_ativos, f, ensure_ascii=False, indent=2)

# Salva apenas os inativos
with open("msrvtt_inactive.json", "w", encoding="utf-8") as f:
    json.dump(videos_inativos, f, ensure_ascii=False, indent=2)

print(f"Total de vídeos ativos: {len(videos_ativos)}")
print(f"Total de vídeos inativos: {len(videos_inativos)}")

""" Total de vídeos ativos: 4880
Total de vídeos inativos: 2130 """