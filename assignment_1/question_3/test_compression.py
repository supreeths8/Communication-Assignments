import cv2
import numpy as np
from scipy.fftpack import dct, idct

image_path = "/home/supreeths/Downloads/SampleImage.tif"
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
Q = np.zeros((8, 8))
Q[0:3, 0:3] = 1


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


def run_length_decode(_encoded_data):
    """Decodes run length encoded data and returns the original list of integers."""
    _decoded_data = []
    for _value, count in _encoded_data:
        _decoded_data += [_value] * count
    return np.array(_decoded_data).reshape(64,)


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


rl_encoded_list = []
blocks = make_image_blocks(image, block_size=8)
for i, block in enumerate(blocks):
    BF = dct(block, norm="ortho")
    BQF = BF * Q
    zig_zag_result = zigzag_scan(BQF)
    rl_encoded = run_length_encode(zig_zag_result)
    rl_encoded_list.append(rl_encoded)
    print(i)
    assert np.array_equal(zig_zag_result.reshape(64,), run_length_decode(rl_encoded))
    rl_decoded = run_length_decode(rl_encoded)
    r = undo_zigzag_scan(rl_decoded)
    assert np.array_equal(r, BQF)
    inverse_res = np.divide(r, Q)
    np.nan_to_num(inverse_res, copy=False)
    back_to_img = idct(inverse_res, norm="ortho")
    break
print(back_to_img)

# m = [[1,2,3,4, 5,6,7,8],
#      [9,10,11,12,13,14,15,16],
#      [17,18,19,20,21,22,23,24],
#      [25,26,27,28,29,30,31,32],
#      [33,34,35,36,37,38,39,40],
#      [41, 42, 43,44,45,46,47,48],
#      [49, 50,51,52,53,54,55,56],
#      [57,58,59,60,61,62,63,64]]
