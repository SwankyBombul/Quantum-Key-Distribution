


def xor(a, b):
    if a+b % 2 == 0:
        return 0
    else:
        return 1


class Channel:
    def __init__(self, error_rate):
        self.error_rate = error_rate
        self.message = []


