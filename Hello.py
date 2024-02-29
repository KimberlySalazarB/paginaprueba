# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import streamlit as st
import pandas as pd
from streamlit.logger import get_logger
import openai
import requests
from PIL import Image
from io import BytesIO

LOGGER = get_logger(__name__)

#def guardar_api_en_github(api_key):
 #   with open('api_key.txt', 'w') as file:
  #      file.write(api_key)
   ## st.write("API key guardada con éxito en 'api_key.txt'")
def obtener_contenido_archivo(url):
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()  # Lanza una excepción si hay un error en la solicitud
        return respuesta.content
    except requests.exceptions.RequestException as e:
        print("Error al obtener el archivo:", e)
        return None
def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Bienvenidos a la página! ❤️")

    

    st.markdown(
        """
        Aquí, nos sumergimos en conversaciones significativas relacionadas con la vacuna contra el 
        Virus del Papiloma Humano (VPH). Utilizamos un clasificador especializado para analizar y 
        categorizar los comentarios de manera precisa y eficiente.
        El objetivo principal es dar los comentarios antivacunas para entender las diversas perspectivas
        expresadas por la comunidad en torno a la vacuna contra el VPH.  

        Nuestro clasificador asigna números específicos a cada comentario 
        para reflejar la postura del autor. La clasificación es la siguiente:

        0: Postura contraria a la vacuna contra el VPH (Antivacuna).  
        1: Postura a favor de la vacuna contra el VPH (Provacuna).  
        2: Expresa dudas relacionadas con la vacuna contra el VPH.  
        3: Comentarios que no se relacionan con la vacuna contra el VPH.  
    """
    )
    
    column_name = st.text_input("Ingrese el nombre de la columna que contiene los comentarios:")

    
    
     # Botón para ocultar/mostrar la API de OpenAI
    api_key = st.text_input("API Key de OpenAI", type="password")
   
    
    # Botón para guardar la API en un documento de GitHub
    #if api_key and st.button("Guardar"):
        #guardar_api_en_github(api_key)
                        
    uploaded_file = st.file_uploader("Cargar archivo", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            file_ext = uploaded_file.name.split(".")[-1]
            if file_ext == "csv":
                data = pd.read_csv(uploaded_file)
            elif file_ext == "xlsx":
                data = pd.read_excel(uploaded_file)
            
            st.write("Datos cargados:")
            st.write(data)
        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")

    # Mostrar la imagen desde una URL
    url_imagen = "https://github.com/KimberlySalazarB/paginaprueba/blob/178217e78744f064994cfcedf5464f262472275e/Imagen3.jpg"
    contenido_imagen = obtener_contenido_archivo(url_imagen)
    if contenido_imagen is not None:
        imagen = Image.open(BytesIO(contenido_imagen))
        st.image(imagen, caption='Imagen desde la URL')
                    
           
                

if __name__ == "__main__":
    run()
    

