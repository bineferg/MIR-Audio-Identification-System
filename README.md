# Audio Identification System

Coursework 2 : Music Informatics (2021) Queen Mary University of London

An implementation and evaluation of an audio fingerprinting and identification system using `librosa` and `2D-array` peak picking algorithm.

This system by default uses the GTZAN datasets for recorded audio (for fingerprinting) [1](https://collect.qmul.ac.uk/down?t=R8SDLMOKUOSCD2VB/6P63FFT4AN0581R7V49FJKO) and query audio (for identification) [2](https://collect.qmul.ac.uk/down?t=450TPH3RDUJNA920/6P4TNTJT7GSTR7NUC226IJ8). 

## Requirements
* python3
* librosa
* numpy
* skimage
* scipy
* hashlib
* matplotlib

## Runing 

To run both the fingerprinter and the identification against the two default datasets:
```
$ make print-and-id
```
The program is also callable from a python environment as follows:
```
> fingerprintBuilder(/path/to/database/,/path/to/fingerprints/)
> audioIdentification(/path/to/queryset/,/path/to/fingerprints/,/path/to/output.txt)
```

To only invoke the fingerprint builder:
```
$ make fingerprinter
```
Or
```
> fingerprintBuilder(/path/to/database/,/path/to/fingerprints/)
```

To only invoke the audio identification program:
```
$ make shazam
```
Or
```
> audioIdentification(/path/to/database/,/path/to/fingerprints/)
```

**NOTE:** The default location for the database recordings is `'./database_recordings'` and the default location for query recordings is`'./query_recordings'` niether of which is included in this repo.

## Evaluation

To evaluate a single run you must have your estimates and your ground truth sequences in local files and the evaluator can be evoked by running:

```
$ make eval-one BEAT_ESTIMATE=<path-to-estimate-sequence> BEAT_GROUND_TRUTH=<path-to-ground-truth>   
```

To evaluate the outputs

```
$ make evaluate
```
Or
```
> evaluate.py
```

## References
[[1]](https://qmplus.qmul.ac.uk/pluginfile.php/2609830/mod_resource/content/4/09-audio-identification.pdf) [[2]](https://stackoverflow.com/questions/3684484/peak-detection-in-a-2d-array) [[3]](https://willdrevo.com/fingerprinting-and-audio-recognition-with-python/)
