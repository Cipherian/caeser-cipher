import ssl
import nltk
import operator
from collections import Counter

alphabet: list[str] = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
                      "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

alphabet_upper = [s.upper() for s in alphabet]



def download():
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    nltk.download("words", quiet=True)
    nltk.download('names', quiet=True)




from nltk.corpus import words, names

word_list = words.words()
name_list = names.words()

def encrypt(string: str, key: int):
    encrypted_output: str = ""

    for letter in string:
        if letter in alphabet:
            temp = (alphabet.index(letter.lower()) + key) % len(alphabet)
            encrypted_output += alphabet[temp]
        elif letter in alphabet_upper:
            temp = (alphabet_upper.index(letter.upper()) + key) % len(alphabet)
            encrypted_output += alphabet_upper[temp]
        else:
            encrypted_output += str(letter)
    return encrypted_output

def decrypt(string: str, key: int):
    return encrypt(string, -key)


def crack(string: str):
    decrypt_dict: dict = {}
    split_string = string.split()

    for letter in split_string:
        for num in range(len(alphabet)):
            decrypt_attempt: str = decrypt(letter, num)
            if decrypt_attempt.lower() in word_list:
                if num in decrypt_dict:
                    decrypt_dict[num] += 1
                else:
                    decrypt_dict[num] = 1
    key: int = max(decrypt_dict.items(), key=operator.itemgetter(1))[0]
    #  https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
    if decrypt_dict[key] >= len(split_string) // 2:
        return decrypt(string, key)

    return ""


if __name__ == "__main__":
    test = encrypt('Hello, how are you?', 5)
    print(crack(test))
    test2 = encrypt('To be, or not To bE that is the answer', 11)
    print(crack(test2))

