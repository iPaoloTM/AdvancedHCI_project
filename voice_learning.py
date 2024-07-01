import speech2text
import text2speech
from openai import OpenAI

client = OpenAI()

if __name__ == '__main__':

    difficulty = speech2text.listen('difficulty')

    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": '''You are a helpful AI assistant that generate one random roman number based on difficulty level:
                                         - if the requested level is easy, generate a roman number from this set {I,V,X,L,C,D,M}
                                         - if the requested level is medium, generate a roman number from this set {I,II,III,IV,V,VI,VII,VIII,IX,X}
                                         - if the requested level is hard, generate whatever string represeting a random roman nmber.
                                         You anser with one and only one number selected according to the difficulty level.
                                         Only answers with the generated number, exclude everything else.'''},
        {"role": "user", "content": difficulty},
      ]
    )

    number_to_guess=response.choices[0].message.content
    print("Random number is: "+number_to_guess)

    number = speech2text.listen('numbers')

    if number!=0:

        print("Success" if (number==number_to_guess) else "Failure")
    else:
        print("Failed while listening for the numbers")
