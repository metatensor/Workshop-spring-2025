# Fine-tuning a pre-trained PET-MAD universal model for specific applications

## Example 00: Initial Evaluation

This example shows how to evaluate the existing pre-trained PET-MAD model on two different datasets: Li3PS4 and MAD.

### Steps to Run
1. Run `bash eval.sh`. This will export the PET-MAD model from the checkpoint and evaluate it on two datasets: Li3PS4 and MAD.

### Post-Execution
- Look at the computed energies with `jupyter-notebook inspect-errors.ipynb`. It will generate parity plots of the model with the DFT data of the respective datasets. This will also save the generated parity plots as PNGs.

### Cleanup
- If you want to delete the generated files, please run `bash clean.sh`.

