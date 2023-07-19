import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Température malgré la clim")

# Création d'une liste des df
if "dfs" not in st.session_state:
    st.session_state["dfs"] = []

# On chois le df en local avec un drag and drop
uploaded_file = st.file_uploader("Choix de la base de données")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep=",", decimal=".")

    # On nettoye les données pour pouvoir les exploiter (format/doublons/on drop des colonnes)
    df["time"] = df["time"].str.split(".", n=1).str[0]
    df['time'] = df['time'].str.replace("T", " ")
    df.index = df.time
    df = df.drop(columns="time")
    df.index = pd.to_datetime(df.index, format="%Y-%m-%d %H:%M:%S")
    df = df.drop_duplicates()
    
    # On ajoute le new df dans la liste des df
    st.session_state["dfs"].append(df)

    # On concat les df de dfs ensemble (on trie par index (date))
    st.session_state["dfs"].sort(key=lambda df: df.index[0])
    df_combined = pd.concat(st.session_state["dfs"])
    df_combined.sort_index(inplace=True)

    # Création et affichage du graph + des ballons car c'est mignon
    fig = px.line(df_combined, x=df_combined.index, y="value")
    fig.update_layout(title="Graphique de la température dans l'open space")
    st.balloons()
    st.write(fig)

    # Affichage des données
    st.write("Voici les données combinées de tous les fichiers :")
    st.write(df_combined)

    # Possibilité de télécharger les données (dans les téléchargement) en sortie
    st.write("Vous pouvez télécharger les données.")
    st.write("Indiquez un nom et un cliquez sur le bouton 'Télécharger' ci-dessous.")

    st.session_state['nom'] = st.text_input('Nom de votre téléchargement', 'data')
    st.write(f'Création d\'un fichier : {st.session_state["nom"]}')

    @st.cache_data()
    def convert_df(df):
        return df.to_csv().encode('utf-8')

    csv = convert_df(df_combined)

    st.download_button(
        label="Télécharger",
        data=csv,
        file_name=f'{st.session_state["nom"]}.csv',
        mime='text/csv',
    )

