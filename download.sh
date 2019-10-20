# Create a Python 2 virtual environment (necessary for gsutil).
virtualenv -p python2 ./visual-questioner-py2-env
source ./visual-questioner-py2-env/bin/activate

# Download Natural Questions data.
# Install gsutil according to https://cloud.google.com/storage/docs/gsutil_install.
mkdir -p nq
pip install gsutil
gsutil -m cp -R gs://natural_questions/v1.0-simplified/simplified-nq-train.jsonl.gz nq/v1.0-simplified_simplified-nq-train.jsonl.gz
cd nq
gunzip v1.0-simplified_simplified-nq-train.jsonl.gz
cd -
deactivate

# Download pre-trained voice cloning models.
code=$(wget --save-cookies cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1n1sPXvT34yXFLT47QZA6FIRGrwMeSsZc' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')
wget -O pretrained.zip --load-cookies cookies.txt "https://docs.google.com/uc?export=download&confirm=${code}&id=1n1sPXvT34yXFLT47QZA6FIRGrwMeSsZc"
unzip pretrained.zip
mv encoder/saved_models voicecloning/encoder
mv synthesizer/saved_models voicecloning/synthesizer
mv vocoder/saved_models voicecloning/vocoder
rmdir encoder
rmdir synthesizer
rmdir vocoder
rm pretrained.zip

# Download lists of names.
mkdir -p names
wget -O names/male.txt "https://www.cs.cmu.edu/afs/cs/project/ai-repository/ai/areas/nlp/corpora/names/male.txt"
wget -O names/female.txt "https://www.cs.cmu.edu/afs/cs/project/ai-repository/ai/areas/nlp/corpora/names/female.txt"
sed -i -e 1,6d names/male.txt
sed -i -e 1,6d names/female.txt

# Download pre-trained im2txt models.
mkdir -p im2txt; cd im2txt
wget -O word_counts.txt "https://docs.google.com/uc?export=download&id=0B0tqC1h-STWAYXlEMV9uZUZ2d28"
code=$(wget --save-cookies cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=0Bw6m_66JSYLlRFVKQ2tGcUJaWjA' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')
wget -O im2txt_2016_10_11.2000000.tar.gz --load-cookies cookies.txt "https://docs.google.com/uc?export=download&confirm=${code}&id=0Bw6m_66JSYLlRFVKQ2tGcUJaWjA"
tar -xvzf im2txt_2016_10_11.2000000.tar.gz
rm im2txt_2016_10_11.2000000.tar.gz

# Convert checkpoint.
source ../visual-questioner-env/bin/activate
cp ../vtensorflow/models/research/im2txt/convert_checkpoint.py .
python3 convert_checkpoint.py
cd -

# Edit config file with current working directory.
python3 update_config.py
deactivate
