import tkinter as tk
import speech2text
import text2speech
from openai import OpenAI
import pygame

# Initialize the mixer module
pygame.mixer.init()

client = OpenAI()

class RomanNumberGame:
    def __init__(self, root):
        self.root = root
        elf.root.title("Roman Number Voice Recognition")

        self.label = tk.Label(root, text="Click the button to start learning roman numbers with body voice")
        self.label.pack(pady=10)
        pygame.mixer.music.load("./assets/start.mp3")
        pygame.mixer.music.play()

        self.start_button = tk.Button(root, text="Start", command=self.choose_difficulty, font=('Helvetica', 14))
        self.start_button.pack(pady=10)

        self.number_label = tk.Label(root, text="", font=('Helvetica', 24))
        self.number_label.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=('Helvetica', 14))
        self.result_label.pack(pady=10)

        self.restart_button = tk.Button(root, text="Restart", command=self.restart_game, font=('Helvetica', 14))
        self.restart_button.pack(pady=10)
        self.restart_button.pack_forget()  # Hide the restart button initially

        self.listening_dot = tk.Canvas(root, width=20, height=20, bg='white', highlightthickness=0)
        self.dot = self.listening_dot.create_oval(5, 5, 15, 15, fill='white')
        self.listening_dot.pack(pady=10)
        self.listening_dot.pack_forget()

    def choose_difficulty(self):
        self.start_button.pack_forget()  # Hide the start button
        self.label.config(text="")

        self.easy_label = tk.Label(self.root, text="easy", font=('Helvetica', 20), fg='green')
        self.easy_label.pack(pady=5)
        self.medium_label = tk.Label(self.root, text="medium", font=('Helvetica', 20), fg='yellow')
        self.medium_label.pack(pady=5)
        self.hard_label = tk.Label(self.root, text="hard", font=('Helvetica', 20), fg='red')
        self.hard_label.pack(pady=5)

        text2speech.read("Choose between easy, medium, or hard to set difficulty level")

        self.start_blinking()  # Start blinking the dot
        difficulty = speech2text.listen('difficulty')
        self.stop_blinking()  # Stop blinking the dot

        self.easy_label.pack_forget()
        self.medium_label.pack_forget()
        self.hard_label.pack_forget()

        if difficulty:
            self.start_game(difficulty)
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
        print("Random number is: " + number_to_guess)
        text2speech.read(number_to_guess)

        self.number_label.config(text=number_to_guess, fg="green")

        self.start_blinking()  # Start blinking the dot
        number = speech2text.listen('numbers')
        self.stop_blinking()  # Stop blinking the dot

        if number != 0:
            if number == number_to_guess:
                self.result_label.config(text="Success", fg="green")
                pygame.mixer.music.load("./assets/victory.mp3")
                pygame.mixer.music.play()
            else:
                self.result_label.config(text="Failure", fg="red")
                pygame.mixer.music.load("./assets/defeat.mp3")
                pygame.mixer.music.play()
        else:
            self.result_label.config(text="Failed while listening for the numbers", fg="red")

        self.restart_button.pack(pady=10)  # Show the restart button at the end of the game

    def restart_game(self):
        self.number_label.config(text="")
        self.result_label.config(text="")
        self.label.config(text="Press the button to start the game")
        self.start_button.pack(pady=10)
        self.restart_button.pack_forget()  # Hide the restart button when restarting the game

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

if __name__ == '__main__':
    root = tk.Tk()
    app = RomanNumberGame(root)
    root.mainloop()
