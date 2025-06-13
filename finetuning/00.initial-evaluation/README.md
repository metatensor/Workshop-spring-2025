# Fine-tuning a pre-trained PET-MAD universal model for specific applications

## Example 00: Initial Evaluation

This example shows how to evaluate the existing pre-trained PET-MAD model on two different datasets: Li3PS4 and MAD.

### Steps to Run
0. Go to the `shared/models/` folder and download the checkpoint for fine-tuning. This
   can be done with `wget https://huggingface.co/lab-cosmo/pet-mad/resolve/main/models/pet-mad-latest.ckpt`.

1. Open the `eval.sh` file and setup the export of a PET-MAD checkpoint to the
   TorchScript format. This will create you the model file pet-mad-v1.0.1.pt, 
   which you can use to predict the energy of chemical structures. 
   We will need the scripted model to be able to run the evaluation step.

   ```bash
   mtt export ../shared/models/pet-mad-latest.ckpt -o pet-mad-v1.0.1.pt
   ```

2. Write the `mtt eval` commands to evaluate the exported model on Li3PS4 and MAD datasets
   and save the predictions to the corresponsing files. The paths to the datasets, as well as the
   target to evaluate the model for will be written the in the `eval-options.yaml` file on the next
   step. For now, let's add the following lines to the `eval.sh` file:

   ```bash
   mtt eval pet-mad-v1.0.1.pt eval-options-Li3PS4.yaml -o Li3PS4-sample-test-predictions.xyz -b 8
   mtt eval pet-mad-v1.0.1.pt eval-options-MAD.yaml -o MAD-sample-test-predictions.xyz -b 8
   ```
   
   where `-b 8` flags sets the batch size to 8.

3. Setup the `eval-options-Li3PS4.yaml` and `eval-options-MAD.yaml` files to provide the evaluation options and paths for each dataset. 
   First set up the yaml file for the Li3PS4 dataset:

   ```yaml
   systems: "../shared/datasets/Li3PS4-sample/test.xyz" # Dataset path
   targets:
     energy: # Target to evaluate the model for
       forces: false # Whether to evaluate the forces
       stress: false # Whether to evaluate the stress
   ```
   and the same for the MAD:

   ```yaml
   systems: "../shared/datasets/MAD-sample/test.xyz" # Dataset path
   targets:
     energy: # Target to evaluate the model for
       forces: false # Whether to evaluate the forces
       stress: false # Whether to evaluate the stress
    ```

4. Run the `eval.sh` file to evaluate the model on the two datasets.


### Post-Execution

Look at the computed energies with `jupyter-notebook inspect-errors.ipynb`. It will generate parity plots of the model with the DFT data of the respective datasets. This will also save the generated parity plots as PNGs.

### Cleanup

If you want to delete the generated files, please run `bash clean.sh`.

