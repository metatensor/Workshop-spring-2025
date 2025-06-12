import argparse

import ase.io
import matplotlib.pyplot as plt
import numpy as np
import torch

from metatomic.torch import (
    AtomisticModel,
    ModelEvaluationOptions,
    ModelMetadata,
    ModelOutput,
)
from metatomic.torch.ase_calculator import MetatomicCalculator

from metatrain.utils.data import collate_fn, Dataset, read_systems, read_targets
from metatrain.utils.io import load_model
from metatrain.utils.neighbor_lists import (
    get_requested_neighbor_lists,
    get_system_with_neighbor_lists,
)
from metatrain.utils.llpr import LLPRUncertaintyModel


# Take the model path and figure name as command line inputs
parser = argparse.ArgumentParser(description="Compute LLPR uncertainties")
parser.add_argument(
    "--model_path",
    type=str,
    default="model-pet.pt",
    help="Path to the exported PET model"
)
parser.add_argument(
    "--output_figure",
    type=str,
    default="ethanol_uq_vs_error.png",
    help="Path to the output figure"
)
args = parser.parse_args()
model_path = args.model_path
output_figure = args.output_figure

# Load the model
model = load_model(model_path)


# Compute the "true" error of the PET model on the ethanol dataset.
# We will use the DFT energies as the ground truth.
systems_path = "../../data/ethanol_reduced_100.xyz"
ethanol_systems = ase.io.read(systems_path, ':',format='extxyz')

DFT_energies = np.array([i.get_potential_energy() for i in ethanol_systems])
PET_energies = []
for atoms in ethanol_systems:
    atoms.calc = MetatomicCalculator(model_path,device="cpu")
    atoms.get_potential_energy()
    PET_energies.append(atoms.get_potential_energy())
PET_energies = np.array(PET_energies)
err_true = np.abs(DFT_energies - PET_energies)

# In metatrain, a Dataset is composed of a list of systems and a dictionary of targets.
# The following lines illustrate how to read systems and targets from xyz files, and
# how to create a Dataset object from them.

# Build the list of systems with neighbor lists
ethanol_systems = read_systems(systems_path)
requested_neighbor_lists = get_requested_neighbor_lists(model)
ethanol_systems = [
    get_system_with_neighbor_lists(system, requested_neighbor_lists)
    for system in ethanol_systems
]

# Build the targets
target_config = {
    "energy": {
        "quantity": "energy",
        "read_from": systems_path,
        "reader": "ase",
        "key": "energy",
        "unit": "kcal/mol",
        "type": "scalar",
        "per_atom": False,
        "num_subtargets": 1,
        "forces": False,
        "stress": False,
        "virial": False,
    },
}
targets, _ = read_targets(target_config)

# Construct the dataset
dataset = Dataset.from_dict({"system": ethanol_systems, **targets})

# Create a dataloader
dataloader = torch.utils.data.DataLoader(
    dataset,
    batch_size=10,
    shuffle=False,
    collate_fn=collate_fn,
)

# We now wrap the model in a LLPRUncertaintyModel object, which will allows us to
# compute prediction rigidity metrics, which are useful for uncertainty quantification
# and model introspection.
llpr_model = LLPRUncertaintyModel(model)
llpr_model.compute_covariance(dataloader)
llpr_model.compute_inverse_covariance(regularizer=1e-12)

# calibrate on the same dataset for simplicity. In reality, a separate
# calibration/validation dataset should be used.
llpr_model.calibrate(dataloader)

exported_model = AtomisticModel(
    llpr_model.eval(),
    ModelMetadata(),
    llpr_model.capabilities,
)

# We can now use the model to compute the LPR for every atom in the ethanol molecule.
# To do so, we create a ModelEvaluationOptions object, which is used to request
# specific outputs from the model. In this case, we request the uncertainty in the
# atomic energy predictions.
evaluation_options = ModelEvaluationOptions(
    length_unit="angstrom",
    outputs={
        # request the uncertainty in the atomic energy predictions
        "energy": ModelOutput(per_atom=False),  # needed to request the uncertainties
        "mtt::aux::energy_uncertainty": ModelOutput(per_atom=False),
    },
    selected_atoms=None,
)

model_dtype = next(exported_model.parameters()).dtype

ethanol_dataset = [
    get_system_with_neighbor_lists(i, requested_neighbor_lists)
    for i in ethanol_systems
]
ethanol_dataset = [s.to(model_dtype) for s in ethanol_dataset]

outputs = exported_model(ethanol_dataset, evaluation_options, check_consistency=False)
lpr = outputs["mtt::aux::energy_uncertainty"].block().values.detach().cpu().numpy()


# Generate a figure of the LLPR uncertainty against the actual error and save
fig, ax = plt.subplots()
ax.scatter(err_true, np.sqrt(lpr))
# ax.scatter(err_true, 1 / np.sqrt(lpr))
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel('True error |DFT - PET| (kcal/mol)')
ax.set_ylabel('LLPR uncertainty')
ax.grid(True, which='both', ls='--', lw=0.5)

plt.savefig(output_figure, dpi=300, bbox_inches="tight")
