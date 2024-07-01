
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

system_prompt_numbers = '''
                        You help in teaching Roman numbers. Your task is to take into account numbers from the user and traduce them into roman numbers, like '17' becomes 'XVII' and '10' becomes 'X' or '2020' becomes 'MMXX' and so on.
                        You only and only reply with the Roman number you traduced. Try your best to understand the number pronounced. Ignore everything that is not a number.
                        '''
system_prompt_difficulty = '''
                            You are a helpful assistant that recognises three words 'Easy','Medium', or 'Hard'. If you don't understand something, return 'Easy'. Ignore everything else.
                            '''

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

def listen(mode):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    if mode=='numbers':
        system_prompt=system_prompt_numbers
    elif mode=='difficulty':
        system_prompt=system_prompt_difficulty

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Adjusted for ambient noise. Start speaking.")

        try:
            print("Listening...")
            audio = recognizer.listen(source, timeout=5)
            print("Processing...")

            wav_data = io.BytesIO(audio.get_wav_data())

            audio_segment = AudioSegment.from_wav(wav_data)
            audio_segment.export("audio.mp3", format="mp3")

            transcription = recognize_speech_with_openai()

            #Post-processing to translate spelled numbers to roman numbers
            number = generate_corrected_transcript(0.1, system_prompt, transcription)

            print("You said: {}".format(number))

            # Exit loop if the user says "exit"
            # if "exit" in transcription.lower():
            #     print("Exiting...")
            #     break

        except sr.WaitTimeoutError:
            print("Timeout, no speech detected.")
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

        return number
