import tkinter as tk
from tkinter import messagebox
import pose
import speech2text
import text2speech
from openai import OpenAI
import pygame
import threading
import time
import GUI1
import GUI2

client = OpenAI()

pygame.mixer.init()

class RomanNumberMainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("aHCI - ROMAN NVMBERS RALLY")
        self.root.geometry("900x900")
        self.root.config(bg="#c4b59b")  # Background color similar to the Colosseum

        self.font_family = 'Trajan Pro'  # Set the font to Trajan Pro or similar

        self.label = tk.Label(root, text="ROMAN NVMBERS RALLY", bg="#c4b59b", fg="#282c34", font=(self.font_family, 22, 'bold'))
        self.label.pack(pady=50)

        self.label2 = tk.Label(root, text="To start learning, click the button!", bg="#c4b59b", fg="#282c34", font=(self.font_family, 18, 'bold'))
        self.label2.pack(pady=20)

        pygame.mixer.music.load("./assets/start.mp3")
        pygame.mixer.music.play()

        self.start_button = tk.Button(root, text="START", command=self.choose_difficulty, bg="#c4b59b", fg="#282c34", font=(self.font_family, 14, 'bold'))
        self.start_button.pack(pady=10)

        self.restart_button = tk.Button(root, text="RESTART", command=self.restart_game, bg="#e5c07b", fg="#282c34", font=(self.font_family, 14, 'bold'))
        self.restart_button.pack(pady=10)
        self.restart_button.pack_forget()  # Hide the restart button initially


    def choose_difficulty(self):
        self.start_button.pack_forget()  # Hide the start button
        self.label2.pack_forget()
        self.label.config(text="Choose between Body or Voice mode!")

        text2speech.read("Choose between Body or Voice mode!")

        choice = speech2text.listen("start")

        if choice=='body':
            GUI1.start()
        elif choice=='voice':
            GUI2.start()
        else:
            exit()

        self.restart_button.pack(pady=10)

    def restart_game(self):
        self.label.config(text="Press the button to start the game")
        self.start_button.pack(pady=10)




if __name__ == '__main__':
    root = tk.Tk()
    app = RomanNumberMainApp(root)
    root.mainloop()
