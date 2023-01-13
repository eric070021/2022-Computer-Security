from pwn import *
from Crypto.Util.number import long_to_bytes, inverse
from sage.all import *

while True:
    ans = []
    p = remote('edu-ctf.zoolab.org',10104)
    prime = int(p.recvline(keepends=False).decode())
    if not mod(prime - 1, prime).is_square():
        p.close()
        continue
    qr = mod(prime - 1, prime).sqrt()
    p.sendline(str(qr).encode())
    reply = p.recvline(keepends=False).decode()
    if reply != 'Bad :(':
        ans = [int(reply), int(qr)]

    if ans:
        print(long_to_bytes(ans[0]))
        print(long_to_bytes(ans[0] * inverse(ans[1], prime) % prime))
        print(long_to_bytes(ans[0] * inverse(pow(ans[1], 2, prime), prime) % prime))
        print(long_to_bytes(ans[0] * inverse(pow(ans[1], 3, prime), prime) % prime))
        break
    p.close()
