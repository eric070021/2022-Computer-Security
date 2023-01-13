import numpy as np

state = 0

result = [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0]

xor = np.fromstring('1,1,0,1,1,0,1,0,0,1,1,1,1,0,0,0,0,1,0,1,1,1,1,1,1,1,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1', dtype=int, sep=',')

def getbit():
    global state
    state <<= 1
    if state & (1 << 64):
        state ^= 0x1da785fc480000001
        return 1
    return 0

def mat_mulmod(A, B, time):
    for _ in range(time):
        A = (A @ B) % 2
    return A

# construct companion matrix
C = np.zeros((64,64), dtype=int)
for i in range(63):
    C[i][i+1] = 1
C[-1] = xor[::-1]
C = C.transpose()

# construct W matirx
w0 = np.zeros(64, dtype=int)
w0[-1] = 1
W = np.zeros((64,64), dtype=int)
c12468  = mat_mulmod(C, C, 12467)
c37 = mat_mulmod(C, C, 36)
for i in range(64):
    W[i] = w0 @ mat_mulmod(c12468, c37, i)

# Output matrix
Y = np.array(result[-70:-6], dtype=int)

# Guass Jordan
dict = {}
for column in range(64):
    for pivot in range(64):
        if(W[pivot][column] == 1 and dict.get(pivot) == None):
            dict[pivot] = True
            break
    for row in range(64):
        if row != pivot and W[row][column] == 1:
            W[row] = W[row] ^ W[pivot]
            Y[row] = Y[row] ^ Y[pivot]

# Solve X
X = np.zeros(64, dtype=int)
for column in range(64):
    for row in range(64):
        if W[row][column] == 1:
            X[column] = Y[row]

for i in range(64):
    state += int(X[i]) * (1 << i)

output = []
for _ in range(336):
    for __ in range(36):
        getbit()
    output.append(getbit())

# Recover flag
flag = ''
for i in range(42):
    temp = ''
    for j in range(8):
        temp += str(output[i*8 + j] ^ result[i*8 + j])
    temp = int(temp, 2)
    flag += chr(temp)

print(flag)
