import os
import pickle
import socket
import cv2
import numpy as np

from utils import combine_image_blocks, undo_zigzag_scan, run_length_decode, MSE, load_grayscale_image, get_logger

os.chdir(os.path.dirname(__file__))
logger = get_logger(__name__)
image_path = "/home/supreeths/Downloads/SampleImage.tif"
image = load_grayscale_image(image_path)


class Receiver:
    """
    Wrapper class for Python Socket API
    """
    def __init__(self, _port=9999):
        self.port = _port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.socket.bind((self.host, self.port))


receiver = Receiver().socket
receiver.listen(10)

logger.info("Waiting for client connection...")
sender, addr = receiver.accept()
logger.info(f"Got connection from {addr}")
# data = b""

# for count in range(5):
data = b""
total_bytes_received = 0
while True:
    packet = sender.recv(4096)
    if not packet:
        break
    total_bytes_received += len(data)
    data += packet
data_arr = pickle.loads(data)
logger.info(f"Data received size : {total_bytes_received}")
B = []
for block in data_arr:
    decoded_data = run_length_decode(block)
    BQF = undo_zigzag_scan(decoded_data)
    inv = cv2.idct(BQF)
    B.append(inv)

B = np.array(B)
final_image = combine_image_blocks(B)
final_image = final_image.astype(np.uint8)
logger.info(f"MSE: {MSE(image, final_image)}")
cv2.imwrite(f"./output/count-{MSE(image, final_image)}.jpg", final_image)
sender.close()
