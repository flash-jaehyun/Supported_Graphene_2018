"""Temp docstring."""

#| - Import Modules
from ase import io

from ase.build import bcc110
from ase.build import fcc111, add_adsorbate

from ase.build import graphene_nanoribbon
from ase import Atoms

import numpy as np
import itertools
import math
#__|


#| - Lattice Parameters
# latt_const = 3.4741 # Value obtained from lattice constant optimization
# latt_const = 3.58

latt_const = 2.856

#| - Calculating Surface Spacing
lattice_angle = math.atan(6.055 / 4.284)
vert_bond_spacing = (latt_const / 2.) / math.cos(lattice_angle)
#__|

supp_latt_units = 2

# Number of graphene lattice constants that fit within side of support unit cell
graph_latt_units = 3
surf_spacing = latt_const / (2. / 2. ** (1. / 2.))

graphene_bond_l = vert_bond_spacing * supp_latt_units / graph_latt_units
#__|


#| - MISC
origin = (0., 0.)

# graph_bond_d = 1.35
graph_bond_d = graphene_bond_l
#__|


#| - Metal Surface
metal = "Fe"

slab = bcc110(
    metal,
    size=(supp_latt_units, supp_latt_units, 4),
    a=latt_const,
    orthogonal=True,
    vacuum=12.0,
    )
# io.write("slab.traj", slab)
metal_lattice = slab.get_cell()
#__|


#| - Adding Graphene to Surface

#| - Drawing Graphene
xy_cell = slab.cell[0:2, 0:2]  # x and y components of unit cell
x_unit_v = xy_cell[0]
y_unit_v = xy_cell[1]

x_unit_v = x_unit_v / np.linalg.norm(x_unit_v)
y_unit_v = y_unit_v / np.linalg.norm(y_unit_v)

patt_cnt_x = 0
patt_cnt_y = 0
C_pos_lst = []
for y_ind in range(graph_latt_units):
    patt_cnt_x = patt_cnt_y
    for x_ind in range(graph_latt_units):

        if patt_cnt_x == 0 or patt_cnt_x == 1:

            pos_x = x_ind * graph_bond_d * x_unit_v
            pos_y = y_ind* graph_bond_d * y_unit_v

            pos_i = np.array(pos_x) + np.array(pos_y)
            pos_i = np.append(pos_i, 0.)

            C_pos_lst.append(pos_i)
            # atom_cent = (origin[0] + x_ind * graph_bond_d - graph_bond_d * y_ind * y_unit_v[0], origin[1] + y_ind * graph_bond_d)

            add_adsorbate(slab, 'C', 2.3, position=(pos_i[0], pos_i[1]))

            patt_cnt_x += 1

        elif patt_cnt_x == 2:
            patt_cnt_x = 0

    if patt_cnt_y == 0:
        patt_cnt_y = 2
        continue

    if patt_cnt_y == 2:
        patt_cnt_y = 1
        continue

    elif patt_cnt_y == 1:
        patt_cnt_y = 0
        continue

C_pos_lst = np.array(C_pos_lst)
#__|

atoms_i = Atoms(
    "C" + str(len(C_pos_lst)),
    positions=C_pos_lst,
    cell=slab.cell
    )
io.write("graph.POSCAR", atoms_i)

#| - OLD | Manually Add Atoms On Top
# xy_cell = slab.cell[0:2, 0:2]  # x and y components of unit cell
# x_latt = xy_cell[0]
# y_latt = xy_cell[1]
#
# pos = y_latt * (2./3.)
# add_adsorbate(slab, 'C', 1., position=(pos[0], pos[1]))
#
#
# pos = x_latt * (1./3.) + y_latt * (0./3.)
# add_adsorbate(slab, 'C', 1., position=(pos[0], pos[1]))
#
# pos = x_latt * (1./3.) + y_latt * (1./3.)
# add_adsorbate(slab, 'C', 1., position=(pos[0], pos[1]))
#
#
# pos = x_latt * (2./3.) + y_latt * (1./3.)
# add_adsorbate(slab, 'C', 1., position=(pos[0], pos[1]))
#
# pos = x_latt * (2./3.) + y_latt * (2./3.)
# add_adsorbate(slab, 'C', 1., position=(pos[0], pos[1]))
#
#
# add_adsorbate(slab, 'C', 1., position=(0, 0 ))
#
#
# # add_adsorbate(slab, graphene, 1)
# slab.center(vacuum=7, axis=2)
# # slab.wrap()
#

# print("#!@!#@$#")
# io.write("comb.POSCAR", slab)
#__|

io.write("comb.POSCAR", slab)

#__|
