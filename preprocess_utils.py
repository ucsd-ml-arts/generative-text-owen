import re

def first_letter_lowercase(text):
    if len(text) > 0:
        text = text.strip()
        text = text[0].lower() + text[1:]
    return text

def first_letter_uppercase(text):
    if len(text) > 0:
        text = text.strip()
        text = text[0].upper() + text[1:]
    return text

def fix_i_contractions(text):
    mapping = [
        ('im', "i'm"),
        ('ive', "i've"),
        ('i m', "i'm"),
        ('i ve', "i've"),
        ('i d', "i'd"),
        ('i ll', "i'll"),
    ]
    mapping.extend(
        [tuple(map(first_letter_uppercase, m)) for m in mapping])
    for bad, good in mapping:
        text = re.sub(r'^%s ' % bad, '%s ' % good, text)
        text = re.sub(r' %s$' % bad, ' %s' % good, text)
        text = text.replace(' %s ' % bad, ' %s ' % good)
    return text

def capitalize_i(text):
    """
    >>> capitalize_i('i think i will stay indoors')
    'I think I will stay indoors'
    >>> capitalize_i("i'll be coming around the mountain")
    "I'll be coming around the mountain"
    """
    for s in ('i', "i'd", "i'll", "i'm", "i've"):
        caps = first_letter_uppercase(s)
        # beginning
        text = re.sub(r'^%s ' % s, '%s ' % caps, text)
        # end
        text = re.sub(r' %s$' % s, ' %s' % caps, text)
        # middle
        text = text.replace(' %s ' % s, ' %s ' % caps)
    return text

def tokenize_punctuation(text):
    """Add spaces around punctuation.
    Inverse of `preprocess_utils.reformat_punctuation`.

    >>> tokenize_punctuation("``hello there''")
    "`` hello there ''"
    >>> tokenize_punctuation('"hello there"')
    "`` hello there ''"
    >>> tokenize_punctuation("jon's quick, red: (fox). lazy; dog?")
    "jon 's quick , red : ( fox ) . lazy ; dog ?"
    """
    # Leading double quotes
    text = re.sub(r'"([^\s])', r'`` \1', text)
    # Closing double quotes
    text = re.sub(r'([^\s])"', r"\1 ''", text)
    # Closing single quotes
    text = re.sub(r"([^\s'])'([^'])", r"\1 '\2", text)

    for char in ('\\(', '``'):
        repl_char = char.replace('\\', '')
        text = re.sub(r'%s([^\s])' % char, r'%s \1' % repl_char, text)
    for char in ('\\.', "''", ';', '\\)', ':', '\\?', ','):
        repl_char = char.replace('\\', '')
        text = re.sub(r'([^\s])%s' % char, r'\1 %s' % repl_char, text)
    return text

def tokenize_ending_punctuation(text):
    """Add spaces before terminal periods and question marks.

    >>> tokenize_ending_punctuation("jon's quick, red: (fox). lazy; dog?")
    "jon's quick, red: (fox). lazy; dog ?"
    """
    for char in ('\\.', '\\?'):
        repl_char = char.replace('\\', '')
        text = re.sub(r'([^\s])%s$' % char, r'\1 %s' % repl_char, text)
    return text

def tokenize_hyphens(text):
    """
    >>> tokenize_hyphens('one-two--3')
    'one - two -- 3'
    """
    for s in ('--', '-'):
        text = re.sub(r'([^\s])%s([^\s])' % s, r'\1 %s \2' % s, text)
    return text

def reformat_punctuation(text):
    """Get rid of spaces around punctuation.
    Inverse of `preprocess_utils.tokenize_punctuation`."""
    text = text.replace('`` ', '"')
    text = text.replace(" ''", '"')
    for char in ('(',):
        text = text.replace(char + ' ', char)
    for char in ('.', "'", ';', ')', ':', '?', ','):
        text = text.replace(' ' + char, char)
    return text

def reformat_hyphens(text):
    """
    >>> reformat_hyphens('one - two -- 3')
    'one-two--3'
    """
    for s in ('-', '--'):
        text = text.replace(' %s ' % s, s)
    return text

def preprocess_input(text, preprocess_options):
    # Strip whitespace
    text = text.strip()
    # Convert first letter to lower/uppercase
    if preprocess_options['lowercase']:
        text = first_letter_lowercase(text)
    else:
        text = first_letter_uppercase(text)
    # Fix "I" contractions
    if preprocess_options['fix_i_contractions']:
        text = fix_i_contractions(text)
    # Add or remove spaces adjacent to punctuation
    if preprocess_options['only_ending_spaces']:
        text = reformat_punctuation(text)
        text = tokenize_ending_punctuation(text)
    elif preprocess_options['punctuation_spaces']:
        text = tokenize_punctuation(text)
    else:
        text = reformat_punctuation(text)
    # Add or remove spaces around hyphens
    if preprocess_options['hyphen_spaces']:
        text = tokenize_hyphens(text)
    else:
        text = reformat_hyphens(text)
    # Capitalize "I"
    return capitalize_i(text)
