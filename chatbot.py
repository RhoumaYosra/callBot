import tkinter as tk
from tkinter import ttk
from gtts import gTTS
import os
import threading
import whisper
import sounddevice as sd
import soundfile as sf
import pygame
import time

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
        tts = gTTS(text=text, lang='fr', slow=False)  # Assurez-vous que slow=False pour une lecture rapide
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
        seconds = 3  # Réduire la durée de l'enregistrement à 3 secondes
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
        self.dialogue_text.insert(tk.END, "Bot: Bonjour, comment puis-je vous aider aujourd'hui ?\n")
        self.speak("Bonjour, comment puis-je vous aider aujourd'hui ?")

        if self.stop_flag:
            return
        
        user_input = self.recognize_speech()
        self.dialogue_text.insert(tk.END, f"Vous: {user_input}\n")

        if self.stop_flag:
            return
        
        self.dialogue_text.insert(tk.END, "Bot: Quel article souhaitez-vous commander ?\n")
        self.speak("Quel article souhaitez-vous commander ?")

        if self.stop_flag:
            return
        
        article_response = self.recognize_speech()
        self.dialogue_text.insert(tk.END, f"Vous: {article_response}\n")

        if self.stop_flag:
            return
        
        self.dialogue_text.insert(tk.END, "Bot: Quelle est votre adresse de livraison ?\n")
        self.speak("Quelle est votre adresse de livraison ?")

        if self.stop_flag:
            return
        
        address_response = self.recognize_speech()
        self.dialogue_text.insert(tk.END, f"Vous: {address_response}\n")

        if self.stop_flag:
            return
        
        confirmation = f"Vous avez commandé {article_response}. Votre commande sera livrée à {address_response}. Merci pour votre commande !"
        self.dialogue_text.insert(tk.END, f"Bot: {confirmation}\n")
        self.speak(confirmation)

    def start_conversation(self):
        self.stop_flag = False  # Réinitialiser l'indicateur d'arrêt
        threading.Thread(target=self.bot_conversation).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = CallBotGUI(root)
    root.mainloop()
