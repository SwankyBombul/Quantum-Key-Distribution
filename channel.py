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
    def __init__(self, error_rate):
        self.error_rate = error_rate
        self.message = []
        self.message_length = 0

    def generate_errors(self):
        for n in range(0, self.message_length):
            if random.randint(1, 200) < self.error_rate:
                print(1)
                new_value = random.randint(0, 1)
                self.message[n] = Qubit(0, new_value, xor(new_value, self.message[n].bit))


