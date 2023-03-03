import logging

import cv2
import numpy as np


def get_logger(name):
    logging.basicConfig(level=logging.DEBUG)
    return logging.getLogger(name)


def load_grayscale_image(image_path: str):
    image = cv2.imread(image_path)
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def run_length_decode(_encoded_data):
    """Decodes run length encoded data and returns the original list of integers."""
    _decoded_data = []
    for _value, count in _encoded_data:
        _decoded_data += [_value] * count
    return np.array(_decoded_data).reshape(64, )


def zigzag_scan(matrix):
    UP, DOWN, LEFT, RIGHT = range(4)

    # Initialize variables for the current position and direction of traversal
    row, col, direction = 0, 0, RIGHT
    # Define a list to store the scanned values
    scanned_values = []
    # Iterate over each element in the matrix
    for _ in range(8 * 8):
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
    return np.array(scanned_values).reshape((8,8))


def undo_zigzag_scan(matrix):
    UP, DOWN, LEFT, RIGHT = range(4)
    row, col, direction = 0, 0, RIGHT
    un_zigzag_matrix = np.zeros((8, 8))
    matrix = matrix.reshape(64, )
    un_zigzag_matrix[row][col] = matrix[0]
    for c, value in enumerate(matrix):
        if c == 0:
            continue
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
        un_zigzag_matrix[row][col] = value
    return un_zigzag_matrix


def make_image_blocks(img, block_size=8):
    row = 0
    col = 0
    _block_list = []
    for i in range(32):
        for j in range(32):
            block = img[row: row+block_size, col:col+block_size]
            _block_list.append(block)
            col = col+block_size
        col = 0
        row = row + block_size
    return _block_list


def combine_image_blocks(block_list):
    hstacks = block_list[0]
    hstack_list = []
    count = 0
    for c, _block in enumerate(block_list):
        if c == 0:
            continue
        if count != 31:
            hstacks = np.hstack((hstacks, _block))
            count += 1
        else:
            count = 0
            hstack_list.append(hstacks)
            hstacks = block_list[c + 1]
        if c == 1023:
            hstack_list.append(hstacks)

    vstack = hstack_list[0]
    for i, h in enumerate(hstack_list):
        if i == 0:
            continue
        vstack = np.vstack((vstack, h))
    return vstack


def run_length_encode(data):
    """Encodes a list of integers using run length encoding."""
    _encoded_data = []
    i = 0
    data = data.reshape(64,)
    while i < len(data):
        j = i + 1
        while j < len(data) and data[j] == data[i]:
            j += 1
        _encoded_data.append((data[i], j - i))
        i = j
    return _encoded_data


def make_quantization_matrix(l=3):
    q = np.zeros((8, 8))
    q[0:l, 0:l] = 1
    return q


def MSE(A, B):
    return np.square(np.subtract(A, B)).mean()
