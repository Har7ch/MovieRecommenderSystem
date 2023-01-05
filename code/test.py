import re
import tkinter.messagebox
from tkinter.tix import IMAGETEXT
import webbrowser
import pygame
import time
from functools import partial
from tkinter import BOTH, END, LEFT, Button, Canvas, Checkbutton, Frame, IntVar, Label, Menu, PhotoImage, Scrollbar, Text, Tk, ttk
import content as ims
import content1 as ims1
from PIL import ImageTk, Image
from tkinter import *


def Exit(option):
    if option == 'quit':
        time.sleep(0.3)
        root.destroy()

def open_popup():
    tkinter.messagebox.showinfo('How it Works?', 'Using Cosine Similarity on IMDb dataset!')



def update_values():
    """
    :return: None
    Updates the content in the dropdown menu based on the keyword entered in the text field.
    """
    filter_str = combo1.get().lower()
    filter_str = ' '.join([word for word in re.split(r'\s+', filter_str) if word != ''])  # handling white space
    # if no input is provided show the entire database
    if filter_str == '':
        combo1['values'] = movie_data
    # else filter based on the input
    else:
        filtered_list_1 = []  # holds values that starts with the input string
        filtered_list_2 = []  # holds values that matches the input pattern in the database
        for value in movie_data:
            if value.lower().startswith(filter_str):
                filtered_list_1.append(value)
            elif filter_str in value.lower():
                filtered_list_2.append(value)
        combo1['values'] = filtered_list_1 + filtered_list_2  # so that values of filtered_list_1 appear first



def get_text(event=None):
    """
    :param event: None
    :return: None
    Gets the recommendations and shows it in a text widget.
    """
    text_widget = Text(frame, font='Courier 13 italic', cursor='arrow', bg='yellow', height=11, width=60)
 
    text_widget.tag_configure('tag-center', justify='center')
    text_widget.tag_configure('tag-left', justify='left')
    query = combo1.get()  # get input from combo widget
    query = ' '.join([word for word in re.split(r'\s+', query) if word != ''])  # handling white space
    text = ims.recommend(query)
    if text is None:  # if the movie/tv show not found print some tips
        text = "Item not found!\n"
        text_widget.insert(1.0, text, 'tag-center')
        text_widget.insert(END, '\nYou can try the following:\n\n 1. Enter keywords and choose from dropdown menu.\n '
                                '2. Check for typos.', 'tag-left')
    else:  # if found iterate over the DataFrame to create hyperlinks in the text widget
        text_widget.delete(1.0, END)  # clear previous entries
        idx = 0
        text_widget.insert(END,"Your's top recommendations for the movie:" + text[0])
        for title in text:  # iterating over the DataFrame as tuples
            if idx != 0 : 
                text_widget.insert(END, str(idx) + '. ' + title) # insert hyperlinks in the
            # widget
            if idx != 10:  # if not the last index, insert a new line after the previous entry
                text_widget.insert(END, '\n')
                text_widget.insert(END, '\n')
            idx = idx + 1
    text_widget.config(highlightcolor='black', highlightbackground="black", highlightthickness=2)
    text_widget.place(x=185, y=310)
    # adding scrollbar to the text widget
    scroll_y = Scrollbar(text_widget, orient='vertical', command=text_widget.yview)
    scroll_y.place(x=185*3 + 30, relheight=1)
    text_widget.configure(state='disabled', yscrollcommand=scroll_y.set)  # making the text widget un-editable


root = Tk()
root.title("Movie Recommender System(GUI)")
root.geometry('960x720')
root.resizable(width=False,height=False)


#background image:
# creating menu widget
menu = Menu(root)
helpMenu = Menu(menu, tearoff=0, postcommand=partial(Exit, 'menu_bar'), font='Courier 11', bg='burlywood2',activebackground='black', activeforeground='white')
menu.add_cascade(label='Menu', menu=helpMenu)
helpMenu.add_command(label='How it Works?', command=open_popup)
helpMenu.add_separator()
helpMenu.add_command(label='Exit', command=partial(Exit, 'quit'))

bg_image = PhotoImage(file=r'bg_pic.png')
bg_label = Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

frame1 = Frame(root,height=7,width=200)
frame1_label = Label(frame1,bg = 'yellow')
frame1_label.pack()
# def selection():
#    selected = (radio.get())
# radio = IntVar()
# r1 = Radiobutton(frame1, text="Popularity-based", variable=radio, value=1, command=selection).pack("left")
# r2 = Radiobutton(frame1,text="Content-based",variable=radio,value=2,command=selection).pack("left")



frame = Frame(root, height=500, width=750, bg='black').place(x=150, y=75)
frame_bg_image = PhotoImage(file=r'bg_pic.png')
frame_label = Label(frame, image=bg_image)
frame_label.pack()


label1 = Label(frame, font='Courier 13 italic', text='Select a Movie!', height=2, width=65,bg='SlateBlue2', highlightthickness=2, highlightbackground="black")
movie_data = ims.get_movies_data()
combo1 = ttk.Combobox(frame, width=55, font=("Courier", 13), postcommand=update_values, values=movie_data)
button1 = Button(frame, text='SEARCH!', font='Arial 13 bold italic', bg='#e50914', width=35, command=get_text)
instructions_text = Text(frame, font='Courier 13 italic', cursor='arrow', bg='burlywood2', height=11, width=60)

instructions_text.tag_configure('tag-center', justify='center')
instructions_text.tag_configure('tag-center-underline', justify='center', underline=1)
instructions_text.tag_configure('tag-left', justify='left')
instructions_text.insert(1.0, 'Welcome to my recommendation system!\n', 'tag-center')
instructions_text.insert(END, "\nInstructions\n", 'tag-center-underline')
instructions_text.insert(END, "\n 1. Enter the keywords of a TV Show/Movie/Documentary. \n 2. Select from the "
                              "dropdown menu. \n 3. Press ENTER or 'GO!' to search.", 'tag-left')


instructions_text.config(highlightcolor='black', highlightbackground="black", highlightthickness=2)
instructions_text.place(x=185, y=310)
instructions_text.configure(state='disabled')
label1.place(x=150, y=150)
root.option_add('*TCombobox*Listbox.font', ("Courier", 13))
root.config(menu=menu)
combo1.place(x=200, y=213, height=32)
button1.place(x=300, y=260)
combo1.bind('<Return>', get_text)


# main loop
if __name__ == '__main__':
    root.mainloop()