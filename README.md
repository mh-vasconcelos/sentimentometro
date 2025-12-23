# ☁️ A Palavra do Dia Coletiva & Sentimentômetro

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange)

Uma aplicação interativa desenvolvida com **Streamlit** que coleta o "humor do dia" dos usuários e utiliza **Inteligência Artificial (Google Gemini)** para analisar sentimentos, gerar frases motivacionais (ou irônicas) e criar visualizações de dados em tempo real.

## 📋 Sobre o Projeto

Este projeto vai além de uma simples nuvem de palavras. Cada entrada do usuário é processada por um modelo de linguagem (LLM) que:
1.  **Analisa a palavra:** Identifica se é feliz, triste, neutra, raivosa, etc.
2.  **Calcula um Score:** Atribui uma nota matemática de "Tristeza" (0.0 a 1.0).
3.  **Reage:** Gera uma resposta personalizada (um "coach" engraçado) baseada no contexto.

Os dados são armazenados localmente e alimentam um **Ranking de Sentimentos** (o "Pódio da Tristeza") e uma **Nuvem de Palavras** coletiva.

## 🚀 Funcionalidades

* **Análise de Sentimento com IA:** Integração com o Google Gemini via LangChain para classificar palavras e gerar respostas em formato JSON.
* **Nuvem de Palavras Dinâmica:** Visualização gráfica das palavras mais frequentes utilizando `wordcloud` e `matplotlib`.
* **Ranking (Gamificação):** Um "Sentimentômetro" que utiliza Pandas para agrupar dados e mostrar quem são os usuários com maior acúmulo de "pontos de tristeza/raiva".
* **Persistência de Dados:** Armazenamento simples e eficiente em arquivo CSV (`words.csv`).
* **Interface Responsiva:** Design limpo e interativo com Streamlit.

## 🛠️ Tecnologias Utilizadas

* **Frontend:** [Streamlit](https://streamlit.io/)
* **IA & LLM:** [LangChain](https://www.langchain.com/) + [Google Gemini API](https://ai.google.dev/)
* **Manipulação de Dados:** [Pandas](https://pandas.pydata.org/)
* **Visualização:** [Matplotlib](https://matplotlib.org/) & [WordCloud](https://amueller.github.io/word_cloud/)
* **Ambiente:** Python & Dotenv

## 📦 Pré-requisitos

Antes de começar, você precisa ter instalado:
* [Python 3.10+](https://www.python.org/)
* Uma chave de API do Google AI Studio (Gratuita). [Obtenha aqui](https://aistudio.google.com/app/apikey).

## 🔧 Instalação e Execução

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-projeto.git](https://github.com/seu-usuario/seu-projeto.git)
    cd seu-projeto
    ```

2.  **Crie um ambiente virtual (Recomendado):**
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as Variáveis de Ambiente:**
    Crie um arquivo chamado `.env` na raiz do projeto e adicione sua chave
