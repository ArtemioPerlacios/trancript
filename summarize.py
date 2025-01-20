import os
import requests
import time

# Obtener la API Key desde las variables de entorno
API_KEY = os.getenv("GROQ_API_KEY")

# Cargar la transcripción
with open("transcription.txt", "r", encoding="utf-8") as file:
    transcription = file.read()

# Dividir la transcripción en fragmentos pequeños (por ejemplo, 2000 caracteres por fragmento)
def split_text(text, max_length=8000):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

fragments = split_text(transcription)

# Endpoint de la API de Groq
url = "https://api.groq.com/openai/v1/chat/completions"

# Configurar los encabezados de la solicitud
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

with open("prompt1.md", "r", encoding="utf-8") as file:
    prompt_file = file.read()

# Función para procesar un fragmento con manejo de límites de tasa
def process_fragment(fragment, retries=3):
    for _ in range(retries):
        data = {
            "model": "llama3-70b-8192",
            "messages": [
                {"role": "system", "content": "Eres un asistente que resume textos."},
                {"role": "user", "content": prompt_file.format(input=fragment)},
            ],
        }
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            # Procesar la respuesta exitosa
            return response.json().get("choices", [{}])[0].get("message", {}).get("content", "Resumen no disponible")
        elif response.status_code == 429:
            # Manejar límite de tasa y esperar antes de reintentar
            retry_after = response.json().get("error", {}).get("retry_after", 10)  # Intentar obtener el tiempo de espera recomendado
            print(f"Límite alcanzado. Esperando {retry_after} segundos...")
            time.sleep(retry_after)
        else:
            # Mostrar otros errores
            print(f"Error en la solicitud: {response.status_code} - {response.text}")
            break
    return f"Error procesando el fragmento: {fragment[:50]}..."

# Procesar todos los fragmentos y guardar los resúmenes parciales
partial_summaries = []
for i, fragment in enumerate(fragments):
    print(f"Procesando fragmento {i + 1}/{len(fragments)}...")
    summary = process_fragment(fragment)
    partial_summaries.append(summary)
    print(f"Resumen del fragmento {i + 1}: {summary}")

# Combinar los resúmenes parciales en Markdown
final_summary = "\n\n".join(partial_summaries)

# Guardar el resumen final en un archivo
with open("summary.md", "w", encoding="utf-8") as f:
    f.write(final_summary)

print("Resumen completo guardado en summary.md.")

