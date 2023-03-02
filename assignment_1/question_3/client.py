import pickle
import socket
import sys

import cv2
import numpy as np
from scipy.fftpack import dct

# create socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

# specify a port for the client to connect to
port = 9999

# connect to the server
client_socket.connect((host, port))

image_path = "/home/supreeths/Downloads/SampleImage.tif"
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
Q = np.zeros((8, 8))
Q[0:8, 0:8] = 1


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


rl_encoded_list = []
blocks = make_image_blocks(image, block_size=8)
s = 0
for i, block in enumerate(blocks):
    BF = dct(block, norm="ortho")
    BQF = BF * Q
    zig_zag_result = zigzag_scan(BQF)
    rl_encoded = run_length_encode(zig_zag_result)
    s += sys.getsizeof(rl_encoded)
    rl_encoded_list.append(rl_encoded)

t = pickle.dumps(rl_encoded_list)
client_socket.send(t)

# close the connection
client_socket.close()
