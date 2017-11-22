#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Servidor de eco en UDP simple."""

import os
import sys
import socketserver


"""Message types."""

METHODS = ['INVITE', 'ACK', 'BYE']
Trying = b'SIP/2.0 100 Trying\r\n'
Ringing = b'SIP/2.0 180 Ringing\r\n'
OK = b'SIP/2.0 200 OK\r\n\r\n'
Bad_Request = b'SIP/2.0 400 Bad Request\r\n\r\n'
Method_Not_Allowed = b'SIP/2.0 405 Method Not Allowed\r\n\r\n'


class EchoHandler(socketserver.DatagramRequestHandler):
    """Client handler requests."""

    def handle(self):
        """Recieve INVITE, ACK, BYE & Sent 100, 180, 200, 400 and 405."""
        while 1:
            Lines = self.rfile.read()
            if len(Lines) == 0:
                break

            Info = Lines.decode('utf-8').split()
            METHOD = Info[0]
            NAME = Info[1].split(':')[1].split('@')[0]
            print(METHOD + ' recieved from: ' + NAME)

            if METHOD == 'INVITE':
                self.wfile.write(Trying + Ringing + OK)
            elif METHOD == 'ACK':
                Exe = './mp32rtp -i 127.0.0.1 -p 23032 < ' + AUDIO_FILE
                print("Vamos a ejecutar", Exe)
                os.system(Exe)
            elif METHOD == 'BYE':
                self.wfile.write(OK)
            elif METHOD not in METHODS:
                self.wfile.write(Method_Not_Allowed)
            else:
                self.wfile.write(Bad_Request)


if __name__ == "__main__":

    try:
        IP = sys.argv[1]
        PORT = int(sys.argv[2])
        AUDIO_FILE = sys.argv[3]
        if PORT < 1024:
            sys.exit(" Port invalid!")
        if not os.path.exists(AUDIO_FILE):
            sys.exit(" File don't exits!")

        serv = socketserver.UDPServer((IP, PORT), EchoHandler)
        print("Listening...")
        serv.serve_forever()

    except IndexError:
        sys.exit(" Usage: python3 server.py IP port audio_file")
    except KeyboardInterrupt:
        print("\n" + "Servidor finalizado")
