import random
from qubit import Qubit


def bit_change(bit):
    return (bit + 1) % 2


def xor(a, b):
    if (a+b) % 2 == 0:
        return 0
    else:
        return 1


class Channel:

    # Creating a channel
    def __init__(self, error_rate):
        """Creates a new channel with a fixed error rate"""
        self.error_rate = error_rate
        self.message = []
        self.message_length = 0

    def generate_errors(self):
        """Changes some qubits that go through the channel. Probability of generating an error is equal to channel's
        error rate"""
        for n in range(0, self.message_length):
            if random.randint(1, 100) < self.error_rate:   # checking condition and replacing the qubit with another
                # one with a random value
                new_value = random.randint(0, 1)
                self.message[n] = Qubit(0, new_value, xor(new_value, self.message[n].bit))


