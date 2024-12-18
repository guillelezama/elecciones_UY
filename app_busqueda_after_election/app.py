import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cargar los conjuntos de datos
df_final = pd.read_csv("df_final.csv")  # Reemplazar con el archivo real
df_final_depto = pd.read_csv("df_final_depto.csv")  # Reemplazar con el archivo real

# Mapeo de nombres de partidos a columnas
party_mapping = {
    "Frente Amplio": ["fa_19", "multi_19", "fa", "orsi"],
    "Coalición Republicana": ["martinez", "lacalle", "core", "delgado"],
}

# Título de la app
st.title("Evolución de los Partidos Políticos")

# Selección del partido
party = st.selectbox("Selecciona un partido:", list(party_mapping.keys()))

# Selección del tipo de datos
dataset_choice = st.radio("Selecciona el tipo de datos:", ["Series", "Departamentos"])

if dataset_choice == "Series":
    selected_data = df_final
    choices = selected_data["series"].unique()
    label = "Selecciona las series:"
else:
    selected_data = df_final_depto
    choices = selected_data["depto"].unique()
    label = "Selecciona los departamentos:"

# Selección múltiple
selections = st.multiselect(label, choices)

# Filtrar los datos
filtered_data = selected_data[selected_data.iloc[:, 0].isin(selections)]

# Columnas para graficar
columns_to_plot = party_mapping[party]

if not filtered_data.empty:
    st.subheader("Evolución a través de Octubre 2019, Balotaje 2019, Octubre 2024 y Balotaje 2024")

    # Preparar los datos para graficar
    time_labels = ["Octubre 2019", "Balotaje 2019", "Octubre 2024", "Balotaje 2024"]
    for selection in selections:
        subset = filtered_data[filtered_data.iloc[:, 0] == selection]
        plt.figure()
        for col in columns_to_plot:
            plt.plot(time_labels, subset[col].values[0:4], label=col)
        plt.title(f"Evolución para {selection}")
        plt.xlabel("Tiempo")
        plt.ylabel("Votos")
        plt.legend()
        st.pyplot(plt.gcf())
else:
    st.warning("No hay datos disponibles para las opciones seleccionadas.")
