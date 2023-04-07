import socket
import cv2
import pickle
import struct
from concurrent.futures import ThreadPoolExecutor

# create client socket and get data from cached server

def video():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = '127.0.0.1'  # Here Require CACHE Server IP
    port = 9999
    client_socket.connect((host_ip, port))  # a tuple
    print("Client connected to video server port", (host_ip, port))
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4*1024)  # 4K
            if not packet:
                break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += client_socket.recv(4*1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("CLIENT 2", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    client_socket.close()


def main():
    val = str(input("You have connected to the MulticastServer: \nType 'PLAY' to watch stream: "))
    while(val == "PLAY"):
        with ThreadPoolExecutor(max_workers=2) as executorStream:
           # executorStream.submit(audio_stream)
            executorStream.submit(video)
        
#  main
if __name__ == "__main__":
    main()
