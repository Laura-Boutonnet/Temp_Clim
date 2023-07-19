import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Température malgré la clim")
st.session_state["df"] = pd.DataFrame()

uploaded_file = st.file_uploader("Choix de la base de données")
if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, sep = ",", decimal = ".")
       
        df["time"] = df["time"].str.split(".", n=1).str[0]
        df['time'] = df['time'].str.replace("T", " ")
        df.index = df.time
        df = df.drop(columns="time")
        df.index = pd.to_datetime(df.index, format="%Y-%m-%d %H:%M:%S")
        df = df.drop_duplicates()
        if df1 not in locals():
                df1 = df
        else : 
                df1 = pd.concat([df1, df])
        fig = px.line(df1, x=df1.index, y="value")
        fig.update_layout(title="Graphique de la température dans l'open space")
        st.balloons()
        st.write(fig)
        st.write("Voici les données")
        st.write(df1)
        
        st.write("Vous pouvez télécharger les données.")
        st.write("Indiquez un nom et un cliquez sur le bouton 'Télécharger' si dessous.")
        
        st.session_state['nom'] = st.text_input('Nom de votre téléchargement', 'data')
        st.write(f'Création d\'un fichier : {st.session_state["nom"]}')
        
        @st.cache_data()
        def convert_df(df):
            return df.to_csv().encode('utf-8')
        
        csv = convert_df(df1)
        
        st.download_button(
            label="Télécharger",
            data=csv,
            file_name=f'{st.session_state["nom"]}.csv',
            mime='text/csv',
        )
