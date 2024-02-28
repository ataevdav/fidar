ENG_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def create_table(alphabet: str):
    array = [[] for i in range(27)]
    array[0].append(' ')
    for i in alphabet:
        array[0].append(i)
    for i in range(1, 27):
        array[i].append(alphabet[i - 1])
    for i in range(1, 27):
            for j in alphabet[i - 1:] + alphabet[:i - 1]:
                array[i].append(j)
    return array

def key_validation(key: str, alphabet: str=ENG_ALPHABET):
    for i in key:
        if i not in alphabet:
            return False
    return True


def encrypt(string: str, key: str, alphabet: str=ENG_ALPHABET):
    array = create_table(alphabet)
    out = ''
    nkey = ''
    spcs = 0
    for i in range(len(string)):
        nkey += key[i % len(key)]
    for y in range(len(string)):
        if string[y] in alphabet:
            out += array[alphabet.find(string[y]) + 1][alphabet.find(nkey[y - spcs]) + 1]
        else:
            spcs += 1
            out += string[y]
    return out


def decrypt(string: str, key: str, alphabet: str=ENG_ALPHABET):
    array = create_table(alphabet)
    out = ''
    nkey = ''
    spcs = 0
    for i in range(len(string)):
        nkey += key[i % len(key)]
    for y in range(len(string)):
        if string[y] in alphabet:
            out += array[0][array[alphabet.find(nkey[y - spcs]) + 1][1:].index(string[y]) + 1]
        else:
            spcs += 1
            out += string[y]
    return out
