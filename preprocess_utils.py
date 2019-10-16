def first_letter_lowercase(text):
    if len(text) > 0:
        text = text.strip()
        text = text[0].lower() + text[1:]
    return text
