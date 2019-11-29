# Python's standard GUI library, Tkinter, does not support Unicode characters
# that are outside the BMP (larger than '\uffff'). In the unlikely case that
# any of the conllus contains such characters (e.g. emojis), they will need
# to be converted into an equivalent sequence of two "invalid" (not allowed in
# regular text files) characters known as "surrogates". The function
# remove_surrogates will replace surrogate pairs with the actual non-BMP
# characters they represent (so a string will be writable to a file), and the
# function with_surrogates will do the opposite, enabling the graphical user
# interface to show them, even though it will think that each emoji is two
# characters instead of one.

# Source of functions:
# http://stackoverflow.com/questions/40222971/python-find-equivalent-surrogate-pair-from-non-bmp-unicode-char/40223212#40223212

def remove_surrogates(s):
    return s.encode('utf-16', 'surrogatepass').decode('utf-16')

import re

_nonbmp = re.compile(r'[\U00010000-\U0010FFFF]')

def _surrogatepair(match):
    char = match.group()
    assert ord(char) > 0xffff
    encoded = char.encode('utf-16-le')
    return (
        chr(int.from_bytes(encoded[:2], 'little')) + 
        chr(int.from_bytes(encoded[2:], 'little')))

def with_surrogates(text):
    return _nonbmp.sub(_surrogatepair, text)

import struct

def withSurrogates(emoji_str):
    return ''.join(c if c <= '\uffff' else ''.join(chr(x) for x in struct.unpack('>2H', c.encode('utf-16be'))) for c in emoji_str)

if __name__ == '__main__':

    print(with_surrogates('\U0001f64f\U0001f64e'))
    print(with_surrogates('jaatte\U0001f64föö'))

    print(withSurrogates('\U0001f64f\U0001f64e'))
    print(withSurrogates('jaatte\U0001f64föö'))

