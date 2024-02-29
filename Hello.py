import os
import streamlit as st
import pandas as pd
import requests
import openai
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
# Función para clasificar los comentarios
def clasificar_comentarios(data, column_name, api_key):
    # Configurar la API Key de OpenAI
    openai.api_key = api_key
    
    # Definir el texto del prompt para la clasificación
    prompt = """
        Tendrás un rol de clasificador de comentarios de una publicación relacionada con la vacuna contra el VPH.
        No tienes permitido responder otra cosa que no sean números. Las clasificaciones son:

        Si el comentario tiene una postura contraria a la vacuna contra el VPH (antivacuna).La respuesta es: 0
        Si el comentario tiene una postura a favor de la vacuna contra el VPH (provacuna).La respuesta es: 1
        Si el comentario refleja una duda o dudas relacionadas con la vacuna contra el VPH.La respuesta es: 2
        Si el comentario habla de cualquier otra cosa. La respuesta es: 3

        Trata de interpretar las intenciones de las personas, ya que se trata de comentarios de Facebook.
        Si no puedes clasificar, tu respuesta debe ser "3".

        Ahora, clasifica el siguiente comentario, teniendo en cuenta que tu respuesta es solo un número:
    """
    batch_size = 20  # Tamaño del lote de comentarios a procesar antes de guardar
    
    output_file = "data_clasificado.xlsx"  # Nombre del archivo de salida
    checkpoint_file = "checkpoint.txt"  # Nombre del archivo de checkpoint
    
    # Variable para almacenar la posición actual en el bucle
    current_index = 0
    completed = False
    while not completed:
        # Verificar si existe un archivo de checkpoint
        try:
            with open(checkpoint_file, 'r') as f:
                current_index = int(f.read())
            print("Se encontró un archivo de checkpoint. Continuando desde la posición:", current_index)
        except FileNotFoundError:
            print("No se encontró un archivo de checkpoint. Comenzando desde el principio.")

        # Crear una columna vacía para almacenar las respuestas si aún no existe
        if 'Clasificación_gpt_4' not in data.columns:
            data['Clasificación_gpt_4'] = ''

        # Iterar sobre cada comentario en el DataFrame
        for index, row in data.iterrows():
            # Verificar si se debe retomar desde el punto de reinicio guardado
            if index < current_index:
                continue

            comment = row[column_name]
            try:
                # Crear la solicitud de completado de chat
                completion = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": comment}
                    ],
                    temperature=0,
                    max_tokens=1
                )

                response = completion.choices[0].message.content.strip()

                # Verificar si la respuesta es un número
                if response.isdigit():
                    # Convertir la respuesta a entero
                    response = int(response)
                else:
                    # Manejar el caso en el que la respuesta no es un número
                    # Puedes asignar un valor predeterminado o tomar cualquier otra acción apropiada
                    response = None  # o cualquier otro valor predeterminado que prefieras

                data.at[index, 'Clasificación_gpt_4'] = response
                
                # Guardar el DataFrame en un archivo después de procesar un lote de comentarios
                if (index + 1) % batch_size == 0 or (index + 1) == len(data):
                    data[:index + 1].to_excel(output_file, index=False)
                    print("Guardando...")

                    # Guardar la posición actual como punto de reinicio
                    with open(checkpoint_file, 'w') as file:
                        file.write(str(index + 1))

            except openai.OpenAIError as e:
                # Manejar el error del servidor de OpenAI
                print("Error del servidor de OpenAI:", e)
                print("Reanudando el proceso desde la iteración", index)
                completed = False
                break
        else:
            # El bucle for se completó sin errores, terminar el proceso
            completed = True
            with open(checkpoint_file, 'w') as file:
                file.write(str(0))
                open_file = True

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
            
            # Clasificar los comentarios si se ha proporcionado la API Key
            if api_key:
                data = clasificar_comentarios(data, column_name, api_key)
                st.write("Datos clasificados:")
                st.write(data)

        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")

    # Mostrar la imagen desde una URL
    url_imagen = "https://raw.githubusercontent.com/KimberlySalazarB/paginaprueba/main/Imagen3.jpg"
    contenido_imagen = obtener_contenido_archivo(url_imagen)
    if contenido_imagen is not None:
        imagen = Image.open(BytesIO(contenido_imagen))
        st.image(imagen, caption='Imagen desde la URL')

    # Mostrar comentarios antivacunas al hacer clic en un botón
    if st.button("Mostrar comentarios antivacunas"):
        comentarios_antivacunas = data[data['Clasificación_gpt_4'] == 0][column_name].tolist()
        st.subheader("Comentarios antivacunas encontrados:")
        if comentarios_antivacunas:
            for comentario in comentarios_antivacunas:
                st.write(comentario)
        else:
            st.write("No se encontraron comentarios antivacunas.")

    # Mostrar comentarios antivacunas al hacer clic en un botón
    if st.button("Mostrar comentarios dudas"):
        comentarios_antivacunas = data[data['Clasificación_gpt_4'] == 3][column_name].tolist()
        st.subheader("Comentarios antivacunas encontrados:")
        if comentarios_antivacunas:
            for comentario in comentarios_antivacunas:
                st.write(comentario)
        else:
            st.write("No se encontraron comentarios antivacunas.")
                    
if __name__ == "__main__":
    run()

    

