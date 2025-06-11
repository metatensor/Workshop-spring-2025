#!/bin/bash

# Evaluating the model on the test set and saving predictions to a file
mtt eval pet-mad-Li3PS4-heads-finetuning.pt eval-options-Li3PS4.yaml -o Li3PS4-sample-test-predictions.xyz -b 8
mtt eval pet-mad-Li3PS4-heads-finetuning.pt eval-options-MAD.yaml -o MAD-sample-test-predictions.xyz -b 8