import streamlit as st
from chatbot import responder

st.set_page_config(page_title="Bolso em dIA", page_icon="💰")

# 🎨 Estilo tipo banco (Bradesco vibes)
st.markdown("""
    <style>
    body {
        background-color: #f5f5f5;
    }
    .stApp {
        background-color: #ffffff;
    }
    h1 {
        color: #cc092f;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💰 Bolso em dIA")
st.write("Seu assistente financeiro inteligente")

if "historico" not in st.session_state:
    st.session_state.historico = []

pergunta = st.text_input("Digite sua pergunta:")

if pergunta:
    resposta, dados_grafico = responder(pergunta, st.session_state.historico)

    st.session_state.historico.append(("Você", pergunta))
    st.session_state.historico.append(("IA", resposta))

    st.write(f"**IA:** {resposta}")

    # 📈 gráfico
    if dados_grafico:
        st.subheader("📈 Evolução do investimento")
        st.line_chart(dados_grafico)

for autor, msg in st.session_state.historico:
    st.write(f"**{autor}:** {msg}")