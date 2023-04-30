from channels.generic.websocket import WebsocketConsumer
import websockets
import pickle
import struct


class VideoConsumer(WebsocketConsumer):

    def connect(self):
        async with websockets.connect('ws://192.168.7.207:9998') as websocket:
            self.accept()
            payload_size = struct.calcsize('Q')
            data = b""
            while True:
                while len(data) < payload_size:
                    packet = await websocket.recv()
                    if not packet:
                        break
                    data += packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack('Q', packed_msg_size)[0]

                while len(data) < msg_size:
                    data += await websocket.recv()

                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)
                await self.send(bytes_data=frame)


    def receive(self, text_data=None, bytes_data=None):
        print(text_data)