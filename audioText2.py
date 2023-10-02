import speech_recognition as sr
import pyaudio
import wave
import openai

class AudioText2:
    def __init__(
        self,
        format,
        channels,
        sample_rate,
        buffer_size,
        recording_duration,
        file_path,
    ):
        self.format = format
        self.channels = channels
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        self.recording_duration = recording_duration
        self.file_path = file_path

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

            for i in range(
                0,
                int(self.sample_rate / self.buffer_size * self.recording_duration)
            ):
                data = stream.read(self.buffer_size)
                frames.append(data)

            print("SE HA GRABADO CORRECTAMENTE...")

            stream.stop_stream()
            stream.close()
            audio.terminate()

            x = wave.open(self.file_path, "wb")
            x.setnchannels(self.channels)
            x.setsampwidth(audio.get_sample_size(self.format))
            x.setframerate(self.sample_rate)
            x.writeframes(b"".join(frames))
            x.close()

            result = self.transcribe_audio(self.file_path)

            if result["status"] == "success":
                return {
                    "status": "success",
                    "message": "Process completed",
                    "text": result["text"],
                }
            return {
                "status": "failed",
                "message": "Process not completed",
            }
        except Exception as exception:
            raise NameError(f"Error: {exception}")

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
                    "message": "Transcription successful",
                    "text": text,
                }
            return {
                "status": "failed",
                "message": "Transcription failed",
            }
        except Exception as exception:
            raise NameError(f"Error: {exception}")

# API Key
api_key = ""

def interact_with_chatgpt(text):
    try:
        openai.api_key = api_key
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=text,
            max_tokens=100  
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    format = pyaudio.paInt16
    channels = 2
    sample_rate = 44100
    buffer_size = 1024
    recording_duration = 15
    file_path = "audio_recording.wav"

    audio_text = AudioText2(
        format, channels, sample_rate, buffer_size, recording_duration, file_path
    )

    recording_result = audio_text.record_audio()

    if recording_result["status"] == "success":
        transcribed_text = recording_result["text"]

        print("")
        print("Pregunta a ChatGPT:", transcribed_text)

        chatgpt_response = interact_with_chatgpt(transcribed_text)

        print("")
        print("Respuesta de ChatGPT:", chatgpt_response)
    else:
        print("Error in recording and transcription.")
