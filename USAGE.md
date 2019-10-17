# Usage

## 1. Initial Setup
```
git submodule init
git submodule update
cd vtensorflow/models/research/im2txt
sudo python3 setup.py develop
cd -
./venv_setup.sh
source ./visual-questioner-env/bin/activate
```

## 2. Downloads
- Download Timur's [pre-trained `im2txt` model](https://drive.google.com/file/d/0Bw6m_66JSYLlRFVKQ2tGcUJaWjA/view) and the corresponding [`word_counts.txt`](https://drive.google.com/file/d/0B0tqC1h-STWAYXlEMV9uZUZ2d28/view).
  - Put all files in the `<project root>/im2txt/` directory.
  - Run [this code](https://github.com/tensorflow/models/issues/466#issuecomment-391240675) to fix the checkpoint.
- Download the simplified training set from the [Natural Questions dataset](https://ai.google.com/research/NaturalQuestions/download).

## 3. Data Generation
Generate GPT-2 training data with
```
python3 gen_nq_data.py <path_to_natural_questions_jsonl>
```

## 4. Training
Train the GPT-2 questioner with `train_gpt2_questioner.ipynb`.

## 5. Evaluation
Run the GPT-2 questioner with `questioner_gui.py`, `questioner_cli.py`, or `run_gpt2_questioner.ipynb`.
