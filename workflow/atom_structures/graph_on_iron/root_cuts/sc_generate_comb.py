"""Temp docstring."""

#| - Import Modules
import sys
import numpy as np
import itertools
import math


from ase import io
from ase.build import fcc111, add_adsorbate
from ase.build import graphene_nanoribbon
from ase import Atoms
from ase.build import root_surface

from misc_modules.numpy_methods import angle_between
from ase_modules.add_adsorbate import add_graphene_layer
#__|

#| - Lattice Parameters
latt_const = 3.4741 # Value obtained from lattice constant optimization
# latt_const = 3.58 # Value obtained from lattice constant optimization

supp_latt_units = 1

# Number of graphene lattice constants that fit within side of support unit cell
graph_latt_units = 9

surf_spacing = latt_const / (2. / 2. ** (1. / 2.))

graphene_bond_l = surf_spacing * supp_latt_units / graph_latt_units
#__|

#| - MISC
# graph_latt_units = 3
graph_latt_units = 1

origin = (0., 0.)
# graph_bond_d = 1.35
graph_bond_d = graphene_bond_l
graph_bond_d_real = 1.4237
#__|

#| - Metal Surface *************************************************************
metal = "Fe"
fcc111 = fcc111(
    metal,
    size=(supp_latt_units, supp_latt_units, 3),
    a=latt_const,
    vacuum=8.0,
    )

# io.write("fcc111.traj", fcc111)
#__|

#| - Root Surface
for root_i in range(20):
    try:
        atoms = root_surface(fcc111, root_i)
        # print("Attempting root cut: " + str(root_i))

        #| - Angle Between Unit Vectors
        v1 = atoms.cell[0]
        v2 = atoms.cell[1]
        angle = angle_between(v1, v2)
        angle = math.degrees(angle)
        # print("Angle between lattice vectors: " + str(angle))

        mag1 = np.linalg.norm(v1)
        mag2 = np.linalg.norm(v2)

        # print("Lattice vector length: " + str(mag1))
        # print("Lattice vector length: " + str(mag2))
        #__|

        for i_ind in range(4):
            num_graph_units = i_ind + 1
            ngu = num_graph_units

            print(str(root_i).zfill(2) + "_" + str(ngu) + "_root")

            num_graph_bond_lengths = (2. + 1.) * ngu

            out_atoms_i = add_graphene_layer(atoms, graphene_units=ngu, graph_surf_d=1.885)

            file_name = str(root_i).zfill(2) + "_" + str(ngu) + "_root" + ".traj"
            out_atoms_i.write(file_name)


    except:
        pass
#__|



#| - OLD
# tmp = mag1 / num_graph_bond_lengths
# strain = 100. * (graph_bond_d_real - tmp) / graph_bond_d_real
# print(strain)
#
# graph_bond_d = mag1 / num_graph_bond_lengths
#
# #| - Drawing Graphene
# slab = atoms
# xy_cell = slab.cell[0:2, 0:2]  # x and y components of unit cell
# x_unit_v = xy_cell[0]
# y_unit_v = xy_cell[1]
#
# x_unit_v = x_unit_v / np.linalg.norm(x_unit_v)
# y_unit_v = y_unit_v / np.linalg.norm(y_unit_v)
#
# patt_cnt_x = 0
# patt_cnt_y = 0
# C_pos_lst = []
# for y_ind in range(graph_latt_units * 3):
#     patt_cnt_x = patt_cnt_y
#     for x_ind in range(graph_latt_units * 3):
#
#         if patt_cnt_x == 0 or patt_cnt_x == 1:
#
#             pos_x = x_ind * graph_bond_d * x_unit_v
#             pos_y = y_ind* graph_bond_d * y_unit_v
#
#             pos_i = np.array(pos_x) + np.array(pos_y)
#             pos_i = np.append(pos_i, 0.)
#
#             C_pos_lst.append(pos_i)
#             # atom_cent = (origin[0] + x_ind * graph_bond_d - graph_bond_d * y_ind * y_unit_v[0], origin[1] + y_ind * graph_bond_d)
#
#             add_adsorbate(slab, 'C', 2.3, position=(pos_i[0], pos_i[1]))
#
#             patt_cnt_x += 1
#
#         elif patt_cnt_x == 2:
#             patt_cnt_x = 0
#
#     if patt_cnt_y == 0:
#         patt_cnt_y = 2
#         continue
#
#     if patt_cnt_y == 2:
#         patt_cnt_y = 1
#         continue
#
#     elif patt_cnt_y == 1:
#         patt_cnt_y = 0
#         continue
#
# C_pos_lst = np.array(C_pos_lst)
# #__|
#
# slab.write(str(root_i).zfill(2) + "_" + str(i_ind) + "_root.traj")

#__|
