import tkinter as tk
from tkinter import messagebox
import pose
import speech2text
import text2speech
from openai import OpenAI
import pygame
import threading
import time

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
        self.root.title("aHCI - ROMAN NVMBERS RALLY")
        self.root.geometry("900x900")
        self.root.config(bg="#c4b59b")  # Background color similar to the Colosseum

        self.font_family = 'Trajan Pro'  # Set the font to Trajan Pro or similar

        self.label = tk.Label(root, text="ROMAN NVMBERS RALLY", bg="#c4b59b", fg="#282c34", font=(self.font_family, 22, 'bold'))
        self.label.pack(pady=50)

        self.label2 = tk.Label(root, text="To start posing, click the button!", bg="#c4b59b", fg="#282c34", font=(self.font_family, 18, 'bold'))
        self.label2.pack(pady=20)

        # pygame.mixer.music.load("./assets/start.mp3")
        # pygame.mixer.music.play()

        self.start_button = tk.Button(root, text="START", command=self.choose_difficulty, bg="#c4b59b", fg="#282c34", font=(self.font_family, 14, 'bold'))
        self.start_button.pack(pady=10)

        self.number_label = tk.Label(root, text="", font=(self.font_family, 40, 'bold'), bg="#c4b59b", fg="#8c7b75")
        self.number_label.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=(self.font_family, 22, 'bold'), bg="#c4b59b", fg="#e06c75")
        self.result_label.pack(pady=10)

        self.correct_number_label = tk.Label(root, text="", font=(self.font_family, 40, 'bold'), bg="#c4b59b", fg="#8c7b75")
        self.correct_number_label.pack(pady=10)

        self.restart_button = tk.Button(root, text="RESTART", command=self.restart_game, bg="#e5c07b", fg="#282c34", font=(self.font_family, 14, 'bold'))
        self.restart_button.pack(pady=10)
        self.restart_button.pack_forget()  # Hide the restart button initially

        self.end_button = tk.Button(root, text="END", command=self.end_game, bg="#e5c07b", fg="#282c34", font=(self.font_family, 14, 'bold'))
        self.end_button.pack(pady=10)
        self.end_button.pack_forget()  # Hide the restart button initially

        self.listening_dot = tk.Canvas(root, width=20, height=20, bg='white', highlightthickness=0)
        self.dot = self.listening_dot.create_oval(5, 5, 15, 15, fill='white')
        self.listening_dot.pack(pady=10)
        self.listening_dot.pack_forget()

    def choose_difficulty(self):
        self.start_button.pack_forget()  # Hide the start button
        self.label2.pack_forget()
        self.label.config(text="Choose difficulty")

        self.easy_label = tk.Label(self.root, text="easy", font=(self.font_family, 40), fg='white', bg="green")
        self.easy_label.pack(pady=5)
        self.medium_label = tk.Label(self.root, text="medivm", font=(self.font_family, 40), fg='white', bg="yellow")
        self.medium_label.pack(pady=5)
        self.hard_label = tk.Label(self.root, text="hard", font=(self.font_family, 40), fg='white', bg="red")
        self.hard_label.pack(pady=5)

        threading.Thread(target=self.capture_difficulty).start()

    def capture_difficulty(self):
        text2speech.read("Choose between easy, medium, or hard to set difficulty level")
        self.start_blinking()  # Start blinking the dot

        difficulty = speech2text.listen('difficulty')
        self.stop_blinking()  # Stop blinking the dot

        self.easy_label.pack_forget()
        self.medium_label.pack_forget()
        self.hard_label.pack_forget()

        if difficulty:
             self.root.after(0, lambda: self.start_game(difficulty))
        else:
            self.label.config(text="Failed to capture difficulty. Please try again.")
            self.start_button.pack(pady=10)

    def start_game(self, difficulty):

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": '''You are a helpful AI assistant that generates one random roman number based on difficulty level:
                                                 - if the requested level is easy, generate a roman number from this set {I,V,X,L,C,D,M}
                                                 - if the requested level is medium, generate a roman number from this set {I,II,III,IV,V,VI,VII,VIII,IX,X}
                                                 - if the requested level is hard, generate whatever string representing a random roman number.
                                                 You answer with one and only one number selected according to the difficulty level'''},
                {"role": "user", "content": difficulty},
            ]
        )

        number_to_guess = response.choices[0].message.content

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": '''You are able to translate Roman numbers into Normal Numbers: e.g. if you receive L you answer 50, if you receive VI you answer 6 and so on.
                                                 You answer only and only with the translated number. Like 6,7 or 100, nothing else.'''},
                {"role": "user", "content": number_to_guess},
            ]
        )

        translated_number = response.choices[0].message.content



        self.number_label.config(text=translated_number+" ", fg="#8c7b75")

        print("Random number is: " + translated_number)
        text2speech.read("Pose like the Roman number " + translated_number)

        self.label.config(text="Pose like the nvmber!")

        time.sleep(2)

        poses = []

        if number_to_guess != '0':
            for x in number_to_guess:
                poses.append(pose.findLetter(7))

            combined_string = "".join(poses)
            self.display_result(combined_string, number_to_guess)
        else:
            self.display_result("error", number_to_guess)

    def display_result(self, result, number_to_guess):
        self.label.config(text="RESVLTS")
        self.number_label.config(text=number_to_guess, fg="#8c7b75")

        if result == number_to_guess:
            self.result_label.config(text="Success", fg='white', bg="green")
            pygame.mixer.music.load("./assets/victory.mp3")
            pygame.mixer.music.play()
            text2speech.read("Grrreat!")
        else:
            self.result_label.config(text="Failure", fg='white', bg="red")
            pygame.mixer.music.load("./assets/defeat.mp3")
            pygame.mixer.music.play()
            text2speech.read("The correct answer was " + number_to_guess + "! Better luck next time!")

        self.restart_button.pack(pady=10)  # Show the restart button at the end of the game
        self.end_button.pack(pady=10)  # Show the end button at the end of the game

    def restart_game(self):
        self.number_label.config(text="")
        self.result_label.config(text="")
        self.number_label.config(text="")
        self.label.config(text="Press the button to start the game")
        self.start_button.pack(pady=10)
        self.restart_button.pack_forget()  # Hide the restart button when restarting the game
        self.end_button.pack_forget()

    def end_game(self):
        exit()

    def start_blinking(self):
        self.listening_dot.pack(pady=10)
        self.blinking = True
        self.blink()

    def stop_blinking(self):
        self.blinking = False
        self.listening_dot.pack_forget()

    def blink(self):
        if self.blinking:
            current_color = self.listening_dot.itemcget(self.dot, 'fill')
            new_color = 'green' if current_color == 'white' else 'white'
            self.listening_dot.itemconfig(self.dot, fill=new_color)
            self.root.after(500, self.blink)


def start():
    root = tk.Tk()
    app = RomanNumberApp(root)
    root.mainloop()
