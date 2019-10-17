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

def preprocess_input(text, preprocess_options):
    # Strip whitespace
    text = text.strip()
    # Convert first letter to lower/uppercase
    if preprocess_options['lowercase']:
        text = first_letter_lowercase(text)
    else:
        text = first_letter_uppercase(text)
    # Add or remove spaces adjacent to punctuation
    if preprocess_options['only_ending_spaces']:
        text = reformat_punctuation(text)
        text = tokenize_ending_punctuation(text)
    elif preprocess_options['punctuation_spaces']:
        text = tokenize_punctuation(text)
    else:
        text = reformat_punctuation(text)
    return text
