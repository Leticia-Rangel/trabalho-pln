""" import re
import matplotlib.pyplot as plt

# Lê o arquivo TXT
with open("avaliacao_resultados.txt", "r", encoding="utf-8") as f:
    conteudo = f.read()

# Extrair consultas
consultas = re.findall(r"Consulta: (.+)", conteudo)

# Extrair métricas
similaridades = [float(x) for x in re.findall(r"Similaridade média \(busca\): ([0-9.]+)", conteudo)]
duracoes = [float(x) for x in re.findall(r"Duração média dos áudios: ([0-9.]+)", conteudo)]
energias = [float(x) for x in re.findall(r"Energia RMS média: ([0-9.]+)", conteudo)]
loudnesses = [float(x) for x in re.findall(r"Loudness médio: (-?[0-9.]+)", conteudo)]
score_min = [float(x) for x in re.findall(r"Score mínimo: ([0-9.]+)", conteudo)]
score_max = [float(x) for x in re.findall(r"máximo: ([0-9.]+)", conteudo)]
desvio = [float(x) for x in re.findall(r"desvio: ([0-9.]+)", conteudo)]

# Função genérica para métricas positivas
def gerar_grafico(valores, titulo, ylabel, filename):
    plt.figure(figsize=(12,6))
    bars = plt.bar(consultas, valores, color="skyblue", edgecolor="black")

    # Ajusta limite do eixo Y
    max_val = max(valores)
    plt.ylim(0, max_val + (0.1 if max_val < 1 else 0.5))

    # Adiciona valores acima das barras
    for bar in bars:
        yval = bar.get_height()
        offset = 0.02 if yval < 0.1 else 0.05
        plt.text(bar.get_x() + bar.get_width()/2, yval + offset,
                 f"{yval:.2f}", ha="center", va="bottom", fontsize=9)

    plt.title(titulo, fontsize=14)
    plt.xlabel("Consulta", fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Gráfico salvo como {filename}")

# Função específica para loudness (valores negativos)
def gerar_grafico_loudness(valores, titulo, ylabel, filename):
    plt.figure(figsize=(12,6))
    bars = plt.bar(consultas, valores, color="skyblue", edgecolor="black")

    # Ajusta eixo Y para valores negativos
    min_val = min(valores)
    max_val = max(valores)
    plt.ylim(min_val - 0.5, max_val + 0.5)

    # Adiciona valores acima das barras
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.2,
                 f"{yval:.2f}", ha="center", va="bottom", fontsize=9)

    plt.title(titulo, fontsize=14)
    plt.xlabel("Consulta", fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f" Gráfico de loudness salvo como {filename}")

# Gerar todos os gráficos
gerar_grafico(similaridades, "Similaridade Média por Consulta", "Similaridade", "similaridade.png")
gerar_grafico(duracoes, "Duração Média dos Áudios por Consulta", "Duração (s)", "duracao.png")
gerar_grafico(energias, "Energia RMS Média por Consulta", "Energia RMS", "energia.png")
gerar_grafico_loudness(loudnesses, "Loudness Médio por Consulta", "Loudness (dBFS)", "loudness.png")
gerar_grafico(score_min, "Score Mínimo por Consulta", "Score mínimo", "score_min.png")
gerar_grafico(score_max, "Score Máximo por Consulta", "Score máximo", "score_max.png")
gerar_grafico(desvio, "Desvio Padrão dos Scores por Consulta", "Desvio", "desvio.png")
 """


import re
import matplotlib.pyplot as plt

# Lê o arquivo TXT
with open("avaliacao_resultados.txt", "r", encoding="utf-8") as f:
    conteudo = f.read()

# Extrair consultas
consultas = re.findall(r"Consulta: (.+)", conteudo)

# Extrair métricas
similaridades = [float(x) for x in re.findall(r"Similaridade média \(busca\): ([0-9.]+)", conteudo)]
duracoes = [float(x) for x in re.findall(r"Duração média dos áudios: ([0-9.]+)", conteudo)]
energias = [float(x) for x in re.findall(r"Energia RMS média: ([0-9.]+)", conteudo)]
loudnesses = [float(x) for x in re.findall(r"Loudness médio: (-?[0-9.]+)", conteudo)]
score_min = [float(x) for x in re.findall(r"Score mínimo: ([0-9.]+)", conteudo)]
score_max = [float(x) for x in re.findall(r"máximo: ([0-9.]+)", conteudo)]
desvio = [float(x) for x in re.findall(r"desvio: ([0-9.]+)", conteudo)]

# Lista de métricas (sem taxa de silêncio)
metricas = [
    (similaridades, "Similaridade Média", "Similaridade"),
    (duracoes, "Duração Média dos Áudios", "Duração (s)"),
    (energias, "Energia RMS Média", "Energia RMS"),
    (loudnesses, "Loudness Médio", "Loudness (dBFS)"),
    (score_min, "Score Mínimo", "Score mínimo"),
    (score_max, "Score Máximo", "Score máximo"),
    (desvio, "Desvio Padrão dos Scores", "Desvio"),
]

# Criar painel de subplots (3 linhas x 3 colunas)
fig, axes = plt.subplots(3, 3, figsize=(18,12))
axes = axes.flatten()

for i, (valores, titulo, ylabel) in enumerate(metricas):
    ax = axes[i]
    bars = ax.bar(consultas, valores, color="skyblue", edgecolor="black")

    # Ajuste especial para loudness (valores negativos)
    if titulo.startswith("Loudness"):
        min_val = min(valores)
        max_val = max(valores)
        ax.set_ylim(min_val - 0.5, max_val + 0.5)
        offset = 0.2

    # Ajuste especial para desvio padrão (valores muito pequenos)
    elif titulo.startswith("Desvio"):
        ax.set_ylim(0, 0.1)   # fixa o eixo Y para dar espaço
        offset = 0.01

    # Ajuste padrão para métricas positivas
    else:
        max_val = max(valores)
        ax.set_ylim(0, max_val + (0.1 if max_val < 1 else 0.5))
        offset = 0.05

    # Adicionar valores acima das barras
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + offset,
                f"{yval:.2f}", ha="center", va="bottom", fontsize=8)

    ax.set_title(titulo, fontsize=12)
    ax.set_xlabel("Consulta", fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.tick_params(axis="x", rotation=45)

# Remove subplots extras (ficam 2 espaços vazios)
for j in range(len(metricas), len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.savefig("painel_metricas.png")
plt.close()

print("✅ Painel completo salvo como 'painel_metricas.png'")
