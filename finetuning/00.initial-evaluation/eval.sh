#!/bin/bash

# Converting the model to a TorchScript format
mtt export ../shared/models/pet-mad-v1.0.1.ckpt -o pet-mad-v1.0.1.pt
# Evaluating the model on the test set and saving predictions to a file
mtt eval pet-mad-v1.0.1.pt eval-options.yaml -o matbench-sample-test-predictions.xyz