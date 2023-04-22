
def get_index(event):
    index=0
    try:
        event.widget.curselection()[0]
    except:
        print("index out of range , sorry!")
    else:
        index = event.widget.curselection()[0]

    return index
