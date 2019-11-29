import tagchart_script as et
from language_importer import *
#import Swedish as lng

from unicodedata import name
from tkinter import *
from tkinter import messagebox # For some reason this seemst to be necessary
from tkinter.ttk import Combobox
from collections import Counter
import tkinter.filedialog
import os
from SurrogatePair import remove_surrogates, with_surrogates

filedialog = tkinter.filedialog

root = Tk()
root.title('pəˈzɛsɪvz fɹɒm "conllu" ˈdeɪtə')

label = Label(root, text='ˈɛntə ˈsɛntəns juː ˈwɪʃ tʊ ˈænəˌlaɪz')
label.grid(row=0, column=0)

label2 = Label(root, text='ðɪ əˈnæləˌsɪs wɪl əˈpiə ˈhiə wɛn juː ˈklɪk "ˈænəˌlaɪz"')
label2.grid(row=0, column=1)

lahe = Text(root, width=50)
lahe.grid(row=1, column=0)

analyysi = Text(root, width=50)
analyysi.grid(row=1, column=1)

#names = lang2ipa # language: ˈlæŋgwɪdʒ
#nimet = ipa2lang # ˈlæŋgwɪdʒ: language

kielet = sorted([w for w in os.listdir('UDtrack') if w.startswith('UD_') and '.' not in w])

kielivaihtoehot = Combobox(values=kielet)
kielivaihtoehot.grid(row=1, column=2, sticky=N)
Label(root, text='sɪˈlɛkt  məˈtiəɹɪəl:').grid(row=0, column=2)


while 'UDtrack' in os.listdir():
    os.chdir('UDtrack')

g = [] # strings

indeksi = None

def analysoi(s):
    """Analyse a string (to string representing a dict of possessive NPs from a conllu string s)."""
    try:
        return et.str2bea(remove_surrogates(s), kielivaihtoehot.get()[3:])
    except:
        return analyysi.get("1.0","end-1c")

def set_text(entry, text):
    entry.delete(0,END)
    entry.insert(0,text)

def kf():
    """Analyse current sentence and insert it to the box on the right."""
    global indeksi
    analyysi.delete('1.0', END)
    if remove_surrogates(lahe.get("1.0","end-1c").strip()) in g: # change browsing index if sentence is in material
        indeksi = g.index(remove_surrogates(lahe.get("1.0","end-1c").strip()))
    analyysi.insert(END, with_surrogates(analysoi(lahe.get("1.0","end-1c"))))


lause_id_entry = Entry(root) # search box for sent_id
lause_id_entry.grid(row=2, column=0)



komento = Button(root, text='ˈænəˌlaɪz', command=kf) # analyse button
komento.grid(columnspan=2)

def eellinen_lause(): # previous sentence
    global indeksi

    if indeksi is None:
        messagebox.showinfo('ˈɛɹə', 'ðə ˈsɛntəns ˈhæzənt ˌbiːn dɪˈfaɪnd ˌjɛt . ˈjuːz ðə ˈsɜːtʃ ˌbɒks ˈfɜːst tə ˈfaɪnd ə ˈsɛntəns .')
        return None

    indeksi -= 1
    
    if indeksi < 0:
        messagebox.showinfo('ˈɛɹə', 'ðɪs ɪz ðə ˈfɜːst ˈsɛntəns')
        indeksi = 0
        return None
    
    lahe.delete('1.0', END)
    lahe.insert(END, g[indeksi])
    kf()

def seurraava_lause(): # next sentence
    global indeksi

    if indeksi is None:
        messagebox.showinfo('ˈɛɹə', 'ðə ˈsɛntəns ˈhæzənt ˌbiːn dɪˈfaɪnd ˌjɛt . ˈjuːz ðə ˈsɜːtʃ ˌbɒks ˈfɜːst tə ˈfaɪnd ə ˈsɛntəns .')
        return None

    indeksi += 1
    
    if indeksi >= len(g):
        messagebox.showinfo('ˈɛɹə', 'ðɪs ɪz ðə ˈlɑːst ˈsɛntəns')
        indeksi = len(g)-1
        return None
    
    lahe.delete('1.0', END)
    lahe.insert(END, g[indeksi])
    kf()

nyk_material = ''

def hae_lause(): # find sentence
    global indeksi
    global g
    global nyk_material
    teksti = lause_id_entry.get()
    loyv = []
    
    nyk_material = kielivaihtoehot.get() # find current language IPA -> orthography
    if nyk_material:
        ng = import_thing(nyk_material)
    else:
        #raise KeyError('')
        return messagebox.showinfo('sɪˈlɛkt ˈlæŋɡwɪdʒ', 'sɪˈlɛkt ˈfɜːst ðə ˈlæŋɡwɪdʒ ænd ˈðɛn ˈsɜːtʃ fəɹ ə ˈsɛntəns')
    for n, i in enumerate(ng):
        d = i.index('# sent_id = ')
        sentid = i[d:][12:].splitlines()[0]
        if sentid.startswith(teksti) or sentid.lstrip().startswith(teksti):
            if not loyv:
                lahe.delete('1.0', END)
                lahe.insert(END, i)
                indeksi = n
                kf()
            loyv.append(sentid)
    #print(len(loyv))
    if not loyv:
        messagebox.showinfo('ˈkɑːnt ˈfaɪnd', 'ˈkɑːnt ˈfaɪnd ˈsɛntəns wɪð ˈɡɪvən aɪˈdiː')
    elif 1 < len(loyv) <= 10:
        messagebox.showinfo('ˈfaʊnd ˈmɔː ðən ˌwɒn , ˈhiəz ðə ˈfɜːst', 'ˈfaʊnd ˈsɛntənsɪz wɪð ˈfɒləʊɪŋ aɪˈdiːz:\n' + '\n'.join(repr(i) for i in loyv))
    elif len(loyv) == 11:
        messagebox.showinfo('ˈfaʊnd ˈmɔː ðən ˌwɒn , ˈhiəz ðə ˈfɜːst', 'ˈfaʊnd ˈsɛntənsɪz wɪð ˈfɒləʊɪŋ aɪˈdiːz:\n' + '\n'.join(repr(i) for i in loyv[:10]) + '\nænd ˈwɒn ˈmɔː')
    elif len(loyv) > 11:
        messagebox.showinfo('ˈfaʊnd ˈmɔː ðən ˌwɒn , ˈhiəz ðə ˈfɜːst', 'ˈfaʊnd ˈsɛntənsɪz wɪð ˈfɒləʊɪŋ aɪˈdiːz:\n' + '\n'.join(repr(i) for i in loyv[:10]) + '\nænd {} ˈmɔː'.format(len(loyv)-10))

    g.clear()
    g.extend(ng)

eellinen = Button(root, text='ˈpɹiːvɪəs', command=eellinen_lause)
eellinen.grid(row=4, column=0)
hae = Button(root, text='ˈsɜːtʃ', command=hae_lause)
hae.grid(row=3, column=0)
seurraava = Button(root, text='ˈnɛkst', command=seurraava_lause)
seurraava.grid(row=4, column=1)

merkintaluokat = ['dep_marked', 'double_marked', 'head_marked', 'zero_marked', 'head_exist']
ekavika = ['θ', 'θ ˈlɑːst']

def hae_merkintatyypin_mukkaan():
    """Find by type of marking (e.g. find first sentence with at least one dependent-marked possessive NP)."""
    global indeksi
    global g
    global nyk_material
    
    if kielivaihtoehot.get():
        nyk_material = kielivaihtoehot.get()
        g.clear()
        g.extend(import_thing(nyk_material))
        language = folder2ipa[nyk_material]
        indeksi = 0
    else:
        return messagebox.showinfo('məˈtiəɹɪəl ˈhæzənt ˌbiːn ˈtʃəʊzən', 'ˈtʃuːz ˈfɜːst ðə məˈtiəɹɪəl ænd ˈðɛn ˈtɹaɪ əˈɡɛn !')
    
    ikkuna = Toplevel()
    ikkuna.title('ˈfaɪnd ˈsɛntəns ɪn "{}" ({})'.format(nyk_material, language))
    #search
    tyyppi_label1 = Label(ikkuna, text='ˈfaɪnd')
    tyyppi_label1.grid(row=0, column=0, sticky=E)
    #whichth
    monesko = Entry(ikkuna, width=6)
    monesko.grid(row=0, column=1)
    set_text(monesko, '1')
    #from the end?
    ekavikabox = Combobox(ikkuna, values=ekavika)
    ekavikabox.grid(row=0, column=2)
    ekavikabox.current(0)
    #containing
    Label(ikkuna, text='kənˈteɪnɪŋ').grid(row=0, column=3)
    #which type of marking the user wants to search for
    mlbox = Combobox(ikkuna, values=merkintaluokat)
    mlbox.grid(row=0, column=4)

    # browse only these?
    # If tickbox is crossed, previous and next buttons will only show sentences containing the searched type of possessive NPs.
    sellaavar = IntVar() # sellaa = 'browse' (in dialectal Finnish)
    sellaa = Checkbutton(ikkuna, text="ˈbɹaʊz ˈəʊnli ˈðiːz", variable=sellaavar)
    sellaa.grid(row=1, column=0)
    
    def haku(): # actual search
        nonlocal ikkuna
        if ekavikabox.get() == 'θ':
            i = 0
            add = 1
        else:
            i = -1
            add = -1


        try:
            nn = int(monesko.get())
            assert nn > 0
        except:
            return messagebox.showinfo('ˈɛɹə', '{} ɪz nˌɒt ə ˈpɒzɪˌtɪv ˈɪntɪdʒə'.format(monesko.get()))

        loyv = []

        mlbox_arvo = mlbox.get()
        if not mlbox_arvo:
            return messagebox.showinfo('ˈtʃuːz wɒt ˈtaɪp jɔː ˈlʊkɪŋ fɔː', 'ˈtʃuːz ˈfɜːst ˈwɪtʃ ˌtaɪp ɒv ˈmɑːkɪŋ juː ˈwɒnt tə ˈfaɪnd'.format(monesko.get()))

        
        if sellaavar.get(): # everything under this "if" statement must end in return statements,
            c = [] # the "while True" loop below is only for cases where the user wants to browse the entire material
            for lause in g:
                vastaus = et.possessiivi(et.to_ordered_dict(lause), nyk_material[3:])
                if mlbox_arvo in vastaus and vastaus[mlbox_arvo] and vastaus[mlbox_arvo] != et.NA:
                    c.append(lause)
            if not c:
                ikkuna.destroy()
                return messagebox.showinfo('ˈkɑːnt ˈfaɪnd ˈɛni', 'ðə ˈtaɪp ɒv ˈmɑːkɪŋ juː ˈtʃəʊz dʌz ˌnɒt əˈpiəɹ ɪn ðə məˈtiəɹɪəl.')
            
            g.clear()
            g.extend(c)
            if add == 1:
                virhe = False
                try:
                    nyk_lause = g[nn-1]
                    indeksi = nn-1
                except IndexError:
                    nyk_lause = g[-1]
                    indeksi = len(g)-1
                    virhe = True
                lahe.delete('1.0', END)
                lahe.insert(END, g[indeksi])
                kf()
                ikkuna.destroy()
                if virhe:
                    return messagebox.showinfo('ˈkɑːnt ˈfaɪnd ðæt ˈmɛni', 'ðə ˈtaɪp ɒv ˈmɑːkɪŋ juː ˈtʃəʊz dʌz ˌnɒt əˈpiəɹ ɪn ðə məˈtiəɹɪəl ðæt ˈmɛni ˈtaɪmz , ˈhiəz ðə ˈlɑːst ˌwɒn')
            else:
                virhe = False
                try:
                    nyk_lause = g[nn]
                    indeksi = g.index(nyk_lause)
                except IndexError:
                    nyk_lause = g[0]
                    indeksi = 0
                    virhe = True
                lahe.delete('1.0', END)
                lahe.insert(END, g[indeksi])
                kf()
                ikkuna.destroy()
                if virhe:
                    return messagebox.showinfo('ˈkɑːnt ˈfaɪnd ðæt ˈmɛni', 'ðə ˈtaɪp ɒv ˈmɑːkɪŋ juː ˈtʃəʊz dʌz ˌnɒt əˈpiəɹ ɪn ðə məˈtiəɹɪəl ðæt ˈmɛni ˈtaɪmz , ˈhiəz ðə ˈfɜːst ˌwɒn')
        
        while True:
            try:
                lause = g[i]
                vastaus = et.possessiivi(et.to_ordered_dict(lause), nyk_material[3:])
                if mlbox_arvo in vastaus and vastaus[mlbox_arvo]:
                    #print(i, add, lause, vastaus)
                    loyv.append(lause)
                if len(loyv) == nn:
                    if add == 1:
                        indeksi = i
                    else:
                        indeksi = len(g)+i
                    assert indeksi >= 0
                    lahe.delete('1.0', END)
                    lahe.insert(END, g[indeksi])
                    kf()
                    ikkuna.destroy()
                    break
                i += add
            except IndexError:
                if loyv:
                    lause = loyv[-1]
                    indeksi = g.index(lause)
                    lahe.delete('1.0', END)
                    lahe.insert(END, g[indeksi])
                    kf()
                    ikkuna.destroy()
                    if add == 1:
                        return messagebox.showinfo('ˈkɑːnt ˈfaɪnd ðæt ˈmɛni', 'ðə ˈtaɪp ɒv ˈmɑːkɪŋ juː ˈtʃəʊz dʌz ˌnɒt əˈpiəɹ ɪn ðə məˈtiəɹɪəl ðæt ˈmɛni ˈtaɪmz , ˈhiəz ðə ˈlɑːst ˌwɒn')
                    else:
                        return messagebox.showinfo('ˈkɑːnt ˈfaɪnd ðæt ˈmɛni', 'ðə ˈtaɪp ɒv ˈmɑːkɪŋ juː ˈtʃəʊz dʌz ˌnɒt əˈpiəɹ ɪn ðə məˈtiəɹɪəl ðæt ˈmɛni ˈtaɪmz , ˈhiəz ðə ˈfɜːst ˌwɒn')
                else:
                    ikkuna.destroy()
                    return messagebox.showinfo('ˈkɑːnt ˈfaɪnd ˈɛni', 'ðə ˈtaɪp ɒv ˈmɑːkɪŋ juː ˈtʃəʊz dʌz ˌnɒt əˈpiəɹ ɪn ðə məˈtiəɹɪəl.')
                    
            
            ikkuna.destroy()
    
    ok = Button(ikkuna, text='  ˌəʊˈkeɪ  ', command=haku)
    ok.grid(columnspan=5, row=1)#, sticky=W)
    
    

haens = Button(root, text='ˈsɜːtʃ baɪ ˈmɑːkɪŋ...', command=hae_merkintatyypin_mukkaan)
haens.grid(row=3, column=1)


root.mainloop()

