import tkinter as tk
from tkinter import messagebox
import pose
import speech2text
import text2speech
from openai import OpenAI
import pygame

client = OpenAI()

pygame.mixer.init()

def get_random_roman_number():
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.1,
        messages=[
            {
                "role": "system",
                "content": "You are an expert in roman numbers and you generate random roman numbers like 'VII', 'XI', 'MMXX' etc. You reply ONLY AND ONLY with the random roman number itself."
            },
            {
                "role": "user",
                "content": "Give me a random roman number between I and X"
            }
        ]
    )

    result = response.choices[0].message.content

    print(f"Generated roman number: {response.choices[0].message.content}")
    text2speech.read(f"Generated roman number is {result}")

    return result

class RomanNumberApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Roman Number Pose Recognition")

        self.label = tk.Label(root, text="Click the button to start learning roman numbers with body poses")
        self.label.pack(pady=10)
        pygame.mixer.music.load("./assets/start.mp3")
        pygame.mixer.music.play()

        self.start_button = tk.Button(root, text="Start", command=self.start_game)
        self.start_button.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=('Helvetica', 14))
        self.result_label.pack(pady=10)

        self.result_text = tk.Text(root, height=10, width=50)
        self.result_text.pack(pady=10)

        self.restart_button = tk.Button(root, text="Restart", command=self.restart_game, font=('Helvetica', 14))
        self.restart_button.pack(pady=10)
        self.restart_button.pack_forget()  # Hide the restart button initially

    def start_game(self):
        number = get_random_roman_number()

        self.result_text.insert(tk.END, f"Generated Number: {number}\n")

        poses = []

        if number != '0':
            for x in number:
                poses.append(pose.findLetter(5))

            combined_string = "".join(poses)
            self.display_result(combined_string, number)
        else:
            self.display_result("error", number)

    def display_result(self, result, generated_number):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"\nRecognized Number: {result}")

        if result == generated_number:
            self.result_label.config(text="Success", fg="green")
            pygame.mixer.music.load("./assets/victory.mp3")
            pygame.mixer.music.play()
        else:
            self.result_label.config(text="Failure", fg="red")
            pygame.mixer.music.load("./assets/defeat.mp3")
            pygame.mixer.music.play()

        self.restart_button.pack(pady=10)  # Show the restart button at the end of the game

    def restart_game(self):
        self.result_label.config(text="")
        self.result_text.insert("")
        self.label = tk.Label(root, text="Click the button to start learning roman numbers with body poses")
        self.start_button.pack(pady=10)
        self.restart_button.pack_forget()  # Hide the restart button when restarting the game


if __name__ == '__main__':
    root = tk.Tk()
    app = RomanNumberApp(root)
    root.mainloop()
