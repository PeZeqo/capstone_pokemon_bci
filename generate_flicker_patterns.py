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


def ssvep(option):
    if option == 'simple':
        frequencies = [7, 11, 17, 31]
    elif option == 'normal':
        frequencies = [4, 5, 6, 7, 11, 17, 23, 31]
    else:
        print("Must specify only between 'simple' and 'normal' for ssvep pattern generation")
        return

    sequences = []
    for frequency in frequencies:
        sequences.append([1] + [0] * (frequency-1))
    for frequency in frequencies:
        print('{} Hz'.format(128 / frequency))

    save_frequency_list(sequences)


def save_frequency_list(sequences):
    with open('flicker_patterns.txt', 'w') as f:
        for sequence in sequences:
            f.write("%s\n" % sequence)


def print_frequency_list():
    flicker_frequency = []
    with open('flicker_patterns.txt') as f:
        for sequence in f:
            flicker_frequency.append(eval(sequence))

    print(flicker_frequency)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Must specify 'cvep' or 'ssvep [simple / normal]'")
    else:
        method = sys.argv[1]
        if method == 'cvep':
            cvep()
        elif method == 'ssvep':
            if len(sys.argv) < 3:
                print("Must specify 'ssvep [simple / normal]'")
            else:
                ssvep(sys.argv[2])
        else:
            print("Must specify 'cvep' or 'ssvep [simple / normal]'")


