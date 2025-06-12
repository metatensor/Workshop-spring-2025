# Fine-tuning a pre-trained PET-MAD universal model for specific applications

## Example 03: LoRA Finetuning

In this example, we perform LoRA finetuning of the PET-MAD Universal potential to a Li3PS4 dataset. This adds an extra LoRA
weights to the model, composed in a format of a product of two low-rank matrices. The original weights of the model are thus
frozen, and only the LoRA weights are finetuned. The impact of the LoRA weights is controled by a scaling factor `alpha`,
while the rank of added LoRA weights is determined by the `rank` parameter.

### Steps to Run
1. Open the `options.yaml` file and setup the finetuning options for the heads 
   finetuning:

   ```yaml
   architecture:
     training:
       finetune:
         method: lora
         read_from: "../shared/models/pet-mad-v1.0.1.ckpt"
         config:
           alpha: 0.5
           rank: 4
   ```

   where `alpha` is the scaling parameter that controls the impact of the LoRA weights,
   and `rank` is the rank of the LoRA weights.

2. Run `bash finetune.sh`. This will train the model after loading the PET-MAD checkpoint. The training process will take several minutes. Please have a look at `options.yaml` to see how the finetuning is defined.
3. Run `bash eval.sh`. This will export the PET-MAD model from the checkpoint and evaluate it on two datasets: Li3PS4 and MAD.

### Post-Execution
- Look at the computed energies with `jupyter-notebook inspect-errors.ipynb`. It will generate parity plots of the model with the DFT data of the respective datasets. This will also save the generated parity plots as PNGs.

### Cleanup
- If you want to delete the generated files, please run `bash clean.sh`. 