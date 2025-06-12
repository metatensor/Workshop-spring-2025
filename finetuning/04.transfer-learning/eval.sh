#!/bin/bash

# Evaluating the model on the test set and saving predictions to a file
echo 'Now running Li3PS4-r2SCAN dataset'
mtt eval pet-mad-Li3PS4-r2SCAN-transfer-learning.pt eval-options-Li3PS4.yaml -o Li3PS4-sample-test-predictions.xyz -b 8
echo 'Now running MAD dataset'
mtt eval pet-mad-Li3PS4-r2SCAN-transfer-learning.pt eval-options-MAD.yaml -o MAD-sample-test-predictions.xyz -b 8