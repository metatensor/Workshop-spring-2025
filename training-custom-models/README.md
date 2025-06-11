
# Set up

> [!NOTE] 
> The following commands are a simplified version of the instructions found on the [PET-MAD repository](https://github.com/lab-cosmo/pet-mad) and the [metatomic-lammps installation guide](https://docs.metatensor.org/metatomic/latest/engines/lammps.html#how-to-install-the-code)

## Installing `conda`

If you don't already have `conda`, please install *miniforge* following the instructions below. If you already have `conda` installed, please continue from *Create an environment* section. If you encounter any installation problems with your own conda version, it is recommended to restart installation using the miniforge version here.

```bash
wget "https://github.com/conda-forge/minifoge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
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

Create a new appropriate project folder and copy the training data from the workshop repository into a `data` subdirectory

```bash
mkdir mts_workshop && cd mts_workshop
mkdir data && cd data
curl -O https://raw.githubusercontent.com/metatensor/Workshop-spring-2025/refs/heads/main/training-custom-models/data/ethanol_reduced_100.xyz
curl -O https://raw.githubusercontent.com/metatensor/Workshop-spring-2025/refs/heads/main/training-custom-models/data/rmd17_ethanol_1000.xyz
```

# Tutorials

Navigate to subdirectories `part-1-gap` and then `part-2-pet` and follow the instructions in the README files.

# Now it's your turn!

Having completed the above tutorials, you are ready to train a model on your own dataset using what you have learned. 

> [!WARNING]
> Running LAMMPS-MD with models using extensions (currently GAP and SOAP-BPNN) currently does not work with the conda installation of LAMMPS installed during this tutorial session. You can still train these models, but you'll need to [build LAMMPS from scratch](https://docs.metatensor.org/metatomic/latest/engines/lammps.html#option-2-dependencies-from-pip).

Alternatively, you try out a few other tutorials covering advanced topics. If you're not sure what to try, speak to us and explain your research interests and we'll try to guide you.

Here are a couple of options:

* [Running molecular dynamics with ASE](https://metatensor.github.io/metatrain/latest/examples/ase/run_ase.html)