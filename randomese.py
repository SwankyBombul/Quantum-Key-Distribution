import random

# This function was supposed to use a file generated by a quantum random number generator, however it is still being
# worked on. The placeholder function returns a random bit using the built-in random library.
def read_single_bit():
    """Returns randomly either a 0 or a 1"""
    return random.choice([0, 1])


# def read_single_bit(bit_position):
#     return random.choice([0, 1])
