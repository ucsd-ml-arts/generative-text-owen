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
        gen_question = gen_question[:gen_question.find('?')+1]
        gen_questions.append(gen_question.strip())
    return gen_questions
