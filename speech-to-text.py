
import speech_recognition as sr
import time
from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play
import io

client = OpenAI()

def recognize_speech_with_openai():
    try:

        audio_file= open("audio.mp3", "rb")
        transcription = client.audio.transcriptions.create(
          model="whisper-1",
          file=audio_file
        )
        return transcription.text
    except Exception as e:
        return f"Error: {e}"

system_prompt = "You are a helpful assistant for the Math students. Your task is to take into account math functions description like 'y equals to x to the power of 2' or 'y equals 3 times x plus 10' and return them translated into math symbols like 'y=x^2' or 'y=3x+10'."

def generate_corrected_transcript(temperature, system_prompt, transcription):

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=temperature,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    )
    return response.choices[0].message.content

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Adjusted for ambient noise. Start speaking.")

        while True:
            try:
                print("Listening...")
                audio = recognizer.listen(source, timeout=5)
                print("Processing...")

                wav_data = io.BytesIO(audio.get_wav_data())

                audio_segment = AudioSegment.from_wav(wav_data)
                audio_segment.export("audio.mp3", format="mp3")

                transcription = recognize_speech_with_openai()

                #Post-processing to translate spelled formulaes to math formulaes
                formula = generate_corrected_transcript(0.1, system_prompt, transcription)


                print("You said: {}".format(formula))

                # Exit loop if the user says "exit"
                if "exit" in transcription.lower():
                    print("Exiting...")
                    break

            except sr.WaitTimeoutError:
                print("Timeout, no speech detected.")
            except sr.UnknownValueError:
                print("Could not understand the audio.")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")

if __name__ == "__main__":
    main()
