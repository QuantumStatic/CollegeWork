from socket import socket

serverSocket = socket()
print("Socket Created")
serverSocket.bind(("127.0.0.1",16000))
serverSocket.listen(3)
print("Waiting for connection")

while True:
    clientSocket, address = serverSocket.accept()
    print(f"Connected with {address}")
    test_case = clientSocket.recv(512)
    print(test_case)
    break


