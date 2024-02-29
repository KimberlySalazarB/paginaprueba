import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

# Función para obtener el contenido de un archivo desde una URL
def obtener_contenido_archivo(url):
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()  # Lanza una excepción si hay un error en la solicitud
        return respuesta.content
    except requests.exceptions.RequestException as e:
        print("Error al obtener el archivo:", e)
        return None

# Función para clasificar los comentarios utilizando la API de OpenAI
def clasificar_comentarios(data, column_name, api_key):
    # Aquí puedes agregar tu lógica de clasificación utilizando la API de OpenAI
    # Por ahora, simplemente agregaremos una columna de clasificación aleatoria
    data['Clasificación'] = [0, 1, 2, 3,0,1,2,3,0,1]  # Ejemplo de clasificación aleatoria
    return data

# Función principal
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
            
            # Clasificar los comentarios y agregar la columna de clasificación al DataFrame
            data_clasificado = clasificar_comentarios(data, column_name, api_key)
            
            # Mostrar el DataFrame clasificado
            st.write("Datos clasificados:")
            st.write(data_clasificado)
        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")

    # Mostrar la imagen desde una URL
    url_imagen = "https://raw.githubusercontent.com/KimberlySalazarB/paginaprueba/main/Imagen3.jpg"
    contenido_imagen = obtener_contenido_archivo(url_imagen)
    if contenido_imagen is not None:
        imagen = Image.open(BytesIO(contenido_imagen))
        st.image(imagen, caption='Imagen desde la URL')
                    
if __name__ == "__main__":
    run()

    

