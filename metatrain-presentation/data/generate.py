from pet_mad.calculator import PETMADCalculator
import ase.build
from ase.md.langevin import Langevin
import ase.units
import ase.io


water = ase.build.molecule('H2O')
calculator = PETMADCalculator("latest")
water.calc = calculator
dyn = Langevin(water, 0.5 * ase.units.fs, temperature_K=300, friction=1.0/(10.0 * ase.units.fs))

all_structures = []
def append_structure():
    all_structures.append(water.copy())

dyn.attach(append_structure, interval=1000)
dyn.run(10000)

for structure in all_structures:
    structure.calc = calculator
    del structure.arrays["momenta"]

ase.io.write("water.xyz", all_structures[1:])
