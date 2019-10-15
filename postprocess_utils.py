import gpt_2_simple as gpt2

def gpt2_gen_question(sess, prefix):
    gen_texts = gpt2.generate(sess, prefix=prefix, length=30, return_as_list=True)
    gen_question = gen_texts[0][len(prefix):]
    gen_question = gen_question[:gen_question.find('?')+1]
    return gen_question.strip()
