# This code will run the drone side, it will send video to cache server
from concurrent.futures import ThreadPoolExecutor
import socket
import cv2
import pickle
import struct
import imutils


host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)


def init_video(camera, value):
    # create server socket with tcp (one to many SOCK_STREAM standards )
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    videoPort = 9999
    socket_address = (host_ip, videoPort)
    server_socket.bind(socket_address)
    server_socket.listen()
    print("Listening at video port", socket_address)
    client_socket, addr = server_socket.accept()
    if camera == True:
        vid = cv2.VideoCapture(0)
    else:
        if value == 1:
            filename = 'E:\MulticastVideo\Video_Server\MainServer\son-tung-m-tp-noi-nay-co-anh.mp4'

        elif value == 2:
            filename = 'E:\MulticastVideo\Video_Server\MainServer\Shaun-the-Sheep-Season-2-Cartoons-for-Kids.mp4'

        else:
            filename = 'E:\MulticastVideo\Video_Server\MainServer\Tom-and-Jerry.mp4'

        vid = cv2.VideoCapture(filename)
    try:
        print('Cached Server {} Connected !'.format(addr))
        if client_socket:
            while(vid.isOpened()):
                img, frame = vid.read()

                frame = imutils.resize(frame, width=600)
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a))+a
                client_socket.sendall(message)
                cv2.imshow("Data Transfering to CacheServer", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    client_socket.close()
                    break

    except Exception as e:
        print(f"Cached Server  {addr} Disconnected")
        pass


def main():
    val = int(input("Choose: \nMulticast camera: 1 \nMulticast video: 2 \n"))
    if(val == 1):
        with ThreadPoolExecutor(max_workers=1) as executorStream:
            executorStream.submit(init_video, True, 0)
    else:
        val = int(input("Choose: \nNoi Nay Co Anh - Son Tung M-TP: 1 \nShaun the Sheep Cartoon: 2 \nTom and Jerry(Cartoon for Kids): 3 \n"))
        with ThreadPoolExecutor(max_workers=1) as executorVideo:
            executorVideo.submit(init_video, False, val)


if __name__ == "__main__":
    main()
