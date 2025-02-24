import streamlit as st
import google.generativeai as genai
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

# Cargar API Key desde variables de entorno
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Configurar modelo Gemini 2.0 Flash
model = genai.GenerativeModel("gemini-2.0-flash")

# Título
st.title("NewsPulse AI - Potenciado por Gemini 2.0 Flash")

# Entrada de usuario
topic = st.text_input("Tema (ej. huracán en Florida)", "")
upload_file = st.file_uploader("Sube un CSV (opcional)", type="csv")
audience = st.selectbox("Audiencia", ["Jóvenes", "General", "Expertos"])

# Procesar
if topic or upload_file:
    if topic:
        prompt_trends = f"Analiza tendencias actuales sobre '{topic}' y devuelve las 5 palabras clave más relevantes."
        trends_response = model.generate_content(prompt_trends)
        trends = trends_response.text.split("\n")[:5]
        text_data = trends_response.text
    elif upload_file:
        df = pd.read_csv(upload_file)
        text_data = " ".join(df["texto"].astype(str))
        prompt_trends = f"Extrae las 5 palabras clave más frecuentes de este texto: {text_data[:5000]}"
        trends_response = model.generate_content(prompt_trends)
        trends = trends_response.text.split("\n")[:5]

    st.write("**Tendencias principales**:", trends)

    prompt_headlines = f"Genera 3 titulares sobre '{topic}' para {audience}, optimizados para engagement."
    headlines_response = model.generate_content(prompt_headlines)
    headlines = headlines_response.text.split("\n")[:3]
    st.write("**Titulares sugeridos**:")
    for i, headline in enumerate(headlines):
        st.write(f"{i+1}. {headline}")

    wordcloud = WordCloud(width=800, height=400).generate(text_data)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)

    report = f"Tema: {topic}\nTendencias: {', '.join(trends)}\nTitulares:\n" + "\n".join(headlines)
    st.download_button("Descargar informe", report, file_name="news_pulse_report.txt")
