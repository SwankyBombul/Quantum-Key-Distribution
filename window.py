from tkinter import *
from human import Human
from channel import Channel
from PIL import Image, ImageTk


class Window(Tk):
    error_table = {"50%": 1, "25%": 2, "12.5%": 3, "6.25%": 4, "3.12%": 5}

    def __init__(self):
        super().__init__()
        self.title("Quantum Key Distribution Simulator")
        self.minsize(width=600, height=400)
        self.config(padx=20, pady=20)

        self.header = Label(text="Welcome to the QKD simulator!")
        self.header.grid(row=0)

        self.checkbox_var = IntVar()

        self.eavesdropper_checkbox = Checkbutton(text="Eve present", variable=self.checkbox_var, onvalue=True,
                                                 offvalue=False,
                                                 command=self.display_setup)
        self.eavesdropper_checkbox.grid(row=1, column=0)

        self.canvas = Canvas(width=200, height=200, highlightthickness=0)
        self.display_setup()

        self.length_input = Entry()
        self.length_input.grid(row=1, column=1)

        # choices = ["50%", "25%", "12.5%", "6.25%", "3.12%"]
        # choicesvar = StringVar(value=choices)
        # self.listbox_one = Listbox(listvariable=choicesvar)
        # self.listbox_one.grid(row=2, column=0)
        # self.listbox_two = Listbox(listvariable=choicesvar)
        # self.listbox_two.grid(row=2, column=1)

        self.start_button = Button(text="START", command=self.start_simulation)
        self.start_button.grid(row=3, column=0)

        self.statistics = Label(text="Statistics")
        self.statistics.grid(row=3, column=1)

    def display_setup(self):
        if self.checkbox_var.get() == 1:
            setup_image = Image.open("Eve_present.png")
        else:
            setup_image = Image.open("Eve_absent.png")

        self.canvas.delete("all")
        setup = ImageTk.PhotoImage(setup_image)
        print(1)
        self.canvas.create_image(100, 100, image=setup)
        self.canvas.grid(row=4, column=2)

    def start_simulation(self):
        length = int(self.length_input.get())
        bob = Human(character="good")
        alice = Human(character="good")
        bob.create_bases(length)
        alice.create_key_and_bases(length)

        error_rate1 = 0  # self.error_table[self.listbox_one.get(0)]

        channel_one = Channel(error_rate=error_rate1)

        if self.checkbox_var.get() == 1:
            eve = Human(character="evil")
            eve.create_bases(length)

            error_rate2 = 0  # self.error_table[self.listbox_two.get(0)]
            channel_two = Channel(error_rate=error_rate2)

            alice.send_to_channel(channel_one)
            eve.receive_from_channel(channel_one)
            eve.send_to_channel(channel_two)
            bob.receive_from_channel(channel_two)

        else:
            alice.send_to_channel(channel_one)
            bob.receive_from_channel(channel_one)

        bob.adjust_bases(alice, eve)
        report = bob.compare_keys(alice)
        self.statistics.config(text="Statistics\n" + report)
