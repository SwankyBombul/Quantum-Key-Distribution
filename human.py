#from qrng import *
from Randomese import *


def xor(a, b):
    if a+b % 2 == 0:
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
        self.bases = []
        self.key = []
        self.key_length = 0

    def initiate_bases(self, qbit_number, bit_position):
        for i in range(0, qbit_number):
            self.bases.append(read_single_bit(bit_position))
            self.key_length = qbit_number

    def initiate_key(self, bit_position):
        for i in range(0, self.key_length):
            self.key.append(read_single_bit(bit_position))
            print(self.key[i], i)

    def send_to_channel(self, channel):
        channel.message = self.key
        channel.message_length = self.key_length

    def adjust_bases(self, sender):
        print(len(self.bases), len(sender.bases))
        adjusted_key1 = []
        adjusted_key2 = []
        for n in range(0, len(self.bases)):
            if self.bases[n] != sender.bases[n]:
                print(n, self.key[n], sender.key[n])
                adjusted_key1.append(self.bases[n])
                adjusted_key2.append(sender.bases[n])

        self.key = adjusted_key1
        sender.key = adjusted_key2

    def compare_keys(self, sender):
        key_length = len(self.key)
        aligned_qubits = 0
        for n in range(0, key_length):
            if self.key[n] == sender.key[n]:
                aligned_qubits += 1

        return f"Percent of well-aligned qubits: {aligned_qubits/key_length*100}%"

