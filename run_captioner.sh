IMAGE_PATH=/home/owen/workspace/visual-questioner/images/water.jpg
CHECKPOINT_PATH=/home/owen/workspace/visual-questioner/im2txt/model.ckpt-2000000
VOCAB_FILE_PATH=/home/owen/workspace/visual-questioner/im2txt/word_counts.txt

cd tensorflow/models/research/im2txt
python3 im2txt/run_inference.py --checkpoint_path=${CHECKPOINT_PATH} --vocab_file=${VOCAB_FILE_PATH} --input_files=${IMAGE_PATH}
