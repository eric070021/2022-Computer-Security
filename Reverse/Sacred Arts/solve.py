from pwn import *

arr = [0x8D909984B8BEBAB3, 0x8D9A929E98D18B92, 0xD0888BD19290D29C,
0x8C9DC08F978FBDD1, 0xD9C7C7CCCDCB92C2, 0xC8CFC7CEC2BE8D91, 0xFFFFFFFFFFFFCF82]

def convert(h):
    b = 0xFFFFFFFFFFFFFFFF
    a = bin(h)
    a = a[:-16] + a[-8:] + a[-16:-8]
    a = int(a, 2)
    a = (a ^ b) + 1
    return p64(a)
    #a = hex(a).replace('0x', '')
 
flag = ''
for h in arr:
    r = convert(h)
    print(r.decode(), end='')

