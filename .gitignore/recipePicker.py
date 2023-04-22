import tkinter as tk
from PIL import ImageTk
import sqlite3
from numpy import random
import pyglet

bg_color = "#7D6aee"

pyglet.font.add_file("fonts/Shanti-Regular.ttf")
pyglet.font.add_file("fonts/Ubuntu-Bold.ttf")


def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def fetch_db():
    connection = sqlite3.connect("data/recipes.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sqlite_schema WHERE type = 'table';")
    all_tables = cursor.fetchall()

    idx = random.randint(0, len(all_tables)-1)

    table_name = all_tables[idx][1]
    cursor.execute("SELECT * FROM " + table_name + ";")
    table_records = cursor.fetchall()

    connection.close()
    return table_name, table_records


def pre_process(table_name, table_records):
    # ----title------
    title = table_name[:-6]
    title = "".join([char if char.islower() else " " + char for char in title])
    ingrediants = []
# ----ingrediants---

    for record in table_records:
        name = record[1]
        qty = record[2]
        unit = record[3]
        if not unit:
            ingrediants.append(qty + " " + "units" + " of " + name)
        elif not unit and not qty:
            rnd_phrase = random.choice("Some ", "A bit of ", "A little of ")
            ingrediants.append(rnd_phrase + name)
        else:
            ingrediants.append(qty + " " + unit + " of " + name)

    return title, ingrediants


def load_frame1():
    clear_widgets(frame2)
    frame1.tkraise()
    frame1.pack_propagate(False)
    # frame widjets
    logo_img = ImageTk.PhotoImage(file="assets/RRecipe_logo.png")
    logo_widget = tk.Label(frame1, image=logo_img, bg=bg_color)
    logo_widget.image = logo_img
    logo_widget.pack()

    tk.Label(frame1, text="Ready for your Random Recipe?",
             bg=bg_color, fg='white', font=("TkMenuFont", 14)).pack()

    # button widget
    tk.Button(frame1, text="Shuffle", font=("Ubuntu", 20), bg="#233954", fg="white", cursor="hand2",
              activebackground="#badee2", activeforeground="black", command=lambda: load_frame2()).pack(pady=20)


def load_frame2():
    clear_widgets(frame1)
    frame2.tkraise()
    table_name, table_records = fetch_db()
    title, ingrediants = pre_process(table_name, table_records)

    # logo widget
    logo_img = ImageTk.PhotoImage(file="assets/RRecipe_logo_bottom.png")
    logo_widget = tk.Label(frame2, image=logo_img, bg=bg_color)
    logo_widget.image = logo_img
    logo_widget.pack(pady=20)

    #
    tk.Label(frame2, text=title,
             bg=bg_color, fg='white', font=("Ubuntu", 20)).pack(pady=25)
    for i in ingrediants:
        tk.Label(frame2, text=i,
                 bg="#2839a1", fg='white', font=("Shanti", 12)).pack(fill="both")
    # button widget
    tk.Button(frame2, text="back", font=("Shanti", 14), bg="#233954", fg="white", cursor="hand2",
              activebackground="#badee2", activeforeground="black", command=lambda: load_frame1()).pack(pady=20)


# initialize app
root = tk.Tk()
root.title("Recipe Picker")
root.eval("tk::PlaceWindow . center")  # allows to write TCL programing syntex
# x = root.winfo_screenwidth()//3
# y = int(root.winfo_screenheight() * 0.1)
# root.geometry('500x600+' + str(x) + '+' + str(y))
frame1 = tk.Frame(root, width=500, height=600, bg=bg_color)
frame2 = tk.Frame(root,  bg=bg_color)


for frame in (frame1, frame2):
    frame.grid(row=0, column=0, sticky="nesw")

# run app
load_frame1()
root.mainloop()
