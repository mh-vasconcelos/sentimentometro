from wordcloud import WordCloud
import matplotlib.pyplot as plt
import csv
import os
import pandas as pd

ARQUIVO_PALAVRAS = "words.csv"

def adicionar_palavra(palavra, usuario, sentimento):
    """
    Adiciona uma nova palavra e o usuário ao arquivo CSV.
    """
    file_exists = os.path.exists(ARQUIVO_PALAVRAS) and os.path.getsize(ARQUIVO_PALAVRAS) > 0

    try:
        with open(ARQUIVO_PALAVRAS, "a", encoding="utf-8", newline='') as f:
            fieldnames = ["palavra", "usuario", "sentimento"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
                
            writer.writerow({"palavra": palavra, "usuario": usuario, "sentimento": sentimento})
            
    except Exception as e:
        print(f"Erro ao salvar a palavra no CSV: {e}")

def ler_todas_palavras():
    """
    Lê o arquivo CSV, extrai APENAS a coluna 'palavra' e retorna 
    todas as palavras como um único texto (para a WordCloud).
    """
    if not os.path.exists(ARQUIVO_PALAVRAS):
        return "" 

    palavras_lista = []
    
    try:
        with open(ARQUIVO_PALAVRAS, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'palavra' in row:
                    palavras_lista.append(row['palavra'])
                    
    except Exception as e:
        print(f"Erro ao ler as palavras: {e}")
        return ""
    
    return " ".join(palavras_lista)

def gerar_df(arquivo):    
    """Lê o CSV e retorna um DataFrame do Pandas"""

    if not os.path.exists(arquivo):
        return pd.DataFrame() 
    return pd.read_csv(arquivo)

def gerar_nuvem_palavras(texto):
    """Gera a imagem da nuvem de palavras a partir de um texto."""
    
    stopwords_pt = ["de", "a", "o", "que", "e", "do", "da", "em", "um", 
                    "para", "com", "não", "uma", "os", "na", "se", "mas"]

    wc = WordCloud(
        width=800, 
        height=400, 
        background_color="white",
        stopwords=stopwords_pt,
        colormap="viridis",
        collocations=False 
    ).generate(texto)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off") 
    
    return fig