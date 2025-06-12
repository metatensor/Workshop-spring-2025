import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt("thermo.out")

fig, axes = plt.subplots(1, 4, figsize=(20, 5))
axes[0].plot(data[:, 0], data[:, 1], label="Temp / K")
axes[1].plot(data[:, 0], data[:, 2], label="Pot. E / eV")
axes[2].plot(data[:, 0], data[:, 3], label="Kin. E / eV")
axes[3].plot(data[:, 0], data[:, 4], label="Total E / eV")

[ax.legend() for ax in axes];

plt.savefig("thermo.png", bbox_inches="tight", dpi=200)