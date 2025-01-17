import whisper

# Cargar el modelo
model = whisper.load_model("base")

# Transcribir el video
result = model.transcribe("video_temp.mp4")

# Guardar el resultado en un archivo
with open("transcription.txt", "w", encoding="utf-8") as f:
    f.write(result["text"])
