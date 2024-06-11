import tkinter as tk
from tkinter import ttk
from gtts import gTTS
import os
import threading
import time
import sounddevice as sd
import soundfile as sf
import pygame
import whisper
from groq import Groq

class CallBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Call Bot")
        self.stop_flag = False  # Indicateur pour arrêter la conversation

        self.create_widgets()

    def create_widgets(self):
        self.dialogue_frame = ttk.Frame(self.root, padding="20")
        self.dialogue_frame.grid(row=0, column=0, sticky="nsew")

        self.dialogue_label = ttk.Label(self.dialogue_frame, text="Dialogue:")
        self.dialogue_label.grid(row=0, column=0, sticky="w")

        self.dialogue_text = tk.Text(self.dialogue_frame, width=50, height=10)
        self.dialogue_text.grid(row=1, column=0, padx=5, pady=5)

        self.start_button = ttk.Button(self.root, text="Commencer la conversation", command=self.start_conversation)
        self.start_button.grid(row=1, column=0, sticky="e")

    def speak(self, text):
        tts = gTTS(text=text, lang='en', slow=False)  # Assurez-vous que slow=False pour une lecture rapide
        tts.save("output.mp3")
        self.play_audio("output.mp3")

    def play_audio(self, file):
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Attendre la fin de la lecture
            time.sleep(0.05)  # Réduire l'attente à 0.05 secondes
        pygame.mixer.quit()  # Fermer le mixer pygame
        os.remove(file)

    def recognize_speech(self):
        # Enregistrer l'audio à partir du microphone
        fs = 44100  # Fréquence d'échantillonnage
        seconds = 4  # Réduire la durée de l'enregistrement à 5 secondes
        print("Enregistrement audio...")
        audio = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()

        # Enregistrer l'audio dans un fichier temporaire
        audio_file = "temp.wav"
        sf.write(audio_file, audio, fs)

        # Transcrire l'audio
        model = whisper.load_model("base")
        result = model.transcribe(audio_file)

        os.remove(audio_file)  # Supprimer le fichier temporaire après transcription

        return result["text"]

    def bot_conversation(self):
        self.dialogue_text.insert(tk.END, "Bot: how can i assist you today?\n")
        self.speak(" how can i assist you today ?")

        while True:
            user_input = self.recognize_speech()
            self.dialogue_text.insert(tk.END, f"Vous: {user_input}\n")

            if user_input.lower() == "au revoir":
                break

            start_time = time.time()
            self.groq_response(user_input)
            end_time = time.time()

            response_time = end_time - start_time
            print(f"Response time: {response_time} seconds")

    def groq_response(self, user_input):
        client = Groq(
            api_key="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",
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
            model="mixtral-8x7b-32768",
        )

        response = chat_completion.choices[0].message.content
        self.dialogue_text.insert(tk.END, f"Bot: {response}\n")
        self.speak(response)

    def start_conversation(self):
        self.stop_flag = False  # Réinitialiser l'indicateur d'arrêt
        threading.Thread(target=self.bot_conversation).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = CallBotGUI(root)
    root.mainloop()
