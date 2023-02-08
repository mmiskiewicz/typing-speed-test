from tkinter import *
import customtkinter
import random
from tkinter import messagebox

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

window = customtkinter.CTk()
window.title("Typing Speed Test")
window.geometry("640x260")
window.resizable(False, False)
timer = 60

words = open('common_words.txt').read().splitlines()
words_list1, words_list2, words_list3, words_list4 = [], [], [], []


def generate_words(words_list):
    """Generates random words."""
    words_list.clear()
    for i in range(4):
        word = random.choice(words)
        if len(words_list) < 4:
            words_list.append(word)
    return words_list


words_list1 = generate_words(words_list1)
words_list2 = generate_words(words_list2)
words_list3 = generate_words(words_list3)
previous_word = ""


def countdown(count):
    """Starts countdown from specified value down to 0."""
    global cpm, wpm, words_list1, words_list2, words_list3
    label_timer.configure(text=count)

    if count > 0:
        label_timer.after(1000, countdown, count-1)
    else:
        messagebox.showinfo(title="Empty file name", message=f"Your CPM: {cpm}, wpm: {wpm/5}")
        cpm = 0
        wpm = 0
        callback.counter = 0
        words_list1 = generate_words(words_list1)
        words_list2 = generate_words(words_list2)
        words_list3 = generate_words(words_list3)
        label_text1a.configure(text=words_list1[0])
        label_text1b.configure(text=" " + " ".join(words_list1[1:]))
        label_text2.configure(text=words_list2)
        label_text3.configure(text=words_list3)
        entry_user_text.delete(0, END)
        countdown(60)


label_timer = customtkinter.CTkLabel(window, font=("Roboto", 40))
label_timer.grid(column=0, row=0, pady=12, padx=10)

frame = customtkinter.CTkFrame(master=window)
frame.grid(column=0, row=1, pady=(0, 10), padx=60)

label_text1a = customtkinter.CTkLabel(frame, text=words_list1[0], font=("Roboto", 24), bg_color='#3E4149')
label_text1a.grid(column=0, row=1, sticky='e')
label_text1b = customtkinter.CTkLabel(frame, text=" " + " ".join(words_list1[1:]), font=("Roboto", 24))
label_text1b.grid(column=1, row=1, sticky='w')
label_text2 = customtkinter.CTkLabel(frame, wraplength=500, text=words_list2, font=("Roboto", 24))
label_text2.grid(column=0, row=2, columnspan=2)
label_text3 = customtkinter.CTkLabel(frame, width=500, wraplength=500, text=words_list3, font=("Roboto", 24))
label_text3.grid(column=0, row=3, pady=(0, 12), padx=10, columnspan=2)

val = StringVar()
entry_user_text = customtkinter.CTkEntry(window, width=150, height=3, textvariable=val, placeholder_text="Type here...", justify="center")
entry_user_text.grid(column=0, row=4, pady=12, padx=10)

countdown(60)

cpm = 0
wpm = 0


def compare_characters(i):
    global cpm, wpm, previous_word
    if len(val.get()) - 1 > len(previous_word):
        for j in range(len(previous_word)):
            cpm += 1
            if val.get()[j] == previous_word[j]:
                wpm += 1
    else:
        for j in range(len(val.get()) - 1):
            cpm += 1
            # print(val.get()[j])
            if val.get()[j] == previous_word[j]:

                wpm += 1
    # print(f"cpm {cpm}")
    # print(f"wpm {wpm}")


def callback(*args):
    """Callback to the user input. Updates words."""
    global words_list1, words_list2, words_list3, previous_word
    if " " in val.get():
        previous_word = words_list1[0]
        if len(words_list1) > 1:
            words_list1.pop(0)
            label_text1a.configure(text=words_list1[0])
            label_text1b.configure(text=" " + " ".join(words_list1[1:]))
        i = callback.counter % 4
        compare_characters(i)
        callback.counter += 1
        entry_user_text.delete(0, END)
        if callback.counter % 4 == 0 and callback.counter != 0:
            words_list1.clear()
            words_list1.extend(words_list2)
            words_list2.clear()
            words_list2.extend(words_list3)
            words_list3 = generate_words(words_list3)
            words_list4.clear()
            words_list4.extend(words_list3)
            label_text1a.configure(text=words_list1[0])
            label_text1b.configure(text=" " + " ".join(words_list1[1:]))
            label_text2.configure(text=words_list2)
            label_text3.configure(text=words_list3)


val.trace('w', callback)
callback.counter = 0

window.mainloop()
