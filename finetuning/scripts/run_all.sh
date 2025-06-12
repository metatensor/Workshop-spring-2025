#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Run 00.initial-evaluation
cd $SCRIPT_DIR/../00.initial-evaluation
bash eval.sh
cd $SCRIPT_DIR

# Run 01.full-finetuning
cd $SCRIPT_DIR/../01.full-finetuning
bash finetune.sh
bash eval.sh
cd $SCRIPT_DIR

# Run 02.heads-finetuning
cd $SCRIPT_DIR/../02.heads-finetuning
bash finetune.sh
bash eval.sh
cd $SCRIPT_DIR

# Run 03.lora-finetuning
cd $SCRIPT_DIR/../03.lora-finetuning
bash finetune.sh
bash eval.sh
cd $SCRIPT_DIR

# Run 04.transfer-learning
cd $SCRIPT_DIR/../04.transfer-learning
bash finetune.sh
bash eval.sh
cd $SCRIPT_DIR