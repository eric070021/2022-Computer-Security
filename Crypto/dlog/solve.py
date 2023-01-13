from pwn import *
from sage.all import *
from Crypto.Util.number import getPrime, long_to_bytes, isPrime

p = 96549462741776062767041902973858681126822696756293536960348268616662675484359728992399038216105466537892135164350944210611191474648681724396796895648393671353704122400357194312226444784328148076008574262187619932510359288362767862188322121756996881680333128527852629594651443545256738398144848370393302835567
b = 11
def primegen():
    while True:
        p = 2
        while p.bit_length() < 1002:
            p *= getPrime(16)
        p *= getPrime(9)
        p += 1
        if p.bit_length() == 1024:
            print('good', end = '')
        if isPrime(p):
            print('nice', end = '')
        #print(p.bit_length())
        if isPrime(p) and p.bit_length() == 1024:
            break
    return p

r = remote('edu-ctf.zoolab.org',10103)
r.recvuntil(b"give me a prime")
p = primegen()
r.sendline(str(p).encode())
r.recvuntil(b"give me a number")
r.sendline(str(b).encode())
r.recvuntil(b"The hint about my secret:")
ct = int(r.recvline(keepends=False).decode())
b = mod(b, p)
ct = mod(ct, p)
flag = discrete_log(ct, b)
print(long_to_bytes(flag))
r.close()
