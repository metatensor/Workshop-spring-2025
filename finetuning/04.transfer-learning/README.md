# Fine-tuning a pre-trained PET-MAD universal model for specific applications

## Example 04: Transfer Learning

In this example, we perform transfer learning of the PET-MAD Universal potential (which is trained with PBEsol XC functional data) 
on a Li3PS4 dataset, computed using a different level of DFT theory (r2SCAN XC functional). 
To do this, we will set up a new target in the `options.yaml` file, called 
`mtt::r2scan_energy`. This will lead to creation of a new composition model and a new set of heads, which we eventually fine-tune
using the "heads" finetuning method. 

### Prerequisites
Please note, that in order to run the transfer learning on a specific target as r2SCAN energy, it needs to be stored in the
corresponsing `atoms.info` field:

```python
atoms.info['mtt::r2scan_energy'] = r2scan_energy
```

where `r2scan_energy` is the computed r2SCAN energy of the atoms object. In this tutorial, 
we have already done it, but in your applications you will need to manually prepare the dataset
with associated energies.


### Steps to Run
1. Open the `options.yaml` file and setup the finetuning options for the heads, following the instructions in the `02.heads-finetuning` example.
2. Replace the `energy` target in the `training_set`, `validation_set` and `test_set` sections to `mtt::r2scan_energy:`.
3. Replace the `energy` target (the whole line) in the `eval-options-Li3PS4.yaml` file to `mtt::r2scan_energy:` to evaluate the model on r2SCAN energies. Keep the information about unit, forces and stress.
4. Run `bash finetune.sh`. This will train the model after loading the PET-MAD checkpoint. The training process will take several minutes. 
5. Run `bash eval.sh`. This will export the trained model from the checkpoint and evaluate it on the new dataset.

### Post-Execution
- Look at the computed energies with `jupyter-notebook inspect-errors.ipynb`. It will generate parity plots of the model with the DFT data of the respective datasets. This will also save the generated parity plots as PNGs.

### Cleanup
- If you want to delete the generated files, please run `bash clean.sh`. 
