from random import *

class Generator:
    def __init__(self):
        pass
    def gen_one_bit(self):
        #pass
        raise NotImplementedError('subclasses must override generate_byte()')
    def gen_one_byte(self):
        byte = '0b'
        for i in range(8):
            byte+=str(self.gen_one_bit())
        return int(byte,2)
    def gen_bytes(self, count):
        arr = []
        for i in range(count):
            #if len(arr)%10000 == 0:
            #    print("Ok")
            arr.append(self.gen_one_byte())
        return arr
    
class PythonGen(Generator):
    def __init__(self):
        pass
    def gen_one_byte(self):
        return randrange(0,255)

class LehmerLowGen(Generator):
    def __init__(self, a = 2**16 + 1, x_0 = 1, c = 119, m = 2**32):
        self.a = a
        self.c = c
        self.m = m
        self.x_0 = randrange(65536,131072)
    def gen_one_byte(self):
        self.x_0 = (self.a*self.x_0 + self.c)%self.m
        return int(str(bin(self.x_0)[2:10]),2)

class LehmerHighGen(LehmerLowGen):
    def gen_one_byte(self):
        self.x_0 = (self.a*self.x_0 + self.c)%self.m # Проблему з бітами вирішив
        return int(str(bin(self.x_0))[:10],2)

class L20Gen(Generator):
    def __init__(self, n):
        self.arr = []
        for i in range(n):
            n = randrange(0,2)
            self.arr.append(n)
            
    def gen_one_bit(self):
        if len(self.arr) > 2**20 -1:
            raise "Stop long"
        t = len(self.arr)
        bit = self.arr[t-3] ^ self.arr[t-5] ^self.arr[t-9] ^ self.arr[t-20]
        self.arr.append(bit)
        return self.arr
        
    def gen_one_byte(self):
        for i in range(8):
            self.gen_one_bit()
        last_8 = self.arr[len(self.arr)-8:]
        #print("Last_8:",last_8)
        result = int(str(last_8[0]),2)
        for i in range(1,8):
            result = result<<1 | int(str(last_8[i]),2)
        return result

class L89Gen(L20Gen):
    def gen_one_bit(self):
        if len(self.arr) > 2**20 -1:
            raise "Stop long"
        t = len(self.arr)
        bit = self.arr[t-38] ^ self.arr[t-89]
        self.arr.append(bit)
        return bit
    
class L9Gen(L20Gen):
    def gen_one_bit(self):
        if len(self.arr) > 2**9 -1:
            pass
            #raise "Stop long"
        t = len(self.arr)-1
        bit = self.arr[t-0] ^ self.arr[t-1] ^ self.arr[t-3]^self.arr[t-4]
        self.arr.append(bit)
        return bit
    
class L10Gen(L20Gen):
    def gen_one_bit(self):
        if len(self.arr) > 2**10 -1:
            pass
            #raise "Stop long"
        t = len(self.arr)-1
        bit = self.arr[t] ^ self.arr[t-3]
        self.arr.append(bit)
        return bit
    
class L11Gen(L20Gen):
    def gen_one_bit(self):
        if len(self.arr) > 2**11 -1:
            pass
            #raise "Stop long"
        t = len(self.arr)-1
        bit = self.arr[t] ^ self.arr[t-2]
        self.arr.append(bit)
        return bit
        
class GeffeGen(Generator):
    def __init__(self):
        self.L9 = L9Gen(9)
        self.L10 = L10Gen(10)
        self.L11 = L11Gen(11)
    def gen_one_bit(self):
        s = self.L10.gen_one_bit()
        x = self.L11.gen_one_bit()
        y = self.L9.gen_one_bit()
        return s&x^(1^s)&y


class WolframGen(Generator):
    def __init__(self):
        self.r = randrange(1,255)
    def gen_one_bit(self):
        bit = self.r % 2
        self.r = (self.r << 1) ^ (self.r | (self.r >> 1)) % 255
        return bit
    
    
class BMGen(Generator):
    def __init__(self):
        self.p = int("CEA42B987C44FA642D80AD9F51F10457690DEF10C83D0BC1BCEE12FC3B6093E3",16)
        self.a = int("5B88C41246790891C095E2878880342E88C79974303BD0400B090FE38A688356",16)
        self.T = randrange(self.p)
        self.q = int("675215CC3E227D3216C056CFA8F8822BB486F788641E85E0DE77097E1DB049F1",16)
        self.temp = (self.p - 1)/2
    def gen_one_bit(self):
        bit = 1 if self.T < self.temp else 0
        self.T = pow(self.a, self.T, self.p)
        return bit
    
class BMGen_byte(BMGen):
    def gen_one_byte(self):
        byte = self.T/((self.p-1)/256)
        self.T = pow(self.a, self.T, self.p)
        return int(byte)
        
class BBSGen(Generator):
    def __init__(self):
        self.p = int("D5BBB96D30086EC484EBA3D7F9CAEB07",16)
        self.q = int("425D2B9BFDB25B9CF6C416CC6E37B59C1F",16)
        self.r = randrange(1,255)
        self.n = self.p * self.q
        
    def gen_one_bit(self):
        self.r = pow(self.r, 2, self.n)
        bit = self.r%2
        return bit

class BBSGen_byte(BBSGen):    
    def gen_one_byte(self):
        self.r = pow(self.r, 2, self.n)
        bit = self.r % 256
        return bit

class LibGen(Generator):
    def __init__(self):
        self.file = open("checktext.txt", "r", encoding="ansi")
        self.text = self.file.read().replace(" ", "")
        self.count = 0
    def gen_one_byte(self):
        if self.count < len(self.text):
            result = ord(self.text[self.count])%256
            self.count+=1
        else:
            self.count = 0
            result = ord(self.text[self.count])%256
        return result



