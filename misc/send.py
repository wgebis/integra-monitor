import binascii
import socket
import struct
import sys
import codecs

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 7878)
sock.connect(server_address)

decode_hex = codecs.getdecoder("hex_codec")

m = decode_hex('0a41463938303032372241444d2d43494422303130364c3023393939395b23393939397c33333530203031203030375d0d')[0]

try:
    print('send socket')
    sock.sendall(m)

    sock.recv(1024)

finally:
    print('closing socket')
    sock.close()