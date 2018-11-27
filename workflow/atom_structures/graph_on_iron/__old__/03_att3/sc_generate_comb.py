"""Temp docstring."""

#| - Import Modules
from ase import io
from ase.build import fcc111, add_adsorbate
from ase.build import graphene_nanoribbon

import math
#__|


#| - Lattice Parameters
latt_const = 3.4741 # Value obtained from lattice constant optimization

supp_latt_units = 2

# Number of graphene lattice constants that fit within side of support unit cell
graph_latt_units = 3

surf_spacing = latt_const / (2. / 2. ** (1. / 2.))

graphene_bond_l = surf_spacing * supp_latt_units / graph_latt_units
#__|


#| - Graphene


#| - OLD | Using Graphene Function from ASE
graphene = graphene_nanoribbon(2, 2, type='zigzag', saturated=False,
C_C=graphene_bond_l, sheet=True)

theta_rot = 90
phi_rot = 0
psi_rot = 0

theta_rot = math.pi / 180. * theta_rot
phi_rot = math.pi / 180. * phi_rot
psi_rot = math.pi / 180. * psi_rot

graphene.rotate_euler(phi=phi_rot, theta=theta_rot, psi=psi_rot)

max_y = min([atom.position[1] for atom in graphene])
mask = ([atom.position[1] for atom in graphene] == max_y)
del graphene[mask]
#__|

# io.write("graphene.traj", graphene)
#__|


#| - Metal Surface
metal = "Fe"

slab = fcc111(metal, size=(supp_latt_units, supp_latt_units, 3), a=latt_const)

io.write("slab.traj", slab)

metal_lattice = slab.get_cell()
#__|


#| - Adding Graphene to Surface
xy_cell = slab.cell[0:2, 0:2]  # x and y components of unit cell
x_latt = xy_cell[0]
y_latt = xy_cell[1]

pos = y_latt * (2./3.)
add_adsorbate(slab, 'C', 1., position=(pos[0], pos[1]))


pos = x_latt * (1./3.) + y_latt * (0./3.)
add_adsorbate(slab, 'C', 1., position=(pos[0], pos[1]))

pos = x_latt * (1./3.) + y_latt * (1./3.)
add_adsorbate(slab, 'C', 1., position=(pos[0], pos[1]))


pos = x_latt * (2./3.) + y_latt * (1./3.)
add_adsorbate(slab, 'C', 1., position=(pos[0], pos[1]))

pos = x_latt * (2./3.) + y_latt * (2./3.)
add_adsorbate(slab, 'C', 1., position=(pos[0], pos[1]))


add_adsorbate(slab, 'C', 1., position=(0, 0 ))


# add_adsorbate(slab, graphene, 1)
slab.center(vacuum=7, axis=2)
# slab.wrap()

io.write('comb.traj', slab)
#__|
