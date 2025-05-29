import re
import keyword
import builtins
from collections import defaultdict

def strip_special_chars(docx):
    return re.sub(r"\W+", " ", docx)

def get_reserved_word_frequency(docx):
    cleaned_docx = strip_special_chars(docx)
    reserved = defaultdict(int)
    identifiers = defaultdict(int)
    builtins_dict = defaultdict(int)
    builtins_list = dir(builtins)

    for token in cleaned_docx.split():
        if token in keyword.kwlist:
            reserved[token] += 1
        elif token in builtins_list:
            builtins_dict[token] += 1
        else:
            identifiers[token] += 1

    return {"reserved": reserved, "identifiers": identifiers, "builtins": builtins_dict}
