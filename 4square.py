import re
import itertools

DECRYPT_ALL_PERMUTATIONS_OF_TEXT = False

def generate_table(key = ''):
    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    table = [[0] * 5 for row in range(5)]
    key = re.sub(r'[\W]', '', key).upper()

    for row in range(5):
        for col in range(5):
            if len(key):
                table[row][col] = key[0]
                alphabet = alphabet.replace(key[0], '')
                key = key.replace(key[0], '')
            else:
                table[row][col] = alphabet[0]
                alphabet = alphabet[1:]
    return table

def decrypt(TL, TR, BL, BR, words):
    ciphertext = ''
    words = re.sub(r'[\W]', '', words).upper().replace('J', '')

    for i in range(0, len(words), 2):
        digraphs = words[i:i+2]
        ciphertext += unmangle(TL, TR, BL, BR, digraphs)
    return ciphertext

def unmangle(TL, TR, BL, BR, digraphs):
    a = position(TR, digraphs[0])
    b = position(BL, digraphs[1])
    return TL[a[0]][b[1]] + BR[b[0]][a[1]]

def position(table, ch):
    for row in range(5):
        for col in range(5):
            if table[row][col] == ch:
                return (row, col)
    return (None, None)

if __name__ == '__main__':
    text = 'THWODDLNFR' #AFORECLOUD

    TL = generate_table('OUTCAST')
    TR = generate_table('TWOFACED')
    BL = generate_table('GRUDGE')
    BR = generate_table('')

    with open('output.csv', 'w') as f:
        if DECRYPT_ALL_PERMUTATIONS_OF_TEXT:
            nums = list(text)
            permutations = list(itertools.permutations(nums))
            for permutation in permutations:
                perm = ''.join(permutation)
                res = decrypt(TL, TR, BL, BR, perm)
                f.write(perm + ' = ' + res + '\n')
        else:
            f.write(text + ' = ' + decrypt(TL, TR, BL, BR, text) + '\n')