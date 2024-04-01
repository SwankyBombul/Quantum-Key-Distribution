# from qrng import *
import random

from randomese import *
from qubit import Qubit


def xor(a, b):
    if (a+b) % 2 == 0:
        return 0
    else:
        return 1


class Human:
    def __init__(self, character, error_rate=0):
        character = character.strip()
        character = character.lower()
        self.character = character

        if self.character == "evil":
            self.error_rate = 0
        self.error_rate = error_rate
        self.qubits = []
        self.bases = []
        self.key = []
        self.length = 0

    def create_key_and_bases(self, length):
        for n in range(0, length):
            self.qubits.append(Qubit())
            self.bases.append(self.qubits[n].base)
            self.key.append(self.qubits[n].bit)

        self.length = len(self.qubits)

    def create_bases(self, length):
        for n in range(0, length):
            self.bases.append(read_single_bit())

        self.length = len(self.bases)

    def receive_from_channel(self, channel):
        for n in range(0, self.length):
            if self.bases[n] == channel.message[n].base:
                self.key.append(xor(channel.message[n].bit, self.bases[n]))
            else:
                self.key.append(random.choice([0, 1]))
            self.qubits.append(Qubit(self.bases[n], self.key[n]))
        # self.qubits = [Qubit(self.bases[n], xor(channel.message[n], self.bases[n])) for n in range(0, self.length)]

    def send_to_channel(self, channel):
        channel.message = [Qubit(single_qubit.base, xor(single_qubit.base, single_qubit.bit)) for single_qubit in
                           self.qubits]
        channel.message_length = self.length
        channel.generate_errors()

    def adjust_bases(self, sender):
        self.key = []
        sender.key = []
        for n in range(0, self.length):
            if self.qubits[n].base == sender.qubits[n].base:
                self.key.append(self.qubits[n].bit)
                sender.key.append(sender.qubits[n].bit)

    def compare_keys(self, sender):
        key_length = len(self.key)
        aligned_qubits = 0
        n = 0
        for qubit in self.key:
            if qubit == sender.key[n]:
                aligned_qubits += 1
                n += 1
        return f"Percent of well-aligned qubits: {round((aligned_qubits/key_length*100))}%"
