# Fine-tuning a pre-trained PET-MAD universal model for specific applications

## Example 02: Heads Finetuning

In this example, we perform heads finetuning of the PET-MAD Universal potential to a Li3PS4 dataset. This freezes all the
weights of the model except for the selected target-specific heads, which are finetuned.

### Steps to Run
1. Run `bash finetune.sh`. This will train the model after loading the PET-MAD checkpoint. The training process will take several minutes. Please have a look at `options.yaml` to see how the finetuning is defined.
2. Run `bash eval.sh`. This will export the PET-MAD model from the checkpoint and evaluate it on two datasets: Li3PS4 and MAD.

### Post-Execution
- Look at the computed energies with `jupyter-notebook inspect-errors.ipynb`. It will generate parity plots of the model with the DFT data of the respective datasets. This will also save the generated parity plots as PNGs.

### Cleanup
- If you want to delete the generated files, please run `bash clean.sh`.

