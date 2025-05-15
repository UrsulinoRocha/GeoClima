import streamlit as st
import requests
import os


def detectar_localizacao():
    try:
        res = requests.get("http://ipwho.is/").json()
        if res["success"]:
            return res["city"], res["country"]
        else:
            return "São Paulo", "Brazil"
    except:
        return "São Paulo", "Brazil"


CIDADES_SUGERIDAS = {
    "Detectar automaticamente": None,
    "São Paulo, Brazil": ("São Paulo", "Brazil"),
    "Rio de Janeiro, Brazil": ("Rio de Janeiro", "Brazil"),
    "Lisboa, Portugal": ("Lisboa", "Portugal"),
    "New York, United States": ("New York", "United States"),
    "London, United Kingdom": ("London", "United Kingdom")
}


@st.cache_data(ttl=600)
def buscar_clima(cidade, pais):
    API_KEY = "" #Token
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": f"{cidade},{pais}",
        "appid": API_KEY,
        "units": "metric",
        "lang": "pt_br"
    }
    try:
        response = requests.get(url, params=params).json()
        if response.get("cod") != 200:
            return None
        return {
            "temperatura": response["main"]["temp"],
            "sensacao": response["main"]["feels_like"],
            "descricao": response["weather"][0]["description"].capitalize(),
            "icone": response["weather"][0]["icon"],
            "umidade": response["main"]["humidity"],
            "vento": response["wind"]["speed"]
        }
    except:
        return None


def aplicar_css_externo(caminho_css="styles.css"):
    if os.path.exists(caminho_css):
        with open(caminho_css) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="Clima Atual", layout="centered")
    aplicar_css_externo()

    st.markdown("<h1 style='text-align: center;'>🌦️ Clima Atual</h1>", unsafe_allow_html=True)
    st.divider()

    escolha = st.selectbox("Escolha uma cidade:", list(CIDADES_SUGERIDAS.keys()))

    if escolha == "Detectar automaticamente":
        cidade, pais = detectar_localizacao()
    else:
        cidade, pais = CIDADES_SUGERIDAS[escolha]

    dados = buscar_clima(cidade, pais)

    if dados:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"### 📍 Localização: **{cidade}, {pais}**")
            st.markdown(f"**🌡️ Temperatura:** {dados['temperatura']} °C")
            st.markdown(f"**🥵 Sensação térmica:** {dados['sensacao']} °C")
            st.markdown(f"**💧 Umidade:** {dados['umidade']}%")
            st.markdown(f"**🌬️ Vento:** {dados['vento']} m/s")
            st.markdown(f"**📝 Condição:** {dados['descricao']}")

        with col2:
            st.image(f"http://openweathermap.org/img/wn/{dados['icone']}@4x.png")

    else:
        st.error("❌ Não foi possível obter os dados do clima. Verifique a chave de API ou tente novamente.")

    st.divider()
    st.markdown("<p style='text-align: center; color: gray;'>Desenvolvido com ❤️ em Python + Streamlit</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
