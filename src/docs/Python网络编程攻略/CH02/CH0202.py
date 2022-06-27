"""
Date: 2022.04.08 13:33:41
LastEditors: Rustle Karl
LastEditTime: 2022.04.08 13:39:52
"""
import os
import socket
import socketserver
import threading

SERVER_HOST='localhost'
SERVER_PORT=0# 让内核动态选取
BUF_SIZE=1024
ECHO_MSG=b"I'm echo server"

def client(ip, port, message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    try:
        s.sendall(message)
        response = s.recv(BUF_SIZE)
        print(f'client received: {response}')
    finally:
        s.close()

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        response = self.request.recv(BUF_SIZE)
        current_process = threading.current_thread()
        print(f"{current_process}: {response}")
        self.request.sendall(response)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def main():
    server = ThreadedTCPServer((SERVER_HOST,SERVER_PORT), ThreadedTCPRequestHandler)
    ip,port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    client(ip,port, 'client1')
    client(ip,port, 'client2')
    client(ip,port, 'client3')

    server.shutdown()
