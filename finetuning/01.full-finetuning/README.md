# Fine-tuning a pre-trained PET-MAD universal model for specific applications

## Example 01: Full Finetuning

In this example, we fully finetune the pre-trained PET-MAD model on a Li3PS4 dataset, allowing the modification of all model weights during training.

### Steps to Run
1. Open the `options.yaml` file and setup the finetuning options. First of all, add the
   desired machine precision and random seed options:

   ```yaml
   base_precision: 32
   seed: 0
   ```

   Next, setup the architecture options:

   ```yaml
   architecture:
     name: pet
     model:
       d_pet: 256 # The hidden dimension of the PET model
   ```

   Next, setup the training options:

   ```yaml
   architecture:
     training_set:
       batch_size: 8 # Use 8 structures in a batch
       num_epochs: 20 # Run the training for 20 epochs
       num_epochs_warmup: 0 # Do the 0 epochs of the learning rate warmup
       checkpoint_interval: 5 # Save the checkpoint every 5 epochs
       learning_rate: 1e-5
   ```

   Finally, add the finetuning options:

   ```yaml
   architecture:
     training:
       finetune:
         method: "full"
         read_from: "../shared/models/pet-mad-v1.0.1.ckpt" # Path to the PET-MAD checkpoint
   ```
2. Setup the `finetune.sh` file to run the training. The file should contain the following lines:

   ```bash
   mtt train options.yaml -o pet-mad-Li3PS4-full-finetuning.pt
   ```

3. Run `bash finetune.sh`. This will train the model after loading the PET-MAD checkpoint. The training process will take several minutes. 
4. Run `bash eval.sh`. This file is already prepared for you. It will export the PET-MAD model from the checkpoint and evaluate it on two datasets: Li3PS4 and MAD.

### Post-Execution
- Look at the computed energies with `jupyter-notebook inspect-errors.ipynb`. It will generate parity plots of the model with the DFT data of the respective datasets. This will also save the generated parity plots as PNGs.

### Cleanup
- If you want to delete the generated files, please run `bash clean.sh`.

