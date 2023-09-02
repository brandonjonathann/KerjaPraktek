import socket
import os

HOST = socket.gethostbyname(socket.gethostname())
PORT = 1

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

file = open("data.csv", "rb")

client.send("not_new_data.csv".encode())
print(f'Sending data: new_data.csv')

data = file.read()
client.sendall(data)
client.send(b"<END>")
print(f'File has been sent.')

file.close()
client.close()