import streamlit as st 
from streamlit_chat import message
from model import gerar_resposta, get_conversas, limpar_historico

st.set_page_config(layout="centered", initial_sidebar_state="collapsed")

messages = get_conversas()

for m in messages:
    message(m["pergunta"], is_user=True, allow_html=True)
    message(m["resposta"], is_user=False, allow_html=True)


st.sidebar.title("Configurações")
if st.sidebar.button("🗑️ Limpar Histórico"):
    limpar_historico()
    st.session_state["key"] = 0  # resetar a chave também
    st.rerun()

key = st.session_state.get("key", 0)
input_text = st.text_input("Escreva uma mensagem", value="", key=key)
if st.button("Enviar"):
    if "key" not in st.session_state: 
        st.session_state["key"] = 0
    st.session_state["key"] += 1
    gerar_resposta(input_text)
    st.rerun()
