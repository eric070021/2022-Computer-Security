#!/usr/bin/env python3

import sys
from pwn import *

p = remote('edu-ctf.zoolab.org',10101)

ct = p.readline()[:-1].decode()
ct = bytes.fromhex(ct)
iv, ct1, ct2, ct3 = ct[:16], ct[16:32], ct[32:48], ct[48:64]
flag = bytearray(48) 
index = 47

count1 = 0
_iv, _ct1, _ct2, _ct3 = bytearray(ct[:16]), bytearray(ct[16:32]), bytearray(ct[32:48]), bytearray(ct[48:64])
for i in range(15, -1, -1):
    count2 = count1
    count1 = 0
    for j in range(256):
        _ct2[i] = j
        p.sendline(bytearray.hex(_ct2+_ct3))
        reply = p.readline()[:-1].decode()
        if reply == 'Well received :)':
            count1 += 1
            if j != ct2[i]:
                flag[index] = ct2[i] ^ _ct2[i] ^ 128

    if abs(count1 - count2) == 1:
        flag[index] = 128
    _ct2[i] = 0 ^ flag[index] ^ ct2[i]
    index -= 1

_iv, _ct1, _ct2, _ct3 = bytearray(ct[:16]), bytearray(ct[16:32]), bytearray(ct[32:48]), bytearray(ct[48:64])
for i in range(15, -1, -1):
    for j in range(256):
        _ct1[i] = j
        p.sendline(bytearray.hex(_ct1+_ct2))
        reply = p.readline()[:-1].decode()
        if reply == 'Well received :)':
            flag[index] = ct1[i] ^ _ct1[i] ^ 128
            break
    _ct1[i] = 0 ^ flag[index] ^ ct1[i]
    index -= 1

_iv, _ct1, _ct2, _ct3 = bytearray(ct[:16]), bytearray(ct[16:32]), bytearray(ct[32:48]), bytearray(ct[48:64])
for i in range(15, -1, -1):
    for j in range(256):
        _iv[i] = j
        p.sendline(bytearray.hex(_iv+_ct1))
        reply = p.readline()[:-1].decode()
        if reply == 'Well received :)':
            flag[index] = _iv[i] ^ iv[i] ^ 128
            break
    _iv[i] = 0 ^ flag[index] ^ iv[i]
    index -= 1

print(bytes(flag))