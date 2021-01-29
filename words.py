import argparse
import pyttsx3
import os

tts = pyttsx3.init()
voices = tts.getProperty('voices')

for voice in voices:
    if voice.name == 'Milena':
        tts.setProperty('voice', voice.id)

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='cmd')

subparsers.add_parser('list')
subparsers.add_parser('add-words')
subparsers.add_parser('add-keys')
subparsers.add_parser('voice')
subparsers.add_parser('learn-words')
subparsers.add_parser('learn-keys')

args = parser.parse_args()

words = set()
keys = set()

words_file = 'words_list.txt'
if not os.path.exists(words_file):
    open(words_file, 'w')

keys_file = 'keys_list.txt'
if not os.path.exists(keys_file):
    open(keys_file, 'w')


def list_words():
    return '\n'.join([f'{i+1} {word}' for i, word in enumerate(sorted(words))])


def list_keys():
    return '\n'.join([f'{i+1} {key}' for i, key in enumerate(sorted(keys))])


def fill_words():
    with open(words_file) as f:
        for line in f:
            words.add(line.strip().lower())


def fill_keys():
    with open(keys_file) as f:
        for line in f:
            keys.add(line.strip().lower())


def voice(array):
    if not len(array):
        print('Пустой список слов')
        return
    print(array)
    indexes = [int(num) - 1 for num in
               input('Укажите номера слов через пробел для повтора (Enter для выхода): ').split()]
    sorted_array = sorted(array)

    for i in indexes:
        tts.say(sorted_array[i])
        tts.runAndWait()
        key = input('Нажмите Enter для следующего слова (любой символ для прекращения): ')
        if key:
            break


if args.cmd == 'add-words':
    fill_words()
    while word := input("Введите слово (для прекращения нажмите Enter): ").lower().strip():
        if not word:
            print(list_words())
        if word in words:
            print('Это слово уже есть')
            continue
        with open(words_file, 'a') as f:
            f.write(f'{word}\n')
        words.add(word)


if args.cmd == 'list':
    fill_words()
    print(list_words())

if args.cmd == 'learn-words':
    fill_words()
    array = list_words()
    voice(array)

if args.cmd == 'learn-keys':
    fill_keys()
    array = list_keys()
    voice(array)
