# import cv2
# import numpy as np
# from scipy.fft import dct
#
# image_path = "/home/supreeths/Downloads/SampleImage.tif"
# image = cv2.imread(image_path)
# image = cv2.cvtColor(cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
# quant_matrix = np.zeros((8, 8))
# quant_matrix[0:3, 0:3] = 1
#
# dct_res = dct(image)
# res = dct_res * quant_matrix
#
#
# def zigzag(matrix):
#     """Scans a 8x8 matrix in a zig-zag format."""
#     rows, cols = len(matrix), len(matrix[0])
#     indices = [(i, j) for i in range(rows) for j in range(cols)]
#     indices.sort(key=lambda x: (x[0] + x[1], -x[1] if (x[0] + x[1]) % 2 == 0 else x[1]))
#     return [matrix[i][j] for i, j in indices]
#
#
# def run_length_encode(data):
#     """Encodes a list of integers using run length encoding."""
#     _encoded_data = []
#     i = 0
#     while i < len(data):
#         j = i + 1
#         while j < len(data) and data[j] == data[i]:
#             j += 1
#         _encoded_data.append((data[i], j - i))
#         i = j
#     return _encoded_data
#
#
# zigzag_data = zigzag(res)
# encoded_data = run_length_encode(zigzag_data)
#
#
# def run_length_decode(_encoded_data):
#     """Decodes run length encoded data and returns the original list of integers."""
#     _decoded_data = []
#     for _value, count in _encoded_data:
#         _decoded_data += [_value] * count
#     return _decoded_data
#
#
# # Decode the run length encoded data and retrieve the original data
# decoded_data = run_length_decode(encoded_data)
from pprint import pprint

import numpy as np

# Define an 8x8 matrix
matrix = [
    [ 1,  2,  3,  4,  5,  6,  7,  8],
    [ 9, 10, 11, 12, 13, 14, 15, 16],
    [17, 18, 19, 20, 21, 22, 23, 24],
    [25, 26, 27, 28, 29, 30, 31, 32],
    [33, 34, 35, 36, 37, 38, 39, 40],
    [41, 42, 43, 44, 45, 46, 47, 48],
    [49, 50, 51, 52, 53, 54, 55, 56],
    [57, 58, 59, 60, 61, 62, 63, 64],
]

# Define constants for the direction of traversal
UP, DOWN, LEFT, RIGHT = range(4)

# Define a function to scan the matrix in a zig-zag format
def zigzag_scan(matrix):
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
            print(row, col, __)
        elif direction == DOWN:
            if row == 7:
                direction = RIGHT
                col += 1
            else:
                row += 1
                direction = UP
            print(row, col, __)
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
            print(row, col, __)
        elif direction == RIGHT:
            if col == 7:
                direction = DOWN
                row += 1
            else:
                col += 1
                direction = LEFT
            print(row, col, __)
    return scanned_values

# Call the zigzag_scan function with the matrix as input
result = zigzag_scan(matrix)

# Print the scanned values
pprint(np.array(matrix).reshape((8, 8)))
print(result)