import os
from csv_functions import read_table
from conllu_reader import avaa

def import_language(language):
    origdir = os.getcwd()

    while 'UDtrack' in os.listdir():
        os.chdir('UDtrack')

    folders = [w for w in os.listdir() if w[3:].startswith(language) and '.' not in w]

    rootfolder = os.getcwd()

    answer = ''

    for folder in folders:
        os.chdir(folder)
        files = os.listdir()
        if folder[3:] + '_THIS.conllu' in files:
            file = folder[3:] + '_THIS.conllu'
            # A final modified file should be have a name that ends with
            # _THIS.conllu
            # e.g. UD_Afrikaans-AfriBooms_THIS.conllu
        else:
            file = folder[3:] + '.conllu'
            # If such a file doesn't exist, just use the original which is named
            # folder without UD_ + '.conllu'

        answer += avaa(file)

        os.chdir(rootfolder)

    answer = answer.strip()

    g = answer.split('\n\n') # merkkijonot

    os.chdir(origdir)

    return g

template_data = read_table('ud_tabmodel.txt')
id2folder = {}
folder2id = {}
id2lang = {}
lang2ids = {}
id2ipa = {}
folder2lang = {}
folder2ipa = {}
lang2ipa = {}
ipa2lang = {}
ids = []
folders = []

for line in template_data[1:]:
    iidee, lang, folder, ipa = line[:4]
    id2folder[iidee] = folder
    folder2id[folder] = iidee
    id2lang[iidee] = lang
    id2ipa[iidee] = ipa
    ids.append(iidee)
    folder2lang[folder] = lang
    folder2ipa[folder] = ipa
    lang2ipa[lang] = ipa
    ipa2lang[ipa] = lang
    
    folders.append(folder)

    if lang not in lang2ids:
        lang2ids[lang] = [iidee]
    else:
        lang2ids[lang].append(iidee)

def find_size(s):
    """Number of words in conllu string"""
    number = 0

    for line in s.splitlines():
        d = line.split('\t')
        try:
            if d[0].isdigit() and d[3] != 'PUNCT':
                number += 1
        except IndexError:
            pass

    return number

def import_data(data, which='material'):
    """Import conllu as string from data, which can be id, folder name or folder name without the 'UD_' start.
Parameter "which" can be:
'material': returns material as list of strings (default)
'size': returns size of material in number of words
'both': returns tuple: first material as list of strings and second the size"""
    origdir = os.getcwd()

    while 'UDtrack' in os.listdir():
        os.chdir('UDtrack')

    answer = None

    try:

        if data in id2folder:
            folder = id2folder[data]
        elif data.startswith('UD_'):
            folder = data
        else:
            folder = 'UD_' + data

        os.chdir(folder)

        files = os.listdir()
        if folder[3:] + '_THIS.conllu' in files:
            file = folder[3:] + '_THIS.conllu'
            # A final modified file should be have a name that ends with
            # _THIS.conllu
            # e.g. UD_Afrikaans-AfriBooms_THIS.conllu
        else:
            file = folder[3:] + '.conllu'
            # If such a file doesn't exist, just use the original which is named
            # folder without UD_ + '.conllu'
        
        answer = avaa(file)
    except:
        print('Failed to import {}.'.format(data))
    finally:
        os.chdir(origdir)
        if which == 'material':
            return answer.strip('\n').split('\n\n')
        elif which == 'size':
            return find_size(answer)
        elif which == 'both':
            return answer.strip('\n').split('\n\n'), find_size(answer)
        elif type(which) == str:
            return ValueError("parameter 'which' must be 'material', 'size' or 'both'.")
        else:
            return TypeError("parameter 'which' must be a string, either 'material', 'size' or 'both'.")

def import_thing(thing):
    if thing in lang2ids:
        return import_language(thing)
    return import_data(thing)
