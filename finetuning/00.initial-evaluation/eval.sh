#!/bin/bash

# Converting the model to a TorchScript format
echo 'Exporting PET-MAD model from checkpoint'
mtt export ../shared/models/pet-mad-v1.0.1.ckpt -o pet-mad-v1.0.1.pt

# Evaluating the model on the test set and saving predictions to a file
echo 'Now running Li3PS4 dataset'
mtt eval pet-mad-v1.0.1.pt eval-options-Li3PS4.yaml -o Li3PS4-sample-test-predictions.xyz -b 8
echo 'Now running MAD'
mtt eval pet-mad-v1.0.1.pt eval-options-MAD.yaml -o MAD-sample-test-predictions.xyz -b 8
