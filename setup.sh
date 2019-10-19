# 1
git submodule init
git submodule update
cd vtensorflow/models/research/im2txt
python3 setup.py develop --user
cd -
./venv_setup.sh

# 2
./download.sh

# 3
source ./visual-questioner-env/bin/activate
python3 gen_nq_data.py nq/v1.0-simplified_simplified-nq-train.jsonl
deactivate
