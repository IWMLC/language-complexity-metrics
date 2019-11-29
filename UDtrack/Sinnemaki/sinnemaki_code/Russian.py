from conllu_reader import *

if '\\' in __file__:
    slash = '\\'
else:
    slash = '/'

LANGUAGE = __file__.split(slash)[-1][:-3]

possessive_pronouns = {'мой', 'твой', 'ее', 'его', 'наш', 'ваш', 'их', 'МОЙ', 'ТВОЙ', 'ЕЕ', 'ЕГО', 'НАШ', 'ВАШ', 'ИХ'}

def possessive(conllu_item, returntype=list):
    """The return type is a dict, the "returntype" argument is a needless remnant of a previous phase of this project.
The point is to avoid crashing if an extra argument is given."""
    try:
        analyses = conllu_item['analyysit']
    except TypeError:
        print(conllu_item)
        return {'dep_marked':[], 'head_marked':[], 'double_marked':[], 'zero_marked':[], 'head_exist':[]}


    sent_id = conllu_item['sent_id']

    def find_head_index(analysis):
        head_str = analysis[6]
        head_i = int(head_str)-1
        return head_i
    
    head_exist = []

    dep_marked = []
    head_marked = []
    double_marked = []
    zero_marked = []

    for a in analyses:

        # possessive pronouns
        if a[2] in possessive_pronouns and a[3] == 'DET' and a[7] == 'det':
            head_i = find_head_index(a)
            if head_i >= 0:
                if analyses[head_i][3] in {'NOUN', 'PROPN'}:
                    dep_marked.append(a)

        # noun possessors
        if a[3] in {'NOUN', 'PROPN'} and 'Case=Gen' in a[5] and a[7] == 'nmod':
            head_i = find_head_index(a)
            if head_i >= 0:
                if analyses[head_i][3] in {'NOUN', 'PROPN'}:
                    # In Russian the letter 'ё' is usually replaced with 'е' though 'ё' has its place in the alphabet.
                    if a[1].lower().replace('ё', 'е') == a[2].lower().replace('ё', 'е'):
                        zero_marked.append(a)
                    else:
                        dep_marked.append(a)
    
    return {'dep_marked':dep_marked, 'head_marked':head_marked, 'double_marked':double_marked, 'zero_marked':zero_marked, 'head_exist':head_exist}


test = r'''# sent_id = test-s434
# text = И тут же добавлял: ``Но с моей сексуальной жизнью всё в порядке! &#39;&#39;
1	И	И	CCONJ	CC	_	4	cc	_	_
2	тут	ТУТ	ADV	RB	_	4	advmod	_	_
3	же	ЖЕ	PART	UH	_	2	advmod	_	_
4	добавлял	ДОБАВЛЯТЬ	VERB	VBC	Aspect=Imp|Gender=Masc|Mood=Ind|Number=Sing|Tense=Past|VerbForm=Fin	0	root	_	SpaceAfter=No
5	:	:	PUNCT	:	_	4	punct	_	_
6	``	``	PUNCT	``	_	14	punct	_	SpaceAfter=No
7	Но	НО	CCONJ	CC	_	14	cc	_	_
8	с	С	ADP	IN	_	11	case	_	_
9	моей	МОЙ	DET	PRP$	Animacy=Inan|Case=Ins|Gender=Fem|Number=Sing|Person=1	11	det	_	_
10	сексуальной	СЕКСУАЛЬНЫЙ	ADJ	JJL	Animacy=Inan|Case=Ins|Gender=Fem|Number=Sing	11	amod	_	_
11	жизнью	ЖИЗНЬ	NOUN	NN	Animacy=Inan|Case=Ins|Gender=Fem|Number=Sing	14	obl	_	_
12	всё	ВСЁ	PRON	DT	Animacy=Inan|Case=Nom|Gender=Neut|Number=Sing	14	nsubj	_	_
13	в	В	ADP	IN	_	14	case	_	_
14	порядке	ПОРЯДОК	NOUN	NN	Animacy=Inan|Case=Loc|Gender=Masc|Number=Sing	4	ccomp	_	SpaceAfter=No
15	!	!	PUNCT	.	_	14	punct	_	_
16	&#39;&#39;	&#39;&#39;	PUNCT	&#39;&#39;	_	14	punct	_	_'''

conllu_item = to_ordered_dict(test)
d = possessive(conllu_item, dict)

if __name__ == '__main__':
    if type(d) == dict:
        for item in d:
            print(item, d[item], len(d[item]))
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
        
if __name__ == '__main__':
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
    

