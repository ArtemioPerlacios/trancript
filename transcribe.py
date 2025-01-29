import whisper
import argparse

# Parse arguments
parser = argparse.ArgumentParser(description="Transcribe audio or video")
parser.add_argument('--audio', type=str, help='Path to audio file', required=True)
args = parser.parse_args()

# Cargar el modelo
model = whisper.load_model("medium")

# Transcribir el archivo de audio
result = model.transcribe(args.audio)

# Guardar el resultado en un archivo
with open("transcription.txt", "w", encoding="utf-8") as f:
    f.write(result["text"])
