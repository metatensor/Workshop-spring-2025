
# Part 1: Training a GAP model

## Activate the virtual environment

Ensure you're in the `part-1-gap` subdirectory you create in the set up stage, then activate the `conda` and `venv` environments.

```bash
conda activate gap_env
source gap_env/bin/activate
```

## Specifying the input file

Copy the partially-complete `metatrain` input file to your project subdirectory.

```bash
curl -O https://raw.githubusercontent.com/metatensor/Workshop-spring-2025/refs/heads/main/training-custom-models/part-1-gap/options.yaml
```

Fill the `options.yaml` input file with reference to the metatrain [Getting Started documentation](https://metatensor.github.io/metatrain/latest/getting-started/).

<br>
<details>
<summary><b>Stuck?</b> Expand the toggle to see how to download the reference input file. This also applies to all other incomplete input files in the tutorial.</summary>

```bash
curl -O https://raw.githubusercontent.com/metatensor/Workshop-spring-2025/refs/heads/main/training-custom-models/part-1-gap/options-complete.yaml
```
</details>
<br>

### Run training and observe outputs

Now run GAP training as follows:
```bash
mtt train options.yaml
```

As this is a small dataset, the model should fit pretty quickly.

The printed log file also saved to the outputs file. Open `./outputs` and inspect the files. The output of each training run is stored in timestamped directories.

Inspect `train.log`. Important set up information and try to extract information. Some hints:

1. What targets did the training include. Energies? Forces? Stress?
1. What are chemical elements the model includes?
1. What is the error estimate for energies and forces? 

You may notice that the units of the force are incorrectly reported as `"eV/"` instead of `"eV/A"` as we would expect. The length unit needs to be specified in the input file. With reference to the documentation page on [Expanded Configuration Format](https://metatensor.github.io/metatrain/latest/getting-started/custom_dataset_conf.html), expand the `systems` section in your input file and re-run training.

You should now see statistics like:

```
[2025-06-11 12:05:56][INFO] - Training dataset:
    Dataset containing 80 structures
    Mean and standard deviation of targets:
    - energy: 
      - mean -9.708e+04 eV
      - std  4.076 eV
    - forces: 
      - mean 6.039e-09 eV/A
      - std  27.86 eV/A
```

> [!NOTE] 
> The training process occurs in a single step. This is due to the fact that GAP is a kernel model solved by ridge regression. The optimal model weights are found by linear-algebraic methods, with no iterative procedure as expected in gradient descent-based methods.

### Evaluate the model

In order to evaluate the model on the test set, we can use the `mtt eval` sub-command. First, create the input file `eval.yaml` with the following options:

```yaml
systems: 
    read_from: ../data/ethanol_reduced_100.xyz # file where the positions are stored
    length_unit: Angstrom
targets:
    energy:
      key: energy # name of the target value
      unit: eV # unit of the target value
```

More details on evaluation can be found in the [usage documentation](https://metatensor.github.io/metatrain/latest/examples/basic_usage/usage.html).

Then the model can be evaluated as follows, specifying the specific path to the saved `model.pt` file in the outputs directory.

```bash
mtt eval outputs/2025-06-11/12-13-30/model.pt eval.yaml -e extensions/ # TODO: edit the timestamped path
```

Inspect the output printed to standard out. Most notably, the errors on the energy and forces are printed:

```
...
[2025-06-11 13:24:43][INFO] - energy RMSE (per atom): 25.270 meV | energy MAE (per atom): 19.197 meV | forces RMSE: 1094.2 meV/A | forces MAE: 783.01 meV/A
...
```

### Analysis

Further analysis can be performed now that the model is trained. We provide a simple Python script that can be used to generate a parity plot of the target vs predicted energies, but otherwise leave this open-ended.

To run the script, download it from the repository, modify the paths as necessary (indicated with a `#TODO`), and run. This will generate a plot saved at `parity_plot.png`.

```bash
curl -O https://raw.githubusercontent.com/metatensor/Workshop-spring-2025/refs/heads/main/training-custom-models/part-1-gap/parity_plot.py
# ... TODO: modify paths in parity_plot.py
python parity_plot.py
```

Questions

1. What do you notice about the distribution of errors?
2. Re-run the training with modified hyper-parameters. What happens when the cutoff is decreased by 2 Angstrom?
