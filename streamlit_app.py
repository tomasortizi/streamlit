import streamlit as st
import pandas as pd
import requests
from io import StringIO

# Función para calcular el dividendo
def calcular_dividendo(precio_total, pie, tasa_interes, años):
    monto_credito = precio_total - pie
    tasa_mensual = tasa_interes / 12 / 100
    n = años * 12
    dividendo = (monto_credito * tasa_mensual) / (1 - (1 + tasa_mensual)**-n)
    return dividendo

# Función ficticia para obtener el arriendo promedio
def obtener_arriendo_promedio(metros_cuadrados, dormitorios, baños):
    # Aquí se debería realizar una consulta a un API o web scraping para obtener los arriendos promedio
    return 500000  # Valor ficticio

st.title("Análisis de Inversión en Departamentos en Santiago")

# Ruta al archivo preexistente
archivo_csv = "/Users/tomasortiz/Documents/Magister Negocios Digitales/Inteligencia Artificial/departamentos_en_venta.csv"

# Cargar archivo preexistente
try:
    df = pd.read_csv(archivo_csv)
    st.write("Datos cargados exitosamente:")
    st.write(df.head())

    # Preguntas al usuario
    pie_uf = st.number_input("¿Cuánto pie puedes pagar en UF?", min_value=0.0, step=0.1)
    dividendo_esperado_clp = st.number_input("¿Cuál es el dividendo esperado para pagar en CLP?", min_value=0)

    # Tasa hipotecaria de www.siii.cl
    tasa_hipotecaria = 4.8  # Porcentaje ficticio, se debería obtener de manera dinámica
    años_credito = 25

    # Procesar cada departamento y calcular la rentabilidad
    resultados = []
    for index, row in df.iterrows():
        precio_total = row['Precio_total']
        metros_cuadrados = row['Metros_cuadrados']
        dormitorios = row['Dormitorios']
        baños = row['Baños']
        link = row['Link']

        # Convertir UF a CLP (suponiendo 1 UF = 30000 CLP)
        precio_total_clp = precio_total * 37590
        pie_clp = pie_uf * 37590

        dividendo = calcular_dividendo(precio_total_clp, pie_clp, tasa_hipotecaria, años_credito)
        arriendo_promedio = obtener_arriendo_promedio(metros_cuadrados, dormitorios, baños)

        rentabilidad = (arriendo_promedio - dividendo) / dividendo

        resultado = {
            "Precio total (UF)": precio_total,
            "Pie a pagar (UF)": pie_uf,
            "Metros cuadrados": metros_cuadrados,
            "Dormitorios": dormitorios,
            "Baños": baños,
            "Dividendo mensual (CLP)": dividendo,
            "Dividendo mensual (UF)": dividendo / 30000,
            "Arriendo promedio (CLP)": arriendo_promedio,
            "Rentabilidad esperada": rentabilidad,
            "Link": link
        }

        resultados.append(resultado)

    resultados_df = pd.DataFrame(resultados)
    st.subheader("Resultados")
    st.write(resultados_df)

    # Descargar resultados
    st.download_button(
        label="Descargar resultados",
        data=StringIO(resultados_df.to_csv(index=False)),
        file_name="resultados_inversion.csv",
        mime="text/csv"
    )

except FileNotFoundError:
    st.error("El archivo no se encontró. Por favor verifica la ruta al archivo.")
