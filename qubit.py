from randomese import read_single_bit


class Qubit:
    def __init__(self, *args):
        if len(args) != 0:
            self.state = (args[0], args[1])
        else:
            self.state = (read_single_bit(), read_single_bit())
        self.base = self.state[0]
        self.bit = self.state[1]
