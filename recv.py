import socket
from Crypto.Cipher import AES
import base64
import os
import sys

def AES_Dec(key, msg):
	BLOCK_SIZE = 16
	PADDING = '{'
	pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
	DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
	cipher = AES.new(key)
	return DecodeAES(cipher, msg)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 44))
s.listen(1)
client, addr = s.accept()
AESkey = 'aaaaaaaaaaaaaaaa'

while True:
	try:
		print(AES_Dec(AESkey,client.recv(1028)).strip())
	except KeyboardInterrupt:
		s.close()
		exit()
