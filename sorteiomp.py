import streamlit as st
import pandas as pd
import random
import time

# ------------------------------------------------------------
# CONFIG DA PÁGINA
# ------------------------------------------------------------
st.set_page_config(
    page_title="Sorteio Matrícula Premiada",
    layout="centered"   # <<< deixa a página mais estreita e organizada
)

# ------------------------------------------------------------
# CSS GLOBAL
# ------------------------------------------------------------
st.markdown("""
<style>

:root {
    --white: #ffffff;
}

/* Fundo principal */
html, body, .stApp {
    background-color: #010038 !important;
}

/* Remove fundo do menu/header */
header, .st-emotion-cache-18ni7ap, .st-emotion-cache-1dp5vir {
    background: transparent !important;
    box-shadow: none !important;
}

/* HERO TEXT */
.hero-title {
    color: white;
    font-size: 36px;   /* diminuído */
    font-weight: 700;
    line-height: 1.25;
}

.hero-sub {
    color: white;
    font-size: 18px;   /* diminuído */
    margin-top: 10px;
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
    transition: 0.15s;
}

div.stButton > button:hover {
    transform: scale(1.04);
}

/* Upload estilizado */
.custom-upload > label {
    background-color: #1a1a5a;
    padding: 20px;
    width: 80%;
    border-radius: 20px;
    border: 2px dashed #3d4ed7;
    text-align: center;
    color: white !important;
    cursor: pointer;
    font-size: 17px;
    display: block;
    margin-left: auto;
    margin-right: auto;
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
# LOGO CENTRAL
# =============================================================
st.image("logoisaac.svg", width=140)

# =============================================================
# HERO — IMAGEM + TEXTO CENTRALIZADOS
# =============================================================
col_img, col_txt = st.columns([1, 1])

with col_img:
    st.image("meninasorteio.webp", width=350)   # <<< TAMANHO CONTROLADO

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

# Espaço
st.markdown("<br><br>", unsafe_allow_html=True)

# =============================================================
# ÁREA DO SORTEIO — TOTALMENTE CENTRALIZADO
# =============================================================
st.markdown("<h2 style='color:white; text-align:center;'>🎉 Realizar Sorteio</h2>", unsafe_allow_html=True)

# Upload card
st.markdown(
    '<div class="custom-upload"><label>📁 Envie o arquivo CSV com as escolas participantes</label></div>',
    unsafe_allow_html=True
)

file = st.file_uploader("", type=["csv"])

# Centraliza tudo do sorteio
center = st.container()
with center:
    if file is not None:
        df = pd.read_csv(file)
        st.success("CSV carregado com sucesso!")

        sortear_center = st.columns([1, 1, 1])
        with sortear_center[1]:
            if st.button("Sortear agora!"):
                tickets = []

                for _, row in df.iterrows():
                    tickets.extend([{
                        "cnpj": row["cnpj"],
                        "branch_name": row["branch_name"]
                    }] * int(row["numeros_da_sorte"]))

                random.seed()
                vencedor = random.choice(tickets)

                # Animação
                placeholder = st.empty()
                nomes_temp = [row["branch_name"] for _, row in df.iterrows()]

                for i in range(35):
                    nome_rodando = random.choice(nomes_temp)
                    placeholder.markdown(
                        f"<h3 style='color:white; text-align:center;'>{nome_rodando}</h3>",
                        unsafe_allow_html=True
                    )
                    time.sleep(0.05 + (i * 0.015))

                # Moldura final
                moldura = f"""
                <div style="
                    border: 0;
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
