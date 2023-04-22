import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import sqlite3 as sq
from numpy import random
import pyglet
import pdb


result = ""

dark_blue = "#1B2A49"
gray_blue = "#465881"
teal_blue = "#00909E"
light_gray = "#C9D1D3"

pyglet.font.add_file("fonts/font_f.ttf")


# app init
root = tk.Tk()
entry_data = tk.StringVar(root)


def get_value():
    return entry_data.get()


root.iconbitmap("image/cn.ico")
root.title("Recipe Manager - מנהל מתכונים")
root.geometry("1200x1000+150+0")


# root[frames]
frame_main = tk.Frame(root, width=1200, height=1000, bg=dark_blue)
frame_main.grid(row=0, column=0, sticky=NSEW)
# frame_main.pack_propagate(False)

# root[frame[header]]
header_container = Canvas(
    frame_main, width=1200, height=120, bg=gray_blue, confine=FALSE)
header_container.grid(row=0, column=0, columnspan=2, sticky=N)
# configuring image for the title
o_image = Image.open("image/cuting_board.png")
photo = ImageTk.PhotoImage(o_image)
# root[frame[header[label.title + label.image]]]
header_title = tk.Label(header_container, image=photo, text="Recipe Manager - מנהל מתכונים", font=(
    "Fredoka bold", 35), compound="center", width=1200, height=120, bg=gray_blue, justify="center")
header_title.grid(row=0)


def search_recipe():
    data = get_value()
    # connection to db
    connection = sq.connect("data/recipe.db")
    cursor = connection.cursor()
    query = "SELECT * FROM recipeDB WHERE name LIKE " + "'%"+data+"%'" + ";"
    cursor.execute(query)
    result = cursor.fetchall()
    print(type(result))  # working!!
    connection.close()
    result_label.configure(text=result[0][1].title(
    ), fg=light_gray, font=("Fredoka bold", 20))


# root[frame[result label]]
result_label = tk.Label(frame_main, font=("Fredoka light", 20), bg=gray_blue,
                        fg=teal_blue, wraplength=FALSE, pady=2, text="Recipe Name - שם המתכון")
result_label.grid(row=2, columnspan=2, padx=30, pady=5, sticky='ew')


# root[frame[text input]]

search_entry = tk.Entry(frame_main, font=(
    "Fredoka light", 20), width=45, textvariable=entry_data)
search_entry.grid(row=1, column=0, pady=10, padx=30, sticky="w")


# root[frame[search button]]
search_button = tk.Button(frame_main, text="Search - חיפוש", font=("Fredoka light", 14), bg=gray_blue, fg=light_gray, compound="left",
                          command=lambda: search_recipe())
search_button.grid(row=1, column=1, pady=10, padx=30, sticky='e')


# get_value()
# pdb.set_trace()

root.mainloop()
