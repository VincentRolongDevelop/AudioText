import speech_recognition as sr
import tkinter as tk
from threading import Thread

class AudioTextGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Grabación de Audio")

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        self.recording = False

        self.start_button = tk.Button(root, text="Iniciar Grabación", command=self.start_recording)
        self.stop_button = tk.Button(root, text="Detener Grabación", command=self.stop_recording)

        self.start_button.pack()
        self.stop_button.pack()

    def start_recording(self):
        self.recording = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="active")

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                while self.recording:
                    audio = self.recognizer.listen(source)
                    text = self.recognizer.recognize_google(audio, language="es-ES")
                    print(text)  # Imprimir el texto transcrito en la consola
            except KeyboardInterrupt:
                pass

    def stop_recording(self):
        self.recording = False
        self.start_button.config(state="active")
        self.stop_button.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioTextGUI(root)
    root.mainloop()


