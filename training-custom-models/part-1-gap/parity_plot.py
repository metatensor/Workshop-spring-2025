import ase.io
import matplotlib.pyplot as plt
import numpy as np

# load the target and prediction data
targets = ase.io.read("../data/ethanol_reduced_100.xyz", ":")  # TODO: modify path
predictions = ase.io.read("./output.xyz", ":")  # TODO: modify path

# extract the energies
e_targets = np.array([frame.get_total_energy() for frame in targets])
e_predictions = np.array([frame.get_total_energy() for frame in predictions])

# load the train, val, test indices
idx_train = np.loadtxt("./outputs/2025-06-11/12-13-30/indices/training.txt", dtype=int)  # TODO: modify path
idx_val = np.loadtxt("./outputs/2025-06-11/12-13-30/indices/validation.txt", dtype=int)  # TODO: modify path
idx_test = np.loadtxt("./outputs/2025-06-11/12-13-30/indices/test.txt", dtype=int)  # TODO: modify path

fig, ax = plt.subplots()
for subset_name, idx_subset, color in zip(["train", "val", "test"], [idx_train, idx_val, idx_test], ["green", "orange", "red"]):
    ax.scatter(e_targets[idx_subset], e_predictions[idx_subset], c=color, label=subset_name)

ax.axline((np.min(e_targets), np.min(e_targets)), slope=1, ls="--", color="gray")
ax.legend()
ax.set_xlabel("target energy / eV")
ax.set_ylabel("predicted energy / eV")

# save plot
plt.savefig("parity_plot.png", dpi=200, bbox_inches="tight")
