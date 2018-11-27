"""Temp docstring."""

#| - Import Modules
from ase import io
from ase.build import fcc111, add_adsorbate
from ase.build import graphene_nanoribbon

import math
#__|


#| - Lattice Parameters
latt_const = 2.856
#__|


#| - Graphene
graphene = graphene_nanoribbon(2, 2, type='zigzag', saturated=False,
C_C=latt_const / (2. / 2. ** (1. / 2.)), sheet=True)

theta_rot = 90
phi_rot = 0
psi_rot = 0

theta_rot = math.pi / 180. * theta_rot
phi_rot = math.pi / 180. * phi_rot
psi_rot = math.pi / 180. * psi_rot

graphene.rotate_euler(phi=phi_rot, theta=theta_rot, psi=psi_rot)

max_y = max([atom.position[1] for atom in graphene])
mask = ([atom.position[1] for atom in graphene] == max_y)
del graphene[mask]

io.write("graphene.traj", graphene)
#__|


#| - Metal Surface
metal = 'Fe'

slab = fcc111(metal, size=(3, 3, 1), a=latt_const)

io.write("slab.traj", slab)

metal_lattice = slab.get_cell()
#__|


#| - Adding Graphene to Surface
add_adsorbate(slab, graphene, 1)
slab.center(vacuum=7, axis=2)
slab.wrap()

io.write('comb.traj', slab)
#__|
