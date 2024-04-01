

from randomese import *
from qubit import Qubit


def xor(a, b):
    if (a+b) % 2 == 0:
        return 0
    else:
        return 1


class Human:
    def __init__(self, error_rate=0): # Human error rate hasn't yet been implemented, it has no effect and is thus
        # equal to 0
        """Creates a human object. Qubits have to be created with different methods."""
        self.error_rate = error_rate
        self.qubits = []
        self.bases = []
        self.key = []
        self.length = 0

    def create_key_and_bases(self, length):
        """Creates tables : Qubit, bases: int, key: int for the Human object and fills them with random values"""
        for n in range(0, length):
            self.qubits.append(Qubit())
            self.bases.append(self.qubits[n].base)
            self.key.append(self.qubits[n].bit)

        self.length = len(self.qubits)

    def create_bases(self, length):
        """Creates the bases: int table for the object and fills it with random values"""
        self.bases = []
        for n in range(0, length):
            self.bases.append(read_single_bit())

        self.length = len(self.bases)

    def update_parameters(self):
        """Updates the objects bases and key tables according to its qubit table"""
        self.bases = [qubit[0] for qubit in self.qubits]
        self.key = [qubit[1] for qubit in self.qubits]

    def receive_from_channel(self, channel):
        """Fills object's qubit: Qubit table with values received from the channel"""
        for n in range(0, self.length):
            if self.bases[n] == channel.message[n].base:
                self.key.append(xor(channel.message[n].bit, self.bases[n]))
            else:
                self.key.append(random.choice([0, 1]))
            self.qubits.append(Qubit(self.bases[n], self.key[n]))

    def send_to_channel(self, channel):
        """Sends the object's qubit: Qubit table to the channel. Generates table message: Qubit for the channel"""
        channel.message = [Qubit(single_qubit.base, xor(single_qubit.base, single_qubit.bit)) for single_qubit in
                           self.qubits]
        channel.message_length = self.length
        channel.generate_errors()

    def implement_strategy(self, strategy):
        """Changes Eve's qubits according to the strategy chosen by the uses"""
        if strategy == 1:   # Using existing bases
            pass
        elif strategy == 2:   # Creating new bases
            self.create_bases(self.length)
            self.qubits = [Qubit(self.bases[n], self.key[n]) for n in range(self.length)]
        elif strategy == 3:   # Sending random qubits
            self.qubits = [Qubit() for n in range(self.length)]
        else:   # strategy == 4: Sending qubits of one type (1, 1)
            self.qubits = [Qubit(1, 1) for n in range(self.length)]
        self.update_parameters()

    def adjust_bases(self, sender):
        """Compares own and sender's bases. Creates new keys for them and appends only when bases are equal. Doesn't
        change qubit: Qubit and bases: int tables"""
        self.key = []
        sender.key = []
        for n in range(0, self.length):
            if self.qubits[n].base == sender.qubits[n].base:
                self.key.append(self.qubits[n].bit)
                sender.key.append(sender.qubits[n].bit)

    def compare_keys(self, sender):
        """Calculates how many qubits were received without errors. Returns updated text for the statistics widget"""
        key_length = len(self.key)
        aligned_qubits = 0
        n = 0
        for qubit in self.key:
            if qubit == sender.key[n]:
                aligned_qubits += 1
            n += 1
        return f"Percent of well-aligned qubits: {round((aligned_qubits/key_length*100))}%"
