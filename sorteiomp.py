import streamlit as st
import pandas as pd
import random
import time

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------
st.set_page_config(
    page_title="Sorteio Matrícula Premiada",
    layout="centered"
)

# ------------------------------------------------------------
# CSS
# ------------------------------------------------------------
st.markdown("""
<style>

html, body, .stApp {
    background-color: #010038 !important;
}

/* Remove fundo do menu/header do Streamlit */
header, .st-emotion-cache-18ni7ap, .st-emotion-cache-1dp5vir {
    background: transparent !important;
    box-shadow: none !important;
}

/* CONTAINER CENTRALIZADO */
.main-container {
    max-width: 600px;
    margin: auto;
}

/* Título */
h2 {
    color: white !important;
    text-align: center !important;
    font-weight: 800;
}

/* Upload estilizado */
.custom-upload > label {
    background-color: #1a1a5a;
    padding: 22px;
    width: 100%;
    border-radius: 18px;
    border: 2px dashed #3d4ed7;
    text-align: center;
    color: white !important;
    cursor: pointer;
    font-size: 17px;
    display: block;
    transition: 0.3s;
}

.custom-upload > label:hover {
    background-color: #23236d;
    border-color: #ff8070;
}

.custom-upload input[type="file"] {
    display: none;
}

/* Botão */
div.stButton > button {
    background-image: linear-gradient(82deg, #ff8070, #3d4ed7);
    color: #ffffff;
    border-radius: 1000px;
    padding: 12px 40px;
    font-weight: 600;
    font-size: 18px;
    border: none;
    transition: 0.15s;
}

div.stButton > button:hover {
    transform: scale(1.04);
}

/* Ajustar mensagens de sucesso */
.stAlert {
    text-align: center !important;
    width: 100% !important;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# LOGO
# ------------------------------------------------------------
st.image("logoisaac.svg", width=120)

# ------------------------------------------------------------
# CONTEÚDO CENTRAL
# ------------------------------------------------------------
st.markdown("<div class='main-container'>", unsafe_allow_html=True)

st.markdown("<h2>🎉 Realizar Sorteio</h2>", unsafe_allow_html=True)

# Upload
st.markdown(
    '<div class="custom-upload"><label>📁 Envie o arquivo CSV com as escolas participantes</label></div>',
    unsafe_allow_html=True
)

file = st.file_uploader("", type=["csv"])

if file:
    df = pd.read_csv(file)
    st.success("CSV carregado com sucesso!")

    center_col = st.columns([1, 2, 1])[1]
    with center_col:
        if st.button("Sortear agora!"):
            tickets = []

            for _, row in df.iterrows():
                tickets.extend([{
                    "cnpj": row["cnpj"],
                    "branch_name": row["branch_name"]
                }] * int(row["numeros_da_sorte"]))

            random.seed()
            vencedor = random.choice(tickets)

            placeholder = st.empty()
            nomes_temp = [row["branch_name"] for _, row in df.iterrows()]

            for i in range(35):
                nome_temp = random.choice(nomes_temp)
                placeholder.markdown(
                    f"<h3 style='color:white; text-align:center;'>{nome_temp}</h3>",
                    unsafe_allow_html=True,
                )
                time.sleep(0.05 + (i * 0.015))

            moldura = f"""
            <div style="
                border-radius: 25px;
                padding: 3px;
                background: linear-gradient(82deg,#ff8070,#3d4ed7);
                margin-top: 30px;
            ">
                <div style="
                    background:#010038;
                    border-radius: 22px;
                    padding: 30px;
                    color:white;
                    text-align:center;
                ">
                    <h2 style='margin-bottom:10px;'>🏆 Vencedor</h2>
                    <h3>{vencedor['branch_name']}</h3>
                    <p style='font-size:20px; margin-top:10px;'>
                        CNPJ: <b>{vencedor['cnpj']}</b>
                    </p>
                </div>
            </div>
            """

            placeholder.markdown(moldura, unsafe_allow_html=True)
            st.balloons()

st.markdown("</div>", unsafe_allow_html=True)
