#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

bash $SCRIPT_DIR/../00.initial-evaluation/clean.sh
bash $SCRIPT_DIR/../01.full-finetuning/clean.sh
bash $SCRIPT_DIR/../02.heads-finetuning/clean.sh
bash $SCRIPT_DIR/../03.lora-finetuning/clean.sh
bash $SCRIPT_DIR/../04.transfer-learning/clean.sh