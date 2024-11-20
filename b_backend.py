import openai
import sqlite3
from langchain.sql_database import SQLDatabase
from langchain_community.chat_models import ChatOpenAI

# Establecer la clave API directamente en el código
openai.api_key = "####"

# Verificar si la clave API está configurada correctamente
if openai.api_key is None:
    raise ValueError("La clave de API de OpenAI no está configurada correctamente.")

# 1. Cargar la base de datos SQLite
db = SQLDatabase.from_uri("sqlite:///ecommerce.db")

# 2. Crear el modelo LLM de OpenAI
llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo', openai_api_key=openai.api_key)

# 3. Función para hacer la consulta utilizando LLM
formato = """
Data una pregunta del usuario:
1. crea una consulta de sqlite3
2. revisa los resultados
3. devuelve el dato
4. si tienes que hacer alguna aclaración o devolver cualquier texto que sea siempre en español
#{question}
"""

def obtener_respuesta_llm(input_usuario):
    # Crear el formato de la consulta en función de la pregunta
    consulta_sql = formato.format(question=input_usuario)
    
    # Llamar a OpenAI para obtener la respuesta utilizando la nueva API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Especifica el modelo a usar
        messages=[
            {"role": "system", "content": "Eres un asistente experto en bases de datos SQL."},
            {"role": "user", "content": consulta_sql}
        ]
    )
    
    # Obtener y devolver la respuesta
    return response['choices'][0]['message']['content']

# 4. Función para ejecutar la consulta SQL
def consulta(input_usuario):
    # Obtener la respuesta de LLM basada en la consulta
    resultado = obtener_respuesta_llm(input_usuario)
    return resultado
