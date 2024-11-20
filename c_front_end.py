import b_backend
import streamlit as st
from streamlit_chat import message

# Título de la aplicación
st.title("App del Negocio")
st.write("Preguntas")

# Iniciar las preguntas y respuestas en el estado de la sesión
if 'preguntas' not in st.session_state:
    st.session_state.preguntas = []
if 'respuestas' not in st.session_state:
    st.session_state.respuestas = []

# Función para manejar el clic
def click():
    if st.session_state.user != '':
        pregunta = st.session_state.user
        respuesta = b_backend.consulta(pregunta)

        # Agregar la pregunta y respuesta al estado de la sesión
        st.session_state.preguntas.append(pregunta)
        st.session_state.respuestas.append(respuesta)

        # Limpiar el input de usuario después de enviar la pregunta
        st.session_state.user = ''

# Crear el formulario en Streamlit
with st.form('my-form'):
    query = st.text_input('¿En qué te puedo ayudar?:', key='user', help='Pulsa Enviar para hacer la pregunta')
    submit_button = st.form_submit_button('Enviar', on_click=click)

# Mostrar las preguntas y respuestas
if st.session_state.preguntas:
    for i in range(len(st.session_state.respuestas)-1, -1, -1):
        message(st.session_state.respuestas[i], key=str(i))

    # Opción para continuar la conversación
    continuar_conversacion = st.checkbox('Quieres hacer otra pregunta?')
    if not continuar_conversacion:
        st.session_state.preguntas = []
        st.session_state.respuestas = []
