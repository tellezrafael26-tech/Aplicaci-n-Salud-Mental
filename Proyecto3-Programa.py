# Comentarios
# UNIVERSIDAD DEL VALLE DE GUATEMALA
# Departamento de Ingenieria Civil
# CC2005- 30
# Autor: Rafael Téllez, Rodrigo Martínez, Allison Figueroa, Andrés Morales, Irvin González
# Fecha: 3/11/2025
# Proyecto: Salud Mental
# Descripción: Salud Mental de los estudiantes y en maestros en la Universidad

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import random

# ======================
# CONFIGURACIÓN GENERAL
# ======================
# 🔧 Configuración general de la página
st.set_page_config(
    page_title="Bienestar Mental UVG",
    layout="wide",
    page_icon="🧠",
    initial_sidebar_state="expanded"
)

page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #0d1117;
    color: #f0f6fc;
}
[data-testid="stSidebar"] {
    background-color: #161b22;
}
h1, h2, h3, h4, h5, h6 {
    color: #58a6ff !important;
}
.stButton>button {
    background-color: #238636;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.6em 1.2em;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #2ea043;
    color: #fff;
}
.stTextInput>div>div>input, .stTextArea textarea, .stSelectbox div, .stSlider {
    background-color: #21262d !important;
    color: #f0f6fc !important;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# 🧠 Encabezado principal
col1, col2 = st.columns([1, 4])
with col1:
    st.image("logo-uvg-1.png", width=170)
with col2:
    st.title("🧠 Bienestar Mental UVG")
    st.markdown("""
    <div style='font-size:18px; color:#d0d7de;'>
    Espacio de <b>análisis emocional, acompañamiento y reflexión</b> para estudiantes y docentes de la Universidad del Valle de Guatemala.  
    </div>
    """, unsafe_allow_html=True)

# 💬 Frase inspiradora
st.markdown("""
<hr style='border: 1px solid #30363d;'>
<div style='text-align:center; font-size:20px; color:#9ecbff; font-style:italic;'>
💭 “Cuidar de tu salud mental también es una forma de éxito.”
</div>
<hr style='border: 1px solid #30363d;'>
""", unsafe_allow_html=True)

# 🎯 Menú o introducción
st.markdown("""
### 🌿 ¿Qué puedes hacer aquí?
- 🧩 **Explorar tus emociones** y registrar cómo te sientes.  
- 📊 **Analizar tendencias** de bienestar mental en la comunidad UVG.  
- 💬 **Compartir experiencias** y recibir sugerencias positivas.  
- 🎧 **Escuchar nuestro podcast** sobre temas de salud mental universitaria.  
- 🧍‍♀️🧍‍♂️ **Conocer al equipo creador** del proyecto.

---
""", unsafe_allow_html=True)

@st.cache_data
def cargar_datos():
    try:
        df = pd.read_csv("interacciones_salud.mental-Rafael.csv", encoding="latin-1")

        if "fecha" in df.columns:
            df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
            df["dia"] = df["fecha"].dt.date
        else:
            df["fecha"] = datetime.now()
            df["dia"] = df["fecha"].dt.date

        if "respuesta_sugerida" not in df.columns:
            df["respuesta_sugerida"] = ""

        return df

    except FileNotFoundError:
        st.error("No se encontró el archivo 'interacciones_salud.mental-Rafael.csv'. Crea uno antes de continuar.")
        columnas = ["usuario", "tipo_interaccion", "contenido", "fecha", "estado_emocional",
                    "categoria", "nivel_intensidad", "respuesta_sugerida"]
        return pd.DataFrame(columns=columnas)

df = cargar_datos()

# ======================
# FRASES AUTOMÁTICAS
# ======================
respuestas_automaticas = [
    "Gracias por compartir. Lo que sientes es válido.",
    "Respira, estás haciendo lo mejor que puedes.",
    "Tu mensaje puede ayudar a otros también.",
    "Este espacio es seguro para ti.",
    "No estás solo. Estamos contigo.",
    "Trátate con la misma compasión que ofreces a los demás.",
    "Pedir ayuda es un acto de valentía, no de debilidad.",
    "Está bien no estar bien. Aquí puedes expresarte sin juicio.",
    "Tu bienestar importa. Mereces sentirte mejor.",
    "A veces, solo estar presente ya es suficiente.",
    "El descanso también es parte del éxito.",
    "Tu voz también merece ser escuchada.",
    "Lo que estás sintiendo tiene sentido.",
    "Cada paso que das hacia el cuidado emocional cuenta.",
    "Eres más fuerte de lo que crees."
]

# ======================
# MENÚ LATERAL Y FILTROS
# ======================
menu = st.sidebar.radio("📂 Navegación", [
    "Inicio",
    "Resumen",
    "Gráficos",
    "Mensajes",
    "Podcast",
    "Información"
])

if df["fecha"].notna().any():
    fecha_min = st.sidebar.date_input("Desde", df["fecha"].min().date())
    fecha_max = st.sidebar.date_input("Hasta", df["fecha"].max().date())
else:
    fecha_min = st.sidebar.date_input("Desde", datetime.now().date())
    fecha_max = st.sidebar.date_input("Hasta", datetime.now().date())

categoria = st.sidebar.multiselect("Categoría", df["categoria"].unique(), default=df["categoria"].unique())
emociones = st.sidebar.multiselect("Estado emocional", df["estado_emocional"].unique(), default=df["estado_emocional"].unique())
intensidad = st.sidebar.slider("Nivel de intensidad", 1, 5, (1, 5))
mostrar_datos = st.sidebar.checkbox("Mostrar tabla de datos")

df_filtrado = df[
    (df["dia"] >= fecha_min) &
    (df["dia"] <= fecha_max) &
    (df["categoria"].isin(categoria)) &
    (df["estado_emocional"].isin(emociones)) &
    (df["nivel_intensidad"] >= intensidad[0]) &
    (df["nivel_intensidad"] <= intensidad[1])
]

# ======================
# SECCIÓN: INICIO / REGISTRO
# ======================
if menu == "Inicio":
    st.header("👋 Bienvenido a Bienestar Mental UVG")

    with st.form("registro_usuario"):
        nombre = st.text_input("Nombre completo")
        correo = st.text_input("Correo institucional")
        facultad = st.selectbox("Facultad", ["Ingeniería", "Ciencias Sociales", "Educación", "Arquitectura", "Ciencias y Humanidades", "Otra"])
        aceptar = st.checkbox("Acepto compartir mis datos de forma confidencial")
        registrar = st.form_submit_button("Registrarme")

        if registrar:
            if not nombre or not correo:
                st.warning("Por favor completa todos los campos requeridos.")
            elif not aceptar:
                st.warning("Debes aceptar las condiciones para continuar.")
            else:
                st.success(f"¡Bienvenido, {nombre}! Gracias por unirte al espacio de bienestar emocional 💚.")
                st.session_state["usuario_actual"] = nombre

    st.markdown("""
    ---
    ### 💡 Sobre esta plataforma
    Este espacio fue diseñado para ofrecer acompañamiento emocional, registrar experiencias y fomentar el bienestar
    entre estudiantes y docentes de la *Universidad del Valle de Guatemala (UVG)*.
    
    Aquí podrás:
    - Analizar datos sobre bienestar emocional 🧾  
    - Visualizar estadísticas 📊  
    - Compartir tus pensamientos 💬  
    - Escuchar podcasts educativos 🎧  
    """)

# ======================
# SECCIÓN: RESUMEN
# ======================
elif menu == "Resumen":
    st.header("📈 Análisis Estadístico")

    st.metric("Total de interacciones", len(df_filtrado))
    st.metric("Usuarios únicos", df_filtrado["usuario"].nunique())

    st.subheader("1️⃣ Promedio de intensidad por categoría")
    st.dataframe(df_filtrado.groupby("categoria")["nivel_intensidad"].mean())

    st.subheader("2️⃣ Intensidad mínima y máxima por emoción")
    st.dataframe(df_filtrado.groupby("estado_emocional")["nivel_intensidad"].agg(["min", "max"]))

    st.subheader("3️⃣ Conteo de interacciones por tipo")
    st.dataframe(df_filtrado["tipo_interaccion"].value_counts())

    st.subheader("4️⃣ Emociones más frecuentes")
    st.dataframe(df_filtrado["estado_emocional"].value_counts())

    st.subheader("5️⃣ Interacciones por día y tipo")
    st.dataframe(df_filtrado.groupby(["dia", "tipo_interaccion"]).size().unstack().fillna(0))

    st.subheader("6️⃣ Interacciones por usuario y categoría")
    st.dataframe(df_filtrado.groupby(["usuario", "categoria"]).size().unstack().fillna(0))

    st.subheader("7️⃣ Porcentaje por tipo de interacción")
    st.dataframe(df_filtrado["tipo_interaccion"].value_counts(normalize=True) * 100)

    st.subheader("8️⃣ Día con más actividad")
    st.success(f"{df_filtrado['dia'].value_counts().idxmax()}")

    st.subheader("9️⃣ Media general de intensidad")
    st.info(round(df_filtrado["nivel_intensidad"].mean(), 2))

    st.subheader("🔟 Categoría con mayor participación")
    st.warning(df_filtrado["categoria"].value_counts().idxmax())

# ======================
# SECCIÓN: GRÁFICOS
# ======================
elif menu == "Gráficos":
    st.header("📊 Visualizaciones")

# ------ BARRAS----------
    st.subheader("Barras: Interacciones por tipo")
    fig1, ax1 = plt.subplots()
    df_filtrado["tipo_interaccion"].value_counts().plot(kind="bar", ax=ax1, color="skyblue")
    ax1.set_title("Interacciones por tipo")
    st.pyplot(fig1)
    
# ------ LÍNEAS----------
    st.subheader("Líneas: Evolución diaria")
    fig2, ax2 = plt.subplots()
    df_filtrado.groupby("dia").size().plot(kind="line", ax=ax2, marker='o', color='teal')
    ax2.set_title("Interacciones por día")
    st.pyplot(fig2)
    
# ------ PASTEL----------
    st.subheader("Pastel: Emociones")
    fig3, ax3 = plt.subplots()
    df_filtrado["estado_emocional"].value_counts().plot.pie(autopct="%1.1f%%", ax=ax3, colors=sns.color_palette("pastel"))
    ax3.set_ylabel("")
    ax3.set_title("Distribución emocional")
    st.pyplot(fig3)

# ------ HISTOGRAMA----------
    st.subheader("Histograma: Intensidad emocional")
    fig4, ax4 = plt.subplots()
    sns.histplot(df_filtrado["nivel_intensidad"], bins=5, kde=True, ax=ax4, color="salmon")
    ax4.set_title("Distribución de intensidad")
    st.pyplot(fig4)

# ------ BARRAS APILADAS----------
    st.subheader("Barras apiladas: Usuario vs Categoría")
    fig5, ax5 = plt.subplots()
    df_filtrado.groupby(["usuario", "categoria"]).size().unstack().fillna(0).plot(kind="bar", stacked=True, ax=ax5)
    ax5.set_title("Interacciones por usuario y categoría")
    st.pyplot(fig5)

# ======================
# SECCIÓN: MENSAJES
# ======================
elif menu == "Mensajes":
    st.header("💬 Chat de acompañamiento")

    with st.form("chat_form"):
        usuario = st.text_input("Tu nombre")
        mensaje = st.text_area("¿Qué te gustaría compartir?")

        emocion = st.selectbox(
            "¿Cómo te sientes?",
            ["ansiedad", "calma", "estrés", "tristeza", "inseguridad", "agotamiento"]
        )

        intensidad = st.slider("¿Qué tan intensa es esta emoción?", 1, 5, 3)

        grupo = st.selectbox("Grupo", ["A", "B", "C"])

        tema = st.selectbox(
            "Tema recurrente:",
            [
                "Apoyo entre pares",
                "Estrés académico",
                "Ansiedad y calma",
                "Autoestima y autocompasión",
                "Relaciones interpersonales",
                "Motivación y metas",
                "Organización del tiempo",
                "Duelo y pérdida",
                "Salud física y mental",
                "Otro tema"
            ]
        )

        enviar = st.form_submit_button("Enviar")

        if enviar and usuario and mensaje:
            respuesta = random.choice(respuestas_automaticas)
            nuevo = pd.DataFrame([{
                "usuario": usuario,
                "tipo_interaccion": "mensaje_chat",
                "contenido": mensaje,
                "fecha": datetime.now(),
                "estado_emocional": emocion,
                "recurso_origen": "chat",
                "categoria": "emocional",
                "nivel_intensidad": intensidad,
                "grupo": grupo,
                "tema_recurrente": tema,
                "respuesta_sugerida": respuesta
            }])

            try:
                nuevo.to_csv("interacciones_salud.mental.csv", mode="a", header=False, index=False)
                st.success(f"Mensaje enviado 💚 {respuesta}")
            except Exception as e:
                st.error(f"⚠️ Error al guardar el mensaje: {e}")

    st.subheader("📜 Mensajes recientes")
    try:
        mensajes_chat = df[df["tipo_interaccion"] == "mensaje_chat"].sort_values("fecha", ascending=False).head(10)
        for _, row in mensajes_chat.iterrows():
            st.write(f"*{row['usuario']}* ({row['estado_emocional']}, Grupo {row['grupo']}): {row['contenido']}")
            st.caption(f"💡 {row.get('respuesta_sugerida', 'Gracias por compartir tu mensaje.')}")
    except Exception as e:
        st.warning(f"No se pudieron cargar los mensajes recientes: {e}")

# ======================
# SECCIÓN: PODCAST
# ======================
elif menu == "Podcast":
    st.header("🎧 Podcast educativo")

    episodios = {
        "Episodio 1": {
            "titulo": "Manejo del estrés académico",
            "mensaje": "¿Te sientes abrumado por tareas y exámenes?",
            "descripcion": (
            "El estrés académico es una respuesta natural ante la presión universitaria. "
            "En este episodio exploramos cómo identificar sus señales, reconocer tus límites "
            "y crear rutinas que te permitan equilibrar el estudio con tu bienestar emocional. "
            "Aprenderás técnicas de respiración, pausas activas y estrategias de organización del tiempo."
        ),
            "cierre": "🎓 Recuerda: tu valor no depende de una nota, sino de tu esfuerzo constante."
    },
        "Episodio 2": {
        "titulo": "Rompiendo el estigma",
        "mensaje": "🧠 ¿Te cuesta pedir ayuda por miedo al qué dirán?",
        "descripcion": (
            "Hablar de salud mental todavía puede generar miedo o vergüenza. "
            "Aquí discutimos los mitos más comunes y cómo normalizar las conversaciones sobre emociones. "
            "Compartimos testimonios reales de estudiantes que encontraron apoyo y aprendieron a expresarse sin temor."
        ),
        "cierre": "💬 Pedir ayuda no te hace débil, te hace humano."
    },
        "Episodio 3": {
        "titulo": "Balance entre trabajo y estudio",
        "mensaje": "⚖️ ¿Sientes que no tienes tiempo para ti?",
        "descripcion": (
            "Muchos estudiantes trabajan y estudian al mismo tiempo. "
            "En este episodio te guiamos para gestionar tu energía, priorizar actividades y evitar el agotamiento. "
            "Te damos consejos sobre cómo desconectarte digitalmente y cuidar tu descanso sin culpa."
        ),
        "cierre": "💤 El descanso también es una parte esencial del éxito."
    },
          "Episodio 4": {
        "titulo": "Apoyo entre pares",
        "mensaje": "🤝 ¿Cómo acompañar sin juzgar?",
        "descripcion": (
            "Escuchar a un amigo que atraviesa un momento difícil puede marcar la diferencia. "
            "Reflexionamos sobre la importancia de la empatía, la validación emocional y el acompañamiento silencioso. "
            "Aprenderás frases que ayudan y qué cosas evitar cuando alguien busca apoyo."
        ),
        "cierre": "🌱 A veces, solo estar presente ya es suficiente."
    },
        "Episodio 5": {
        "titulo": "Cuando pedir ayuda es urgente",
        "mensaje": "🚨 ¿Sabes reconocer señales de alerta?",
        "descripcion": (
            "Hablamos sobre cómo detectar signos de crisis emocional en ti o en otros. "
            "Compartimos pasos para buscar apoyo profesional, líneas de ayuda y recursos universitarios. "
            "Recordamos que la intervención temprana puede salvar vidas."
        ),
        "cierre": "❤️ Tu bienestar merece atención inmediata. No estás solo."
    },
        "Episodio 6": {
        "titulo": "Autoestima y autocompasión",
        "mensaje": "💖 ¿Te hablas con amabilidad?",
        "descripcion": (
            "La forma en que te hablas impacta directamente en tu bienestar. "
            "En este episodio exploramos cómo desarrollar una voz interna más compasiva, "
            "aceptar los errores como parte del crecimiento y construir una autoestima saludable. "
            "Incluye ejercicios prácticos para mejorar tu diálogo interno."
        ),
        "cierre": "🌷 Trátate con el mismo cariño con el que tratarías a tu mejor amigo."
    },
        "Episodio 7": {
        "titulo": "Ansiedad social en la universidad",
        "mensaje": "😰 ¿Te cuesta participar en clase o grupos?",
        "descripcion": (
            "La ansiedad social puede limitar tu participación y conexión con otros. "
            "Analizamos qué la causa, cómo se manifiesta y cómo puedes afrontarla con pequeñas acciones. "
            "Incluye tips de exposición gradual, autoconfianza y manejo de pensamientos negativos."
        ),
        "cierre": "🎤 Tu voz también merece ser escuchada."
    },
         "Episodio 8": {
        "titulo": "Cómo acompañar a un amigo que sufre",
        "mensaje": "🤗 ¿Quieres ayudar sin invadir?",
        "descripcion": (
            "Acompañar a alguien en dolor requiere empatía, respeto y paciencia. "
            "Te damos herramientas para escuchar activamente, cuidar tus límites y ofrecer apoyo real sin sobrecargarte. "
            "También compartimos recursos de ayuda profesional para guiar a otros de forma segura."
        ),
        "cierre": "💚 A veces, solo estar ahí, con presencia y empatía, ya es suficiente."
    }
}
                    
    opcion = st.selectbox("Elige un episodio para escuchar", list(episodios.keys()))
    ep = episodios[opcion]
    st.markdown(f"### {ep['titulo']}")
    st.info(ep["mensaje"])
    st.write(ep["descripcion"])
    st.success(ep["cierre"])

# ======================
# SECCIÓN: INFORMACIÓN FINAL
# ======================
elif menu == "Información":
    st.header("👩‍💻 Información del proyecto")

    st.markdown("""
    *Desarrollado por:*
    - Rafael Téllez  
    - Andrés Morales  
    - Irvin González  
    - Rodrigo Martínez  
    - Allison Figueroa  

    ---
    *Universidad del Valle de Guatemala – Ingeniería Civil*  
    Proyecto final de Programación, 2025.
    """)

    st.markdown("""
    💬 *Agradecimiento especial:*
    
    Gracias por utilizar esta plataforma y por confiar en el proceso de bienestar emocional.  
    Esperamos que esta herramienta contribuya a fortalecer la empatía, la reflexión y el apoyo mutuo
    dentro de la comunidad universitaria 💚.
    """)
