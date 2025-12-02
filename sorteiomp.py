import streamlit as st
import pandas as pd
import random
import time

def formatar_cnpj(cnpj):
    """Formatar CNPJ para 00.000.000/0000-00"""
    cnpj = str(cnpj).zfill(14)  # garante 14 dígitos
    return f"{cnpj[0:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}"

# ------------------------------------------------------------
# CONFIG DA PÁGINA
# ------------------------------------------------------------
st.set_page_config(
    page_title="Sorteio | Matrícula Premiada",
    layout="centered" 
)

# ------------------------------------------------------------
# CSS GLOBAL
# ------------------------------------------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Verdana:wght@400;700&display=swap');

html, body, .stApp {
    background-color: #010038 !important;
    font-family: Halcyon, Verdana, sans-serif !important;
}

/* Remove fundo do cabeçalho */
header, .st-emotion-cache-18ni7ap, .st-emotion-cache-1dp5vir {
    background: transparent !important;
    box-shadow: none !important;
}

/* TÍTULO + LOGO */
.title-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
    margin-top: 5px;
}

.title-text {
    color: white;
    font-size: 30px;
    font-weight: 700;
}

/* Botões */
div.stButton > button {
    background-image: linear-gradient(82deg, #ff8070, #3d4ed7);
    color: #ffffff;
    border-radius: 1000px;
    padding: 12px 40px;
    font-weight: 600;
    font-size: 18px;
    border: none;
    width: 260px;
    transition: 0.15s;
    display: block;
    margin: 0 auto;
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

/* Centralizar sucesso */
.success-center {
    text-align: center;
}

</style>
""", unsafe_allow_html=True)



# ------------------------------------------------------------
# TOPO — LOGO + TÍTULO
# ------------------------------------------------------------
st.markdown("""
<div class="title-container">
    <img src="logoisaac.svg" width="90">
    <span class="title-text">Realizar sorteio</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)



# ------------------------------------------------------------
# UPLOAD CENTRALIZADO
# ------------------------------------------------------------
st.markdown(
    '<div class="custom-upload"><label>📁 Envie o arquivo CSV com as escolas participantes</label></div>',
    unsafe_allow_html=True
)

file = st.file_uploader("", type=["csv"])



# ------------------------------------------------------------
# SORTEIO
# ------------------------------------------------------------
if file is not None:
    df = pd.read_csv(file)

    st.markdown(
        "<p class='success-center'><span style='color:#4ade80;font-size:18px;'>CSV carregado com sucesso! ✔</span></p>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Botão realmente centralizado
    centered_btn = st.container()
    with centered_btn:
        btn_col = st.columns([1, 1, 1])
        with btn_col[1]:
            sortear = st.button("Sortear agora!", use_container_width=True)

    if sortear:
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
                font-family: Halcyon, Verdana, sans-serif;
            ">
                <h3 style='margin-bottom:10px;'>🏆 Escola Vencedora</h3>
                <h3>{vencedor['branch_name']}</h3>
                <p style='font-size:18px; margin-top:10px;'>CNPJ: <b>{formatar_cnpj(vencedor['cnpj'])}</b></p>
            </div>
        </div>
        """

        placeholder.markdown(moldura, unsafe_allow_html=True)
        st.balloons()



