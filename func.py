from wordcloud import WordCloud
import matplotlib.pyplot as plt
import csv
import os
import pandas as pd
from frases import palavras_felizes, palavras_tristes

# Define o nome do arquivo que usaremos como nosso "banco de dados"
ARQUIVO_PALAVRAS = "words.csv"

# --- Funções Auxiliares ---
def adicionar_palavra(palavra, usuario, sentimento):
    """
    Adiciona uma nova palavra e o usuário ao arquivo CSV.
    """
    
    # Verifica se o arquivo já existe para sabermos se precisamos escrever o cabeçalho
    # Usamos 'os.path.getsize' para também tratar casos de arquivos vazios
    file_exists = os.path.exists(ARQUIVO_PALAVRAS) and os.path.getsize(ARQUIVO_PALAVRAS) > 0

    try:
        # Abrimos o arquivo no modo 'a' (append)
        # newline='' é essencial para o módulo CSV funcionar corretamente no Windows
        with open(ARQUIVO_PALAVRAS, "a", encoding="utf-8", newline='') as f:
            
            # Define os nomes das colunas (nosso padrão)
            fieldnames = ["palavra", "usuario", "sentimento"]
            
            # Usamos DictWriter para facilitar a escrita baseada nos nomes das colunas
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            # Se o arquivo for novo (ou vazio), escreve o cabeçalho primeiro
            if not file_exists:
                writer.writeheader()
                
            # Escreve a linha com os novos dados
            writer.writerow({"palavra": palavra, "usuario": usuario, "sentimento": sentimento})
            
    except Exception as e:
        # Em um app Streamlit, você usaria st.error(), mas print funciona
        print(f"Erro ao salvar a palavra no CSV: {e}")

def ler_todas_palavras():
    """
    Lê o arquivo CSV, extrai APENAS a coluna 'palavra' e retorna 
    todas as palavras como um único texto (para a WordCloud).
    """
    if not os.path.exists(ARQUIVO_PALAVRAS):
        return "" # Retorna vazio se o arquivo não existir

    palavras_lista = []
    
    try:
        with open(ARQUIVO_PALAVRAS, "r", encoding="utf-8") as f:
            
            # Usamos DictReader para ler o CSV como um dicionário (ex: row['palavra'])
            reader = csv.DictReader(f)
            
            for row in reader:
                # Adicionamos à lista apenas o valor da coluna 'palavra'
                if 'palavra' in row:
                    palavras_lista.append(row['palavra'])
                    
    except csv.Error:
        # Isso pode acontecer se o arquivo estiver mal formatado ou sem cabeçalho
        print(f"Erro ao ler o arquivo CSV. Verifique o formato de {ARQUIVO_PALAVRAS}")
        return ""
    except Exception as e:
        print(f"Erro ao ler as palavras: {e}")
        return ""
    
    # A WordCloud espera um único stringão com todas as palavras, separadas por espaço
    return " ".join(palavras_lista)

def gerar_df(ARQUIVO_PALAVRAS):    
    return pd.read_csv(ARQUIVO_PALAVRAS)
def gerar_stats(df):
  if df is None:
    df = gerar_df(ARQUIVO_PALAVRAS=ARQUIVO_PALAVRAS)
  
    
        
    
def gerar_nuvem_palavras(texto):
    """Gera a imagem da nuvem de palavras a partir de um texto."""
    
    # Define algumas stopwords em português para ignorar palavras comuns
    # Você pode expandir esta lista
    stopwords_pt = ["de", "a", "o", "que", "e", "do", "da", "em", "um", 
                    "para", "com", "não", "uma", "os", "na", "se", "mas"]

    # Cria o objeto WordCloud
    # background_color="white" e colormap="viridis" são boas opções estéticas
    wc = WordCloud(
        width=400, 
        height=200, 
        background_color="white",
        stopwords=stopwords_pt,
        colormap="viridis",
        collocations=False # Evita que a biblioteca junte palavras (ex: "bom dia")
    ).generate(texto)

    # Usa matplotlib para criar a figura
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off") # Remove os eixos x e y
    
    # Retorna a figura do matplotlib para o Streamlit exibir
    return fig