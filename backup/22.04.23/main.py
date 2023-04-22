import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import sqlite3 as sq
from numpy import random
import pyglet
from time import sleep
import pdb
import Get_Listbox_pos as glp

user_message1 = 'Press "Save Edit" to add to the recipe'
result = ""
dark_blue = "#1B2A49"
gray_blue = "#465881"
teal_blue = "#7C96AB"
light_gray = "#C9D1D3"

pyglet.font.add_file("fonts/font_f.ttf")

idx_LB_g = int()
ing_current_line_edit = str()
entry_text = str()


def get_value():
    '''used for rading data at any given moment using an avent from the search_entry widget 
    it is being called by the 'data' var that is in the 'search_recipe' method'''
    return entry_data.get()


# app init
root = tk.Tk()

entry_data = tk.StringVar(root)


def clear_SE():
    print('-------------- clear SE ---------------')
    search_entry.delete(0, 'end')


def get_ing_index():
    print('-------------- find Pointer ---------------')
    return ingrediants_LB.curselection()[0]


def edit_recipe():
    print('-------------- Save Edit ---------------edit_recipe')
    entry_text = get_value()
    # if LB whould be distabled ,the LB wont fill up
    ingrediants_LB.configure(state=NORMAL)

    if entry_text == user_message1:  # 1) if user pressed Entr , remove user_message1 from ingrediants_array
        list_ingrediants.pop(-2)
        ingrediants_LB.configure(state=DISABLED)
    else:
        if entry_text not in list_ingrediants:
            list_ingrediants[idx_LB_g] = entry_text
    # ListBox rewrite:
    ingrediants_LB.delete(0, 'end')  # 1) delete all entries
    print('line 56 : list_ingredients :', list_ingrediants)

    for i in range(len(list_ingrediants)):  # 2) fill a entries
        ingrediants_LB.insert(i, list_ingrediants[i])

    ingrediants_LB.bind('<<ListboxSelect>>', copy_LB_selected_to_SE)
    # ingrediants_LB.unbind('<Double-1>')


def delete_LB_line(event):
    print('--------------------Del button pressed  ---------------delete_LB_line')
    i = glp.get_index(event)
    ingrediants_LB.config(state=NORMAL)
    ingrediants_LB.delete(i)
    ingrediants_LB.unbind('<Delete>')
    list_ingrediants.clear()
    for j in range(event.widget.size()):
        list_ingrediants.append(ingrediants_LB.get(j))

    clear_SE()


def edit_LB_line(event):  # Double-1
    print('-------------- Double-1 LB edit ---------------edit_LB_line')
    '''when a list item is selected and double clicked ,the function saves the content of the line to the
    ing_current_line_edit variable'''
    ingrediants_LB.bind('<Delete>', delete_LB_line)

    idx = glp.get_index(event)
    # value of current cell at DoubleClick event
    ing_current_line_edit = ingrediants_LB.get(
        idx)  # finding the double clicked line

    ingrediants_LB.configure(disabledforeground='darkorange')
    ingrediants_LB.config(state=DISABLED)
    instructions_LB.config(state=DISABLED)
    # ingrediants_LB.unbind('<Double-1>')
    # ingrediants_LB.unbind('<<ListboxSelect>>')

    if len(ing_current_line_edit) == 0 and idx == event.widget.size()-1:
        # if double click made on an empty line, new empty line added to the ingerediants_array
        list_ingrediants.insert(-1, '')
        clear_SE()
        search_entry.configure(fg=teal_blue)
        search_entry.focus()
        search_entry.insert(0, user_message1)
    # else:
    #     ingrediants_LB.bind('<Delete>', delete_LB_line)

    global idx_LB_g
    idx_LB_g = idx  # pass index value of LB to global var

    search_button.config(state=DISABLED)
    edit_button.config(state=NORMAL)


def copy_LB_selected_to_SE(event):
    print('-------------- copy LB line to SE---------------')

    event.widget.unbind('<Delete>')
    # 1) clear
    search_entry.delete(0, 'end')
    idx = glp.get_index(event)
    search_entry.insert(0, event.widget.get(idx))
    print('line 112 : idx : ', idx)
    idx_LB_g = idx  # IMPORTANT!!!
    '''
        try:# 2) find LB index
            index = ingrediants_LB.curselection()[0]
        except:
            print("line 105 IndexError: tuple index out of range")
        else: # 3) copy
            search_entry.insert(0, ingrediants_LB.get(index))
            # search_entry.insert(0,ingrediants_LB.get(index))
     '''


root.iconbitmap("image/cn.ico")
root.title("Recipe Manager - מנהל מתכונים")
root.geometry("1200x1000+150+0")
root.columnconfigure(3)


# root[frames]
frame_main = tk.Frame(root, width=1200, height=1000, bg=dark_blue,)
frame_main.grid(row=0, column=0, sticky=NSEW)
frame_main.grid_propagate(FALSE)


# root[frame[header]]
header_container = Canvas(
    frame_main, width=1200, height=120, bg=gray_blue, confine=FALSE)
header_container.grid(row=0, column=0, columnspan=6, sticky='n')
# configuring image for the title
o_image = Image.open("image/cuting_board.png")
photo = ImageTk.PhotoImage(o_image)
# root[frame[header[label.title + label.image]]]
header_title = tk.Label(header_container, image=photo, text="Recipe Manager - מנהל מתכונים", font=(
    "Fredoka bold", 35), compound="center", width=1200, height=120, bg=gray_blue, justify="center")
header_title.grid(row=0, column=0, columnspan=6)


def fill_list_boxes(ingrediants_ordered_array, instructions_ordered_array):
    print('-------------- fill LBoxes---------------')
    '''this function receives an ingredients and instructions arrays and being inserted to the 
    'ingrediants_LB' and 'instruction_list' Listboxes widgets when this function is being called 
    by the 'search_recipe' function
    '''
    ingrediants_LB.delete(0, 'end')
    instructions_LB.delete(0, 'end')

    ing_arr = ingrediants_ordered_array
    ins_arr = instructions_ordered_array
# -------- keeping it neet with shortened var names------------#
    for i in range(len(ing_arr)):
        ingrediants_LB.insert(i, ing_arr[i])
    for i in range(len(ins_arr)):
        instructions_LB.insert(i, ins_arr[i])


def fill_lists(array):
    print('-------------- fill lists---------------fill_lists')
    ''' this function receives an array of raw lists from the ingrediantsDB
    and proccess it in clean in order to divide the lists into two lists,
    the lists being returned , and these returned values are being used by the 
    'search_recipe' function in order to fill the ingrediants and instruction listBoxes
    '''
    global list_ingrediants
    global list_instructions
    ingrediants = []
    list_ingrediants = []
    instructions = []
    list_instructions = []
    # first step is to clean the array from all the NONE values and empty strings while splitting in in half (8 cells in a db record)
    for item in array:
        line = item
        ingrediants_half, instructions_half = line[:4], line[4:]
        for i in range(4):
            if ingrediants_half[i] == "" or ingrediants_half[i] == None:
                pass
            else:
                ingrediants.append(str(ingrediants_half[i]) + " ")
        for i in range(4):
            if instructions_half[i] == "" or instructions_half[i] == None:
                instructions.append(" ")
            else:
                instructions.append(str(instructions_half[i]) + " ")
        ingrediants.pop(0)
        # print(ingrediants) # working!!
        if len(ingrediants) > 0:
            list_ingrediants.append("".join(ingrediants))

            if len(instructions) > 0:
                list_instructions.append("".join(instructions))
        ingrediants.clear()
        instructions.clear()
    # seting up an extra line in the lisbox item for further editing
    list_instructions.append("")
    # seting up an extra line in the lisbox item for further editing
    list_ingrediants.append("")

    return list_ingrediants, list_instructions


def search_recipe():
    print('-------------- search db---------------search_recipe')
    ''' this function retrives raw data from the databases with 2 queries and proccess it for view 
    while calling the 'fill_lists' and the 'fill_lists_boxes' functions and in addition handaling the errors
    occuring by the user    '''
    data = get_value()  # this fuction draws data from the search_entry text
    # connection to db
    if data.isalpha():

        connection = sq.connect("data/recipe.db")
        cursor = connection.cursor()
        query = "SELECT * FROM recipeDB WHERE name LIKE " + "'%"+data+"%'" + ";"
        cursor.execute(query)
        result = cursor.fetchall()

        try:
            print(" line 217 try : ", result[0][0])
        except IndexError:
            print(" line 219 Error occured")
        else:
            query = "SELECT * FROM ingrediantsDB WHERE id = " + \
                str(result[0][0])+";"
            cursor.execute(query)
            ingrediants_array = cursor.fetchall()
            # print("ayya :\n", ingrediants_array) #working!
            # ------------------ values set as two lists and ready to be filled
            ingrediants, instructions = fill_lists(ingrediants_array)

            fill_list_boxes(ingrediants, instructions)
            # in the bottom list boxes!
        connection.close()
        if not result:
            result_label.configure(
                text="No Such Recipe - אין מתכון כזה", fg=light_gray, font=("Fredoka bold", 20))

        else:
            result_label.configure(text=result[0][1].title(),
                                   fg=light_gray, font=("Fredoka bold", 20))

    if data == "":
        result_label.configure(
            text="Please Enter Recipe Name - נא להכניס את שם המתכון", fg=light_gray, font=("Fredoka bold", 20))


# root[frame[result label]]
result_label = tk.Label(frame_main, font=("Fredoka light", 20), bg=gray_blue,
                        fg=teal_blue, wraplength=FALSE, pady=2, text="Recipe Name - שם המתכון")
result_label.grid(row=2, columnspan=6, padx=15, pady=5, sticky='ew')

# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------
# root[frame[text input]]

search_entry = tk.Entry(frame_main, font=(
    "Fredoka light", 20), width=30, textvariable=entry_data)
search_entry.grid(row=1, column=0, columnspan=2, pady=10, padx=15, sticky=W)
# search_entry.bind('<FocusOut>',search_entry_lost_focus)

# root[frame[search button]]
search_button = tk.Button(frame_main, text="Search - חיפוש", font=("Fredoka light", 14), bg=teal_blue, fg=light_gray,
                          command=lambda: search_recipe())
search_button.grid(row=1, column=4, columnspan=2, pady=10, padx=15, sticky=E)

edit_button = tk.Button(frame_main, text="Save Edit - לשמור שינוי",
                        font=("Fredoka bold", 14), bg='darkorange', fg=dark_blue, state=DISABLED, activebackground=light_gray,
                        command=edit_recipe)
edit_button.grid(row=1, column=2, columnspan=2, pady=10, padx=15, sticky=E)

# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------
# root[frame[ingredients label]]
ingrediants_label = tk.Label(frame_main, font=("Fredoka light", 14), bg=gray_blue,
                             fg=light_gray,  text="Ingrediants - מרכיבים")
ingrediants_label.grid(row=3, column=3, columnspan=3,
                       padx=15, pady=10, sticky='ew')

# root[frame[instructions label]]
instructions_label = tk.Label(frame_main, font=("Fredoka light", 14), bg=gray_blue,
                              fg=light_gray,  text="Instructions - הוראות הכנה")
instructions_label.grid(row=3, column=0, columnspan=3,
                        padx=15, pady=10,  sticky='ew')
# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------

# root[frame[ingredients listBox]]
ingrediants_LB = tk.Listbox(frame_main, height=25, font=(
    "Fredoka light", 14), relief='flat', justify="center", background=light_gray, foreground=dark_blue)
ingrediants_LB.grid(row=4, column=3, columnspan=3,
                    sticky='new', pady=5, padx=15)

ingrediants_LB.bind('<<ListboxSelect>>', copy_LB_selected_to_SE)
ingrediants_LB.bind('<Double-1>', edit_LB_line)


# root[frame[instructions listBox]]
instructions_LB = tk.Listbox(frame_main, height=25, font=(
    "Fredoka light", 14), relief='flat', justify="center", background=light_gray, foreground=dark_blue)
instructions_LB.grid(row=4, column=0, columnspan=3,
                     sticky='new', pady=5, padx=15)

instructions_LB.bind('<<ListboxSelect>>', copy_LB_selected_to_SE)
# ingrediants_LB.bind('<Double-1>', edit_LB_line)

# pdb.set_trace()

root.mainloop()
