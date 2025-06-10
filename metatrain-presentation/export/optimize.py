import ase.build
from metatomic.torch.ase_calculator import MetatomicCalculator
from ase.optimize import LBFGS


water = ase.build.molecule('H2O')

calculator = MetatomicCalculator("pet-mad-latest.pt")
water.calc = calculator

optimizer = LBFGS(water)
optimizer.run(fmax=0.01)
