import argparse
import pyttsx3
import random
from time import sleep

tts = pyttsx3.init()
voices = tts.getProperty('voices')

for voice in voices:
    if voice.name == 'Milena':
        tts.setProperty('voice', voice.id)

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='cmd')

subparsers.add_parser('list')
subparsers.add_parser('add')
subparsers.add_parser('voice')
subparsers.add_parser('learn')

args = parser.parse_args()

words = set()
file_name = 'words_list.txt'


def list_words():
    return '\n'.join([f'{i+1} {word}' for i, word in enumerate(sorted(words))])


def fill_words():
    with open(file_name) as f:
        for i, line in enumerate(f):
            words.add(f'{line.strip()}')


if args.cmd == 'add':
    fill_words()
    while word := input("Введите слово (для прекращения нажмите Enter): ").lower().strip():
        if not word:
            print(list_words())
        if word in words:
            print('Это слово уже есть')
            continue
        with open(file_name, 'a') as f:
            f.write(f'{word}\n')
        words.add(word)

if args.cmd == 'list':
    fill_words()
    print(list_words())

if args.cmd == 'voice':
    fill_words()
    for word in words:
        tts.say(word)
        tts.runAndWait()
        sleep(5)

if args.cmd == 'learn':
    fill_words()
    print(list_words())
    indexes = [int(num) - 1 for num in input('Укажите номера слов через пробел для повтора (Enter для выхода): ').split()]
    sorted_words = sorted(words)

    for i in indexes:
        key = input('Нажмите Enter для следующего слова (любой символ для прекращения): ')
        if key:
            break
        tts.say(sorted_words[i])
        tts.runAndWait()

