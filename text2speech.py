from openai import OpenAI
#import the library
from playsound import playsound

def read(text):

    client = OpenAI()

    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="onyx",
        input=text,
    ) as response:
        response.stream_to_file("speech.mp3")

    playsound('speech.mp3')

if __name__ == '__main__':
    main()
