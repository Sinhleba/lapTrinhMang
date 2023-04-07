# Cache server will recieve video stream from the the original server
# Also it will serve this video stream to multiple clients

import socket
import pickle
import struct
import threading
import socket
import threading


#  communication between cached server and clients
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '127.0.0.1'
print('HOST IP:', host_ip)
cachedPort = 9999
socket_address = (host_ip, cachedPort)
server_socket.bind(socket_address)
server_socket.listen()
print("Cache server listening at video port from server", socket_address)

# creating variables get data for transisting to clients
global frame
frame = None


# get video data from original server
def init_video():
    global frame
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = '192.168.1.3'  # Here provide Drone IP

    videoPortFromServer = 9999
    client_socket.connect((host_ip, videoPortFromServer))
    print("Cache server connected to Origin server with address",
          (host_ip, videoPortFromServer))
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(1024)
            if not packet:
                break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += client_socket.recv(1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
    client_socket.close()


def client(addr, client_socket):
    global frame
    try:
        print('Client {} connected to Cache Server !'.format(addr))
        if client_socket:
            while True:
                a = pickle.dumps(frame)
                videoMessage = struct.pack("Q", len(a))+a
                client_socket.sendall(videoMessage)

    except Exception as e:
        print(f"Client {addr} disconnected from Server")
        pass


def main():
    thread1 = threading.Thread(target=init_video, args=())
    thread1.start()
    # listen if having any new client
    while True:
        client_socket, addr = server_socket.accept()
        thread2 = threading.Thread(target=client, args=(addr, client_socket))
        thread2.start()
        print("Number of Clients are Joining  ", threading.active_count()-2)


if __name__ == "__main__":
    main()
