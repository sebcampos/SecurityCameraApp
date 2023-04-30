import asyncio
import cv2
import pickle
import struct
import websockets


# port = 9998
# host_ip = '192.168.7.207'

async def client():
    async with websockets.connect('ws://192.168.7.207:9998') as websocket:
        test = True
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

            if test:
                cv2.imshow("Recieving from cacheserver", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(client())
