#!/usr/bin/env python3
#sender.py

import os, sys, getopt, time
from encrypt import encrypt
from netinterface import network_interface
from decrypt import decrypt

NET_PATH = './'
OWN_ADDR = 'A'

# test session keys
session_msg_key = b'abcdefghijklmnopqrstuvwxyz1234567890'
session_mac_key = b'zyxwvutsrqponmlkjihgfedcba0987654321'

# ------------
# main program
# ------------

try:
	opts, args = getopt.getopt(sys.argv[1:], shortopts='hp:a:', longopts=['help', 'path=', 'addr='])
except getopt.GetoptError:
	print('Usage: python sender.py -p <network path> -a <own addr>')
	sys.exit(1)

for opt, arg in opts:
	if opt == '-h' or opt == '--help':
		print('Usage: python sender.py -p <network path> -a <own addr>')
		sys.exit(0)
	elif opt == '-p' or opt == '--path':
		NET_PATH = arg
	elif opt == '-a' or opt == '--addr':
		OWN_ADDR = arg

if (NET_PATH[-1] != '/') and (NET_PATH[-1] != '\\'): NET_PATH += '/'

if not os.access(NET_PATH, os.F_OK):
	print('Error: Cannot access path ' + NET_PATH)
	sys.exit(1)

if len(OWN_ADDR) > 1: OWN_ADDR = OWN_ADDR[0]

if OWN_ADDR not in network_interface.addr_space:
	print('Error: Invalid address ' + OWN_ADDR)
	sys.exit(1)

# main loop
netif = network_interface(NET_PATH, OWN_ADDR)
encryptionEngine = encrypt(OWN_ADDR, session_msg_key, session_mac_key)
decryptionEngine = decrypt(session_msg_key,session_mac_key)
receive_mode = True
print('Main loop started...')
while True:
	msg = input('Type a message: ')
	dst = input('Type a destination address: ')

	encryptionEngine.send(msg, dst, netif)
	while receive_mode:
		status, msg = netif.receive_msg(blocking=False)      # when returns, status is True and msg contains a message
		if status:
			label, msg = msg[:3], msg[3:]
			if (label == b'msg'):
				decryptionEngine.generate_derived_msg_key(msg)
			elif (label == b'mac'):
				decryptionEngine.generate_derived_mac_key(msg)
			elif (label == b'enc'):
				if decryptionEngine.has_keys():
					decrypt_msg = decryptionEngine.decrypt_msg(msg)
					print(decrypt_msg)
					receive_mode = False
				else:
					print("you ain't got no keys bruh")

	if input('Continue? (y/n): ') == 'n': break
	receive_mode = True
