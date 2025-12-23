import streamlit as st
import random
import os
import json
from dotenv import load_dotenv
from func import * 
from tratamento import *

# --- Configuração da IA (Gemini) ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7, 
    google_api_key=GOOGLE_API_KEY
)

def analisar_palavra_com_ia(palavra, nome_usuario):
    """
    Envia a palavra para o Gemini e retorna sentimento, score e frase.
    """
    prompt_template = """
    Você é um assistente divertido que analisa o "humor do dia" das pessoas com base em uma única palavra.
    O usuário {nome} disse que a palavra do dia dele é: "{palavra}".

    Sua tarefa:
    1. Identifique o sentimento dessa palavra (Felicidade, Tristeza, Raiva, Tédio, Esperança, etc).
    2. Atribua um 'score_tristeza' de 0.0 a 1.0, onde:
       - 0.0 é extemamente feliz/positivo.
       - 0.5 é neutro.
       - 1.0 é extremamente triste/raivoso/negativo.
    3. Crie uma frase curta (máximo 150 caracteres). Se for algo triste, seja um "coach motivacional engraçado". Se for feliz, seja um coach pessimista e mau-humorado.

    RETORNE APENAS UM JSON NO SEGUINTE FORMATO (sem crase, sem markdown):
    {{
        "sentimento_texto": "nome do sentimento",
        "score_tristeza": 0.0,
        "frase": "sua frase aqui"
    }}
    """
    
    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = prompt | llm
    
    try:
        resposta = chain.invoke({"palavra": palavra, "nome": nome_usuario})
        texto_limpo = resposta.content.replace('```json', '').replace('```', '').strip()
        dados = json.loads(texto_limpo)
        return dados
    except Exception as e:
        # Fallback caso a IA falhe
        return {
            "sentimento_texto": "Indefinido", 
            "score_tristeza": 0.5, 
            "frase": f"A IA bugou, mas sua palavra '{palavra}' foi anotada!"
        }
    
    



# --- Interface do Streamlit ---

st.set_page_config(layout="wide", page_title="Palavra do Dia com IA")
st.title("☁️ A Palavra do Dia Coletiva")

st.markdown("Qual palavra define melhor o seu dia hoje?")

col1, col2, col3 = st.columns([2, 1, 2]) 

with st.container(border=True):
    with col1:
        st.header("Contribua")
        nome_usuario = st.text_input("Digite seu nome", max_chars=60)
        palavra_usuario = st.text_input("Digite sua palavra:", max_chars=30)
        
        if st.button("Enviar Palavra", type="primary"):
            if palavra_usuario and nome_usuario:
                
                with st.spinner('A IA está analisando seu estado de espírito...'):
                    palavra_limpa = remover_acentos(palavra_usuario.strip().lower())
                    nome_limpo = remover_acentos(nome_usuario.strip().lower())

                    if " " in palavra_limpa:
                        st.warning("Ei, é uma nuvem de PALAVRAS. Digite apenas uma, por favor.")
                    else:
                        # CHAMADA DA IA
                        resultado_ia = analisar_palavra_com_ia(palavra_limpa, nome_limpo)
                        
                        score = float(resultado_ia['score_tristeza'])
                        frase = resultado_ia['frase']
                        sentimento_label = resultado_ia['sentimento_texto']
                        if score > 0.6:
                            st.warning(f"{frase}", icon="😢") # Triste/Raiva
                        elif score < 0.4:
                            st.success(f"{frase}", icon="😁") # Feliz
                        else:
                            st.info(f"{frase}", icon="😐") # Neutro

                        adicionar_palavra(palavra_limpa, nome_limpo, sentimento=score)
                        
                        st.caption(f"A IA classificou isso como: {sentimento_label} (Nível de Tristeza: {score})")

            else:
                st.error("Por favor, preencha seu nome e a palavra.")

with st.container(border=True):
    # --- Seção da Nuvem de Palavras ---
    st.header("Nossa Nuvem de Palavras")
    texto_completo = ler_todas_palavras()
    
    if not texto_completo.strip():
        st.info("A nuvem está vazia. Seja o primeiro a adicionar uma palavra!")
    else:
        try:
            figura_nuvem = gerar_nuvem_palavras(texto_completo)
            st.pyplot(figura_nuvem)
        except Exception as e:
            st.error("Poucas palavras para gerar a nuvem ainda.")

# Parte analítica
with st.container(border=True):
    try:
        df = gerar_df(ARQUIVO_PALAVRAS)
        
        if not df.empty:
            st.title("Sentimentômetro da Galera")
            
            # Agrupa e soma os scores de tristeza
            agrupado = df.groupby('usuario')['sentimento'].sum().rename('nível de tristeza').to_frame().sort_values(by=['nível de tristeza'], ascending=False)
            
            st.subheader("🏆 O Pódio da Tristeza (Scores dados pela IA)")
            st.write("A IA atribui notas de 0.0 (Feliz) a 1.0 (Triste/Puto). Aqui somamos tudo.")

            top_3 = agrupado.head(3)

            # Cria 3 colunas para o pódio
            c1, c2, c3 = st.columns(3)
            colunas_podio = [c1, c2, c3]
            emojis = ["🥇", "🥈", "🥉"]

            for i, (usuario_idx, row) in enumerate(top_3.iterrows()):
                if i < 3: 
                    with colunas_podio[i]:
                        val_formatado = f"{row['nível de tristeza']:.1f}" # Formata casa decimal
                        st.metric(label=f"{emojis[i]} {usuario_idx}", 
                                  value=f"{val_formatado} pts")
        else:
            st.write("Ainda sem dados suficientes para o ranking.")
            
    except Exception as e:
        st.write("Comece a adicionar palavras para ver o ranking!")