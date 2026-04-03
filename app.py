from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import streamlit as st
from langchain_groq import ChatGroq

DEFAULT_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "openai/gpt-oss-120b",
]

st.set_page_config(page_title="Bertoldi ChatAI", page_icon="🤖", layout="centered")
st.title("Bertoldi ChatAI")

st.sidebar.header("Configurações")
selected_model = st.sidebar.selectbox(
    "Escolha o modelo",
    options=DEFAULT_MODELS + ["Outro (digitar manualmente)"],
    index=0,
)

custom_model = ""
if selected_model == "Outro (digitar manualmente)":
    custom_model = st.sidebar.text_input(
        "Nome do modelo",
        placeholder="Ex.: llama-3.3-70b-versatile",
    ).strip()

model_name = custom_model if custom_model else selected_model
temperature = st.sidebar.slider("Temperatura", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

if selected_model == "Outro (digitar manualmente)" and not custom_model:
    st.sidebar.warning("Informe o nome do modelo para continuar.")

st.sidebar.markdown("---")
st.sidebar.markdown(
    "Criado por Rodrigo Bertoldi Pereira - [rodrigorbp@gmail.com](mailto:rodrigorbp@gmail.com)"
)

if "messages" not in st.session_state: #verifica se a chave "messages" existe no estado da sessão, se não existir, cria uma lista vazia para armazenar as mensagens do chat.
    st.session_state.messages = []

messages = st.session_state["messages"] #recupera a lista de mensagens do estado da sessão e a armazena na variável "messages". Essa lista é usada para exibir o histórico do chat e para adicionar novas mensagens à medida que o usuário interage com o aplicativo.
for type, content in messages:
    chat = st.chat_message(type)
    chat.markdown(content)

in_message = st.chat_input("Digite sua mensagem aqui...")
if in_message:
    if selected_model == "Outro (digitar manualmente)" and not custom_model:
        st.error("Defina um modelo valido no menu lateral antes de enviar.")
        st.stop()
    llm = ChatGroq(model=model_name, temperature=temperature)
    messages.append(("human", in_message))#adiciona a mensagem do usuário à lista de mensagens, indicando que é uma mensagem do tipo "human". Isso é importante para manter o histórico do chat e para que o modelo possa responder de forma adequada com base nas mensagens anteriores.
    chat = st.chat_message("human")
    chat.markdown(in_message)
    response = llm.invoke(messages).content #chama o método "invoke" do modelo de linguagem (llm) passando a lista de mensagens como entrada. O modelo processa as mensagens e gera uma resposta, que é armazenada na variável "response". A resposta é extraída do objeto retornado pelo modelo usando a propriedade "content".
    messages.append(("assistant", response)) #adiciona a resposta do modelo à lista de mensagens, indicando que é uma mensagem do tipo "assistant". Isso mantém o histórico do chat atualizado com a resposta gerada pelo modelo.
    chat = st.chat_message("assistant")
    chat.markdown(response) 

#para executar: streamlit run .\app.py