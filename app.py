from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import streamlit as st
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7
)

st.set_page_config(page_title="Llama Groq", page_icon="🤖", layout="centered")
st.title("Llama Groq")

if "messages" not in st.session_state: #verifica se a chave "messages" existe no estado da sessão, se não existir, cria uma lista vazia para armazenar as mensagens do chat.
    st.session_state.messages = []

messages = st.session_state["messages"] #recupera a lista de mensagens do estado da sessão e a armazena na variável "messages". Essa lista é usada para exibir o histórico do chat e para adicionar novas mensagens à medida que o usuário interage com o aplicativo.
for type, content in messages:
    chat = st.chat_message(type)
    chat.markdown(content)

in_message = st.chat_input("Digite sua mensagem aqui...")
if in_message:
    messages.append(("human", in_message))#adiciona a mensagem do usuário à lista de mensagens, indicando que é uma mensagem do tipo "human". Isso é importante para manter o histórico do chat e para que o modelo possa responder de forma adequada com base nas mensagens anteriores.
    chat = st.chat_message("human")
    chat.markdown(in_message)
    response = llm.invoke(messages).content #chama o método "invoke" do modelo de linguagem (llm) passando a lista de mensagens como entrada. O modelo processa as mensagens e gera uma resposta, que é armazenada na variável "response". A resposta é extraída do objeto retornado pelo modelo usando a propriedade "content".
    messages.append(("assistant", response)) #adiciona a resposta do modelo à lista de mensagens, indicando que é uma mensagem do tipo "assistant". Isso mantém o histórico do chat atualizado com a resposta gerada pelo modelo.
    chat = st.chat_message("assistant")
    chat.markdown(response) 

#para executar: streamlit run .\app.py