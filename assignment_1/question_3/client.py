import os

import cv2
import numpy as np
import pickle
import socket

from utils import zigzag_scan, run_length_encode, load_grayscale_image, make_image_blocks, make_quantization_matrix, get_logger
os.chdir(os.path.dirname(__file__))

logger = get_logger("CLIENT")
L = 3


class Client:
    def __init__(self, _port=9999):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.port = _port

    def connect(self):
        self.socket.connect((self.host, self.port))

    def send(self, _data):
        self.socket.send(_data)

    def close(self):
        self.socket.close()


image_path = "SampleImage.tif"
image = load_grayscale_image(image_path)

blocks = make_image_blocks(image, block_size=8)
client = Client()
client.connect()
rl_encoded_list = []

for block in blocks:
    BF = cv2.dct(block.astype(np.float32))
    Q = make_quantization_matrix(L)
    BQF = BF * Q
    zig_zag_result = zigzag_scan(BQF)
    rl_encoded = run_length_encode(zig_zag_result)
    rl_encoded_list.append(rl_encoded)
data_to_send_bytes = pickle.dumps(rl_encoded_list)
client.send(data_to_send_bytes)
logger.info(f"Data sent")
client.close()
