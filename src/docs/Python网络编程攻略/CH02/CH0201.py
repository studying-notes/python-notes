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

class ForkingClient(object):

    def __init__(self, ip,port):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((ip, port))

    def run(self):
        current_process_id = os.getpid()
        print(f"PID {current_process_id} sending echo message to the server: {ECHO_MSG}")
        self._socket.send(ECHO_MSG)
        response = self._socket.recv(BUF_SIZE)
        print(f"PID {current_process_id} received: {response}")

    def shutdown(self):
        self._socket.close()

class ForkingServerRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        response=self.request.recv(BUF_SIZE)
        current_process_id = os.getpid()
        print(f"PID {current_process_id} received: {response}")
        self.request.send(response)


class ForkingServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

def main():
    server = ForkingServer((SERVER_HOST, SERVER_PORT), ForkingServerRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    print(f"Server loop running PID: {os.getpid()}")

    c1 = ForkingClient(ip, port)
    c1.run()

    c2 = ForkingClient(ip, port)
    c2.run()

    c1.shutdown()
    c2.shutdown()

    server.socket.close()

