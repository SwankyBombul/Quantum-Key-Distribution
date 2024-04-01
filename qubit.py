from randomese import read_single_bit


class Qubit:
    def __init__(self, *args):
        """Creates a single qubit with attributes: base: int, bit: int and state: (base: int, bit: int). If two
        parameters are given base=args[0], bit=arg[1]. If no parameters are given the values are random"""
        if len(args) != 0:
            self.state = (args[0], args[1])
        else:
            self.state = (read_single_bit(), read_single_bit())
        self.base = self.state[0]
        self.bit = self.state[1]
