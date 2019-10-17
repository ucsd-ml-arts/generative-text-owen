# Download Natural Questions data.
# Install gsutil according to https://cloud.google.com/storage/docs/gsutil_install.
mkdir -p nq
gsutil -m cp -R gs://natural_questions/v1.0-simplified/simplified-nq-train.jsonl.gz nq/v1.0-simplified_simplified-nq-train.jsonl.gz
cd nq
gunzip v1.0-simplified_simplified-nq-train.jsonl.gz
cd -

# Download pre-trained im2txt models.
mkdir -p im2txt; cd im2txt
wget -O word_counts.txt "https://docs.google.com/uc?export=download&id=0B0tqC1h-STWAYXlEMV9uZUZ2d28"
code=$(wget --save-cookies cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=0Bw6m_66JSYLlRFVKQ2tGcUJaWjA' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')
wget -O im2txt_2016_10_11.2000000.tar.gz --load-cookies cookies.txt "https://docs.google.com/uc?export=download&confirm=${code}&id=0Bw6m_66JSYLlRFVKQ2tGcUJaWjA"
tar -xvzf im2txt_2016_10_11.2000000.tar.gz
rm im2txt_2016_10_11.2000000.tar.gz

# Convert checkpoint.
cp ../vtensorflow/models/research/im2txt/convert_checkpoint.py .
python3 convert_checkpoint.py
cd -

# Edit config file with current working directory.
python3 update_config.py
