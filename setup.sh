# 1
git submodule init
git submodule update
cd vtensorflow/models/research/im2txt
sudo python3 setup.py develop
cd -
./venv_setup.sh
source ./visual-questioner-env/bin/activate

# 2
./download.sh

# 3
python3 gen_nq_data.py nq/v1.0-simplified_simplified-nq-train.jsonl

# 4
python3 train_gpt2_questioner.py
deactivate
