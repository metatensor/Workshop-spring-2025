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
> To ensure a demo-length run time, set `num_epochs` to `10`. We will increase this value later.

Run PET training as follows:

```bash
mtt train options.yaml
```

[PET is a transformer-based GNN that is trained by gradient descent](https://arxiv.org/abs/2305.19302v3), as opposed to [GAP](https://link.aps.org/doi/10.1103/PhysRevLett.104.136403) that is trained by a one-steop linear algebraic fitting. The iterative minimization of the loss over a number of epochs is seen in the output log file.

Copy the `eval.yaml` options file you created before in subdirectory `part-1-gap` to the working directory. Run model evaluation as before. As PET requires no extensions, this can be omitted from the command.

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

## Using our bespoke ethanol model

Now that we have a trained PET model, we will use it as the energies and forces calculator for running molecular dynamics (MD) in LAMMPS.

Let's prepare the LAMMPS input file. We have provided a near-complete file for you to inspect and fill in. As understanding LAMMPS inputs can be complex for those not familiar, we will keep these completions simple.

First, create a subdirectory called `pet-ethanol-md`:

```bash
mkdir pet-ethanol-md && cd pet-ethanol-md
```

Next, download the relevant input files from the repository

```bash
curl -O https://raw.githubusercontent.com/metatensor/Workshop-spring-2025/refs/heads/main/training-custom-models/part-2-pet/ethanol.in
curl -O https://raw.githubusercontent.com/metatensor/Workshop-spring-2025/refs/heads/main/training-custom-models/part-2-pet/ethanol.data
```

LAMMPS needs typically two input files, a `.data` specifying the starting geometry and a `.in` file specifiying the input settings. For the former, in `ethanol.data`, the first frame from the file `rmd17_ethanol_1000.xyz` is used. For the latter, in `ethanol.in`, various settings are specified and some left blank. Find the `# TODO:` comments and input the following:

- path to the `.data` file containing the initial configuration
- the correct pair style - `"metatomic"` - and path to the model `.pt` object.
- the temperature - 300 K
- the number of steps - start with 1000 and we will increase later.

Once filled, run MD with LAMMPS.

```bash
lmp -in ethanol.in
```

If everything is specified correctly, the simulation should run for 1000 steps and complete in a only a few minutes.

A log file `log.lammps` is written, as well as the output trajectory `ethanol.xyz`. Inspect the log file. What do you notice about the quantities that should be conserved, such as the temperature?

Download a helper script to plot the thermodynamic qunatities. Run it, and observe the plot saved in `thermo.png`:
```bash
curl -O https://raw.githubusercontent.com/metatensor/Workshop-spring-2025/refs/heads/main/training-custom-models/part-2-pet/plot_thermo.py
```

> [!NOTE] > `.xyz` files output with LAMMPS include the atomic type numbers instead of the symbols. For the purposes of this demo, we will find and replace these types with their symbols to give an `.xyz` file that is readable by common visualization software.

Download and use a helper script to make this change:

```bash
curl -O https://raw.githubusercontent.com/metatensor/Workshop-spring-2025/refs/heads/main/training-custom-models/part-2-pet/convert_xyz_symbols.sh
chmod +x convert_xyz_symbols.sh
./convert_xyz_symbols.sh
```

Now you can use your favourite software, such as Ovito, VMD, or `chemiscope` in Python ([link here](https://chemiscope.org/)) to visualize the trajectory. If you are unsure, Ovito (download link [here](https://www.ovito.org/)) is recommended.

What do you notice about the trajectory, and how does this align with what you saw in the log file?

In essence, our training run wasn't extensive enough to achieve an accurate or stable enough model - the trajectory blows up!

## Using the PET-MAD foundation model

Now you've seen how PET can be trained from scratch on a dataset. Due to time constraints, we are not able to convergence it to a high accuracy such that it produces a stable MD trajectory.

Now let's instead download the PET-MAD foundation model introduced in the talks. This is a universal MLIP trained on the Massive Atomic Diversity (MAD) dataset. For a lot of systems it should produce reliable trajectories.

First create a new subdirectory.

```bash
cd .. && mkdir pet-mad-md && cd pet-mad-md
```

Export the PET-MAD model, downloading from the Hugging-Face repository. More detailed instructions can again be found in the [PET-MAD repository](https://github.com/lab-cosmo/pet-mad).

```bash
mtt export https://huggingface.co/lab-cosmo/pet-mad/resolve/main/models/pet-mad-latest.ckpt
```

Copy the LAMMPS input files from before to the current directory.

```bash
cp ../pet-ethanol-md/ethanol.data .
cp ../pet-ethanol-md/ethanol.in .
cp ../pet-ethanol-md/plot_thermo.py .
cp ../pet-ethanol-md/convert_xyz_symbols.sh .
```

Now change the path of the model in the `pair_style` command:

```bash
# pair_style metatomic ../model.pt  # before
pair_style metatomic pet-mad-latest.pt  # after
```

and now we can run MD again!

```bash
lmp -in ethanol.in
```

Plot again the thermodynamic quantities and visualize the trajectory. What do you notice now?


# Part 2c: Uncertainty Quantification

Uncertainty quanitfication, as seen in the talks, is another important part of atomistic machine learning that is garnering more attention in recent years. Based on the last layer prediction rigidity (LLPR) formalism, the uncertainty of models in metatrain can be evaluated.

> [!NOTE]
> Relevant references can be found [here](https://pubs.acs.org/doi/10.1021/acs.jctc.3c00704) and [here](https://arxiv.org/html/2403.02251v1).

In this section we will demonstrate how this is done. As this is not currently available directly in metatrain using CLI commands, we will use some helper scripts instead. This is based on the [programmatic LLPR tutorial](https://metatensor.github.io/metatrain/latest/examples/programmatic/llpr/llpr.html) found in the metatrain documentation.

First create a new subdirectory.

```bash
cd .. && mkdir pet-mad-uq && cd pet-mad-uq
```

Download the helper script for computing the uncertainty

```bash
curl -O https://raw.githubusercontent.com/metatensor/Workshop-spring-2025/refs/heads/main/training-custom-models/part-2-pet/uq.py
```

Generate an uncertainty plot for the latest version of PET-MAD.

```bash
python uq.py --model_path=../pet-mad-md/pet-mad-latest.pt --output_figure="ethanol_uncertainty_vs_error_petmad.png"
```

Inspect the output plot. Here we plot the actual error on the energy against the uncertainty on the energy. We would expect to see somewhat of a positive correlation between the two, but as the dataset here is small it is difficult to resolve.
