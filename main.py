from window import Window
from tkinter import Canvas
from human import *
from channel import *
from Randomese import read_single_bit


canvas_instance = Canvas

bit_position = 0

window = Window(canvas_instance, bit_position)


file_path = "QNGFFile.dat"

window.mainloop()