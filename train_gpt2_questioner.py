import argparse
import subprocess
import gpt_2_simple as gpt2

import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', '-d', type=str, default='nq_data.txt')
    parser.add_argument('--model_name', '-m', type=str, default='124M')
    parser.add_argument('--steps', '-s', type=int, default=500)
    args = parser.parse_args()

    # Start afresh
    subprocess.call(['./cleanup.sh'])  # this will delete old models

    # Download model
    gpt2.download_gpt2(model_name=args.model_name)

    sess = gpt2.start_tf_sess()
    gpt2.finetune(sess, args.data_path, model_name=args.model_name, steps=args.steps)
