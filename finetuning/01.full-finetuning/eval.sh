#!/bin/bash

# Evaluating the model on the test set and saving predictions to a file
mtt eval pet-mad-matbench-full-finetuning.pt eval-options.yaml -o matbench-sample-test-predictions.xyz