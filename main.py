from tkinter import *
from PIL import Image, ImageTk
import pandas
from random import choice

current_city = {}
dictionary = {}

try:
    data = pandas.read_csv("data/cities to learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/cities.csv")
    dictionary = original_data.to_dict(orient="records")
else:
    dictionary = data.to_dict(orient="records")


# ----------------------- GENERATE ------------------------ #

def remove_city():
    dictionary.remove(current_city)
    new_data = pandas.DataFrame(dictionary)
    new_data.to_csv("data/cities to learn.csv", index=False)
    next_city()

def next_city():
    global current_city, timer
    window.after_cancel(timer)
    current_city = choice(dictionary)
    canvas.itemconfig(city_label, text=current_city["City"])
    timer = window.after(5000, province)


def province():
    window.after_cancel(timer)
    canvas.itemconfig(city_label, font=("Courier", 15), text=f"{current_city["City"]} "
                                       f"is a city \nin the province of \n{current_city["Province"]}")
# ----------------------- UI ------------------------------ #

window = Tk()
window.title("Tamriel Cities & Provinces")
window.config(padx=50, pady=50)

timer = window.after(5000, province)

input_image_path = "photo/scroll.png"
original_image = Image.open(input_image_path)
target_width = 400
width_percent = (target_width / float(original_image.size[0]))
target_height = int((float(original_image.size[1]) * float(width_percent)))
resized_image = original_image.resize((target_width, target_height))
img = ImageTk.PhotoImage(resized_image)
canvas = Canvas(window, width=500, height=600, highlightthickness=0)
canvas.create_image(50, 30, anchor='nw', image=img)
canvas.grid(row=0, column=0, columnspan=2)

city_label = canvas.create_text(250, 250, text="", font=("Courier", 30, "italic"))

known_button = Button(text="I know it", font=("Ariel", 20), command=remove_city)
known_button.grid(row=2, column=0)

unknown_button = Button(text="Next", font=("Ariel", 20), command=next_city)
unknown_button.grid(row=2, column=1)

next_city()

window.mainloop()