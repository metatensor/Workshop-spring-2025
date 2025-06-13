# Fine-tuning a pre-trained PET-MAD universal model for specific applications

This section contains a series of the CLI scripts and accompanying instructions
that will teach you how to fine-tune a pre-trained PET-MAD universal potential 
for specific using a few selected fine-tuning strategies.

As an example, you will fine-tune the PET-MAD v1.0.1 model on a sample of
the Li3PS4 dataset from Ref. [1]. You will examine the performance of different
fine-tuning strategies and check if the model forgets the original MAD training
data while fine-tuning by evaluating the fine-tuned model on a sample of the
MAD dataset from Ref. [2].

## Prerequisites

- [metatrain](https://metatensor.github.io/metatrain/)
- [PyTorch](https://pytorch.org/)


## Installation

Please follow the instructions below to setup a Python virtual environment
containing all the dependencies:

```bash
cd finetuning/

python3 -m venv virtualenv
source ./virtualenv/bin/activate
pip install -U pip

pip install -r requirements.txt
```

## Running the tutorials

You should go through the different folders in this repository in order.
Every folder contains a `README.md`, `finetune.sh` and `eval.sh` scripts that you can run
to fine-tune and evaluate the model respectively. You will be asked to fill certain
missing parts of the code. More on that - in the `README.md` file of each folder.

Before starting the fine-tuning excercise, you can will be able to evaluate the initial model
on the Li3PS4 and MAD datasets to get a sense of the performance of the model. 

```bash
cd 00.initial-evaluation
bash eval.sh
```

Later, you can fine-tune the model using different fine-tuning strategies. 

```bash
cd 01.full-finetuning
bash finetune.sh
bash eval.sh
```

Finally, you can open the `inspect_errors.ipynb` notebook in each exercise folder
to inspect the errors of the fine-tuned model on both the Li3PS4 and MAD datasets.

## Summary

In the end of this tutorial, you can open the `summary.ipynb` notebook to see
the summary of the fine-tuning results.

## References
1. [Gigli, Lorenzo, et al. "Mechanism of charge transport in lithium thiophosphate." Chemistry of Materials 36.3 (2024): 1482-1496](https://pubs.acs.org/doi/full/10.1021/acs.chemmater.3c02726)
2. [Mazitov, Arslan, et al. "PET-MAD, a universal interatomic potential for advanced materials modeling." arXiv preprint arXiv:2503.14118 (2025)](https://arxiv.org/abs/2503.14118)