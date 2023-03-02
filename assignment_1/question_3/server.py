import json
import pickle
import socket

import cv2
import numpy as np
from scipy.fftpack import idct


def run_length_decode(_encoded_data):
    """Decodes run length encoded data and returns the original list of integers."""
    _decoded_data = []
    for _value, count in _encoded_data:
        _decoded_data += [_value] * count
    return np.array(_decoded_data).reshape(64,)


def undo_zigzag_scan(matrix):
    UP, DOWN, LEFT, RIGHT = range(4)
    row, col, direction = 0, 0, RIGHT
    un_zigzag_matrix = np.zeros((8,8))
    matrix = matrix.reshape(64,)
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
            # print(c)
            hstack_list.append(hstacks)
            hstacks = block_list[c+1]
        if c == 1023:
            hstack_list.append(hstacks)

    vstack = hstack_list[0]
    for i, h in enumerate(hstack_list):
        if i == 0:
            continue
        vstack = np.vstack((vstack, h))
    return vstack



def MSE(A, B):
    return np.square(np.subtract(A, B)).mean()

# create socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

# specify a port for the server to listen on
port = 9999

# bind the socket to a public host, and a well-known port
server_socket.bind((host, port))

# set the server to listen for incoming connections
server_socket.listen(5)

# wait for a client connection
print("Waiting for client connection...")
client_socket, addr = server_socket.accept()
print("Got connection from", addr)
Q = np.zeros((8, 8))
Q[0:3, 0:3] = 1
data = b""
while True:
    packet = client_socket.recv(4096)
    if not packet:
        break
    data += packet
data_arr = pickle.loads(data)
client_socket.close()
print(f"Data size {np.array(data_arr).nbytes}")

B = []
for block in data_arr:
    decoded_data = run_length_decode(block)
    BQF = undo_zigzag_scan(decoded_data)
    inv = idct(BQF, norm="ortho")
    B.append(inv)

B = np.array(B)
final_image = combine_image_blocks(B)
# close the connection
image_path = "/home/supreeths/Downloads/SampleImage.tif"
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("original", image)
cv2.waitKey(0)
final_image = final_image.astype(np.uint8)
cv2.imshow("test", final_image)
cv2.waitKey(0)
print(f"MSE: {MSE(image, final_image)}")
