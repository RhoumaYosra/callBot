import whisper
import time

# Liste des modèles à tester
models = ["tiny", "base", "small", "medium", "large"]

# Chemin vers le fichier audio en français
audio_file = "./audio1.wav"

# Fonction pour tester un modèle et mesurer le temps de réponse
def test_model(model_name):
    print(f"Testing model: {model_name}")
    model = whisper.load_model(model_name)
    start_time = time.time()
    result = model.transcribe(audio_file, language="fr")
    end_time = time.time()
    response_time = end_time - start_time
    print(f"Response time for {model_name}: {response_time} seconds")
    print("Transcription:")
    print(result["text"])
    print("\n")

# Tester chaque modèle
for model_name in models:
    test_model(model_name)
