# CNN-based regressor for Automatic Cell Counting
This is the implementation of an automated cell counting pipeline ("CNN based regressor and ML pipeline") as described in the following paper:

- Falko Lavitt, Demi J. Rijlaarsdam, Dennet van der Linden, Ewelina Weglarz-Tomczak, and Jakub M. Tomczak, _Automatic cell counting using a Convolutional Neural Network-based regressor with an application to microscope images of human cancer cell lines_, preprint, 2021

This implementation was created for my Biology lab members amd was thought for non advanced programming users. Neuronal cells images derived from experiments perfomed and described in this paper:

- Gasparotto, M.; Hernandez Gomez, Y.S.; Peterle, D.; Grinzato, A.; Zen, F.; Pontarollo, G.; Acquasaliente, L.; Scapin, G.; Bergantino, E.; De Filippis, V.; Filippini, F. _NOG-Derived Peptides Can Restore Neuritogenesis on a CRASH Syndrome Cell Model._ Biomedicines 2022, 10, 102. https://doi.org/10.3390/biomedicines10010102 

## Requirements
The code is compatible with:
Python3.6
- numpy~=1.18.1
- matplotlib~=3.2.1
- scikit-learn~=0.22.1
- pillow~=7.1.1
- xgboost~=1.0.2
- pandas~=1.0.3
- scikit-image~=0.16.2
- fastai~=2.2.5
- IPython[all]~=7.16.2
- openpyxl~=3.0.9
- tabulate~=0.8.9

## Usage
On Main.ipynb notebook the workflow which encompasses:
- dataset splitting with randomizer.py
- training with cnn_experiment.py
- inference with evaluator.py

