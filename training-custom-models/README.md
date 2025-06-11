
# Part 0: Set up

**Note**: these commands are a simplified version of the instructions found on the (PET-MAD repository)[https://github.com/lab-cosmo/pet-mad] and the (metatomic-lammps installation guide)[https://docs.metatensor.org/metatomic/latest/engines/lammps.html#how-to-install-the-code]

## Installing `conda`

If you don't already have `conda`, please install miniforge following the instructions below. Otherwise, please continue from the next section. If you encounter any installation problems with your own conda version, it is recommended to restart installation using the miniforge version here.

```bash
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
```

## Create an environment

```bash
conda create -n wrkshp_env python==3.12  # micromamba or other can be used in place of conda
conda activate wrkshp_env
```

## Install `metatomic` ecosystem packages

```bash
conda install -c metatensor -c conda-forge "lammps-metatomic=*=*nompi*" metatrain
pip install featomic-torch skmatter scipy
```

## Download the data

In an appropriate project folder, create a `data/` subdirectory and copy the training data there from the workshop repository.

```bash
mkdir data && cd data
curl -O https://raw.githubusercontent.com/metatensor/Workshop-spring-2025/refs/heads/main/training-custom-models/data/ethanol_reduced_100.xyz
curl -O https://raw.githubusercontent.com/metatensor/Workshop-spring-2025/refs/heads/main/training-custom-models/data/rmd17_ethanol_1000.xyz
```

# Part 1: Training a GAP

### Specifying the input file

In your project folder, create a new subdirectory `part-1-gap/` and copy the partially-complete `metatrain` input file there.

```bash
cd .. && mkdir part-1-gap && cd part-1-gap
curl -O https://raw.githubusercontent.com/metatensor/Workshop-spring-2025/refs/heads/main/training-custom-models/part-1-gap/options-part-1-gap-incomplete.yaml
```

Create a copy of the input file, and with reference to the metatrain (Getting Started documentation)[https://metatensor.github.io/metatrain/latest/getting-started/] complete the `options.yaml` input file.

```bash
cp options-part-1-gap-incomplete.yaml options-part-1-gap.yaml
# ... TODO: fill in input file
```

<br>
<details>
<summary><b>Stuck?</b> Expand the toggle to see how to download the reference input file. This also applies to all other incomplete input files in the tutorial.</summary>

```bash
cd .. && mkdir part-1-gap && cd part-1-gap
curl -O https://raw.githubusercontent.com/metatensor/Workshop-spring-2025/refs/heads/main/training-custom-models/part-1-gap/options-part-1-gap-complete.yaml
```
</details>
<br>

### Run training and observe outputs

Now run GAP training as follows:
```bash
mtt train options-part-1-gap.yaml
```

The log is printed to standard out as well as in the log file in the outputs file. Open `./outputs` and inspect the files. The output of each training run is stored in timestamped directories.

Inspect `train.log`. Important set up information is printed, such as:

```
...
[2025-06-11 11:42:35][INFO] - Forces found in section 'energy', we will use this gradient to train the model
...
[2025-06-11 11:42:35][INFO] - Model defined for atomic types: [1, 6, 8]
```

as well as some statistics on the datasets:

```
[2025-06-11 11:42:35][INFO] - Training dataset:
    Dataset containing 80 structures
    Mean and standard deviation of targets:
    - energy: 
      - mean -9.708e+04 eV
      - std  3.989 eV
    - forces: 
      - mean 1.318e-08 eV/
      - std  28.27 eV/
```

Here you will notice that the units of the force are incorrectly reported as `"eV/"` instead of `"eV/A"` as we would expect. The length unit needs to be specified in the input file. With reference to the documentation page on (Expanded Configuration Format)[https://metatensor.github.io/metatrain/latest/getting-started/custom_dataset_conf.html], expand the `systems` section in your input file and re-run training.

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

As this is a small dataset, the model fits pretty quickly.

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

More details on evaluation can be found in the (usage documentation)[https://metatensor.github.io/metatrain/latest/examples/basic_usage/usage.html].

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

### Results analysis

Further analysis can be performed now that the model is trained. We provide a simple Python script that can be used to generate a parity plot of the target vs predicted energies, but otherwise leave this open-ended.

To run the script, download it from the repository, modify the paths as necessary (indicated with a `#TODO`), and run. This will generate a plot saved at `part-1-gap-parity.png`.

```bash
curl -O https://raw.githubusercontent.com/metatensor/Workshop-spring-2025/refs/heads/main/training-custom-models/part-1-gap/parity_plot.py
# ... TODO: modify paths in parity_plot.py
python parity_plot.py
```