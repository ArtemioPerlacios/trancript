import os
import requests

# Obtener la API Key desde las variables de entorno
API_KEY = os.getenv("GROQ_API_KEY")

# Cargar la transcripción
with open("transcription.txt", "r", encoding="utf-8") as file:
    transcription = file.read()

# Endpoint de la API de Groq
url = "https://api.groq.com/openai/v1/chat/completions"

# Configurar los encabezados de la solicitud
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

# Configurar los datos de la solicitud
data = {
    "model": "llama3-70b-8192",  # Asegúrate de que este modelo esté disponible en tu cuenta de Groq
    "messages": [
        {"role": "system", "content": "Eres un asistente que resume textos."},
        {"role": "user", "content": transcription},
    ],
}

# Enviar la solicitud POST a la API de Groq
response = requests.post(url, json=data, headers=headers)

# Verificar la respuesta
if response.status_code == 200:
    summary = response.json().get("choices", [{}])[0].get("message", {}).get("content", "Resumen no disponible")
    # Guardar el resumen en un archivo
    with open("summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)
else:
    print(f"Error en la solicitud: {response.status_code} - {response.text}")
