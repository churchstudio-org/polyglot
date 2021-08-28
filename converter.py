import json
import os.path
import re

from functools import reduce

source_folder = 'src/'
target_folder = 'dist/'

source_language = input('Type the SOURCE language:')
target_language = input('Type the TARGET language:')

filename = f'{source_language}-{target_language}.dict.txt'
filepath = source_folder + filename
output = f'{source_language}-{target_language}.dict.json'
dict = {}

if not os.path.isfile(filepath):
    print(f'File {filename} was not found inside src/ folder')
    print(f'Conversion failed')
    exit()

else:
    print(f'Converting file {filename} to JSON format')

def remove_comments(line: str):
    pair = [e.strip() for e in line.split('::') if e.strip()]

    if len(pair) <= 1:
        return None

    else:
        comments = r'(\{.*?\}|\(.*?\)$|\(.*?\)|\[.*?\]|\/.*?\/)'
        return re.sub(comments, '', pair[0]).strip() + '::' + re.sub(comments, '', pair[1]).strip()

def split_words(line: str):
    words = line.split('::')
    return [words[0].strip(), *[e.strip() for e in words[1].split(',')]]

def reduce_dict(dict: object, words: 'list[str]'):
    dict[words[0]] = [*(dict[words[0]] if words[0] in dict else []), *words[1:]]
    return dict

with open(filepath, encoding='utf8') as file:
    lines = file.readlines()

    no_intro = filter(lambda e: not e.startswith('#'), lines)

    lower_case = map(lambda e: e.lower(), no_intro)

    no_comments = map(remove_comments, lower_case)

    no_nulls = filter(lambda e: e != None, no_comments)

    words_list = map(split_words, no_nulls)

    dict = reduce(reduce_dict, list(words_list), {})

    for word in dict:
        dict[word] = list(set(dict[word]))

with open(target_folder + output, 'w', encoding='utf8') as file:
    json.dump(dict, file, ensure_ascii=False, indent=4)

print('Conversion successed')