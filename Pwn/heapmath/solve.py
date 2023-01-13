import re
from pwn import *

r = remote('edu-ctf.zoolab.org', 10006)

# tcache chall
tcache = {}
print(r.recvline().decode()) # "----------- ** tcache chall ** -----------"
for _ in range(7):
    s = r.recvline().decode()
    print(s)
    result = re.search(r'char \*(.) = \(char \*\) malloc\((.*)\)', s).groups()
    tmp = int(result[1], 16) - 0x8
    if tmp % 0x10:
        tmp = (tmp & ~0xf) + 0x20
    else:
        tmp += 0x10
    tcache[result[0]] = tmp
ans20 = ''
ans30 = ''
ans40 = ''
for _ in range(7):
    s = r.recvline().decode()
    print(s)
    free = re.search(r'free\((.)\)', s).group(1)
    if tcache[free] == 0x20:
        ans20 = free + ' --> ' + ans20
    elif tcache[free] == 0x30:
        ans30 = free + ' --> ' + ans30
    elif tcache[free] == 0x40:
        ans40 = free + ' --> ' + ans40
ans20 += 'NULL'
ans30 += 'NULL'
ans40 += 'NULL'
print(ans20)
print(ans30)
print(ans40)
r.recvuntil(b'?\n> ')
r.sendline(ans30.encode())
r.sendline(ans40.encode())

# address chall
print(r.recvuntil(b'\n----------- ** address chall ** -----------\n').decode()) 
s = r.recvline().decode()
print(s)
result = re.search(r'assert\( (.) == (.*) \)', s).groups()
s = r.recvuntil(b'\n> ').decode()
print(s)
target = re.search(r'(.) == ?', s).group(1)
tmp = int(result[1], 16)
for i in range(ord(target) - ord(result[0])):
    tmp += tcache[chr(ord(result[0]) + i)]
r.sendline(hex(tmp).encode())

# index chall
print(r.recvuntil(b'\n----------- ** index chall ** -----------\n').decode()) 
s = r.recvline().decode()
print(s)
size = int(re.search(r'malloc\((.*)\)', s).group(1), 16)
print(r.recvline().decode())
s = r.recvline().decode()
print(s)
index = int(re.search(r'Y\[(.)\]', s).group(1), 10)
print(r.recvuntil(b'\n> ').decode()) 
ans = size/8 + 2 + index
r.sendline(str(int(ans)).encode())

# tcache fd chall
print(r.recvuntil(b'\n----------- ** tcache fd chall ** -----------\n').decode()) 
s = r.recvuntil(b' );\n').decode()
print(s)
address = int(re.search(r'assert\( Y == (.*) \)', s).group(1), 16)
print(r.recvuntil(b'\n> ').decode())
ans = address - 0x10 - size
print(hex(ans))
r.sendline(hex(ans).encode())

# tcache fd chall
print(r.recvuntil(b'\n----------- ** fastbin fd chall (final) ** -----------\n').decode()) 
s = r.recvuntil(b' );\n').decode()
print(s)
address = int(re.search(r'assert\( Y == (.*) \)', s).group(1), 16)
ans = address - 0x20 - size
r.sendline(hex(ans).encode())
r.interactive()