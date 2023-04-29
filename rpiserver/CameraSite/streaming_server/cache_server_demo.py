import socket, cv2, pickle, struct
import imutils
import threading
import cv2
import sys

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#host_name = socket.gethostname()
#host_ip = socket.gethostbyname(host_name)
host_ip = '0.0.0.0'
port = 9999
socket_address = (host_ip, 9998)
server_socket.bind(socket_address)
server_socket.listen()

# global frame
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


#thread = threading.Thread(target=start_video_stream, args=())
#thread.start()

def server_client(addr, client_socket):
    global frame
    try:
        print('Client {} connected'.format(addr))
        if client_socket:
            while True:
                a = pickle.dumps(frame)
                message = struct.pack('Q', len(a)) + a
                client_socket.sendall(message)


    except Exception as e:
        print('Client disconnected')
        print(e)



if __name__ == "__main__":
    
    thread1 = threading.Thread(target=start_video_stream, args=())
    thread1.start()
    
    # TODO add thread pool?
    while True:
        try:
            client_socket, addr = server_socket.accept()
            print(addr)
            thread2 = threading.Thread(target=server_client, args=(addr, client_socket))
            thread2.start()
        except Exception as e:
            print(e, 'tear down ?')
        finally:
            thread1.join()
            thread2.join()
            sys.exit(0)

