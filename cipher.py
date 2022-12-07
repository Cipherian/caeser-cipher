import ssl
import nltk
import operator
from collections import Counter
from nltk.corpus import words, names
def download():
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context


    nltk.download("words", quiet=True)
    nltk.download('names', quiet=True)


def languages(language: str):
    english_alphabet: list[str] = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
                           "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

    german_alphabet = {
        "A": "Anton",
        "Ä": "Ärger",
        "B": "Berta",
        "C": "Cäsar",
        "Ch": "Charlotte",
        "D": "Dora",
        "E": "Emil",
        "F": "Friedrich",
        "G": "Gustav",
        "H": "Heinrich",
        "I": "Ida",
        "J": "Joseph Julius",
        "K": "Kaufmann",
        "L": "Ludwig",
        "M": "Martha",
        "N": "Nordpol",
        "O": "Otto",
        "Ö": "Ökonom",
        "P": "Paula",
        "Q": "Quelle",
        "R": "Richard",
        "S": "Samuel",
        "Sch": "Schule",
        "ß": "Eszett",
        "T": "Theodor",
        "U": "Ulrich",
        "Ü": "Übermut",
        "V": "Viktor",
        "W": "Wilhelm",
        "X": "Xanthippe",
        "Y": "Ypsilon",
        "Z": "Zacharias"
    }

    german_alphabet_list: list[str] = []

    for keys in german_alphabet:
        german_alphabet_list.append(keys.lower())

    if language == 'de':
        return german_alphabet_list
    elif language == 'en':
        return english_alphabet



def encrypt(string: str, key: int, language: str = languages('en')) -> str:
    encrypted_output: str = ""
    alphabet_upper = [s.upper() for s in language]

    for letter in string:
        if letter in language:
            temp = (language.index(letter.lower()) + key) % len(language)
            encrypted_output += language[temp]
        elif letter in alphabet_upper:
            temp = (alphabet_upper.index(letter.upper()) + key) % len(language)
            encrypted_output += alphabet_upper[temp]
        else:
            encrypted_output += str(letter)
    return encrypted_output

def decrypt(string: str, key: int, language = languages('en')):
    return encrypt(string, -key, language)


def crack(string: str, language = languages('en')):
    download()
    word_list = words.words()
    name_list = names.words()
    german_list = []
    if language == languages('de'):
        with open('german.dic', 'rb') as file:
            while line := file.readline().rstrip():
                german_list.append(line)

    print(german_list)
    decrypt_dict: dict = {}
    split_string = string.split()
    print(decrypt_dict)

    for letter in split_string:
        for num in range(len(language)):
            decrypt_attempt: str = decrypt(letter, num, language)
            if decrypt_attempt.lower() in word_list:
                if num in decrypt_dict:
                    decrypt_dict[num] += 1
                else:
                    decrypt_dict[num] = 1
    key: int = max(decrypt_dict.items(), key=operator.itemgetter(1))[0]
    #  https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
    if decrypt_dict[key] >= len(split_string) // 2:
        return decrypt(string, key, language)

    return ""


if __name__ == "__main__":
    test = encrypt('Der du von dem Himmel bist \n Der du von dem Himmel bist, \n Alles Leid und Schmerzen stillest, \n Den, der doppelt elend ist, \nDoppelt mit Erquickung füllest; \n Ach, ich bin des Treibens müde! \n Was soll all der Schmerz und Lust? \n Süßer Friede, \n Komm, ach komm in meine Brust!', 5, language = languages('de'))
    print(test)
    print(crack(test, language=languages('de')))
    # test2 = encrypt('To be, or not To bE that is the answer', 11)
    # print(crack(test2))

