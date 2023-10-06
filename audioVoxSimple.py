from vosk import Model, KaldiRecognizer
import pyaudio

model = Model(r"/home/vincent/Escritorio/PYTHON PROJECT/vosk-model-small-es-0.42")
recognizer = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)

while True:
    data = stream.read(4096)
    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
        print(result[14:-3])
