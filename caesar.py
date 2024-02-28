def encrypt(string: str, key: int):
    ans = ''
    if key < 0:
        key = key % 26 + 26
    for i in string:
        if i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            if (ord(i) + (key % 26) - 64) % 26 == 0:
                ans += chr((ord(i) + (key % 26) - 64) % 26 + 64 + 26)
            else:
                ans += chr((ord(i) + (key % 26) - 64) % 26 + 64)
        else:
            ans += i
    return ans


def decrypt(string: str, key: int):
    if key > 0:
        return encrypt(string, 26 - (key % 26))
    else:
        return encrypt(string, (abs(key) % 26))