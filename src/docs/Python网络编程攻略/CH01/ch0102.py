"""
Date: 2022.04.08 13:13:02
LastEditors: Rustle Karl
LastEditTime: 2022.04.08 13:18:18
"""
import socket

host = 'localhost'
payload = 2048
backlog = 5

def echo_server(port=8089):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(backlog)
    while True:
        client, client_address = s.accept()
        data = client.recv(payload)
        if data:
            client.send(data)
            client.close()
    
def echo_client(port=8089):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall("OK")
    data = s.recv(16)
    if data:
        s.sendall(data)
    s.close()