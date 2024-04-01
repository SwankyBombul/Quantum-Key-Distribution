import tkinter.messagebox
from tkinter import *
from human import Human
from channel import Channel


class Window(Tk):

    def __init__(self):
        """Creates a Window class object. Window class inherits from Tk and has all the necessary widgets initiated
        and set up"""
        super().__init__()
        self.title("Quantum Key Distribution Simulator")   # Changing window title
        self.config(padx=50, pady=50)

        # Configuring and displaying the header label with a welcome message
        self.header = Label(text="Welcome to the QKD simulator!", font=("Comic Sans MS", 24), padx=40, pady=20)
        self.header.grid(row=0, column=0, columnspan=4)

        # Configuring and placing a slider responsible for channel one's error rate
        self.scale_slider_one = Scale(orient="horizontal", from_=0, to=20, font=("Comic Sans MS", 16))
        self.scale_slider_one.grid(row=3, column=0)
        self.slider_label_one = Label(text="Channel 1 error [%]", font=("Comic Sans MS", 16), padx=40, pady=20)
        self.slider_label_one.grid(row=3, column=1)

        # Configuring and placing a slider responsible for channel two's error rate
        self.scale_slider_two = Scale(orient="horizontal", from_=0, to=20, font=("Comic Sans MS", 16), state="disabled")
        self.scale_slider_two.grid(row=4, column=0)
        self.slider_label_two = Label(text="Channel 2 error [%]", font=("Comic Sans MS", 16), padx=40, pady=20)
        self.slider_label_two.grid(row=4, column=1)

        # Label for the Eve's strategies section of the window
        self.strategy_choice_label = Label(text="Eve's strategies: ", font=("Comic Sans MS", 16), padx=40, pady=20)
        self.strategy_choice_label.grid(row=5, column=1, columnspan=2)

        # Configuring and displaying different choices for Eve's strategy. Only one option can be selected at a time.
        # They remain disabled while the Eve listening checkbox is unchecked.
        self.strategy_var = IntVar()
        self.strategy_var.set(1)
        self.radio_buttons = []

        radio1 = Radiobutton(self, text="Use existing base", font=("Arial", 12), variable=self.strategy_var, value=1)
        self.radio_buttons.append(radio1)
        radio1.grid(row=6, column=1)
        radio2 = Radiobutton(self, text="Generate a new base", font=("Arial", 12), variable=self.strategy_var, value=2)
        self.radio_buttons.append(radio2)
        radio2.grid(row=6, column=2)
        radio3 = Radiobutton(self, text="Send random qubits", font=("Arial", 12), variable=self.strategy_var, value=3)
        self.radio_buttons.append(radio3)
        radio3.grid(row=7, column=1)
        radio4 = Radiobutton(self, text="Send all qubits in the same state", font=("Arial", 12), variable=self.strategy_var, value=4)
        self.radio_buttons.append(radio4)
        radio4.grid(row=7, column=2)

        # Configuring and displaying the Eve listening checkbox
        self.checkbox_var = IntVar()
        self.eavesdropper_checkbox = Checkbutton(variable=self.checkbox_var, onvalue=True, text="Eve listening", font=(
            "Comic Sans MS", 16), offvalue=False, padx=40, pady=20, command=self.display_setup)
        self.eavesdropper_checkbox.grid(row=1, column=0)
        self.eavesdropper_label = Label(font=("Comic Sans MS", 16), padx=40, pady=20)
        self.change_eavesdropper_status()
        self.eavesdropper_label.grid(row=1, column=1)

        # Configuring and placing the entry box for the number of qubits used in the simulation.
        self.length_input = Entry(font=("Comic Sans MS", 16))
        self.length_input.grid(row=2, column=0)
        self.length_label = Label(text="Number of sent qubits", font=("Comic Sans MS", 16), padx=40, pady=20)
        self.length_label.grid(row=2, column=1)

        # Creating and placing a button that starts the simulation with the selected parameters.
        self.start_button = Button(text="START", font=("Comic Sans MS", 20), command=self.start_simulation, padx=40,
                                   pady=20)
        self.start_button.grid(row=8, column=1, columnspan=2)

        # Creates and places the box where the results will show up.
        self.statistics = Label(text="Statistics", font=("Comic Sans MS", 20), padx=40, pady=20)
        self.statistics.grid(row=2, rowspan=3, column=2, columnspan=2)

    def change_eavesdropper_status(self):
        """Updates Eve's status on a dedicated label"""
        if self.checkbox_var.get():
            self.eavesdropper_label.config(text="Eve listening!!!")
        else:
            self.eavesdropper_label.config(text="Eve is afk :)")

    def display_setup(self):
        """Updates widgets' configurations according to options chosen by the user"""
        if self.checkbox_var.get():
            self.scale_slider_two.config(state="normal")
            for button in self.radio_buttons:
                button.config(state="normal")
                button.deselect()
            self.strategy_var.set(1)
        else:
            self.scale_slider_two.set(0)
            self.scale_slider_two.config(state="disabled")  # Disabling the second channel slider and strategy
            # buttons if Eve is absent
            for button in self.radio_buttons:
                button.config(state="disabled")
            self.strategy_var.set(0)
        self.change_eavesdropper_status()

    def start_simulation(self):
        """Starts the simulation with the parameters chosen by the user. Displaces results in a dedicated widget"""
        try:
            length = int(self.length_input.get())

        except ValueError:  # Show a warning if the qubit number hasn't been put in
            tkinter.messagebox.showwarning(title="Incorrect number of qubits", message="Please input the number of qubits")

        else:
            # If the qubit value is chosen initiate the objects and run the simulation
            bob = Human()
            alice = Human()
            bob.create_bases(length)
            alice.create_key_and_bases(length)

            error_rate1 = self.scale_slider_one.get()

            channel_one = Channel(error_rate=error_rate1)

            if self.checkbox_var.get() == 1:   # When Eve is present
                eve = Human()
                eve.create_bases(length)

                error_rate2 = self.scale_slider_two.get()  # self.error_table[self.listbox_two.get(0)]
                channel_two = Channel(error_rate=error_rate2)

                alice.send_to_channel(channel_one)
                eve.receive_from_channel(channel_one)
                eve.send_to_channel(channel_two)
                bob.receive_from_channel(channel_two)

            else:
                alice.send_to_channel(channel_one)
                bob.receive_from_channel(channel_one)

            bob.adjust_bases(alice)
            report = bob.compare_keys(alice)
            self.statistics.config(text="Statistics\n" + report, font=("Comic Sans MS", 14))   # Displaying statistics
