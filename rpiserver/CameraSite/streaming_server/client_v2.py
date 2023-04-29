import websockets, cv2, pickle, struct, asyncio

async def client():
    data = b""
    frame = False
    async with websockets.connect('ws://192.168.7.207:9998') as websocket:
        test = True
        payload_size = struct.calcsize('Q')
        # await websocket.send('')
        while True:
            while True:
                # host_name = socket.gethostname()
                port = 9998
                host_ip = '192.168.7.207'
                # client_socket.connect((host_ip, port))
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
                    print(len(frame_data), msg_size)
                    data = data[msg_size:]
                    frame = pickle.loads(frame_data)
                if test and frame:
                    cv2.imshow("Recieving from cacheserver", frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        break


asyncio.get_event_loop().run_until_complete(client())
