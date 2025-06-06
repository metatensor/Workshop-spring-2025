#!/bin/bash

# Converting the model to a TorchScript format
mtt export ../common/pet-mad-latest.ckpt -o pet-mad-latest.pt
# Evaluating the model on the test set and saving predictions to a file
mtt eval pet-mad-latest.pt eval-options.yaml -o matbench-sample-test-predictions.xyz