from project_constants import PATTERN_LENGTH
from collections import deque

if __name__ == "__main__":
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

    with open('flicker_patterns.txt', 'w') as f:
        for sequence in sequences:
            f.write("%s\n" % sequence)

    flicker_frequency = []
    with open('flicker_patterns.txt') as f:
        for sequence in f:
            flicker_frequency.append(eval(sequence))

    print(flicker_frequency)
