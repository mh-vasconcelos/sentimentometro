import streamlit as st
from func import *
from frases import *
import random
from tratamento import *


# --- Interface do Streamlit ---

st.set_page_config(layout="wide")
st.title("☁️ A Palavra do Dia Coletiva")

st.markdown("Qual palavra, em português, define melhor o seu dia hoje?")

# Criamos colunas para organizar a interface
col1, col2, col3 = st.columns([2, 1, 2]) # A coluna da nuvem (direita) é 2x maior
with st.container(border=True):
  with col1:
      # --- Seção de Input ---
      st.header("Contribua")
      nome_usuario = st.text_input("Digite seu nome", max_chars=60)
      palavra_usuario = st.text_input("Digite sua palavra:", max_chars=30)
      
      if st.button("Enviar Palavra"):
          if palavra_usuario:
              # Limpa a palavra (remove espaços e converte para minúscula)
              palavra_limpa = remover_acentos(palavra_usuario.strip().lower())
              nome_limpo = remover_acentos(nome_usuario.strip().lower())

              if " " in palavra_limpa:
                  st.warning("Por favor, envie apenas uma palavra.")
              else:
                  if palavra_limpa in palavras_felizes:
                    frase_resposta = remover_acentos(random.choice(frases_coach_felizes))
                    # st.success vem com um ícone de "check"
                    st.success(frase_resposta, icon="😊")
                    adicionar_palavra(palavra_limpa, nome_limpo, sentimento=0.0)
                  elif palavra_limpa in palavras_tristes:
                    frase_resposta = remover_acentos(random.choice(frases_coach_tristes))
                    # st.warning vem com um ícone de "aviso"
                    st.warning(frase_resposta)
                    adicionar_palavra(palavra_limpa, nome_limpo, sentimento=1.0)
                  else:
                    frase_resposta = remover_acentos(random.choice(frases_coach_neutras))
                    palavras_neutras.append(palavra_limpa)
                    # st.info vem com um ícone de "informação"
                    st.info(frase_resposta, icon="📝")
                    adicionar_palavra(palavra_limpa, nome_limpo, sentimento=0.5)
                  
                  st.success(f"Palavra '{palavra_limpa}' adicionada à nuvem!")
                  # Força o Streamlit a rodar novamente para atualizar a nuvem. 
                  # Mas antes, deixa um time sleep para a frase motivacional aparecer na tela
                #   time.sleep(6)
                #   st.rerun()
          else:
              st.error("Por favor, digite uma palavra.")

with st.container(border=True):

# with col3:
    # --- Seção da Nuvem de Palavras ---
    st.header("Nossa Nuvem de Palavras")
    
    # Lê todo o texto acumulado
    texto_completo = ler_todas_palavras()
    
    if not texto_completo.strip():
        st.info("A nuvem está vazia. Seja o primeiro a adicionar uma palavra!")
    else:
        # Gera e exibe a nuvem
        figura_nuvem = gerar_nuvem_palavras(texto_completo)
        st.pyplot(figura_nuvem)

# Parte analítica
with st.container(border=True):
   df = gerar_df(ARQUIVO_PALAVRAS)
   st.title("Sentimentômetro")
   agrupado = df.groupby('usuario')['sentimento'].sum().rename('nível de tristeza').to_frame().sort_values(by=['nível de tristeza'], ascending=False)
   st.subheader("🏆 O Pódio da Tristeza")
   st.write("Quanto maior o índice, mais triste/com raiva o usuário está")

# Pega os 3 primeiros do seu dataframe
top_3 = agrupado.head(3)

# Cria 3 colunas
col1, col2, col3 = st.columns(3)

# Lista de colunas e emojis para facilitar
colunas = [col1, col2, col3]
emojis = ["🥇", "🥈", "🥉"]

# Itera sobre os top 3 e cria um st.metric para cada
# (usamos .iterrows() para pegar o usuário (indice) e a linha (row))
for i, (usuario, row) in enumerate(top_3.iterrows()):
    with colunas[i]:
        # 'usuario' vem do índice do DataFrame
        # row['nível de tristeza'] pega o valor da coluna
        st.metric(label=f"{emojis[i]} {usuario}", 
                  value=f"{row['nível de tristeza']} pts")