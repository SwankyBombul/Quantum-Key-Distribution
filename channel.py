from Randomese import *


def xor(a, b):
    if a+b % 2 == 0:
        return 0
    else:
        return 1


class Channel:
    def __init__(self, error_rate):
        self.message_length = 0
        self.error_rate = error_rate
        self.message = []
        self.message_length = 0

    def send_message(self, recipient, bit_position):
        for i in range(0, self.message_length):
            sent_correct = True
            temp = False
            for n in range(0, self.error_rate):
                if read_single_bit(bit_position) == 1:
                    temp = True

            if not temp:
                sent_correct = False
            print(self.message[2])
            if sent_correct:
                recipient.key.append(self.message[i])
            else:
                recipient.key.append(read_single_bit(bit_position))
