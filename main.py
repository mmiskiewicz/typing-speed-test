from tkinter import *
import customtkinter
import random

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

window = customtkinter.CTk()
window.title("Typing Speed Test")
window.geometry("650x420")
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


def countdown(count):
    """Starts countdown from specified value down to 0."""
    label_timer.configure(text=count)

    if count > 0:
        label_timer.after(1000, countdown, count-1)


label_timer = customtkinter.CTkLabel(window, font=("Roboto", 24))
label_timer.grid(column=0, row=0, pady=12, padx=10)

frame = customtkinter.CTkFrame(master=window)
frame.grid(column=0, row=1, pady=60, padx=60)

label_text1 = customtkinter.CTkLabel(frame, wraplength=500, width=500, text=words_list1, font=("Roboto", 24))
label_text1.grid(column=0, row=1)
label_text2 = customtkinter.CTkLabel(frame, wraplength=500, text=words_list2, font=("Roboto", 24))
label_text2.grid(column=0, row=2)
label_text3 = customtkinter.CTkLabel(frame, wraplength=500, text=words_list3, font=("Roboto", 24))
label_text3.grid(column=0, row=3, pady=(0, 12), padx=10)


val = StringVar()
entry_user_text = customtkinter.CTkEntry(window, width=150, height=3, textvariable=val, placeholder_text="Type here...", justify="center")
entry_user_text.grid(column=0, row=4, pady=12, padx=10)

countdown(60)


def callback(*args):
    """Callback to the user input. Updates words."""
    global words_list1, words_list2, words_list3
    if " " in val.get():
        i = callback.counter % 4
        #TODO: call function to compare characters and keep track of score

        # if val.get() == words_list1[i] + " ":
        #     print("all characters are correct")
        #     entry_user_text.delete(0, END)
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
            label_text1.configure(text=words_list1)
            label_text2.configure(text=words_list2)
            label_text3.configure(text=words_list3)


val.trace('w', callback)
callback.counter = 0

window.mainloop()
