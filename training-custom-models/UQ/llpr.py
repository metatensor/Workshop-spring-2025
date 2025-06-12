"""
Computing LLPR Uncertainties
============================

This tutorial demonstrates how to use an already trained and exported model
from Python to perform uncertainty quantification using the
last-layer prediction rigidity (`LLPR <LLPR_>`_) approximation.

.. _LPR: https://pubs.acs.org/doi/10.1021/acs.jctc.3c00704
.. _LLPR: https://arxiv.org/html/2403.02251v1

We will use the PET model trained on the ethanol dataset, that we just trained.
You can also use your own model.
"""

# %%
#

import torch

from metatrain.utils.io import load_model
from metatomic.torch.ase_calculator import MetatomicCalculator
import argparse
import ase.io  as aseio  # noqa: E402
import numpy as np  # noqa: E402

from metatomic.torch import ModelEvaluationOptions, ModelOutput  # noqa: E402

from metatrain.utils.data import Dataset, read_systems, read_targets  # noqa: E402
from metatrain.utils.neighbor_lists import (  # noqa: E402
    get_requested_neighbor_lists,
    get_system_with_neighbor_lists,
)

from metatomic.torch import (  # noqa: E402
    AtomisticModel,
    ModelMetadata,
)

from metatrain.utils.llpr import LLPRUncertaintyModel  # noqa: E402
from metatrain.utils.data import collate_fn  # noqa: E402
import matplotlib.pyplot as plt

# %%
#
# Models can be loaded using the :func:`metatrain.utils.io.load_model` function from
# the. For already exported models The function requires the path to the exported model
# and, for many models, also the path to the respective extensions directory. Both are
# produced during the training process.

parser = argparse.ArgumentParser(description="Compute LLPR uncertainties")
parser.add_argument(
    "--model-path",
    type=str,
    default="model-pet.pt",
    help="Path to the exported PET model"
)
args = parser.parse_args()
model_path = args.model_path
#model_path = "pet-mad-latest.pt"
model = load_model(model_path)


# %%
#
# Compute the "true" error of the PET model on the ethanol dataset.
# We will use the DFT energies as the ground truth.

ethanol_systems = aseio.read("ethanol_reduced_100.xyz",':',format='extxyz')

DFT_energies = np.array([i.get_potential_energy() for i in ethanol_systems])
PET_energies = []
for atoms in ethanol_systems:
    atoms.calc = MetatomicCalculator(model_path,device="cpu")
    atoms.get_potential_energy()
    PET_energies.append(atoms.get_potential_energy())
PET_energies = np.array(PET_energies)
err_true = np.abs(DFT_energies - PET_energies)

# %%
#
# In metatrain, a Dataset is composed of a list of systems and a dictionary of targets.
# The following lines illustrate how to read systems and targets from xyz files, and
# how to create a Dataset object from them.


ethanol_systems = read_systems("ethanol_reduced_100.xyz")
target_config = {
    "energy": {
        "quantity": "energy",
        "read_from": "ethanol_reduced_100.xyz",
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

requested_neighbor_lists = get_requested_neighbor_lists(model)
ethanol_systems = [
    get_system_with_neighbor_lists(system, requested_neighbor_lists)
    for system in ethanol_systems
]
dataset = Dataset.from_dict({"system": ethanol_systems, **targets})

ethanol_dataset = [get_system_with_neighbor_lists(
    i, requested_neighbor_lists
) for i in ethanol_systems]

# %%
#
# The dataset is fully compatible with torch. For example, be used to create
# a DataLoader object.


dataloader = torch.utils.data.DataLoader(
    dataset,
    batch_size=10,
    shuffle=False,
    collate_fn=collate_fn,
)


# %%
#
# We now wrap the model in a LLPRUncertaintyModel object, which will allows us
# to compute prediction rigidity metrics, which are useful for uncertainty
# quantification and model introspection.


llpr_model = LLPRUncertaintyModel(model)
llpr_model.compute_covariance(dataloader)
llpr_model.compute_inverse_covariance(regularizer=1e-4)

# calibrate on the same dataset for simplicity. In reality, a separate
# calibration/validation dataset should be used.
llpr_model.calibrate(dataloader)

exported_model = AtomisticModel(
    llpr_model.eval(),
    ModelMetadata(),
    llpr_model.capabilities,
)

# %%
#
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

ethanol_dataset = [s.to(model_dtype) for s in ethanol_dataset]

outputs = exported_model(ethanol_dataset, evaluation_options, check_consistency=False)
lpr = outputs["mtt::aux::energy_uncertainty"].block().values.detach().cpu().numpy()
print(f"LPR values: {lpr}")


plt.figure()
plt.loglog(err_true, np.sqrt(lpr), 'o', markersize=5, alpha=0.7)
plt.xlabel('True error |DFT - PET| (kcal/mol)')
plt.ylabel('LLPR uncertainty')
plt.title('True error vs LLPR on log–log scale')
plt.grid(True, which='both', ls='--', lw=0.5)
plt.tight_layout()
plt.savefig("ethanol_llpr_vs_true_error.png", dpi=300)
plt.show()

