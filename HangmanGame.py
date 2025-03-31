from tkinter import Tk, Canvas, Button
import random

word_list = [
    'transmission', 'clutch', 'engine', 'windshield', 'fender', 
    'exhaust', 'suspension', 'catalytic converter', 'chassis',  
    'differential', 'alternator', 'gasket', 'piston', 'battery', 
    'crankshaft', 'hood', 'muffler', 'door', 'tire', 'axle', 
    'horn', 'wheel', 'radiator'
]

class HangmanGame:
    def __init__(self, master):
        self.master = master
        master.title("Hangman")
        master.geometry("1280x720")
        master.resizable(False, False)

        self.selected_word = random.choice(word_list).lower()
        self.guessed_letters = []
        self.remaining_guesses = 7
        self.display_word = ['_'] * len(self.selected_word)
        self.buttons = []

        self.canvas = Canvas(master, bg="#FFFFFF", height=720, width=1280)
        self.canvas.pack()

        # Hangman figure display
        self.hangman_lines = []
        for i in range(6):
            line = self.canvas.create_text(100, 150 + i*30, text="", 
                                         anchor="nw", font=("Courier New", 14))
            self.hangman_lines.append(line)
        self.update_hangman(0)

        # Game text elements
        self.canvas.create_text(640, 50, text="Hangman", 
                              font=("Arial", 64), fill="#000000")
        
        self.word_display = self.canvas.create_text(640, 300, 
                                                  text=" ".join(self.display_word),
                                                  font=("Arial", 48), fill="#CB8C8C")
        
        self.guesses_display = self.canvas.create_text(100, 100, 
                                                     text=f"Guesses left: {self.remaining_guesses}",
                                                     font=("Arial", 24), anchor="nw")

        self.create_buttons()

    def create_buttons(self):
        keyboard_layout = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
        ]

        for row_idx, row in enumerate(keyboard_layout):
            for col_idx, letter in enumerate(row):
                btn = Button(self.master, text=letter, width=4, height=2,
                           command=lambda l=letter: self.guess_letter(l),
                           font=("Arial", 14))
                x_base = 400 if row_idx == 0 else 425 if row_idx == 1 else 455
                btn.place(x=x_base + col_idx*55, y=450 + row_idx*50)
                self.buttons.append(btn)

    def update_hangman(self, stage):
        hangman_stages = [
            [
                "  __________",
                " |",
                " |",
                " |",
                " |",
                "_|_"
            ],
            [
                "  __________",
                " |          |",
                " |",
                " |",
                " |",
                "_|_"
            ],
            [
                "  __________",
                " |          |",
                " |          O",
                " |",
                " |",
                "_|_"
            ],
            [
                "  __________",
                " |          |",
                " |          O",
                " |          |",
                " |",
                "_|_"
            ],
            [
                "  __________",
                " |          |",
                " |          O",
                " |         /|",
                " |",
                "_|_"
            ],
            [
                "  __________",
                " |          |",
                " |          O",
                " |         /|\\",
                " |",
                "_|_"
            ],
            [
                "  __________",
                " |          |",
                " |          O",
                " |         /|\\",
                " |         /",
                "_|_"
            ],
            [
                "  __________",
                " |          |",
                " |          O",
                " |         /|\\",
                " |         / \\",
                "_|_"
            ]
        ]
        
        current_stage = hangman_stages[stage]
        for i in range(6):
            self.canvas.itemconfig(self.hangman_lines[i], text=current_stage[i])

    def guess_letter(self, letter):
        letter_lower = letter.lower()
        if letter_lower in self.guessed_letters:
            return

        button_index = [btn['text'] for btn in self.buttons].index(letter)
        self.buttons[button_index].config(state="disabled")
        self.guessed_letters.append(letter_lower)

        if letter_lower in self.selected_word:
            new_display = [char.upper() if letter_lower == char else self.display_word[i] 
                         for i, char in enumerate(self.selected_word)]
            self.display_word = new_display
            self.canvas.itemconfig(self.word_display, text=" ".join(self.display_word))
            
            if "_" not in self.display_word:
                self.canvas.itemconfig(self.word_display, text="YOU WIN!", fill="green")
                self.disable_all_buttons()
        else:
            self.remaining_guesses -= 1
            stage = 7 - self.remaining_guesses
            self.update_hangman(stage)
            self.canvas.itemconfig(self.guesses_display, 
                                text=f"Guesses left: {self.remaining_guesses}")

            if self.remaining_guesses <= 0:
                self.canvas.itemconfig(self.word_display, 
                                     text=f"Game Over! Word: {self.selected_word.upper()}", 
                                     fill="red")
                self.disable_all_buttons()

    def disable_all_buttons(self):
        for btn in self.buttons:
            btn.config(state="disabled")

if __name__ == "__main__":
    root = Tk()
    game = HangmanGame(root)
    root.mainloop()