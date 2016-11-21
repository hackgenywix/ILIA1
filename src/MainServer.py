import socket
from random import randint
import hashlib
import image
from PIL import Image

BIND_IP = "0.0.0.0"
BIND_PORT = 9999
BACKLOG = 5

IMAGE_MODE = "L"
IMAGE_COLORS = "RGBA"

MAX_SALT_RANGE = 2E32


class MainServer(socket.socket):

    def __init__(self):
        super().__init__()

        self.bind((BIND_IP, BIND_PORT))
        self.listen(BACKLOG)

        self.clients_socket = []
        self.last_captcha_text = {}

    def accept_clients(self):
        try:
            while not self.s.close():
                self.clients_socket.append(self.s.accept())
        except BlockingIOError:
            pass

    def send_client_captcha(self, client):
        captcha2send = image.generate_image()
        client.send(
            self.image2bytes(
                self.captcha_generator.generate()
            )
        )

    def check_user_in_system(self, username, password):
        pass

    def check_user_captcha_guess(self, client, guess):
        return self.last_captcha_text.get(client).get_text() == guess

    @staticmethod
    def image2bytes(image):
        image_as_bytes = [image.height, image.width]

        for i in range(image.height):
            for j in range(image.width):
                image_as_bytes.append(image.getpixel((i, j)))

        return image_as_bytes

    @staticmethod
    def bytes2images(image_as_bytes):
        height = image_as_bytes[0]
        width = image_as_bytes[1]
        image = Image.new(IMAGE_MODE, (height, width), IMAGE_COLORS)

        for i in range(height):
            for j in range(width):
                image.putpixel((i, j), image_as_bytes[i * width + j + 2])

        return image

    @staticmethod
    def encrypt(password):
        return hash((hash("sfsjhydkg"+password+"ddhjtrysef")))
