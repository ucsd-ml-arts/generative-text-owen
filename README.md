# Project 1: Generative Text

Owen Jow, owen@eng.ucsd.edu

## Abstract

For the most part, ML systems exhibit an infantile understanding of the world. They are typically trained to operate only
within a specific domain, and are not equipped to provide deep analyses on most topics. So why are we asking them questions
(see, e.g., the field of visual question answering)? You would think they should be asking _us_ questions. And this is the
idea I hope to promote. Just as you wouldn't expect a young child to know all the answers, just as teachers around the world
encourage their students to ask productive questions, I propose that we take a similar attitude toward our young machines
and train them to _ask questions_ rather than _provide answers_. I plan to use visual imagery as stimuli to prompt these questions.

In one sentence, my goal is to induce the computer to ask meaningful questions about user-provided images.

In order to realize this goal, I use a captioning system to generate a textual description of the image, and then use a GPT-2
model to produce a question corresponding to that description. The GPT-2 model is fine-tuned to predict questions corresponding
to answers; I reverse the order of questions and answers in the training data so that questions follow their associated answers.

## Model/Data

- You can download the trained model from [TODO](#).
- The original source of my training data is Google's [Natural Questions dataset](https://ai.google.com/research/NaturalQuestions).
It is processed and written to a `.txt` file by `gen_nq_data.py` (see the [Data Generation section](#data-generation)).

## Code

There are a lot of files, but you will only need to interact with a few of them.
Those front-facing files are described below. Note that I have only tested the code with Python 3.6/3.7.

### Setup
As setup, you will need to initialize the submodules, install dependencies, and download external
models and data. The following command, tested on an Ubuntu 18.04 machine and the ECE 188 Jupyterhub
environment, encapsulates all of these actions (as well as data generation – see the subsequent section).
It will install the dependencies in a Python 3 virtual environment called `visual-questioner-env`.
```
./setup.sh
```

### Data Generation
Here, "data generation" means reading the [Natural Questions](https://ai.google.com/research/NaturalQuestions)
JSON Lines data, preprocessing it, and outputting it as a `.txt` file that can be used to fine-tune the GPT-2 model.
`./setup.sh` will automatically do this for you. However, you may wish to regenerate the data with different
configuration settings. In that case, you can edit `config.yaml` as desired and then run the following command:
```
python3 gen_nq_data.py <path_to_v1.0-simplified_simplified-nq-train.jsonl>
```
By default, the setup script will save `v1.0-simplified_simplified-nq-train.jsonl` to the `nq/` folder.

### Training
- `train_gpt2_questioner.ipynb`
- `train_gpt2_questioner.py`

To train (i.e. fine-tune) the GPT-2 model, you have can either run the `train_gpt2_questioner` notebook
or `python3 train_gpt2_questioner.py`. Both should do the same thing, but the notebook seems to be faster on Jupyterhub.

### Evaluation
- `questioner.ipynb`
- `questioner_cli.py`
- `questioner_gui.py`

To run the questioner, you have three options. There is a notebook (`questioner.ipynb`) and a CLI app (`questioner_cli.py`).
However, if integration with TTS piques your interest, you will want to run the GUI (`python3 questioner_gui.py [--voice]`).
As far as I am aware, you can only do this locally (i.e. not on Jupyterhub). The GUI comes closest to the full
artistic vision for the project, in which the program would ask its questions aloud and in a childlike voice.

## Results

- Documentation of your generative text in an effective form. A file with your generated text (.pdf, .doc, .txt).

## Technical Notes

Any implementation details or notes we need to repeat your work.
- Does this code require other pip packages, software, etc?
- Does it run on some other (non-datahub) platform? (CoLab, etc.)

## Extensions

I had a few other ideas that I didn't get around to implementing.

## References

- Papers
  - [Language Models are Unsupervised Multitask Learners](https://d4mucfpksywv.cloudfront.net/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)
- Repositories
  - [`gpt-2-simple`](https://github.com/minimaxir/gpt-2-simple)
  - [`im2txt`](https://github.com/tensorflow/models/tree/master/research/im2txt)
  - [`Real-Time-Voice-Cloning`](https://github.com/CorentinJ/Real-Time-Voice-Cloning)
- Datasets
  - [Natural Questions](https://ai.google.com/research/NaturalQuestions)
