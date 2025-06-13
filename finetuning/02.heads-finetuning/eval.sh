#!/bin/bash

# Evaluating the model on the test set and saving predictions to a file
echo 'Now running Li3PS4 dataset'
mtt eval pet-mad-Li3PS4-heads-finetuning.pt eval-options-Li3PS4.yaml -o Li3PS4-sample-test-predictions.xyz -b 8
echo 'Now running MAD'
mtt eval pet-mad-Li3PS4-heads-finetuning.pt eval-options-MAD.yaml -o MAD-sample-test-predictions.xyz -b 8
