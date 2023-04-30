import socket, cv2, pickle, struct
import imutils
import threading

import asyncio
import websockets
import django
import cv2
import sys


#django.setup()

host_ip = '0.0.0.0'
port = 9999
socket_address = (host_ip, 9998)
frame = None

def start_video_stream():
    global frame
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host_ip, port))
    data = b""
    payload_size = struct.calcsize('Q')
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4*1024)
            if not packet:
                break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack('Q', packed_msg_size)[0]
        
        while len(data) < msg_size:
            data += client_socket.recv(4*1024)

        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)

    client_socket.close()


async def server_client(websocket, path):
    global frame
    #await websocket.recv()
    while True:
        a = pickle.dumps(frame)
        message = struct.pack('Q', len(a)) + a
        await websocket.send(message)

if __name__ == "__main__":
    
    thread1 = threading.Thread(target=start_video_stream, args=())
    thread1.start()
    
    start_server = websockets.serve(server_client, *socket_address)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
     
