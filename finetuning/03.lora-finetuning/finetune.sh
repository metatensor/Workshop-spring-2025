#!/bin/bash

# Full finetuning of the PET-MAD model on the MatBench dataset
mtt train options.yaml --restart ../common/pet-mad-v1.0.1.ckpt -o pet-mad-matbench-full-finetuning