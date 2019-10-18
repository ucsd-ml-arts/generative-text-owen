"""
Visual Questioner CLI.
Run with `python3 questioner_cli.py <image_path>`.
"""

import os
import yaml
import logging
import argparse
import gpt_2_simple as gpt2
from captioner import Captioner
from postprocess_utils import gpt2_gen_questions

import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('tensorflow').setLevel(logging.FATAL)
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

def main(image_path, nsamples, temperature):
    # Generate questions
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess)
    config = yaml.load(open('config.yaml', 'r'), Loader=yaml.FullLoader)
    checkpoint_path = os.path.join(config['project_root_dir'], config['checkpoint_path'])
    vocab_file_path = os.path.join(config['project_root_dir'], config['vocab_file_path'])
    captioner = Captioner(sess, checkpoint_path, vocab_file_path)
    caption = captioner.caption(image_path)
    questions = gpt2_gen_questions(
        sess, caption, nsamples=nsamples, temperature=temperature)

    # Print generated questions
    print('----------\nQuestions:')
    for i, question in enumerate(questions):
        print('%d. %s' % (i + 1, question))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_path', type=str)
    parser.add_argument('--nsamples', '-n', type=int, default=1)
    parser.add_argument('--temperature', '-t', type=float, default=0.7)
    args = parser.parse_args()
    main(args.image_path, args.nsamples, args.temperature)
