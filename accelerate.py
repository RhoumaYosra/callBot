# import tkinter as tk
# from tkinter import ttk
# import pyttsx3
# import os
# import threading
# import time
# import sounddevice as sd  # Import sounddevice for audio recording
# import soundfile as sf  # Import soundfile for saving audio
# import whisper
# from groq import Groq
# import logging

# # Set up logging for latency analysis
# logging.basicConfig(filename='latency_log.txt', level=logging.INFO)

# class CallBotGUI:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Call Bot")
#         self.stop_flag = False

#         self.create_widgets()

#     def create_widgets(self):
#         self.dialogue_frame = ttk.Frame(self.root, padding="20")
#         self.dialogue_frame.grid(row=0, column=0, sticky="nsew")

#         self.dialogue_label = ttk.Label(self.dialogue_frame, text="Dialogue:")
#         self.dialogue_label.grid(row=0, column=0, sticky="w")

#         self.dialogue_text = tk.Text(self.dialogue_frame, width=50, height=10)
#         self.dialogue_text.grid(row=1, column=0, padx=5, pady=5)

#         self.start_button = ttk.Button(self.root, text="Commencer la conversation", command=self.start_conversation)
#         self.start_button.grid(row=1, column=0, sticky="e")

#     def log_time_taken(self, task_name, start_time, end_time):
#         elapsed_time = end_time - start_time
#         logging.info(f"{task_name} took {elapsed_time:.2f} seconds")
#         print(f"{task_name} took {elapsed_time:.2f} seconds")

#     def speak(self, text):
#         start_time = time.time()
#         engine = pyttsx3.init()
#         voices = engine.getProperty('voices')
#         for voice in voices:
#             if 'english' in voice.name.lower():
#                 engine.setProperty('voice', voice.id)
#                 break
#         engine.setProperty('rate', 150)  # Adjust the speech rate here (default is 200)
#         engine.say(text)
#         engine.runAndWait()
#         end_time = time.time()
#         self.log_time_taken("Text-to-Speech (pyttsx3)", start_time, end_time)

#     def recognize_speech(self):
#         start_time = time.time()
#         model = whisper.load_model("base")
#         fs = 44100
#         seconds = 4
#         print("Recording audio...")
#         audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1)  # Use sounddevice for audio recording
#         sd.wait()
#         end_recording_time = time.time()
#         self.log_time_taken("Audio Recording", start_time, end_recording_time)

#         audio_file = "temp.wav"
#         sf.write(audio_file, audio, fs)
#         end_saving_time = time.time()
#         self.log_time_taken("Saving Audio", end_recording_time, end_saving_time)

#         result = model.transcribe(audio_file)
#         end_transcription_time = time.time()
#         self.log_time_taken("Audio Transcription", end_saving_time, end_transcription_time)

#         os.remove(audio_file)
#         end_time = time.time()
#         self.log_time_taken("Total Speech Recognition", start_time, end_time)
#         return result["text"]

#     def bot_conversation(self):
#         self.dialogue_text.insert(tk.END, "Bot: how can I assist you today?\n")
#         self.speak("How can I assist you today?")

#         while True:
#             user_input = self.recognize_speech()
#             self.dialogue_text.insert(tk.END, f"Vous: {user_input}\n")

#             if user_input.lower() == "au revoir":
#                 break

#             start_time = time.time()
#             self.groq_response(user_input)
#             end_time = time.time()

#             response_time = end_time - start_time
#             self.log_time_taken("Total Response Time", start_time, end_time)

#     def groq_response(self, user_input):
#         start_time = time.time()
#         client = Groq(api_key="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")

#         chat_completion = client.chat.completions.create(
#             messages=[
#                 {
#                     "role": "user",
#                     "content": user_input,
#                 }
#             ],
#             model="mixtral-8x7b-32768",
#         )

#         response = chat_completion.choices[0].message.content
#         end_time = time.time()
#         self.log_time_taken("Groq API Call", start_time, end_time)

#         self.dialogue_text.insert(tk.END, f"Bot: {response}\n")
#         self.speak(response)

#     def start_conversation(self):
#         self.stop_flag = False
#         thread = threading.Thread(target=self.bot_conversation)
#         thread.daemon = True
#         thread.start()

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = CallBotGUI(root)
#     root.mainloop()


import tkinter as tk
from tkinter import ttk
import pyttsx3
import os
import threading
import time
import sounddevice as sd  # Importer sounddevice pour l'enregistrement audio
import soundfile as sf  # Importer soundfile pour sauvegarder l'audio
import whisper
from groq import Groq
import logging

# Configurer le journal pour l'analyse de la latence
logging.basicConfig(filename='latency_log.txt', level=logging.INFO)

class CallBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bot d'appel")
        self.stop_flag = False

        self.create_widgets()

    def create_widgets(self):
        self.dialogue_frame = ttk.Frame(self.root, padding="20")
        self.dialogue_frame.grid(row=0, column=0, sticky="nsew")

        self.dialogue_label = ttk.Label(self.dialogue_frame, text="Dialogue :")
        self.dialogue_label.grid(row=0, column=0, sticky="w")

        self.dialogue_text = tk.Text(self.dialogue_frame, width=50, height=10)
        self.dialogue_text.grid(row=1, column=0, padx=5, pady=5)

        self.start_button = ttk.Button(self.root, text="Commencer la conversation", command=self.start_conversation)
        self.start_button.grid(row=1, column=0, sticky="e")

    def log_time_taken(self, task_name, start_time, end_time):
        elapsed_time = end_time - start_time
        logging.info(f"{task_name} a pris {elapsed_time:.2f} secondes")
        print(f"{task_name} a pris {elapsed_time:.2f} secondes")

    def speak(self, text):
        start_time = time.time()
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'french' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        engine.setProperty('rate', 150)  # Ajuster la vitesse de parole ici (par défaut est 200)
        engine.say(text)
        engine.runAndWait()
        end_time = time.time()
        self.log_time_taken("Texte-à-parole (pyttsx3)", start_time, end_time)

    def recognize_speech(self):
        start_time = time.time()
        model = whisper.load_model("base")
        fs = 44100
        seconds = 4
        print("Enregistrement audio...")
        audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1)  # Utiliser sounddevice pour l'enregistrement audio
        sd.wait()
        end_recording_time = time.time()
        self.log_time_taken("Enregistrement audio", start_time, end_recording_time)

        audio_file = "temp.wav"
        sf.write(audio_file, audio, fs)
        end_saving_time = time.time()
        self.log_time_taken("Sauvegarde audio", end_recording_time, end_saving_time)

        result = model.transcribe(audio_file)
        end_transcription_time = time.time()
        self.log_time_taken("Transcription audio", end_saving_time, end_transcription_time)

        os.remove(audio_file)
        end_time = time.time()
        self.log_time_taken("Reconnaissance vocale totale", start_time, end_time)
        return result["text"]

    def bot_conversation(self):
        self.dialogue_text.insert(tk.END, "Bot : Comment puis-je vous aider aujourd'hui ?\n")
        self.speak("Comment puis-je vous aider aujourd'hui ?")

        while True:
            user_input = self.recognize_speech()
            self.dialogue_text.insert(tk.END, f"Vous : {user_input}\n")

            if user_input.lower() == "au revoir":
                break

            start_time = time.time()
            self.groq_response(user_input)
            end_time = time.time()

            response_time = end_time - start_time
            self.log_time_taken("Temps de réponse total", start_time, end_time)

    def groq_response(self, user_input):
        start_time = time.time()
        client = Groq(api_key="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")

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
        end_time = time.time()
        self.log_time_taken("Appel API Groq", start_time, end_time)

        self.dialogue_text.insert(tk.END, f"Bot : {response}\n")
        self.speak(response)

    def start_conversation(self):
        self.stop_flag = False
        thread = threading.Thread(target=self.bot_conversation)
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = CallBotGUI(root)
    root.mainloop()
