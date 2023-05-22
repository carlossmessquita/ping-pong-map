from tkinter import *
import random
import time
from PIL import Image, ImageTk

class Game:
    def __init__(self):
        self.root = Tk()
        self.root.title("Ping Pong")
        self.root.resizable(0, 0)
        self.root.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.root, width=800, height=600, bd=0, highlightthickness=0)
        self.canvas.pack()
        background_image_path = "background.png"
        bg_image = Image.open(background_image_path)
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor=NW)
        self.level_label = Label(self.root, text="Qual nível você gostaria de jogar? 1/2/3/4/5", font=("Arial", 20))
        self.level_label.pack()
        self.level_entry = Entry(self.root, font=("Arial", 20))
        self.level_entry.pack()
        self.submit_button = Button(self.root, text="Enviar", font=("Arial", 20), command=self.set_level)
        self.submit_button.pack()
        self.submit_button.bind("<Return>", self.set_level)
        self.count = 0
        self.lost = False
        self.root.mainloop()

    def set_level(self, event=None):
        self.level = int(self.level_entry.get())
        self.length = 500 / self.level
        self.level_label.destroy()
        self.level_entry.destroy()
        self.submit_button.destroy()
        self.init_game()

    def init_game(self):
        self.Barra = Barra(self.canvas, "olive", self.length, self)
        self.Bola = Bola(self.canvas, self.Barra, "white", self)
        self.score_now = self.canvas.create_text(370, 20, text="Você acertou " + str(self.count) + "x", fill="lime", font=("Arial", 20))
        self.game = self.canvas.create_text(400, 300, text=" ", fill="white", font=("Arial", 40))
        self.canvas.bind_all("<Button-1>", self.start_game)
        self.start_game()

    def start_game(self, event=None):
        self.lost = False
        self.count = 0
        self.score()
        self.canvas.itemconfig(self.game, text=" ")
        time.sleep(1)
        self.Barra.draw()
        self.Bola.draw()

    def score(self):
        self.canvas.itemconfig(self.score_now, text="Você acertou " + str(self.count) + "x")

    def game_over(self):
        self.canvas.itemconfig(self.game, text="Game over!")

class Bola:
    def __init__(self, canvas, Barra, color, game):
        self.canvas = canvas
        self.Barra = Barra
        self.game = game
        self.id = canvas.create_oval(0, 0, 15, 15, fill=color)
        self.canvas.move(self.id, 245, 200)

        starts_x = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts_x)

        self.x = starts_x[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)

        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= self.canvas_height:
            self.y = -3
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3

        self.Barra_pos = self.canvas.coords(self.Barra.id)

        if pos[2] >= self.Barra_pos[0] and pos[0] <= self.Barra_pos[2]:
            if pos[3] >= self.Barra_pos[1] and pos[3] <= self.Barra_pos[3]:
                self.y = -3
                self.game.count += 1
                self.game.score()
        if pos[3] <= self.canvas_height:
            self.canvas.after(10, self.draw)
        else:
            self.game.game_over()
            self.game.lost = True


class Barra:
    def __init__(self, canvas, color, length, game):
        self.canvas = canvas
        self.id = self.canvas.create_rectangle(0, 0, length, 10, fill=color)
        self.canvas.move(self.id, 200, 400)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.game = game
        self.canvas.bind_all("<KeyPress-Left>", self.move_left)
        self.canvas.bind_all("<KeyPress-Right>", self.move_right)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        self.pos = self.canvas.coords(self.id)

        if self.pos[0] <= 0:
            self.x = 0
        if self.pos[2] >= self.canvas_width:
            self.x = 0
        if not self.game.lost:
            self.canvas.after(10, self.draw)

    def move_left(self, event):
        if self.pos[0] >= 0:
            self.x = -3

    def move_right(self, event):
        if self.pos[2] <= self.canvas_width:
            self.x = 3


game = Game()
