from pprint import pprint

import cv2
import numpy as np
from scipy.fft import dct

image_path = "/home/supreeths/Downloads/SampleImage.tif"
image = cv2.imread(image_path)
image = cv2.cvtColor(cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
Q = np.zeros((8, 8))
Q[0:3, 0:3] = 1

BF = dct(image)
res = BF * Q


def run_length_encode(data):
    """Encodes a list of integers using run length encoding."""
    _encoded_data = []
    i = 0
    while i < len(data):
        j = i + 1
        while j < len(data) and data[j] == data[i]:
            j += 1
        _encoded_data.append((data[i], j - i))
        i = j
    return _encoded_data


def zigzag_scan(matrix):
    UP, DOWN, LEFT, RIGHT = range(4)

    # Initialize variables for the current position and direction of traversal
    row, col, direction = 0, 0, RIGHT
    # Define a list to store the scanned values
    scanned_values = []
    # Iterate over each element in the matrix
    for __, _ in enumerate(range(8 * 8)):
        # Append the current element to the scanned values list
        scanned_values.append(matrix[row][col])
        # Move to the next element based on the current direction of traversal
        if direction == UP:
            if row == 0:
                col += 1
                direction = LEFT
            elif col == 7:
                row += 1
                direction = LEFT
            else:
                row -= 1
                col += 1
        elif direction == DOWN:
            if row == 7:
                direction = RIGHT
                col += 1
            else:
                row += 1
                direction = UP
        elif direction == LEFT:
            if col == 0 and row != 7:
                row += 1
                direction = UP
            elif row == 7:
                col += 1
                direction = UP
            else:
                row += 1
                col -= 1
                direction = LEFT
        elif direction == RIGHT:
            if col == 7:
                direction = DOWN
                row += 1
            else:
                col += 1
                direction = LEFT
    return scanned_values


zig_zag_result = zigzag_scan(res)

# Print the scanned values
result = run_length_encode(zig_zag_result)
pprint(result)