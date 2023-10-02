import speech_recognition as sr
import pyaudio
import wave
import tkinter as tk
from threading import Thread

class AudioText3:
    def __init__(
        self,
        format,
        channels,
        sample_rate,
        buffer_size,
        file_path,
    ):
        self.format = format
        self.channels = channels
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        self.file_path = file_path
        self.is_recording = False

    def record_audio(self):
        try:
            audio = pyaudio.PyAudio()
            stream = audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.buffer_size,
            )

            print("GRABANDO........")

            frames = []

            self.is_recording = True

            while self.is_recording:
                data = stream.read(self.buffer_size)
                frames.append(data)

            print("DETENIENDO GRABACIÓN...")

            stream.stop_stream()
            stream.close()
            audio.terminate()

            x = wave.open(self.file_path, "wb")
            x.setnchannels(self.channels)
            x.setsampwidth(audio.get_sample_size(self.format))
            x.setframerate(self.sample_rate)
            x.writeframes(b"".join(frames))
            x.close()

            return {
                "status": "success",
                "message": "Proceso completado",
                "file_path": self.file_path,
            }
        except Exception as exception:
            return {
                "status": "failed",
                "message": f"Error: {exception}",
            }

    def transcribe_audio(self, audio_path):
        try:
            r = sr.Recognizer()
            audio_file = sr.AudioFile(audio_path)

            with audio_file as source:
                audio = r.record(source)

            text = r.recognize_google(audio, language="es-ES")

            if text:
                return {
                    "status": "success",
                    "message": "Transcripción exitosa",
                    "text": text,
                }
            return {
                "status": "failed",
                "message": "Transcripción fallida",
            }
        except Exception as exception:
            return {
                "status": "failed",
                "message": f"Error: {exception}",
            }


def start_recording():
    global recording_thread
    recording_thread = Thread(target=audio_text.record_audio)
    recording_thread.start()

def stop_recording():
    if recording_thread.is_alive():
        audio_text.is_recording = False
        recording_thread.join()
        
        recording_result = audio_text.transcribe_audio(file_path)
        
        if recording_result["status"] == "success":
            transcribed_text = recording_result["text"]
            print("Texto Transcrito:", transcribed_text)
        else:
            print("Error en la transcripción.")

if __name__ == "__main__":
    format = pyaudio.paInt16
    channels = 2
    sample_rate = 44100
    buffer_size = 1024
    file_path = "audio_recording.wav"

    audio_text = AudioText3(
        format, channels, sample_rate, buffer_size, file_path
    )

    root = tk.Tk()
    root.title("Grabación de audio")

    start_button = tk.Button(root, text="Iniciar Grabación", command=start_recording)
    stop_button = tk.Button(root, text="Detener Grabación", command=stop_recording)

    start_button.pack()
    stop_button.pack()

    root.mainloop()
