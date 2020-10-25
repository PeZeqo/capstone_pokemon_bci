from project_constants import PATTERN_LENGTH
from collections import deque
import sys


def cvep():
    sequences = []
    on_off = [0, 1]

    for bit_1 in on_off:
        for bit_2 in on_off:
            for bit_3 in on_off:
                pattern = deque([bit_1, bit_2, bit_3, 1])
                seq = []
                while len(seq) < PATTERN_LENGTH:
                    next_bit = pattern.popleft() != pattern[0]
                    seq.append(next_bit)
                    pattern.append(next_bit)
                sequences.append(seq)

    save_frequency_list(sequences)
    print_frequency_list()


def ssvep():
    sequences = []

    for off_bits in range(1,9):
        sequences.append([1] + [0] * off_bits)

    save_frequency_list(sequences)
    print_frequency_list()


def save_frequency_list(sequences):
    with open('flicker_patterns.txt', 'w') as f:
        for sequence in sequences:
            f.write("%s\n" % sequence)

    print_frequency_list()


def print_frequency_list():
    flicker_frequency = []
    with open('flicker_patterns.txt') as f:
        for sequence in f:
            flicker_frequency.append(eval(sequence))

    print(flicker_frequency)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Must specify 'cvep' or 'ssvep'")
    else:
        option = sys.argv[1]
        if option == 'cvep':
            cvep()
        elif option == 'ssvep':
            ssvep()
        else:
            print("Must specify 'cvep' or 'ssvep'")


