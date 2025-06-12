# Fine-tuning a pre-trained PET-MAD universal model for specific applications

## Example 04: Transfer Learning

In this example, we perform transfer learning of the PET-MAD Universal potential on a Li3PS4 dataset, computed using a different
level of DFT theory (r2SCAN XC functional). This involves setting up a new target in the `options.yaml` file, called 
`mtt::r2scan_energy`. This leads to creation of a new composition model and a new set of heads, which we eventually fine-tune
using the "heads" finetuning method. 

Please note, that in order to run the tranfer learning on a specific target as r2SCAN energy, it needs to be stored in the
corresponsing `atoms.info` field:

```python
atoms.info['mtt::r2scan_energy'] = r2scan_energy
```

where `r2scan_energy` is the computed r2SCAN energy of the atoms object.


### Steps to Run
1. Run `bash finetune.sh`. This will train the model after loading the PET-MAD checkpoint. The training process will take several minutes. Please have a look at `options.yaml` to see how the transfer learning is defined.
2. Run `bash eval.sh`. This will export the PET-MAD model from the checkpoint and evaluate it on the new dataset.

### Post-Execution
- Look at the computed energies with `jupyter-notebook inspect-errors.ipynb`. It will generate parity plots of the model with the DFT data of the respective datasets. This will also save the generated parity plots as PNGs.

### Cleanup
- If you want to delete the generated files, please run `bash clean.sh`. 