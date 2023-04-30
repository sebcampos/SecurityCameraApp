from channels.generic.websocket import WebsocketConsumer
import socket
import pickle
import struct


class VideoConsumer(WebsocketConsumer):

    def connect(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name = socket.gethostname()
        port = 9999
        host_ip = socket.gethostbyname(host_name)
        client_socket.connect((host_ip, port))
        data = b""
        payload_size = struct.calcsize('Q')
        while True:
            while len(data) < payload_size:
                packet = client_socket.recv(4 * 1024)
                if not packet:
                    break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack('Q', packed_msg_size)[0]

            while len(data) < msg_size:
                data += client_socket.recv(4 * 1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            await self.send(bytes_data=frame)

    def receive(self, text_data=None, bytes_data=None):
        print(text_data)
