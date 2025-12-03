import streamlit as st
import pandas as pd
import random
import time
import streamlit.components.v1 as components

def formatar_cnpj(cnpj):
    """Formatar CNPJ para 00.000.000/0000-00"""
    cnpj = str(cnpj).zfill(14)
    return f"{cnpj[0:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}"

# ------------------------------------------------------------
# CONFIG DA PÁGINA
# ------------------------------------------------------------
st.set_page_config(
    page_title="Sorteio | Matrícula Premiada",
    layout="centered"
)

# ------------------------------------------------------------
# INSERIR LOGO NA NAVBAR (FUNCIONA NO STREAMLIT CLOUD)
# ------------------------------------------------------------
components.html("""
    <script>
        const checkHeader = setInterval(() => {
            const header = window.parent.document.querySelector('header[data-testid="stHeader"]');
            if (header && !header.querySelector('.mp-logo')) {
                const img = document.createElement('img');
                img.src = 'https://raw.githubusercontent.com/mavimelato/sorteio_mp/main/logomp.png';
                img.className = 'mp-logo';
                img.style.height = '45px';
                img.style.marginLeft = '100px';
                img.style.objectFit = 'contain';
                header.prepend(img);
                clearInterval(checkHeader);
            }
        }, 200);
    </script>
""", height=0)

# ------------------------------------------------------------
# CSS GLOBAL + NAVBAR ESCURA
# ------------------------------------------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Verdana:wght@400;700&display=swap');

html, body, .stApp {
    background-color: #010038 !important;
    font-family: Halcyon, Verdana, sans-serif !important;
}

/* NAVBAR ESCURA */
header[data-testid="stHeader"] {
    background-color: #000025 !important;
    height: 70px;
    display: flex;
    align-items: center;
    padding-left: 12px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    box-shadow: none !important;
}

.st-emotion-cache-18ni7ap, .st-emotion-cache-1dp5vir {
    background: transparent !important;
}

/* BOTÕES */
div.stButton > button {
    background-image: linear-gradient(82deg, #ff8070, #3d4ed7);
    color: #ffffff;
    border-radius: 1000px;
    padding: 12px 40px;
    font-weight: 600;
    font-size: 18px;
    border: none;
    width: 230px;
    transition: 0.15s;
    margin: 0 auto;
}

div.stButton > button:hover {
    transform: scale(1.04);
}

/* UPLOAD */
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

.success-center {
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# TÍTULO
# ------------------------------------------------------------
st.markdown("""
<h3 style='text-align:center;color:white;'>
    Realizar sorteio
</h3>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# UPLOAD
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

    col = st.columns([1, 1, 1])
    with col[1]:
        sortear = st.button("Sortear agora!", use_container_width=True)

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

        for i in range(35):
            nome_temp = random.choice(nomes_temp)
            placeholder.markdown(
                f"<h3 style='color:white; text-align:center;'>{nome_temp}</h3>",
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
                <h3 style='margin-bottom:10px;'>🏆 Escola vencedora</h3>
                <h3>{vencedor['branch_name']}</h3>
                <p style='font-size:18px;'>CNPJ: <b>{formatar_cnpj(vencedor['cnpj'])}</b></p>
            </div>
        </div>
        """

        placeholder.markdown(moldura, unsafe_allow_html=True)
        st.balloons()


