import streamlit as st
import pandas as pd
import random
import time

# ------------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ------------------------------------------------------------
st.set_page_config(
    page_title="Sorteio Matrícula Premiada",
    layout="centered"
)

# ------------------------------------------------------------
# ESTILO CUSTOMIZADO (cores + gradiente do botão + fundo)
# ------------------------------------------------------------
custom_css = """
<style>

:root {
    --white: #ffffff;
}

html, body, .stApp {
    background-color: #010038 !important;
}

/* Remove a barra superior cinza padrão do Streamlit */
header, .css-18ni7ap, .css-1dp5vir, .st-emotion-cache-18ni7ap {
    background-color: #010038 !important;
    box-shadow: none !important;
}

/* Diminuir tamanho do título (h2) */
h2 {
    font-size: 1.8rem !important;
    color: white !important;
    text-align: center;
}

/* Botão customizado */
div.stButton > button {
    background-image: linear-gradient(82deg, #ff8070, #3d4ed7);
    color: var(--white);
    text-align: center;
    transform-style: preserve-3d;
    border-radius: 1000px;
    padding-top: 10px;
    padding-bottom: 8px;
    padding-left: 28px;
    padding-right: 28px;
    font-weight: 600;
    transition: transform .2s;
    border: none;
}

div.stButton > button:hover {
    transform: scale(1.04);
}

/* Caixa de sucesso */
.stAlert {
    border-radius: 10px;
}

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ------------------------------------------------------------
# LOGO DO ISAAC (AGORA NO CANTO ESQUERDO)
# ------------------------------------------------------------
st.markdown(
    """
    <div style="display:flex; align-items:center;">
        <img src="logoisaac.svg" width="100">
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# TÍTULO (AGORA H2)
# ------------------------------------------------------------
st.markdown("<h2>🎉 Sorteio Matrícula Premiada</h2>", unsafe_allow_html=True)

# ------------------------------------------------------------
# UPLOAD DO CSV
# ------------------------------------------------------------

file = st.file_uploader("Escolha o arquivo CSV", type=["csv"])

if file is not None:
    df = pd.read_csv(file)

    st.success("CSV carregado com sucesso!")

    if st.button("Sortear!"):
        # Criar tickets
        tickets = []
        for _, row in df.iterrows():
            tickets.extend([{
                "cnpj": row["cnpj"],
                "branch_name": row["branch_name"]
            }] * int(row["numeros_da_sorte"]))

        random.seed()
        vencedor = random.choice(tickets)  # sempre 1 vencedor

        st.markdown("### 🏆 Resultado do Sorteio")

        # ------------------------------------------------------------
        # ANIMAÇÃO DE ROLETA
        # ------------------------------------------------------------
        placeholder = st.empty()
        nomes_temp = [row["branch_name"] for _, row in df.iterrows()]

        for i in range(35):
            nome_rodando = random.choice(nomes_temp)
            placeholder.markdown(
                f"<h3 style='color:white; text-align:center;'>{nome_rodando}</h3>",
                unsafe_allow_html=True
            )
            time.sleep(0.05 + (i * 0.015))

        # ------------------------------------------------------------
        # EXIBIR VENCEDOR COM MOLDURA ESTILO 3
        # ------------------------------------------------------------
        moldura_html = f"""
        <div style="
            border: 0;
            border-radius: 25px;
            padding: 3px;
            background: linear-gradient(82deg,#ff8070,#3d4ed7);
            width: 70%;
            margin: auto;
            margin-top: 20px;
        ">
            <div style="
                background:#010038;
                border-radius: 22px;
                padding: 25px;
                color:white;
                text-align:center;
            ">
                <h3 style='margin-bottom:10px;'>E o vencedor é...</h3>
                <h3>{vencedor['branch_name']}</h3>
                <p style='font-size:20px; margin-top:10px;'>CNPJ: <b>{vencedor['cnpj']}</b></p>
            </div>
        </div>
        """

        placeholder.markdown(moldura_html, unsafe_allow_html=True)

        st.balloons()
