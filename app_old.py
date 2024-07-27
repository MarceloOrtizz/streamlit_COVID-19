import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Cargar el archivo CSV
@st.cache_data
def load_data():
    # Reemplaza 'tu_archivo.csv' con el nombre de tu archivo CSV
    return pd.read_csv('data/processed/prediccion_ML_deceased.csv')

# Cargar los datos
data = load_data()

# Convertir la columna de fecha a datetime
data['date'] = pd.to_datetime(data['date'])

# Interfaz de usuario
st.title('Predicción de los Próximos 14 Días')

# Selector de país
countries = data['location_key'].unique()
selected_country = st.selectbox('Selecciona un país:', countries)

# Selector de fecha, con fecha predeterminada 2021-01-01
selected_date = st.date_input('Selecciona una fecha:', value=datetime(2021, 1, 1), min_value=datetime(2021, 1, 1), max_value=datetime.now().date())

# Filtrar los datos para el país y la fecha seleccionados
filtered_data = data[(data['location_key'] == selected_country) & (data['date'] == pd.to_datetime(selected_date))]

if not filtered_data.empty:
    # Obtener los datos de los próximos 14 días
    future_dates = [selected_date + timedelta(days=i) for i in range(15)]
    future_data = data[(data['location_key'] == selected_country) & (data['date'].isin(future_dates))]
    
    # Formatear la columna de fechas para mostrar solo la fecha sin la hora
    future_data['date'] = future_data['date'].dt.strftime('%Y-%m-%d')
    
    st.write('Predicciones para los próximos 14 días:')
    st.write(future_data[['date', 'location_key', 'Prediccion']].to_html(index=False), unsafe_allow_html=True)
else:
    st.write('No hay datos disponibles para la fecha y el país seleccionados.')

