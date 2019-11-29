from conllu_reader import *

if '\\' in __file__:
    slash = '\\'
else:
    slash = '/'

LANGUAGE = __file__.split(slash)[-1][:-3]

# In the possessive function, before endswith_possessive_suffix is called, it is checked whether Style=Coll is in the tag.
# If someone wants to change that order, then the following possessive_suffixes_dict should be used instead.
##possessive_suffixes_dict = {'ni': [('Number[psor]=Sing', 'Person[psor]=1')],
##                            's': [('Number[psor]=Sing', 'Person[psor]=2', 'Style=Coll'), ('Person[psor]=3', 'Style=Coll')],
##                            'si': [('Number[psor]=Sing', 'Person[psor]=2')],
##                            'sa': [('Person[psor]=3', 'Style=Coll')],
##                            'sä': [('Person[psor]=3', 'Style=Coll')],
##                            'nsa': [('Person[psor]=3',)],
##                            'nsä': [('Person[psor]=3',)],
##                            'mme': [('Number[psor]=Plur', 'Person[psor]=1')],
##                            'nne': [('Number[psor]=Plur', 'Person[psor]=2')],
##                            'ns': [('Person[psor]=3', 'Style=Coll')]}

possessive_suffixes_dict = {'ni': [('Number[psor]=Sing', 'Person[psor]=1')],
                            's': [('Number[psor]=Sing', 'Person[psor]=2'), ('Person[psor]=3')],
                            'si': [('Number[psor]=Sing', 'Person[psor]=2')],
                            'sa': [('Person[psor]=3')],
                            'sä': [('Person[psor]=3')],
                            'nsa': [('Person[psor]=3',)],
                            'nsä': [('Person[psor]=3',)],
                            'mme': [('Number[psor]=Plur', 'Person[psor]=1')],
                            'nne': [('Number[psor]=Plur', 'Person[psor]=2')],
                            'ns': [('Person[psor]=3')]}

possessive_suffixes = sorted(possessive_suffixes_dict, key=lambda i:len(i), reverse=True)

#nending = set('seitsemän kahdeksan yhdeksän kymmenen'.split()) # Standard Finnish words whose genitive and nominative are identical

vowels = set('aeiouyåäöæœøüAEIOUYÅÄÖÆŒØÜ:') # characters that can precede a possessive suffix, : is included

# all Latin vowels that appear in material before a whitespace character
word_final_wowels = {'A', 'E', 'I', 'O', 'U', 'Y', 'a', 'e', 'i', 'o', 'u', 'y',
                    'À', 'Ä', 'à', 'á', 'ä', 'å', 'é', 'ë', 'ó', 'ö', 'ā', 'ē',
                    'ī', 'ı', 'ō'}


def endswith_possessive_suffix(word, tag):
    """Attempt at checking if Finnish word with tag ends with a possessive suffix.
In order for that to be the case, the ending must be in the list of
possessive suffixes AND the character before that ending must be a vowel or :.

May return false positives but should return no true negatives, unless the data
contains dialectal possessive suffixes that are absent from the list. Such are for
example an old -nno ending for the second person plural that was used in some
Savonian dialects, but probably isn't used anymore."""
    for ending in possessive_suffixes: # Find which possessive suffix the word ends with, if any
        if word.endswith(ending) or word.endswith(ending.upper()): # the list is sorted according to length
            break
    else:
        return False

    try:
        letter = word[-len(ending)-1]
        if letter not in vowels:
            return False
        needed_tags = possessive_suffixes_dict[ending]
        for tagtuple in needed_tags:
            if all(s in tag for s in tagtuple):
                return True
        return False
    except IndexError:
        return False

def execindented(s): # this function is for debugging purposes only
    k = []
    s = s.replace(r'''try:
        analyses = conllu_item['analyysit']
    except TypeError:
        print(conllu_item)
        return {'dep_marked':[], 'head_marked':[], 'double_marked':[], 'zero_marked':[], 'head_exist':[]}''', r'''try:
        analyses = conllu_item['analyysit']
    except TypeError:
        print(conllu_item)
        print({'dep_marked':[], 'head_marked':[], 'double_marked':[], 'zero_marked':[], 'head_exist':[]});raise''')
    if s[0].strip():
        s = '    '+s
    for i in s.splitlines():
        k.append(i[4:].replace('nonlocal ', 'global '))
    print('\n'.join(k))

execindent = execindented

def possessive(conllu_item, returntype=dict):
    try:
        analyses = conllu_item['analyysit']
    except TypeError:
        print(conllu_item)
        return {'dep_marked':[], 'head_marked':[], 'double_marked':[], 'zero_marked':[], 'head_exist':[]}


    sent_id = conllu_item['sent_id']

    def find_head_index(analysis):
        if analysis[7] == 'flat':
            b = int(analysis[6])-1
            if b >= 0:
                return find_head_index(analyses[b])
            else:
                return -1
        head_str = analysis[6]
        head_i = int(head_str)-1
        return head_i

    
    #1.1. Dependent and head are separate words

    dep_head_exist = [] # items are dependents
    head_exist = [] # items are heads


    def check_last_condition_1_2(i):
        """The head word has no such dependent
whose POS is ”NOUN”, ”PROPN” or ”PRON”
and whose syntactic function is ”nmod:poss” or ”nmod” and also
no such dependent whose POS is DET
and whose morphological tag contains ”Case=Gen” or ”Poss=yes”."""
        nonlocal analyses
        #dependents = [a for a in analyses if a[6] == analyses[i][0]]

        for d in analyses:
            if d[6] != analyses[i][0]:
                continue # not a dependent
            if d[3] in {'NOUN', 'PROPN', 'PRON'} and d[7] == 'nmod:poss':
                return False
            if d[3] == 'DET' and ('Case=Gen' in d[5] or 'Poss=Yes' in d[5]):
                return False

        return True
        
    # Building dep_head_exist
    for a in analyses:
        #print('a in analyses, a =', a)
        if (a[3] in {'NOUN', 'PROPN', 'PRON'} and (a[7] == 'nmod:poss' or ('Case=Gen' in a[5] and a[7] == 'nmod')))\
           or (a[3] == 'DET' and a[7] == 'det' and 'PronType=Prs' in a[5]):
            # a is the dependent
            if a[3] == 'PRON' and 'PronType=Prs' not in a[5]:
                continue
            head_i = find_head_index(a)
            if head_i >= 0:
                if analyses[head_i][3] in {'NOUN', 'PROPN'}:
                    dep_head_exist.append(a)

        if a[7] == 'flat':
            tod_i = find_head_index(a)
            etunimi_i = int(a[6])-1
            if tod_i >= 0 and etunimi_i >= 0:
                aa = analyses[tod_i]
                etunimi = analyses[etunimi_i]
                if a[3] in {'NOUN', 'PROPN'} and (etunimi[7] == 'nmod:poss' or ('Case=Gen' in a[5] and etunimi[7] == 'nmod')):
                    head_i = tod_i
                    #if head_i >= 0: # already checked
                    if aa[3] in {'NOUN', 'PROPN'}:
                        dep_head_exist.append(etunimi[:1] + a[1:6] + etunimi[6:])
        
        #1.2. Only head is present (e.g. pyörä-ni '(of) my bike', '(of) my wheel', 'my bikes', 'my wheels')
        if a[3] in {'NOUN', 'PROPN'}:
            #a is the head
            if "psor" in a[5]:
                #head_exist.append(a)
                if check_last_condition_1_2(int(a[0])-1): # might be needless but might not be
                    head_exist.append(a)


    # 2. Morphological analysis of possessive constructions

    dep_marked = []
    head_marked = []
    double_marked = []
    zero_marked = []

    for a in dep_head_exist:
        if 'Typo=Yes' in a[5]: # skip typos, they yield some "erroneous" zero-marking. Those would be correct in some dialects,
            continue # maybe even most of them, but if the sentence is written in the formal language, then it's a typo and marked as such.
        
        # a is DEPENDENT
        head_i = find_head_index(a)

        ainanalyses = a in analyses

        if ainanalyses:
            to_append = a
        else:
            to_append = analyses[int(a[0])-1]
        
        if head_i >= 0: # head must exist
            #2.1. Dependent marking
            if 'Case=Gen' in a[5] and 'psor' not in analyses[head_i][5]:
                if a[1].lower() == a[2].lower().replace('#', '') and a[2] and a[2][-1] in word_final_wowels:
                    # the lemma of "Helsingin" in "Helsingin Sanomat" is marked as "helsingin" and not "helsinki"  as it should be
                    # all potential zero-marking (unmarked genitives) end in vowels.
                    zero_marked.append(to_append) # "#" symbols separate compound word parts only in Finnish-TDT.conllu, not in FTB
                else:
                    dep_marked.append(to_append)

            #2.2. Head marking

            elif 'Case=Gen' not in a[5] and 'psor' in analyses[head_i][5]:
            # As of May 17, 2019 at 1:03 PM, the only head-marked was from flat:name in sentence:
            # "Tuossa näkyy muuten Disney Couturen Pocahontas-korunikin, uskalsin vihdoinkin vihkiä sen käyttöön.:)"
            # where the genitive is in the flat "Couturen" whose head is "Disney" (sent_id =  b202.23)
			# As of June 5, that is a dependent-marking with Disney as its dependent.
                for word in analyses:
                    if word[6] == a[0] and 'Case=Gen' in word[5] and 'flat' in word[7]:
                        if word[1].lower() == word[2].lower().replace('#', ''):
                            zero_marked.append(to_append) # "#" symbols separate compound word parts only in Finnish-TDT.conllu, not in FTB
                        else:
                            dep_marked.append(to_append)
                        break
                else: # there is no head-marking (with dependent also present in the sentence) in Finnish
                    head_marked.append(to_append) # so this block should never be reached

            #2.3. Double marking

            elif 'Case=Gen' in a[5] and 'psor' in analyses[head_i][5]:
                # checking if the possessive suffix is really there
                if 'PronType=Prs' not in a[5]:
                    dep_marked.append(to_append) # Kanarian lomaltaan
                elif 'Style=Coll' not in analyses[head_i][5]:
                    double_marked.append(to_append)
                elif endswith_possessive_suffix(analyses[head_i][1], analyses[head_i][5]) and not analyses[head_i][1].replace('#', '').lower() == analyses[head_i][2].replace('#', '').lower():
                    double_marked.append(to_append) # sun juttuus
                else: # meidän suhde
                    dep_marked.append(to_append)
        
            #elif 'Case=Gen' not in a[5] and 'psor' not in analyses[head_i][5]:
                #zero_marked.append(to_append)
                
    set_of_items = set()

    answer = sorted(set_of_items, key=lambda i:i[1])
    
    #print(set_of_items)
    
    return {'dep_marked':dep_marked, 'head_marked':head_marked, 'double_marked':double_marked, 'zero_marked':zero_marked, 'head_exist':head_exist}



#originally the POS of word 10 (Hallelujah) was X
test = r'''# sent_id = xlp42-4348
# text = Lovin´ Spoonfulin Darling Be Home Soon ja Leonard Cohenin Hallelujah ovat selvästi sähköisempiä kuin Hectorin tulkinnat .
1	Lovin´	lovin´	X	Unknown,Foreign	Foreign=Yes	2	amod	_	Alt=2_amod|Missed-Rel=attr|Missed-SUBCAT=FOREIGN
2	Spoonfulin	spoonful	X	Unknown,Foreign	Foreign=Yes	4	nmod	_	Alt=4_nmod|Missed-Rel=attr|Missed-SUBCAT=FOREIGN
3	Darling	darling	X	Unknown,Foreign	Foreign=Yes	4	vocative	_	Missed-SUBCAT=FOREIGN
4	Be	be	X	Unknown,Foreign	Foreign=Yes	13	csubj:cop	_	Alt=13_csubj|Missed-Rel=subj|Missed-SUBCAT=FOREIGN
5	Home	home	X	Unknown,Foreign	Foreign=Yes	4	nmod	_	Alt=4_nmod|Missed-Rel=advl|Missed-SUBCAT=FOREIGN
6	Soon	soon	X	Unknown,Foreign	Foreign=Yes	4	advmod	_	Alt=4_advmod|Missed-Rel=advl|Missed-SUBCAT=FOREIGN
7	ja	ja	CCONJ	Pcle,CC	_	10	cc	_	_
8	Leonard	leonard	PROPN	N,Prop,Sg,Nom	Case=Nom|Number=Sing	10	nmod	_	Alt=name
9	Cohenin	cohen	PROPN	N,Prop,Sg,Gen	Case=Gen|Number=Sing	8	flat	_	_
10	Hallelujah	hallelujah	PROPN	Unknown,Foreign	Foreign=Yes	4	conj	_	Missed-SUBCAT=FOREIGN
11	ovat	olla	AUX	V,Act,Ind,Pres,Pl3	Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act	13	cop	_	_
12	selvästi	selvästi	ADV	Adv	_	13	advmod	_	_
13	sähköisempiä	sähköinen	ADJ	A,Cmp,Pl,Par	Case=Par|Degree=Cmp|Number=Plur	0	root	_	_
14	kuin	kuin	SCONJ	Pcle,CS	_	16	mark	_	FTB-Sub=comparator
15	Hectorin	hector	PROPN	N,Prop,Sg,Gen	Case=Gen|Number=Sing	16	nmod	_	_
16	tulkinnat	tulkinta	NOUN	N,Pl,Nom	Case=Nom|Number=Plur	13	advcl	_	FTB-Sub=comparison
17	.	.	PUNCT	Pun	_	16	punct	_	_'''

conllu_item = to_ordered_dict(test)
d = possessive(conllu_item, dict)

if __name__ == '__main__':
    if type(d) == dict:
        for item in d:
            print(item, d[item])
    else:
        for item in d:
            print(item)


def str2poss(s, returntype=dict):
    conllu_item = to_ordered_dict(s)
    return possessive(conllu_item, returntype)

def str2bea(s, returntype=dict):
    d = str2poss(s, returntype)
    if type(d) == dict:
        for item in d:
            print(item, d[item], len(d[item]))
    else:
        for item in d:
            print(item)

def str2beastr(s):
    d = str2poss(s, dict)
    answer = []
    for item in d:
        answer.append('{} {} {}'.format(item, d[item], len(d[item])))
    return '\n'.join(answer)

def strip_indent(s, i=1):
    c = []
    for j in s.splitlines():
        c.append(j[4*i:])
    return '\n'.join(c)
        
if __name__ == '__main__': # help debugging, there should be no other need to run this script as main
    exec(r'''import os

while 'UDtrack' in os.listdir():
    os.chdir('UDtrack')

folders = [w for w in os.listdir() if LANGUAGE in w and '.' not in w]

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
''')
    g = [w for w in g if w.strip()]
    h = [to_ordered_dict(w) for w in g]
    zero = []
    for sent in h:
        if possessive(sent, dict)['zero_marked']:
            zero.append(sent)
    

