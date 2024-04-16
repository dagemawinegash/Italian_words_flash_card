from tkinter import *
from tkinter import messagebox
import pandas
import random
import pygame
import os

pygame.mixer.init()
clock_tick_sound = pygame.mixer.Sound("Sound/ticking-clock.wav")
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
BACKGROUND_MUSIC = "Sound/background music.mp3"
global counter


def play_clock_tick_sound():
    pygame.mixer.Channel(0).play(clock_tick_sound, loops=-1)


def stop_clock_tick_sound():
    pygame.mixer.Channel(0).stop()


def start_timer():
    global flip_timer, counter
    counter = 5
    update_counter_label()
    flip_timer = window.after(1000, countdown)
    play_clock_tick_sound()


def countdown():
    global counter
    counter -= 1
    update_counter_label()
    if counter > 0:
        window.after(1000, countdown)
    else:
        flip_card()


def stop_timer():
    window.after_cancel(flip_timer)
    stop_clock_tick_sound()
    update_counter_label(reset=True)


def update_counter_label(reset=False):
    if reset:
        counter_label.config(text="")
    else:
        counter_label.config(text=f"Next flip in {counter} seconds")


try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/Italian Words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="Italian", fill="black")
    canvas.itemconfig(card_word, text=current_card["Italian"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    start_timer()


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)
    stop_timer()


def is_known():
    if len(to_learn) > 1:
        to_learn.remove(current_card)
        data = pandas.DataFrame(to_learn)
        data.to_csv("data/words_to_learn.csv", index=False)
        stop_timer()
        next_card()
    else:
        messagebox.showinfo(title="Success!!", message="You have memorized all the words!!")
        os.remove("data/words_to_learn.csv")


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(5000, func=flip_card)
pygame.mixer.music.load(BACKGROUND_MUSIC)
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(loops=-1)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "normal"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

counter_label = Label(text="", font=("Arial", 16, "bold"), bg=BACKGROUND_COLOR, fg="gray")
counter_label.grid(row=1, column=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=2, column=0)

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=2, column=1)

next_card()

window.mainloop()
