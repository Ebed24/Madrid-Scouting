import streamlit as st
import pandas as pd
import altair as alt

st.title('Visualización y Filtros de Jugadores - Scouting')

@st.cache_data
def load_data():
    return pd.read_csv('D:\\Mexico FC\\Futbol_Madrid\\Madrid_futbol_2025.csv')

df = load_data()

# Sidebar para selección de jugadores (para la página comparativa)
st.sidebar.subheader('Selección de Jugadores para Comparativa')
jugadores_disponibles = sorted(df['Nombre'].unique().tolist())
jugadores_seleccionados = st.sidebar.multiselect('Selecciona jugadores para comparar:', jugadores_disponibles)

# Guardar selección en la sesión
if 'jugadores_comparar' not in st.session_state:
    st.session_state['jugadores_comparar'] = []

if jugadores_seleccionados:
    st.session_state['jugadores_comparar'] = jugadores_seleccionados

# Filtros iniciales
equipos = ['Todos'] + sorted(df['Equipo'].unique().tolist())
equipo = st.selectbox('Selecciona un equipo:', equipos)

if equipo != 'Todos':
    df_filtrado = df[df['Equipo'] == equipo]
else:
    df_filtrado = df.copy()

# Filtro de categoría
categorias = ['Todas'] + sorted(df_filtrado['categoria'].unique().tolist())
categoria = st.sidebar.selectbox('Selecciona una categoría:', categorias)

if categoria != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['categoria'] == categoria]

# Filtro de posición
posiciones = ['Todas'] + sorted(df_filtrado['Posicion'].unique().tolist())
posicion = st.sidebar.selectbox('Selecciona una posición:', posiciones)

if posicion != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['Posicion'] == posicion]

# Filtros adicionales
min_edad, max_edad = int(df_filtrado['Edad'].min()), int(df_filtrado['Edad'].max())
edad = st.sidebar.slider('Rango de Edad', min_value=min_edad, max_value=max_edad, value=(min_edad, max_edad))

min_altura, max_altura = int(df_filtrado['Altura'].min()), int(df_filtrado['Altura'].max())
altura = st.sidebar.slider('Rango de Altura (cm)', min_value=min_altura, max_value=max_altura, value=(min_altura, max_altura))

min_elo, max_elo = int(df_filtrado['ELO'].min()), int(df_filtrado['ELO'].max())
elo = st.sidebar.slider('Rango de ELO', min_value=min_elo, max_value=max_elo, value=(min_elo, max_elo))

min_partidos, max_partidos = int(df_filtrado['Partidos_jugados'].min()), int(df_filtrado['Partidos_jugados'].max())
partidos = st.sidebar.slider('Rango de Partidos Jugados', min_value=min_partidos, max_value=max_partidos, value=(min_partidos, max_partidos))

min_goles, max_goles = int(df_filtrado['Goles'].min()), int(df_filtrado['Goles'].max())
goles = st.sidebar.slider('Rango de Goles', min_value=min_goles, max_value=max_goles, value=(min_goles, max_goles))

# Aplicar filtros
df_filtrado = df_filtrado[
    (df_filtrado['Edad'] >= edad[0]) & (df_filtrado['Edad'] <= edad[1]) &
    (df_filtrado['Altura'] >= altura[0]) & (df_filtrado['Altura'] <= altura[1]) &
    (df_filtrado['ELO'] >= elo[0]) & (df_filtrado['ELO'] <= elo[1]) &
    (df_filtrado['Partidos_jugados'] >= partidos[0]) & (df_filtrado['Partidos_jugados'] <= partidos[1]) &
    (df_filtrado['Goles'] >= goles[0]) & (df_filtrado['Goles'] <= goles[1])
]

# Resumen estadístico
total_jugadores = len(df_filtrado)
promedio_goles = df_filtrado['Goles'].mean() if total_jugadores > 0 else 0
promedio_altura = df_filtrado['Altura'].mean() if total_jugadores > 0 else 0
promedio_edad = df_filtrado['Edad'].mean() if total_jugadores > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Jugadores", total_jugadores)
col2.metric("Promedio Goles", f"{promedio_goles:.2f}")
col3.metric("Promedio Altura (cm)", f"{promedio_altura:.1f}")
col4.metric("Promedio Edad", f"{promedio_edad:.1f}")
col5.write("")

df_filtrado['Grupo_Edad'] = df_filtrado['Edad'].apply(lambda x: 'Menor o igual a 23' if x <= 23 else 'Mayor a 23')

if not df_filtrado.empty:
    st.subheader('Gráfico de Impacto Total')
    scatter = alt.Chart(df_filtrado).mark_circle(size=80).encode(
        x='Edad',
        y='Impacto_Total',
        color=alt.Color('Grupo_Edad', scale=alt.Scale(domain=['Menor o igual a 23', 'Mayor a 23'], range=['green', 'orange'])),
        tooltip=['Nombre', 'Equipo', 'Edad', 'Impacto_Total', 'ELO']
    ).interactive()

    st.altair_chart(scatter, use_container_width=True)

    max_partidos = df['Partidos_jugados'].max()
    minimo_partidos = max_partidos / 2

    top5 = df_filtrado[df_filtrado['Partidos_jugados'] > minimo_partidos]

    if not top5.empty:
        st.subheader('Top 5 Jugadores según Impacto Total (Jugadores con más del 50% de partidos jugados)')
        top5_sorted = top5.sort_values(by='Impacto_Total', ascending=False).head(5)
        st.table(top5_sorted[['Nombre', 'Edad', 'Altura', 'Partidos_jugados', 'Equipo']].reset_index(drop=True))
        st.info(f'Estos jugadores han disputado más del 50% de los {int(max_partidos)} partidos posibles.')

        metrica_goles = st.selectbox(
            'Selecciona la métrica para el gráfico de goleadores:',
            options=['Goles', 'Goles_por_partido']
        )

        top_goleadores = df_filtrado.sort_values(by=metrica_goles, ascending=False).head(10)

        goles_chart = alt.Chart(top_goleadores).mark_bar().encode(
            x=alt.X(f'{metrica_goles}:Q', title=metrica_goles.replace('_', ' ')),
            y=alt.Y('Nombre:N', sort='-x', title='Jugador'),
            color=alt.Color('Grupo_Edad', scale=alt.Scale(domain=['Menor o igual a 23', 'Mayor a 23'], range=['green', 'orange'])),
            tooltip=['Nombre', 'Equipo', 'Edad', metrica_goles]
        ).properties(height=400).interactive()

        st.altair_chart(goles_chart, use_container_width=True)

        st.subheader('Top 5 Jugadores según Aporte_Goles')
        top_aporte_goles = df_filtrado.sort_values(by='Aporte_Goles', ascending=False).head(5)
        st.table(top_aporte_goles[['Nombre', 'Edad', 'Altura', 'Partidos_jugados', 'Equipo', 'Aporte_Goles']].reset_index(drop=True))

        st.subheader('Rendimiento Contextual (RC)')
        st.markdown("""
        **¿Qué es el Rendimiento Contextual (RC)?**

        El RC es una métrica que evalúa el rendimiento de un jugador considerando las condiciones específicas en las que participa:
        - Nivel competitivo de su equipo.
        - Nivel de los rivales.
        - Situaciones particulares de los partidos.

        Permite detectar jugadores valiosos más allá de sus números brutos.
        """)

        scatter_rc = alt.Chart(df_filtrado).mark_circle(size=80).encode(
            x='Edad',
            y='RC',
            color=alt.Color('Grupo_Edad', scale=alt.Scale(domain=['Menor o igual a 23', 'Mayor a 23'], range=['green', 'orange'])),
            tooltip=['Nombre', 'Equipo', 'Edad', 'RC', 'ELO']
        ).interactive()

        st.altair_chart(scatter_rc, use_container_width=True)

        st.subheader('Top 5 Jugadores según Rendimiento Contextual (RC)')
        top_rc = df_filtrado[df_filtrado['Partidos_jugados'] > minimo_partidos]
        top_rc_sorted = top_rc.sort_values(by='RC', ascending=False).head(5)
        st.table(top_rc_sorted[['Nombre', 'Edad', 'Altura', 'Partidos_jugados', 'Equipo', 'RC']].reset_index(drop=True))
        st.info(f'Estos jugadores han disputado más del 50% de los {int(max_partidos)} partidos posibles y destacan en RC.')

        st.subheader('Índice de Desempeño Defensivo (IDR)')
        st.markdown("""
        **¿Qué es el IDR?**

        El Índice de Desempeño Defensivo (IDR) mide la eficacia de un jugador en tareas defensivas clave, considerando:
        - Intercepciones.
        - Despejes.
        - Duelos defensivos ganados.
        - Contexto de dificultad defensiva.

        Es un indicador integral para evaluar a los defensas más sólidos y consistentes.
        """)

        defensas = df_filtrado[df_filtrado['Posicion'].isin(['Defensas'])]

        if not defensas.empty:
            scatter_idr = alt.Chart(defensas).mark_circle(size=80).encode(
                x='Edad',
                y='IDR',
                color=alt.Color('Grupo_Edad', scale=alt.Scale(domain=['Menor o igual a 23', 'Mayor a 23'], range=['green', 'orange'])),
                tooltip=['Nombre', 'Equipo', 'Edad', 'IDR', 'ELO']
            ).interactive()

            st.altair_chart(scatter_idr, use_container_width=True)

            st.subheader('Top 5 Defensas según IDR (Jugadores con más del 50% de partidos jugados)')
            top_idr = defensas[defensas['Partidos_jugados'] > minimo_partidos]
            top_idr_sorted = top_idr.sort_values(by='IDR', ascending=False).head(5)

            st.table(top_idr_sorted[['Nombre', 'Edad', 'Altura', 'Partidos_jugados', 'Equipo', 'IDR']].reset_index(drop=True))
            st.info(f'Estos defensas han disputado más del 50% de los {int(max_partidos)} partidos posibles y destacan en IDR.')

        else:
            st.warning('No hay defensas que cumplan con los filtros seleccionados.')

    else:
        st.warning('No hay jugadores que cumplan con el filtro de participación mínima (más del 50% de partidos jugados).')

else:
    st.warning('No hay jugadores que cumplan con los filtros seleccionados.')
