a = 0x37ee3030a4e730d0a930303030309dc330e9c630e66f30ac30033030e070c4f9fc3016b356303469af8f30092a613030e69830ba306c30da361d3052182f308d10
b = 0x41924147efbc658bf26f755f6d75df9a5fb38f61893161f53f5d61698f219d96a7615cec035f703cc0dc79566e256f5fbddd72ff733469b56d585f0c494072c85d # compare byte array
c = 0x3030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030303030 # send 65 '0'
flag = hex(a ^ b ^ c).replace('0x','')
print(bytes.fromhex(flag).decode())