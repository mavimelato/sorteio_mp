import streamlit as st
import pandas as pd
import random
import time

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------
st.set_page_config(
    page_title="Sorteio | Matrícula Premiada",
    layout="centered"
)

# ------------------------------------------------------------
# CSS DO LAYOUT (NAVBAR + ESTILO GERAL)
# ------------------------------------------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, .stApp {
    background-color: #0f172a !important;
    font-family: 'Inter', sans-serif;
}

/* NAVBAR */
.navbar {
    width: 100%;
    padding: 15px 30px;
    background-color: #0f172a;
    border-bottom: 1px solid #1e293b;
    display: flex;
    align-items: center;
    justify-content: left;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 999;
}

.navbar img {
    height: 38px;
}

/* Espaço abaixo da navbar */
.page-content {
    margin-top: 90px;
}

/* CARD DO SORTEIO */
.card {
    background: #1e293b;
    border-radius: 20px;
    padding: 35px;
    width: 520px;
    margin-left: auto;
    margin-right: auto;
    box-shadow: 0px 0px 15px #00000030;
}

.card-title {
    color: white;
    text-align: center;
    font-size: 26px;
    font-weight: 700;
    margin-bottom: 25px;
}

/* BOTÃO */
div.stButton > button {
    background-image: linear-gradient(82deg, #ff8070, #3d4ed7);
    color: white;
    border-radius: 12px;
    padding: 14px 30px;
    font-size: 17px;
    border: none;
    width: 100%;
    transition: 0.2s;
}

div.stButton > button:hover {
    transform: scale(1.03);
}

.upload-msg {
    text-align: center;
    color: #CBD5E1;
    font-size: 15px;
    margin-bottom: 5px;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# NAVBAR
# ------------------------------------------------------------
st.markdown("""
<div class="navbar">
    <img src="https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg">
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# CONTEÚDO PRINCIPAL
# ------------------------------------------------------------
st.markdown('<div class="page-content">', unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown("<div class='card-title'>Realizar Sorteio</div>", unsafe_allow_html=True)

st.markdown("<p class='upload-msg'>📁 Envie o arquivo CSV com as escolas participantes</p>", unsafe_allow_html=True)

file = st.file_uploader("", type=["csv"])

# ------------------------------------------------------------
# LÓGICA DO SORTEIO
# ------------------------------------------------------------
def formatar_cnpj(cnpj):
    cnpj = str(cnpj).zfill(14)
    return f"{cnpj[0:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}"

if file:
    df = pd.read_csv(file)
    st.success("CSV carregado com sucesso!")

    sortear = st.button("Sortear agora!")

    if sortear:
        tickets = []

        for _, row in df.iterrows():
            tickets.extend([{
                "cnpj": row["cnpj"],
                "branch_name": row["branch_name"]
            }] * int(row["numeros_da_sorte"]))

        vencedor = random.choice(tickets)

        placeholder = st.empty()
        nomes_temp = [row["branch_name"] for _, row in df.iterrows()]

        for i in range(30):
            nome = random.choice(nomes_temp)
            placeholder.markdown(
                f"<h3 style='color:white; text-align:center;'>{nome}</h3>",
                unsafe_allow_html=True
            )
            time.sleep(0.06)

        resultado = f"""
        <div style="
            margin-top:20px;
            background:#0f172a;
            border-radius:15px;
            padding:25px;
            text-align:center;
            color:white;
            border:2px solid #3d4ed7;
        ">
            <h3>🏆 Escola Vencedora</h3>
            <h2 style="margin-top:10px;">{vencedor['branch_name']}</h2>
            <p style="margin-top:10px;">CNPJ: <b>{formatar_cnpj(vencedor['cnpj'])}</b></p>
        </div>
        """
        placeholder.markdown(resultado, unsafe_allow_html=True)
        st.balloons()

st.markdown("</div>", unsafe_allow_html=True)  # fecha card
st.markdown("</div>", unsafe_allow_html=True)  # fecha page-content
