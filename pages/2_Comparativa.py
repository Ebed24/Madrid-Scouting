import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Comparativa de Jugadores')

@st.cache_data
def load_data():
    return pd.read_csv('D:\Mexico FC\Futbol_Madrid\Madrid_futbol_2025.csv')

df = load_data()

jugadores_seleccionados = st.session_state.get('jugadores_comparar', [])

if not jugadores_seleccionados or len(jugadores_seleccionados) < 2:
    st.warning('Selecciona al menos dos jugadores para comparar en la página anterior.')
    st.stop()

df_comparativa = df[df['Nombre'].isin(jugadores_seleccionados)]

metricas = [
    'Partidos_jugados', 'ELO', 'Partidos_titular', 'Goles',
    'Tarjetas_amarillas', 'Aporte_Goles', 'Aporte_Puntos',
    'RC', 'IDR', 'Impacto_Total'
]

# Normalizar métricas (%)
for metrica in metricas:
    min_val = df[metrica].min()
    max_val = df[metrica].max()
    if max_val - min_val != 0:
        df_comparativa[metrica + '_%'] = ((df_comparativa[metrica] - min_val) / (max_val - min_val)) * 100
    else:
        df_comparativa[metrica + '_%'] = 0

# Preparar datos para radar
radar_data = df_comparativa[['Nombre'] + [metrica + '_%' for metrica in metricas]]
radar_data = radar_data.melt(id_vars='Nombre', var_name='Métrica', value_name='Valor')
radar_data['Métrica'] = radar_data['Métrica'].str.replace('_%', '').str.replace('_', ' ')

# Radar plot con colores automáticos
fig = px.line_polar(
    radar_data,
    r='Valor',
    theta='Métrica',
    color='Nombre',
    line_close=True,
    color_discrete_sequence=px.colors.qualitative.Set2  # Paleta con colores suaves pero bien diferenciados
)

fig.update_traces(fill='toself')  # Relleno para cada jugador

fig.update_layout(
    title='Radar de Comparación de Jugadores (Datos Estandarizados)',
    polar=dict(
        bgcolor='rgb(50,50,50)',  # Solo el fondo dentro del radar en gris oscuro
        radialaxis=dict(
            visible=True,
            range=[0, 100],
            gridcolor='beige',
            tickfont=dict(color='beige'),
            linecolor='beige'
        ),
        angularaxis=dict(
            gridcolor='beige',
            tickfont=dict(color='beige'),
            linecolor='beige'
        )
    ),
    paper_bgcolor=None,
    plot_bgcolor=None,
    font=dict(color='beige')
)

st.plotly_chart(fig, use_container_width=True)

# ---- Tabla resumen y barra comparativa ----
st.subheader('Resumen Comparativo')

jug1, jug2 = jugadores_seleccionados[:2]

df_resumen = df_comparativa[['Nombre'] + [metrica + '_%' for metrica in metricas]].set_index('Nombre').T
df_resumen.index = df_resumen.index.str.replace('_%', '').str.replace('_', ' ')
df_resumen = df_resumen[[jug1, jug2]]

def comparar_filas(row):
    if row[jug1] > row[jug2]:
        return jug1
    elif row[jug1] < row[jug2]:
        return jug2
    else:
        return 'Empate'

df_resumen['Mejor'] = df_resumen.apply(comparar_filas, axis=1)

def highlight_best_row(x):
    return ['background-color: lightgreen' if v == x['Mejor'] else '' for v in x[:-1]] + ['']

st.dataframe(df_resumen.style.apply(highlight_best_row, axis=1))

victorias = {
    jug1: (df_resumen['Mejor'] == jug1).sum(),
    jug2: (df_resumen['Mejor'] == jug2).sum()
}
empates = (df_resumen['Mejor'] == 'Empate').sum()

st.markdown('---')
st.markdown('### Resultado general de comparación')

total_competidas = victorias[jug1] + victorias[jug2]
if total_competidas == 0:
    st.info('No hay métricas para comparar o todas están empatadas.')
else:
    porc_jug1 = victorias[jug1] / total_competidas * 100
    porc_jug2 = victorias[jug2] / total_competidas * 100

    st.write(f'**{jug1}** ganó en {victorias[jug1]} métricas')
    st.write(f'**{jug2}** ganó en {victorias[jug2]} métricas')
    st.write(f'Empates en {empates} métricas')

    barra_fig = px.bar(
        x=[jug1, jug2],
        y=[porc_jug1, porc_jug2],
        labels={'x': 'Jugador', 'y': '% Métricas Ganadas'},
        text=[f'{porc_jug1:.1f}%', f'{porc_jug2:.1f}%'],
        color=[jug1, jug2],
        color_discrete_map={jug1: 'green', jug2: 'orange'},
        range_y=[0, 100],
    )
    barra_fig.update_traces(textposition='outside')
    barra_fig.update_layout(yaxis_title='% Métricas Ganadas', showlegend=False)
    st.plotly_chart(barra_fig, use_container_width=True)
