"""
Date: 2022.04.08 15:10
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2022.04.08 15:10
"""
import select
import socket
import sys
import signal
import pickle
import struct
import argparse

SERVER_HOST = 'localhost'
CHAT_SERVER_NAME = 'server'

def send(channel:socket.socket, *args):
    buffer = pickle.dumps(args)
    value = socket.htonl(len(buffer))
    size = struct.pack("L", value)
    channel.send(size)
    channel.send(buffer)

def receive(channel:socket.socket):
    size = struct.calcsize("L")
    size = channel.recv(size)

    try:
        size = socket.ntohl(struct.unpack("L", size)[0])
    except struct.error as e:
        return ''

    buf = ''
    while len(buf)<size:
        buf = channel.recv(size-len(buf))

    return pickle.loads(buf)[0]

class ChatServer(object):
    def __init__(self, port, backlog=5):
        self.clients = 0
        self.clients_map = {}
        self.outputs = []

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((SERVER_HOST, port))
        print(f'Server listening to port: {port}')
        self.server.listen(backlog)
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signal_number, frame):
        for output in self.outputs:
            output.close()
        self.server.close()

    def get_client_name(self, client)->str:
        info = self.clients_map[client]
        host, name = info[0][0], info[1]
        return '@'.join((name, host))

    def run(self):
        inputs = [self.server, sys.stdin]
        self.outputs = []
        running = True
        while running:
            try:
                readable, writeable, exceptional = select.select(inputs, self.outputs, [])
            except select.error as e:
                break

            for s in readable:
                if s == self.server:
                    client, client_address = self.server.accept()
                    print('chat server: got connection %d from %s'%(client.fileno(), client_address))
                    client_name = receive(client).split('NAME:')[1]
                    self.clients +=1
                    send(client, 'CLIENT: %s'%client_address[0])
                    inputs.append(client)
                    self.clients_map[client]  = (client_address, client_name)
                    msg = f"Connected：New client（{self.clients}）from {self.get_client_name(client)}"
                    for output in self.outputs:
                        send(output, msg)
                    self.outputs.append(client)
                elif s == sys.stdin:
                    junk = sys.stdin.readline()
                    running=False
                else:
                    try:
                        data=receive(s)
                        msg = self.get_client_name(s)+">>"+data
                        for output in self.outputs:
                            if output!=s:
                                send(output,msg)
                            else:
                                print(f'chat server: {s.fileno()} hung up')
                                self.clients-=1
                                s.close()
                                inputs.remove(s)
                                self.outputs.remove(s)
                                msg = "hung up"
                                for output in self.outputs:
                                    send(output, msg)
                    except socket.error as e:
                        inputs.remove(s)
                        self.outputs.remove(s)
                        self.server.close()
