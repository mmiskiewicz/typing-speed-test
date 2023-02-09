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
words = open('common_words.txt').read().splitlines()
words_list1, words_list2, words_list3 = [], [], []
# CPM - Correct Characters Per Minute
# WPM - Correct Words Per Minute (CPM / 5)
cpm, wpm = 0, 0


def generate_words(words_list):
    """Generates random words."""
    words_list.clear()
    # Generates 4 random words in a single line.
    for i in range(4):
        word = random.choice(words)
        if len(words_list) < 4:
            words_list.append(word)
    return words_list


def countdown(count):
    """Starts countdown from specified value down to 0."""
    global cpm, wpm, words_list1, words_list2, words_list3
    label_timer.configure(text=count)

    # Decrease timer by 1 if timer > 0.
    if count > 0:
        label_timer.after(1000, countdown, count-1)
    else:
        # Show final score, generate new words, set cpm and wpm back to 0, clear user input and start countdown from 60.
        wpm = cpm / 5
        messagebox.showinfo(title="Your score", message=f"Your CPM score is: {cpm}, wpm score: {wpm}.")
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


def compare_characters():
    """Checks if characters are the same."""
    global cpm, wpm, previous_word
    for j in range(len(previous_word)):
        # If both characters match, increment cpm by 1.
        if val.get()[j] == previous_word[j]:
            cpm += 1
        # Includes space to the overall cpm score.
        if j == len(previous_word) - 1:
            cpm += 1


def callback(*args):
    """Callback to the user input. Updates words."""
    global words_list1, words_list2, words_list3, previous_word
    # Execute only if space is included in user's input.
    if " " in val.get():
        # Assign value to other variable, because it gets popped from the list later.
        previous_word = words_list1[0]
        # If there are is more than 1 word in a list, then pop it out and update UI labels.
        if len(words_list1) > 1:
            words_list1.pop(0)
            label_text1a.configure(text=words_list1[0])
            label_text1b.configure(text=" " + " ".join(words_list1[1:]))
        # Checks if characters are the same.
        compare_characters()
        # Adds 1 to the overall number of functions executions.
        callback.counter += 1
        # Deletes user input.
        entry_user_text.delete(0, END)
        # Updates the lists and UI labels when user entered 4 words from the first line.
        if callback.counter % 4 == 0 and callback.counter != 0:
            words_list1.clear()
            words_list1.extend(words_list2)
            words_list2.clear()
            words_list2.extend(words_list3)
            words_list3 = generate_words(words_list3)
            label_text1a.configure(text=words_list1[0])
            label_text1b.configure(text=" " + " ".join(words_list1[1:]))
            label_text2.configure(text=words_list2)
            label_text3.configure(text=words_list3)


# Creates 3 lists (because of 3 lines of words in the UI) and generates 4 random words to each of them.
words_list1 = generate_words(words_list1)
words_list2 = generate_words(words_list2)
words_list3 = generate_words(words_list3)
previous_word = ""

# Creates UI.
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
entry_user_text = customtkinter.CTkEntry(window, width=150, height=3, textvariable=val, placeholder_text="Type here...",
                                         justify="center")
entry_user_text.grid(column=0, row=4, pady=12, padx=10)

# Start counting down to 0 from 60.
countdown(60)
# Dynamically reacts to the user input.
val.trace('w', callback)
# Sets number of executions of callback function to 0.
callback.counter = 0
window.mainloop()
