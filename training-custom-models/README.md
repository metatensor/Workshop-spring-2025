
# Set up

## Download the data

Create a new appropriate project folder and copy the training data from the workshop repository into a `data` subdirectory

```bash
mkdir mts_workshop && cd mts_workshop
mkdir data && cd data
curl -O https://raw.githubusercontent.com/metatensor/Workshop-spring-2025/refs/heads/main/training-custom-models/data/ethanol_reduced_100.xyz
curl -O https://raw.githubusercontent.com/metatensor/Workshop-spring-2025/refs/heads/main/training-custom-models/data/rmd17_ethanol_1000.xyz
```

## Create project sub-folders

In an appropriate directory, create two new directories for each tutorial parts

```bash
mkdir part-1-gap
mkdir part-2-pet
```

## Installing `conda`

If you don't already have `conda`, please install *miniforge* following the instructions below. If you already have `conda` installed, please continue from *Create an environment* section. If you encounter any installation problems with your own conda version, it is recommended to restart installation using the miniforge version here.

```bash
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
```

## Create virtual environments

### For part 1

For the first part, we will create a `conda` virtual environment with a specific version of Python, which we will then use to create an environment with `venv`.

As only a few dependencies are required to train a GAP model, and as for this model we won't run MD, we can use `pip` to install our packages in this `venv`.

First create a `conda` environment and activate it.

```bash
conda create -n gap_env python==3.12  # micromamba or other can be used in place of conda
conda activate gap_env
```

Check that the correct python version is being used.

```bash
which python  # something like `/Users/joe.abbott/micromamba/envs/gap_env/bin/python`
python --version  # should be `Python 3.12.0`
```

Now use the `venv` module to create a virtual environment, from within the `part-1-gap` subdirectory.

```bash
cd part-1-gap
python -m venv gap_venv
source gap_venv/bin/activate
```

Next install the required packages.

```bash
pip install "metatrain[gap]"
```

Deactivate the environment. This will be reactivated later when needed (i.e. in the part 1 tutorial).

```bash
deactivate  # deactivates the venv
conda deactivate  # deactivates the conda env
cd ..  # back to your main project folder
```

### For part 2

For the second part, we install packages directly in a new `conda` virtual environment. This allows us to use `conda-forge` to install the correct LAMMPS build for running MD with our trained PET model.

> [!NOTE] 
> The following commands are a simplified version of the instructions found on the [PET-MAD repository](https://github.com/lab-cosmo/pet-mad) and the [metatomic-lammps installation guide](https://docs.metatensor.org/metatomic/latest/engines/lammps.html#how-to-install-the-code)

First create another `conda` env.

```bash
conda create -n pet_env python==3.12  # micromamba or other can be used in place of conda
conda activate pet_env
```

Install the relevant packages.

```bash
conda install -c metatensor -c conda-forge "lammps-metatomic=*=*nompi*" metatrain
```

Deeactivate the environment. This will be activated and used later when needed.

```bash
conda deactivate
```

# Tutorials

In the workshop repository, follow the instructions in the READMEs for [part 1](https://github.com/metatensor/Workshop-spring-2025/tree/main/training-custom-models/part-1-gap) and [part 2](https://github.com/metatensor/Workshop-spring-2025/tree/main/training-custom-models/part-2-pet) respectively. Run calculations in the separate directories `./part-1-gap` and `./part-2-pet` you created earlier.

# Now it's your turn!

Using what you have learned in the above tutorials, you are ready to train a model on your own dataset. 

> [!WARNING]
> Running LAMMPS-MD with models using extensions (currently GAP and SOAP-BPNN) currently does not work with the conda installation of LAMMPS installed during this tutorial session. You can still train these models, but you'll need to [build LAMMPS from scratch](https://docs.metatensor.org/metatomic/latest/engines/lammps.html#option-2-dependencies-from-pip).

Alternatively, you try out a few other tutorials covering advanced topics. If you're not sure what to try, speak to us and explain your research questions and we'll try to guide you.

Here are a couple of options:

* [Running molecular dynamics with ASE](https://metatensor.github.io/metatrain/latest/examples/ase/run_ase.html)
