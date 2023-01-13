f = open('packet.txt', 'r')
text = f.read()
fp = open("flag.png", "wb")
key ='0vCh8RrvqkrbxN9Q7Ydx\0'
for i in range(int(len(text)/2)):
    decode = int(text[2*i]+text[2*i+1],16) ^ ord(key[i%21])
    #print(decode, end='')
    fp.write(decode.to_bytes(1, 'little'))