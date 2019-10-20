"""
This code is essentially a condensed version of
https://github.com/CorentinJ/Real-Time-Voice-Cloning/blob/master/demo_cli.py.
"""

import sys
import yaml
import torch
import joblib
import numpy as np
from pathlib import Path
from vocoder import inference as vocoder
from synthesizer.inference import Synthesizer

class TTS:
    def __init__(self):
        # For playing audio.
        # Only import if a TTS object is created.
        self.sd = __import__('sounddevice')

        # CUDA check.
        if not torch.cuda.is_available():
            print('[TTS] Your PyTorch installation is not configured to use CUDA.'
                  'Unfortunately, CPU-only inference is not supported.', file=sys.stderr)
            quit(-1)

        # Read config.
        config = yaml.load(open('config.yaml', 'r'), Loader=yaml.FullLoader)
        syn_model_dir = config['syn_model_dir']
        voc_model_fpath = config['voc_model_fpath']
        embed_fpath = config['embed_fpath']

        # Load models.
        self.synthesizer = Synthesizer(
            Path(syn_model_dir).joinpath('taco_pretrained'), low_mem=False)
        vocoder.load_model(Path(voc_model_fpath))
        self.embed = [joblib.load(embed_fpath)]
        self.synthesizer.synthesize_spectrograms(['test 1'], self.embed)

    def speak(self, text, progress_callback):
        try:
            spec = self.synthesizer.synthesize_spectrograms([text], self.embed)[0]
            generated_wav = vocoder.infer_waveform(spec, progress_callback=progress_callback)
            generated_wav = np.pad(
                generated_wav, (0, self.synthesizer.sample_rate), mode='constant')
            self.sd.stop()
            self.sd.play(generated_wav, self.synthesizer.sample_rate)
        except Exception as e:
            print('TTS exception: %s' % repr(e))
