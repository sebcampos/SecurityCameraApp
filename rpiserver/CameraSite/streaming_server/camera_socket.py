import socket, cv2, pickle, struct
import imutils
import threading
import cv2


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#host_name = socket.gethostname()
port = 9999
#host_ip = socket.gethostbyname(host_name)
socket_address = ('0.0.0.0', port)
server_socket.bind(socket_address)
server_socket.listen()


def start_video_stream():
    client_socket, addr = server_socket.accept()
    vid = cv2.VideoCapture(0)

    try:
        print('Client {} connected'.format(addr))
        if client_socket:
            while vid.isOpened():
                img, frame = vid.read()

                frame = imutils.resize(frame, width=320)
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a)) + a
                client_socket.sendall(message)
    
    except Exception as e:
        print(f'Cache server disconnected')


if __name__ == "__main__":
    while True:
        start_video_stream()

