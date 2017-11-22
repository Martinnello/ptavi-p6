#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Programa cliente que abre un socket a un servidor."""

import sys
import socket


try:

    METHOD = str.upper(sys.argv[1])
    CLIENT = sys.argv[2]

    NAME = CLIENT.split('@')[0]
    IP = CLIENT.split('@')[1].split(':')[0]
    PORT = int(CLIENT.split(':')[1])

except IndexError:
    sys.exit(" Usage: python3 client.py method receiver@IP:SIPport ")

"""Configuramos y lo atamos a un servidor para establecer comunicación."""

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((IP, PORT))
    Mess = (' sip:' + NAME + '@' + IP + ':' + str(PORT) + ' SIP/2.0')
    my_socket.send(bytes(METHOD + Mess, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
    Reply = data.decode('utf-8').split()

    if Reply[1] == "100" and Reply[4] == "180" and Reply[7] == "200":
        my_socket.send(bytes('ACK' + Mess, 'utf-8') + b'\r\n')

    print(data.decode('utf-8'))
    print("Terminando socket...")

print("Fin")
