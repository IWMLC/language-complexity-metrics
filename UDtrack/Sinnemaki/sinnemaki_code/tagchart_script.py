import sys

from time import monotonic
from collections import defaultdict
from conllu_reader import *
from language_importer import import_data, folder2lang, id2folder
from csv_functions import read_table, list2csv#, tabsep2csv
import Finnish
#import Afrikaans
import Swedish
import Vietnamese
import Chinese
import RomanianHYPHENRRT
import Hebrew
import RomanianHYPHENNonstandard
import German
import KoreanHYPHENGSD
import KoreanHYPHENKaist
import Russian
import PolishHYPHENLFG
import PolishHYPHENSZ

hard_languages = """Finnish
Swedish
Vietnamese
Chinese
Romanian-RRT
Hebrew
Romanian-Nonstandard
German
Korean-GSD
Korean-Kaist
Russian
Polish-LFG
Polish-SZ""".splitlines() # languages and materials that are not doable with the simple rules allowed by the chart

hard_materials = [w for w in hard_languages if '-' in w]
# cases where there are more than one treebank for a single language
# and possessive NPs are not recognized from them using the same logic


def compare(tag, condition):
    """Determine whether a single tag meets a condition."""
    if condition == '': # empty condition, meaning the content of that particular cell is irrelevant
        return True
    if ';' in condition: # ";" means 'or': if any of the subconditions separated by semicolons are true, the whole condition is true
        return any(compare(tag, c) for c in condition.split(';')) # separate first by "or" conditions and then by "and" conditions
    # That is a recursion. Cannot be infinite as there are no semicolons in a list that was formed by splitting a string at semicolons.

    conditions = condition.split('&')

    answers = []

    for ehto in conditions: # ran out of variable names.
        #"ehto" is Finnish for 'condition'
    
        if ehto.startswith('on.!'): #on.!string = not equal to "string"
            answers.append(tag != ehto[4:])
        elif ehto.startswith('on.'): #on.string = equal to "string"
            answers.append(tag == ehto[3:])
        elif ehto.startswith('sis.!'): #sis.!string = does not contain "string"
            answers.append(ehto[5:] not in tag)
        elif ehto.startswith('sis.'): #sis.!string = contains "string"
            answers.append(ehto[4:] in tag)

    return all(answers) # in order for a tag to meet an "and" condition, all of its subconditions must be true

ehtotaulukko = [] # tag table as list of strings
provisional = set() # languages whose pronouns or nouns we can deal with, but not both. Should be empty by the end of the project.

for line in avaa('tag_chart.txt').strip().splitlines()[1:]:
    if len(line.split()) > 2:
        ehtotaulukko.append(line.split('\t'))
    else: # in case there are two or less non-blank cells*, that means the language is provisional, meaning only pronouns or nouns have been done.
        provisional.add(line.strip().split('\t')[-1]) # When the tag chart is ready, this block should never be reached.
    # *now that the only whitespace characters are tabs. This would likely not work if e.g. there were spaces in the file.

# if a hard language to be provisional, it is indicated there by adding there an otherwise unused variable called "provisional"
for language in hard_languages:
    if 'provisional' in dir(eval(language.replace('-', 'HYPHEN'))):
        provisional.add(language)

print('Provisional languages:', provisional)

#If there are no provisional languages, the following one-line command would create ehtotaulukko but it would not create provisional.
#ehtotaulukko = [line.split('\t') for line in avaa('tag_chart.txt').strip().splitlines()[1:] if len(line.split()) > 2]

condition_ddict = defaultdict(lambda:[])

for line in ehtotaulukko:
    condition_ddict[line[1]].append(line[2:]) # language: conditions
    condition_ddict[line[0]].append(line[2:]) # id: conditions
    condition_ddict[id2folder[line[0]]].append(line[2:]) # folder: conditions
    condition_ddict[id2folder[line[0]][3:]].append(line[2:]) # folder without UD_ : conditions
    # Because of the previous four lines, condition_ddict is really flexible in how you call it.
    

languages = [line[1] for line in ehtotaulukko]
languages = sorted(set(languages), key=lambda j:languages.index(j))

NA = 'NA'

def lemma_comparison(wordform, lemma, language): # language is e.g. Estonian-EDT
    """Compare whether wordform and lemma are the same, taking into account the special markings in the lemma (e.g. "#" for compounds).
Language parameter is the name of the folder without the 'UD_' beginning, for example 'Estonian-EDT'."""
    if language.startswith('Basque'):
        return wordform.lstrip('*').lower() == lemma.lstrip('*').lower()
    elif language.startswith('Estonian'):
        real_wordform = wordform.lower().replace('_', '') # final .replace('_', '') probably needless here...
        if real_wordform in {'mina', 'ma', 'me', 'meie'} and lemma == 'mina': # I, we
            return True
        if real_wordform in {'sina', 'sa', 'te', 'teie'} and lemma == 'sina': # you
            return True
        if real_wordform in {'nemad', 'nad', 'ta', 'tema'} and lemma == 'tema': # he, she, they
            return True
        return real_wordform == lemma.lower().replace('_', '') # ... but this .replace('_', '') is definitely needed.
    elif language.startswith('Ukrainian'):
        if lemma.endswith('.'):
            lemma = lemma[:-1]
        return wordform.lower() == lemma.lower()
    return wordform.lower() == lemma.lower() # default

def is_done(kieli):
    """Find if there is information on this language's possessive NPs either in the tag table or in a script."""
    if kieli in folder2lang:
        kieli = folder2lang[kieli].replace(' ', '_')

    if kieli in hard_languages:
        try:
            eval(kieli.replace(' ', '_').replace('-', 'HYPHEN') + '.possessive')
            return True
        except NameError:
            return False

    if kieli not in condition_ddict:
        print(kieli, '(not done yet)', end= ' ')
        return False
    
    return True

    

def possessiivi(lause, kieli):
    """Find dependents of possessive NPs n a sentence (lause).
lause is an ordered dict (conllu item), kieli is the language or the material (folder or id).

If the language or material has its own script, it will use that, otherwise it will look for instructions in the tag chart."""

    language_only = kieli.split('-')[0]

    if kieli in hard_materials:
        return eval(kieli.replace('-', 'HYPHEN') + '.possessive(lause, dict)')
    elif language_only in hard_languages:
        return eval(language_only + '.possessive(lause, dict)')

    def find_head_index(word):
        return int(word[6])-1

    answers = []

    analyses = lause['analyysit']

    if kieli not in condition_ddict:
        return {'dep_marked':NA, 'double_marked':NA, 'head_marked':NA, 'zero_marked':NA, 'head_exist':NA}
    else:
        conditions = condition_ddict[kieli]

        

    answer = defaultdict(lambda:[])


    for ehto in conditions:
            
        if ehto[:3] == ['', '', '']:
            if ehto[3:5] != ['', ''] and (ehto[5].startswith('on.') or ehto[5].startswith('sis.') or ehto[5] == ''):
                for dependent in analyses: # "for word in analyses" would be more readable, but this checks if it is a dependent.
                    dep_pos = dependent[3]
                    dep_tag = dependent[5]
                    dep_synt = dependent[7]
                    head_i = find_head_index(dependent)
                    if head_i < 0:
                        continue
                    head = analyses[head_i]
                    head_pos = head[3]
                    head_tag = head[5]

                    lst = [dep_pos, dep_tag, dep_synt, head_pos, head_tag]

                    if all(compare(*pair) for pair in zip(lst, ehto[3:])):
                        if ehto[-1].startswith('clemma.'): # compare lemma and word form
                            class_choices = ehto[-1][7:].split(';')
                            if lemma_comparison(dependent[1], dependent[2], kieli):
                                answer[class_choices[0] + '_marked'].append(dependent)
                                #print(class_choices[0] + '_marked', dependent)
                            else:
                                answer[class_choices[1] + '_marked'].append(dependent)
                                #print(class_choices[1] + '_marked', dependent)
                        else:
                            answer[ehto[-1]].append(dependent)
            else: # head_exist ("pyöränsä")
                for head in analyses:
                    head_pos = head[3]
                    head_tag = head[5]
                    lst = [head_pos, head_tag]
                    nmodposs = ehto[5] # nmod tai nmod:poss, NOT: "on.nmod" nor "on.nmod:poss"
                    if all(compare(*pair) for pair in zip(lst, ehto[6:])):
                        if all([(word[6] != head[0] or word[7] != nmodposs) for word in analyses]):
                            answer[ehto[-1]].append(head)
        else:
            for word in analyses:
                part_lemma = word[2]
                part_pos = word[3]
                part_synt = word[7]
                dep_i = find_head_index(word)
                if dep_i < 0:
                    continue
                dependent = analyses[dep_i]
                dep_pos = dependent[3]
                dep_tag = dependent[5]
                dep_synt = dependent[7]
                head_i = find_head_index(dependent)
                if head_i < 0:
                    continue
                head = analyses[head_i]
                head_pos = head[3]
                head_tag = head[5]

                lst = [part_lemma, part_pos, part_synt, dep_pos, dep_tag, dep_synt, head_pos, head_tag]

                if all(compare(*pair) for pair in zip(lst, ehto)):
                    if ehto[-1].startswith('clemma.'): # compare lemma and word form
                        class_choices = ehto[-1][7:].split(';')
                        if lemma_comparison(dependent[1], dependent[2], kieli):
                            answer[class_choices[0] + '_marked'].append(dependent)
                            #print(class_choices[0] + '_marked', dependent)
                        else:
                            answer[class_choices[1] + '_marked'].append(dependent)
                            #print(class_choices[1] + '_marked', dependent)
                    else:
                        answer[ehto[-1]].append(dependent)


    return answer

tabmodel = read_table('ud_tabmodel.txt')

all_languages = sorted(set(languages + hard_languages))

table_filename = 'language_stats.txt'
csv_filename = 'Sinnemäki.csv'

def mean(x): # Count mean dependency lenghths with this mean function. If no such marking exists, return NA.
    if len(x) == 0:
        return NA
    return sum(x)/len(x)

def save(name=table_filename):
    """Analyze all materials and save them to a tab-separated file."""
    with open(name, 'wt', encoding='utf-8') as file:
        print('id\tlanguage\tdep_marked\tdouble_marked\thead_marked\tzero_marked\thead_exist\tdep_dl_mean\tdouble_dl_mean\thead_dl_mean\tzero_dl_mean\tmean_dl	size', file=file)
        for language in tabmodel[1:]:
            material = language[2]
            print('Working on {}'.format(language[2]), end=' ')
            starttime = monotonic()
            dep_distances = []
            double_distances = []
            head_distances = []
            zero_distances = []

            distances = []
            
            if language[2][3:] not in hard_languages and not is_done(language[1].replace(' ', '_')):
                counts = {'dep_marked':NA, 'double_marked':NA, 'head_marked':NA, 'zero_marked':NA, 'head_exist':NA}
                size = import_data(material, 'size')
            else:
                d, size = import_data(material, 'both')
##                if language[2][3:] in hard_languages:
##                    kieli = language[2][3:]
##                else:
##                    kieli = language[1].replace(' ', '_')
                items = [possessiivi(to_ordered_dict(i), language[2][3:]) for i in d]
                counts = {'dep_marked':0, 'double_marked':0, 'head_marked':0, 'zero_marked':0, 'head_exist':0}
                for defdict in items:
                    for k in defdict:
                        assert defdict[k] != NA
                        counts[k] += len(defdict[k])
                        if k.endswith('_marked'):
                            this_marked = [abs(int(depanalysis[6])-int(depanalysis[0])) for depanalysis in defdict[k]]
                            distances.extend(this_marked)
                            if k == 'dep_marked':
                                dep_distances.extend(this_marked)
                            elif k == 'double_marked':
                                double_distances.extend(this_marked)
                            elif k == 'head_marked':
                                head_distances.extend(this_marked)
                            elif k == 'zero_marked':
                                zero_distances.extend(this_marked)
                            else:
                                raise Exception('Invalid type of marking... {}'.format(k))
##                        if 9 in distances: # for purposes of making sure this is working correctly. It is super easy to indent these wrong.
##                            print(d[items.index(defdict)])
##                print(distances[:200])
            if language[1] in provisional or material[3:] in provisional:
                print(language[0] + ' (provisional)', language[1], counts['dep_marked'], counts['double_marked'],
                      counts['head_marked'], counts['zero_marked'],
                      counts['head_exist'], mean(dep_distances), mean(double_distances),
                      mean(head_distances), mean(zero_distances), mean(distances), size, sep='\t', file=file)
            else:
                print(language[0], language[1], counts['dep_marked'], counts['double_marked'],
                      counts['head_marked'], counts['zero_marked'],
                      counts['head_exist'], mean(dep_distances), mean(double_distances),
                      mean(head_distances), mean(zero_distances), mean(distances), size, sep='\t', file=file)

            print('took {} seconds.'.format(format(monotonic()-starttime, '.3f')))

def str2bea(s, language): # for the GUI
    """Returns a string representing the dependents of each possessive NP of a sentence s
(as a string representing the conllu item) and language (material)."""
    answer = []
    d = possessiivi(to_ordered_dict(s), language)

    for item in ['dep_marked', 'double_marked', 'head_marked', 'zero_marked', 'head_exist']:
        if d[item] == NA:
            answer.append('{}: {}'.format(item, d[item]))
        else:
            answer.append('{}: {} ({} kpl)'.format(item, d[item], len(d[item])))

    return '\n'.join(answer)

def generate_final_csv(tabstats=table_filename, output_name=csv_filename):
    statstable = read_table(table_filename)

    final_table = [['id', 'language', 'dm', 'hm', 'dep_dl', 'double_dl', 'head_dl', 'zero_dl']]

    for row in statstable[1:]:
        iidee, language, dep_marked, double_marked, head_marked, zero_marked, head_exist, dep_dl_mean, double_dl_mean, head_dl_mean, zero_dl_mean, mean_dl, size = row

        dep_marked = int(dep_marked)
        double_marked = int(double_marked)
        head_marked = int(head_marked)
        zero_marked = int(zero_marked)
        head_exist = int(head_exist)

        all_possessives = dep_marked+double_marked+head_marked+zero_marked+head_exist
        
        dm = (dep_marked+double_marked)/all_possessives
        hm = (double_marked+head_marked+head_exist)/all_possessives
        
        final_table.append([iidee, language, dm, hm, dep_dl_mean, double_dl_mean, head_dl_mean, zero_dl_mean])

    list2csv(final_table, output_name)

            

if __name__ == '__main__':# and 'idlelib' in sys.modules:
    save()
    generate_final_csv()
    #tabsep2csv(table_filename, csv_filename)#, first_n_columns=7) # this is the final file. Convert saved file to csv.
