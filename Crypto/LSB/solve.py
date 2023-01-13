#!/usr/bin/env python3

import sys
from pwn import *
from Crypto.Util.number import long_to_bytes

p = remote('edu-ctf.zoolab.org',10102)

n = int(p.readline()[:-1].decode())
e = int(p.readline()[:-1].decode())
enc = int(p.readline()[:-1].decode())

flag = 0
count = 0
i = 0
a = 0
while count < 20:
    p.sendline(str((pow(3, -e * i, n) * enc) % n))
    reply = int(p.readline()[:-1].decode())
    aa = (reply - (a * pow(3, -1, n) % n)) % 3
    print(aa)
    a = aa + a * pow(3, -1, n)
    flag += pow(3, i) * aa

    if aa == 0:
        count += 1
    else:
        count = 0
    i += 1

print(long_to_bytes(flag))