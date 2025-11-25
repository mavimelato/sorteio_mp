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

body, .stApp {
    background-color: #010038 !important;
}

/* Títulos */
h1, h2, h3 {
    color: #ffffff !important;
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
# LOGOS (opcional)
# ------------------------------------------------------------
col1, col2, col3 = st.columns([1,2,1])
with col2:
     st.image("logoisaac.svg", width=220)

# ------------------------------------------------------------
# TÍTULO
# ------------------------------------------------------------
st.title("🎉 Sorteio Matrícula Premiada")
st.markdown("<h3 style='color:white;'>Boa sorte a todos os participantes!</h3>", unsafe_allow_html=True)

# ------------------------------------------------------------
# UPLOAD DO CSV
# ------------------------------------------------------------
st.markdown("<p style='color:white;'>Faça upload do CSV contendo: cnpj, branch_name, numeros_da_sorte</p>", unsafe_allow_html=True)

file = st.file_uploader("Escolha o arquivo CSV", type=["csv"])

if file is not None:
    df = pd.read_csv(file)

    # Apenas mensagem simples conforme Jurídico
    st.success("CSV carregado com sucesso!")

    total_vencedores = st.number_input(
        "Quantos vencedores sortear?",
        min_value=1,
        max_value=len(df),
        value=1,
        step=1
    )

    if st.button("Sortear!"):
        # Criar tickets
        tickets = []
        for _, row in df.iterrows():
            tickets.extend([{
                "cnpj": row["cnpj"],
                "branch_name": row["branch_name"]
            }] * int(row["numeros_da_sorte"]))

        random.seed()
        vencedores = random.sample(tickets, k=total_vencedores)

        st.markdown("### 🏆 Resultado do Sorteio")

        # ------------------------------------------------------------
        # ANIMAÇÃO DE ROLETA
        # ------------------------------------------------------------
        placeholder = st.empty()
        nomes_temp = [row["branch_name"] for _, row in df.iterrows()]

        for i in range(35):
            nome_rodando = random.choice(nomes_temp)
            placeholder.markdown(
                f"<h2 style='color:white; text-align:center;'>{nome_rodando}</h2>",
                unsafe_allow_html=True
            )
            time.sleep(0.05 + (i * 0.015))  # desacelera progressivamente

        # ------------------------------------------------------------
        # EXIBIR VENCEDOR COM MOLDURA ESTILO 3
        # ------------------------------------------------------------
        vencedor = vencedores[0]  # sempre mostrar o primeiro (ou loop para vários)

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
                <h2 style='margin-bottom:10px;'>🎉 Vencedor</h2>
                <h3>{vencedor['branch_name']}</h3>
                <p style='font-size:20px; margin-top:10px;'>CNPJ: <b>{vencedor['cnpj']}</b></p>
            </div>
        </div>
        """

        placeholder.markdown(moldura_html, unsafe_allow_html=True)

        st.balloons()
