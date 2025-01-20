import os
import requests

# Obtener la API Key desde las variables de entorno
API_KEY = os.getenv("GROQ_API_KEY")

# Cargar la transcripción
with open("transcription.txt", "r", encoding="utf-8") as file:
    transcription = file.read()

# Endpoint de la API de Groq
url = "https://api.groq.com/summarize"

# Enviar la transcripción a la API de Groq para obtener un resumen
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

data = {
    "text": transcription,
}

response = requests.post(url, json=data, headers=headers)

# Verificar la respuesta
if response.status_code == 200:
    summary = response.json().get("summary", "Resumen no disponible")
    # Guardar el resumen en un archivo
    with open("summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)
else:
    print("Error en la solicitud:", response.status_code, response.text)
