#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" Servidor de eco en UDP simple. """

import os
import sys
import socketserver


try:
    IP = sys.argv[1]
    PORT = int(sys.argv[2])
    AUDIO_FILE = sys.argv[3]
except IndexError:
    sys.exit("python3 server.py IP port audio_file")


METHODS = ['INVITE', 'ACK', 'BYE']

class EchoHandler(socketserver.DatagramRequestHandler):

    def handle(self):

        while 1:
            Lines = self.rfile.read()
            if len(Lines) == 0:
                break

            Info = Lines.decode('utf-8').split()
            METHOD = Info[0]
            NAME = Info[1].split(':')[1].split('@')[0]
            print(METHOD + ' recieved from: ' + NAME)

            if METHOD in METHODS:
                if METHOD == 'INVITE':
                    self.wfile.write(b'SIP/2.0 100 Trying\r\n')
                    self.wfile.write(b'SIP/2.0 180 Ringing\r\n')
                    self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')

                if METHOD == 'ACK':
                    Exe = './mp32rtp -i 127.0.0.1 -p 23032 < ' + AUDIO_FILE
                    print("Vamos a ejecutar", Exe)
                    os.system(Exe)

                if METHOD == 'BYE':
                    self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')

                else:
                    self.wfile.write(b'SIP/2.0 400 Bad Request\r\n\r\n')

            else:
                    self.wfile.write(b'SIP/2.0 405 Method Not Allowed\r\n\r\n')
        

if __name__ == "__main__":
    serv = socketserver.UDPServer((IP, PORT), EchoHandler)
    print("Listening...")

    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("\n" + "Servidor finalizado")
