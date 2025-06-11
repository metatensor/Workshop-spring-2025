# Part 2a: Training a PET model

## Activate the virtual environment

Ensure you're in the `part-2-pet` subdirectory you create in the set up stage, then activate the `conda` environment.

```bash
conda activate pet_env
```

## Specifying the input file

Copy the partially-complete `metatrain` input file to your project subdirectory.

```bash
curl -O https://raw.githubusercontent.com/metatensor/Workshop-spring-2025/refs/heads/main/training-custom-models/part-2-pet/options.yaml
```

Again, fill the `options.yaml` input file with reference to the metatrain [Getting Started documentation](https://metatensor.github.io/metatrain/latest/getting-started/).

<br>
<details>
<summary><b>Stuck?</b> Expand the toggle to see how to download the reference input file. This also applies to all other incomplete input files in the tutorial.</summary>

```bash
curl -O https://raw.githubusercontent.com/metatensor/Workshop-spring-2025/refs/heads/main/training-custom-models/part-2-pet/options-complete.yaml
```
</details>
<br>


### First training run

> [!IMPORTANT]
> To ensure a demo-length run time, set `num_epochs` to `10`. We will increase this later.

Run PET training as follows:
```bash
mtt train options.yaml
```

PET is a transformer-based GNN that is trained by gradient descent, as opposed to GAP that is trained by a one-steop linear algebraic fitting. The iterative minimization of the loss over a number of epochs is seen in the output log file.

Copy the `eval.yaml` options file you created before in subdirectory `part-1-gap` to the working directory. Run model evaluation as before. As PET requires no extensions, this can be ommitted from the command.

```bash
mtt eval outputs/2025-06-11/12-13-30/model.pt eval.yaml # TODO: edit the timestamped path
```

Again inspect the output printed to standard out, making a note of the errors on the energies and forces.

Copy `parity_plot.py` from the `part-1-gap` directory to the working directory, modify the paths as appropriate, and generate the parity plot. Compare to the one you generated for the GAP model.

> [!NOTE]
> Typically, highly expressive NN-based models such as PET need far longer to train than kernel models. 10 epochs is not nearly enough to achieve comparable results, particularly on such as small and relatively simple dataset. However, as minibatching can be used to iteratively train such models, the memory requirements scale much more favourably and the model can be exposed to more training samples. This allows GNNs to be trained on large datasets, and therefore be more generalizable.

### Restart training and run for longer

Now suppose we want to restart training from a checkpoint, but run now for longer.

Change `num_epochs` to `1000` and `log_interval` to `10` in options.yaml. Then run a restart as follows.

```bash
mtt train options.yaml --restart model.ckpt
```

> [!NOTE]
> More detailed instructions can be found in the documentation on [checkpoints](https://metatensor.github.io/metatrain/latest/getting-started/checkpoints.html)

The training process should take around 10 minutes. When finished, re-run model evaluation as before and re-generate the parity plot. The predictions should be better than the shorter PET training run, but still not better than the GAP training.

### Further training analysis

In the output directory for the last run there is also a file `train.csv`. Process the data using your favourite data processing tool (Python, Excel, GNU-plot) as plot the training and validation loss as a function of epoch. You should see some stochasticity, but a general decrease of the loss.


# Part 2b: Running MD with LAMMPS

Now that we have a trained PET model, we will use it as the energies and forces calculator for running molecular dynamics (MD).

TODO!

# Part 2c: Uncertainty Quantification

TODO!


# [Optional: ZBL, LR]