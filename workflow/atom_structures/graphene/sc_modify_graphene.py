#!/usr/bin/env python

"""

Author: Raul A. Flores
"""

#| - Import Modules
from ase import io

#__|

atoms = io.read("init.traj")

positions = atoms.get_positions()
positions[:, 2] = 5

atoms.set_positions(positions)

cell = atoms.get_cell()

cell[2][2] = 10.

atoms.set_cell(cell)

print(atoms.get_cell())

io.write("out.traj", atoms)
