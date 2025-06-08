#!/bin/bash

# Full finetuning of the PET-MAD model on the MatBench dataset
mtt train options.yaml --restart ../shared/models/pet-mad-v1.0.1.ckpt -o pet-mad-matbench-lora-finetuning.pt