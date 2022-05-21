class Formatter:
    def __init__(self):
        pass

    def hex2bin(self, x):
        '''hex string을 bin string으로 변환 (항상 8비트를 리턴하도록 패딩 적용)'''
        assert(len(x) % 2 == 0)
        binstr = ''
        for i in range(len(x) // 2):
            data = bin(int(x[i*2:i*2+2], 16))[2:]
            lead_zeros = 8 - len(data)
            binstr += '0'*lead_zeros + data
        return binstr
    
    def int2bin6(self, x):
        '''integer를 bin string으로 변환 (항상 6비트를 리턴하도록 패딩 적용)'''
        assert(x < 0b1000000)
        binstr = ''
        data = bin(x)[2:]
        if len(data) < 6:
            lead_zeros = 6 - len(data)
            binstr += '0'*lead_zeros
        binstr += data
        return binstr

class Base64:
    def __init__(self):
        self.t = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
        self.pad = '='

    def encode(self, x):
        '''Base64 인코딩'''
        encoded = ''
        f = Formatter()
        # 3바이트 단위로 나눠떨어지는 부분은 base64 테이블에서 치환
        for i in range(len(x) // 6):
            state = f.hex2bin(x[i*6:i*6+6])
            encoded += self.t[int(state[0:6], 2)]
            encoded += self.t[int(state[6:12], 2)]
            encoded += self.t[int(state[12:18], 2)]
            encoded += self.t[int(state[18:24], 2)]

        # 3바이트 단위로 나눠떨어지지 않는 부분은 별도로 패딩 추가
        remains = len(x) // 2 % 3
        if remains == 1:
            state = f.hex2bin(x[-remains*2:])
            encoded += self.t[int(state[0:6], 2)]
            encoded += self.t[int(state[6:8]+'0'*4, 2)]
            encoded += self.pad * (3-remains)
        elif remains == 2:
            state = x[-remains*2*2]
            encoded += self.t[int(state[0:6], 2)]
            encoded += self.t[int(state[6:12], 2)]
            encoded += self.t[int(state[12:16]+'0'*2, 2)]
            encoded += self.pad * (3-remains)
        
        return encoded

    def decode(self, x):
        '''Base64 디코딩 구현하기'''
        decoded = ''
        state = ''
        f = Formatter()
        for i in range(len(x)):
            # 패딩 문자는 원본을 디코딩 하는 것과 관계 없으므로 탈출
            if x[i] == self.pad:
                break
            state += f.int2bin6(self.t.index(x[i]))
        assert(len(state)%8 == 0)
        for i in range(len(state) // 8):
            decoded += chr(int(state[i*8:i*8+8], 2))
        return decoded

def main():
    b64 = Base64()
    text = b'49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
    encoded = b64.encode(text)
    print(encoded)  # SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t
    decoded = b64.decode(encoded)
    print(decoded)  # I'm killing your brain like a poisonous mushroom

main()
