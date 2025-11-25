import streamlit as st
import pandas as pd
import random
import time

# ------------------------------------------------------------
# CONFIG DA PÁGINA
# ------------------------------------------------------------
st.set_page_config(
    page_title="Sorteio Matrícula Premiada",
    layout="wide"
)

# ------------------------------------------------------------
# CSS GLOBAL (cores, fundo, botão, upload elegante)
# ------------------------------------------------------------
st.markdown("""
<style>

:root {
    --white: #ffffff;
}

html, body, .stApp {
    background-color: #010038 !important;
}

/* Remove fundo escuro que apareceu no menu */
section[data-testid="stHeader"] {
    background: rgba(0,0,0,0) !important;
}

/* Centralização geral */
.main-container {
    max-width: 1100px;
    margin: auto;
}

/* Logo */
.header-logo {
    width: 140px;
    display: block;
    margin: 25px auto 10px auto;
}

/* Texto principal (MENOR AGORA) */
.hero-title {
    color: white;
    font-size: 34px;
    font-weight: 700;
    line-height: 1.25;
}

.hero-sub {
    color: white;
    font-size: 19px;
    margin-top: 12px;
}

/* Imagem menor */
.hero-img {
    max-width: 800px;
    width: 100%;
    margin: auto;
    display: block;
}

/* Botões */
div.stButton > button {
    background-image: linear-gradient(82deg, #ff8070, #3d4ed7);
    color: var(--white);
    border-radius: 1000px;
    padding: 12px 40px;
    font-weight: 600;
    font-size: 18px;
    border: none;
    transition: 0.2s;
    display: block;
    margin: auto;
}

div.stButton > button:hover {
    transform: scale(1.04);
}

/* Upload bonito — CENTRALIZADO */
.custom-upload > label {
    background-color: #1a1a5a;
    padding: 25px;
    width: 80%;
    margin: auto;
    border-radius: 20px;
    border: 2px dashed #3d4ed7;
    text-align: center;
    color: white !important;
    cursor: pointer;
    font-size: 19px;
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

</style>
""", unsafe_allow_html=True)

# =============================================================
# 1) LOGO NO TOPO
# =============================================================
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.image("logoisaac.svg", use_column_width=False, width=160)

# =============================================================
# 2) SEÇÃO HERO (imagem + texto ao lado)
# =============================================================

col_img, col_txt = st.columns([1.1, 1])

with col_img:
    st.image("meninasorteio.webp", use_column_width=False, width=800)

with col_txt:
    st.markdown("""
    <div class="hero-title">
        Chegou o grande momento! 🎉<br>
        Você acumulou <i>números da sorte</i><br>
        utilizando as funcionalidades da<br>
        Plataforma isaac.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-sub">
        Agora é hora de descobrir qual escola será a grande vencedora<br>
        da campanha <b>Matrícula Premiada</b>. Boa sorte! 🍀
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

# =============================================================
# 3) ÁREA DO SORTEIO — Centralizada
# =============================================================

st.markdown("<hr style='opacity:0.3;'>", unsafe_allow_html=True)

st.markdown(
    "<h2 style='color:white; text-align:center;'>🎉 Realizar Sorteio</h2>",
    unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)

# Caixa premium (centralizada)
st.markdown(
    '<div class="custom-upload"><label>📁 Envie o arquivo CSV com as escolas participantes</label></div>',
    unsafe_allow_html=True
)

file = st.file_uploader("", type=["csv"])

# ----------- se CSV enviado -----------
if file is not None:
    df = pd.read_csv(file)
    st.success("CSV carregado com sucesso!")

    # BOTÃO CENTRALIZADO
    botao = st.button("Sortear agora!")

    if botao:
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
            nome_rodando = random.choice(nomes_temp)
            placeholder.markdown(
                f"<h3 style='color:white; text-align:center;'>{nome_rodando}</h3>",
                unsafe_allow_html=True
            )
            time.sleep(0.05 + (i * 0.015))

        moldura = f"""
        <div style="
            border-radius: 25px;
            padding: 3px;
            background: linear-gradient(82deg,#ff8070,#3d4ed7);
            width: 70%;
            margin: auto;
            margin-top: 25px;
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
                <p style='font-size:20px; margin-top:10px;'>CNPJ: <b>{vencedor['cnpj']}</b></p>
            </div>
        </div>
        """

        placeholder.markdown(moldura, unsafe_allow_html=True)
        st.balloons()

st.markdown("</div>", unsafe_allow_html=True)
