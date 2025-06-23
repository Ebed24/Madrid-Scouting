import streamlit as st

# Configuración inicial
st.set_page_config(
    page_title='Ebed - Scouting App Madrid',
    layout="wide",
    page_icon="⚽"
)

# Título y bienvenida
st.title('Scouting Madrid ⚽')

st.write("""
Bienvenido a **Scouting Madrid**, una aplicación de scouting diseñada específicamente para las categorías **División de Honor** y **Tercera Federación** de la Comunidad de Madrid.

### 🌟 ¿Cuál es el objetivo de esta aplicación?
El propósito de esta herramienta es **apoyar a los equipos en la gestión de plantillas, la realización de scouting y la evaluación del rendimiento de los jugadores**, todo ello mediante el uso de datos relevantes, accesibles y adaptados a las necesidades de estas categorías.

### 💡 ¿Qué ofrece Scouting Madrid?
- Gestión visual de plantillas.
- Filtros para analizar jugadores por edad, posición, impacto y rendimiento.
- Información centralizada de los jugadores para facilitar la toma de decisiones.
- Soluciones **innovadoras y de bajo coste** para clubes con recursos limitados.

### 🚀 Futuras funcionalidades
Actualmente, esta app está en proceso de desarrollo y se encuentra en constante evolución. En las próximas versiones se incorporarán:
- **Gráficos de rendimiento individual y colectivo.**
- **Comparación de jugadores.**
- **Análisis visual y métricas avanzadas.**
- Mejoras en el diseño para que sea más **intuitivo, dinámico y fácil de utilizar.**

---

Utiliza el **menú lateral** para explorar las distintas secciones:
- 📋 Seleccionar equipo
- 🧑‍💼 Plantilla del equipo

¡Gracias por confiar en Scouting Madrid y ser parte de esta evolución hacia un scouting más accesible y eficiente! ⚽📊
""")
