"""
Visual Questioner CLI.
Run with `python3 questioner_cli.py <image_path>`.
"""

import argparse
import gpt_2_simple as gpt2
from captioner import Captioner
from postprocess_utils import gpt2_gen_questions

def main(image_path):
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess)
    checkpoint_path = '/home/owen/workspace/visual-questioner/im2txt/model.ckpt-2000000'
    vocab_file_path = '/home/owen/workspace/visual-questioner/im2txt/word_counts.txt'
    captioner = Captioner(sess, checkpoint_path, vocab_file_path)
    caption = captioner.caption(image_path)
    questions = gpt2_gen_questions(sess, caption, nsamples=1, temperature=0.7)
    print('Questions:')
    for i, question in enumerate(questions):
        print('%d. %s' % (i + 1, question))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_path', type=str)
    args = parser.parse_args()
    main(args.image_path)
