alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!? '


def create_table(alphabet: str):
    q = len(alphabet)
    if q ** 0.5 > int(q ** 0.5):
        q = int(q ** 0.5 + 1)
    else:
        q = int(q ** 0.5)

    array = [[] for i in range(q)]
    for y in range(q):
        for x in range(q):
            if y * q + x < len(alphabet):
                array[y].append(alphabet[y * q + x])
            else:
                array[y].append('')
    return array


def in_validation(string: str, alphabet: str):
    string = string.upper()
    lstr = list(set(list(string)))
    for i in lstr:
        if i not in alphabet:
            return False
    return True

def out_validation(string: str, alphabet: str):
    array = create_table(alphabet)
    for i in string.split('-'):
        a = int(i) // 10
        b = int(i) % 10
        try:
            if array[b - 1][a - 1] == '':
                return False
        except IndexError:
            return False
    return True


def encrypt(string: str, alphabet: str):
    array = create_table(alphabet)
    string = string.upper()
    out = []
    for i in string:
        for a in range(7):
            if i in array[a]:
                out.append(str((''.join(array[a]).index(i) + 1) * 10 + a + 1))
    return '-'.join(out)


def decrypt(string: str, alphabet: str):
    array = create_table(alphabet)
    out = []
    for i in string.split('-'):
        a = int(i) // 10
        b = int(i) % 10
        out.append(array[b - 1][a - 1])
    return ''.join(out)
