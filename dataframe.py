import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Température malgré la clim')
st.session_state['df'] = pd.DataFrame()

uploaded_file = st.file_uploader("Choix de la base de données")
if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, sep = ',', decimal = '.')
       
        df["time"] = df["time"].str.split(".", n=1).str[0]
        df['time'] = df['time'].str.replace('T', ' ')
        df.index = df.time
        df = df.drop(columns='time')
        formatted_index = pd.to_datetime(df.index, format='%Y-%m-%d %H:%M:%S')
        df.index = formatted_index
        df = df.drop_duplicates()
        fig = px.line(df, x=df.index, y=df.value)
        fig.update_layout(title="Graphique de la température dans l'open space")
        st.balloons()
        st.write(fig)
        st.write('Voici les données')
        st.write(df)
       
