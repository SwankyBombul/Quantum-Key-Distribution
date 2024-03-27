from tkinter import *
from human import Human
from channel import Channel


class Window(Tk):
    error_table = {"50%": 1, "25%": 2, "12.5%": 3, "6.25%": 4, "3.12%": 5}

    def __init__(self, canvas, bit_position):
        super().__init__()
        self.title("Quantum Key Distribution Simulator")
        self.minsize(width=600, height=400)
        self.config(padx=20, pady=20)

        self.header = Label(text="Welcome to the QKD simulator!")
        self.header.grid(row=0)

        self.eve_listening = False
        self.eavesdropper_checkbox = Checkbutton(text="Eve present", variable=self.eve_listening, onvalue=True, offvalue=False, command=self.display_setup)
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

        self.start_button = Button(text="START", command=lambda: self.start_simulation(bit_position))
        self.start_button.grid(row=3, column=0)

        self.statistics = Label(text="Statistics")
        self.statistics.grid(row=3, column=1)

    def display_setup(self):
        if self.eve_listening:
            setup_image = PhotoImage(file="Eve_present.png")
        else:
            setup_image = PhotoImage(file="Eve_absent.png")

        self.canvas.delete("all")
        self.canvas.create_image(100, 100, image=setup_image)
        self.canvas.grid(row=2)

    def start_simulation(self, bit_position):
        length = int(self.length_input.get())
        bob = Human(character="good")
        alice = Human(character="good")
        bob.initiate_bases(length, bit_position)
        alice.initiate_bases(length, bit_position)
        alice.initiate_key(bit_position)

        error_rate1 = 0 #self.error_table[self.listbox_one.get(0)]

        channel_one = Channel(error_rate=error_rate1)

        if self.eve_listening:
            eve = Human(character="evil")
            eve.initiate_bases(length, bit_position)

            error_rate2 = 0 #self.error_table[self.listbox_two.get(0)]
            channel_two = Channel(error_rate=error_rate2)

            alice.send_to_channel(channel_one)
            channel_one.send_message(eve, bit_position)
            eve.send_to_channel(channel_two)
            channel_two.send_message(bob, bit_position)

        else:
            alice.send_to_channel(channel_one)
            channel_one.send_message(bob, bit_position)

        bob.adjust_bases(alice)
        report = bob.compare_keys(alice)
        self.statistics.config(text="Statistics\n" + report)
