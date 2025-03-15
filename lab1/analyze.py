import requests
import json

def ocr_space_file(filename, overlay=False, api_key='K85016083988957', language='eng'):
    url = "https://api.ocr.space/parse/image"
    
    # Datos para la solicitud
    payload = {
        'isOverlayRequired': overlay,
        'apikey': api_key,
        'language': language
    }

    # Realizar la solicitud POST con el archivo de imagen
    with open(filename, 'rb') as file:
        response = requests.post(url, files={filename: file}, data=payload)
    
    # Retornar el contenido decodificado de la respuesta en formato JSON
    return response.content.decode()


def read_image(filename):
    # Obtener el resultado de la API OCR
    ocr_result = ocr_space_file(filename=filename, language='eng')

    # Convertir el resultado JSON a un diccionario de Python
    ocr_data = json.loads(ocr_result)

    # Extraer el texto 
    parsed_text = ocr_data["ParsedResults"][0]["ParsedText"]

    return parsed_text
