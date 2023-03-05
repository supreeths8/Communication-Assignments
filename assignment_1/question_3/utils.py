import logging
from enum import Enum, auto

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


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


def _get_zig_zag_indices(direction, row, col):
    # UP, DOWN, LEFT, RIGHT = range(4)
    if direction == Direction.UP:
        if row == 0:
            col += 1
            direction = Direction.LEFT
        elif col == 7:
            row += 1
            direction = Direction.LEFT
        else:
            row -= 1
            col += 1
    elif direction == Direction.DOWN:
        if row == 7:
            direction = Direction.RIGHT
            col += 1
        else:
            row += 1
            direction = Direction.UP
    elif direction == Direction.LEFT:
        if col == 0 and row != 7:
            row += 1
            direction = Direction.UP
        elif row == 7:
            col += 1
            direction = Direction.UP
        else:
            row += 1
            col -= 1
            direction = Direction.LEFT
    elif direction == Direction.RIGHT:
        if col == 7:
            direction = Direction.DOWN
            row += 1
        else:
            col += 1
            direction = Direction.LEFT
    return direction, row, col


def zigzag_scan(matrix):
    row, col, direction = 0, 0, Direction.RIGHT
    scanned_values = []
    for _ in range(8 * 8):
        scanned_values.append(matrix[row][col])
        direction, row, col = _get_zig_zag_indices(direction, row, col)
    return np.array(scanned_values).reshape((8, 8))


def undo_zigzag_scan(matrix):
    row, col, direction = 0, 0, Direction.RIGHT
    un_zigzag_matrix = np.zeros((8, 8))
    matrix = matrix.reshape(64, )
    un_zigzag_matrix[row][col] = matrix[0]
    for c, value in enumerate(matrix):
        if c == 0:
            continue
        direction, row, col = _get_zig_zag_indices(direction, row, col)
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
