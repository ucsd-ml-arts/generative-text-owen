import subprocess
import gpt_2_simple as gpt2

import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

# Start afresh
subprocess.call(['./cleanup.sh'])  # this will delete old models

# Download model
model_name = '124M'
gpt2.download_gpt2(model_name=model_name)

sess = gpt2.start_tf_sess()
gpt2.finetune(sess, 'nq_data.txt', model_name=model_name, steps=500)
