import gpt_2_simple as gpt2

def compute_batch_size(nsamples):
    for batch_size in range(64, 0, -1):
        if nsamples % batch_size == 0:
            return batch_size

def gpt2_gen_questions(sess, prefix, nsamples=1, temperature=0.7):
    batch_size = compute_batch_size(nsamples)
    gen_texts = gpt2.generate(sess,
                              prefix=prefix,
                              length=30,
                              return_as_list=True,
                              nsamples=nsamples,
                              batch_size=batch_size,
                              temperature=temperature)
    gen_questions = []
    for gen_text in gen_texts:
        gen_question = gen_text[len(prefix):]
        gen_questions.append(postprocess_question(gen_question))
    return gen_questions

def first_letter_uppercase(text):
    if len(text) > 0:
        text = text.strip()
        text = text[0].upper() + text[1:]
    return text

def reformat_punctuation(text):
    """Get rid of some of the spaces around punctuation."""
    text = text.replace('`` ', '"')
    text = text.replace(" ''", '"')
    for char in ('(',):
        text = text.replace(char + ' ', char)
    for char in ('.', "'", ';', ')', ':', '?', ','):
        text = text.replace(' ' + char, char)
    return text

def postprocess_question(gen_question):
    gen_question = gen_question[:gen_question.find('?')+1]
    gen_question = first_letter_uppercase(gen_question)
    return reformat_punctuation(gen_question)

def postprocess_caption(sentence):
    """Reformat caption for readability."""
    sentence = first_letter_uppercase(sentence)
    return reformat_punctuation(sentence)
