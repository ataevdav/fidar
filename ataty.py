from PIL import Image
import random as r

def text_validation(string: str):
    for i in string:
        if ord(i) > 255:
            return False
    return True


def encrypt(string: str, image_key: str, file_name: str):
    img = Image.open(image_key).convert('L')
    size = img.size
    new_img = Image.new('L', size, 'white')
    new_img.paste(img)
    de_key = []
    px_out = (-1, -1)
    for i in range(len(string)):
        px_in = (i % size[0], i // size[0])
        px_out = (r.randint(0, size[0] - 1), r.randint(0, size[1] - 1))
        if px_out in de_key:
            while px_out in de_key:
                px_out = (r.randint(0, size[0] - 1), r.randint(0, size[1] - 1))
        de_key.append(px_out)
        new_img.putpixel(px_out, (ord(string[i]) + img.getpixel((px_in))) % 256)
    for i in range(len(de_key)):
        de_key[i] = hex(de_key[i][0])[2:].zfill(4) + hex(de_key[i][1])[2:].zfill(4)
    de_key = ''.join(de_key)
    new_img.show()
    img.close()
    new_img.save(file_name)
    new_img.close()
    return new_img, de_key


def decrypt(cipher, image_key, de_key):
    cipher = Image.open(cipher)
    image_key = Image.open(image_key).convert('L')
    ans = ''
    de_key = list(map(lambda x: int(x, 16), [de_key[i:i + 4] for i in range(0, len(de_key), 4)]))
    de_key = [(de_key[i], de_key[i+1]) for i in range(0, len(de_key), 2)]
    for i in range(len(de_key)):
        size = image_key.size
        let = chr((cipher.getpixel(de_key[i]) - image_key.getpixel((i % size[0], i // size[0]))) % 256)
        ans += let
    image_key.close()
    cipher.close()
    return ans