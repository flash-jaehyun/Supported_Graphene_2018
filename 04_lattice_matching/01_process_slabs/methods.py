#!/usr/bin/env python

"""
"""

#| - Import Modules
import copy
import math

import numpy as np

from ase import io
from ase.visualize import view
from ase.constraints import FixAtoms
#__|

def dotproduct(v1, v2):
    return(sum((a * b) for a, b in zip(v1, v2)))

def length(v):
    return(math.sqrt(dotproduct(v, v)))

def angle(v1, v2):
    return(math.acos(dotproduct(v1, v2) / (length(v1) * length(v2))))

def process_atom(
    atoms_i,
    max_thickness=4,
    z_vacuum=13,
    frac_constr_supp=0.5,
    ):
    """
    """
    #| - process_atom

    atoms_i = copy.deepcopy(atoms_i)

#     # Read Single Atoms Object
#     atoms_i = io.read("temp.traj")

    angle_i = math.degrees(
        angle(
            atoms_i.cell[0],
            [1., 0., 0.]),
        )

    atoms_i.rotate(angle_i, 'z', rotate_cell=True)

    # Trying to get the atoms into the 1st quadrant
    if atoms_i.cell[1][1] < 0.:
        atoms_i.cell[1] = -1 * atoms_i.cell[1]

        atoms_i.set_cell(
            atoms_i.cell,
            scale_atoms=True,
            )

    # Wrap atoms into unit cell
    atoms_i.wrap()


    # Mirror atoms about xy-plane if Graphene layer is on the bottom
    c_z_pos = np.mean(np.array([i.position[-1] for i in atoms_i if i.symbol == "C"]))
    m_z_pos = np.mean(np.array([i.position[-1] for i in atoms_i if i.symbol != "C"]))

    if c_z_pos < m_z_pos:
        print("Graphene is below support")

        new_positions = []
        for pos_i in atoms_i.positions:
            pos_i[-1] = -1 * pos_i[-1]
            new_positions.append(pos_i)
        atoms_i.set_positions(new_positions)
        atoms_i.center()


    # Add z-space vacuum
    z_new = 50.
    new_cell = copy.copy(atoms_i.cell)
    new_cell[-1][-1] = z_new
    atoms_i.set_cell(new_cell)

    atoms_i.center()

    # Set slab thickness
    max_slab_z = np.array([i.position[-1] for i in atoms_i if i.symbol != "C"]).max()
    min_slab_z = np.array([i.position[-1] for i in atoms_i if i.symbol != "C"]).min()

    atoms_to_delete_index_list = []
    for atom_j in atoms_i:
        if atom_j.position[-1] < max_slab_z - max_thickness:
            atoms_to_delete_index_list.append(atom_j.index)
    del atoms_i[atoms_to_delete_index_list]


    # Constrain lower part of support
    max_slab_z = np.array([i.position[-1] for i in atoms_i if i.symbol != "C"]).max()
    min_slab_z = np.array([i.position[-1] for i in atoms_i if i.symbol != "C"]).min()

    c_atoms_i = atoms_i[[i.index for i in atoms_i if i.symbol == "C"]]
    m_atoms_i = atoms_i[[i.index for i in atoms_i if i.symbol != "C"]]

    frac_constr_supp = 0.55
    z_cutoff = (max_slab_z - min_slab_z) * frac_constr_supp + min_slab_z

    constraints_index_list = [i.index for i in m_atoms_i if i.position[-1] < z_cutoff]

    c = FixAtoms(indices=[atom.index for atom in atoms_i if atom.index in constraints_index_list])
    atoms_i.set_constraint(c)


    # Set z-spacing again
    new_cell = copy.copy(atoms_i.cell)

    # Added 2 to account for still unknown graphene spacing
    new_cell[-1][-1] = z_vacuum + (max_slab_z - min_slab_z + 2)
    atoms_i.set_cell(new_cell)

    atoms_i.center()


    return(atoms_i)
    #__|


def get_unique_str_repr(row_i):
    """
    """
    #| - get_unique_str_repr
    dupl_prop_dict = {
    #     "": row_i[],
    #     "facet": str(row_i["facet"]),  # Not facet, some may be equiv.

        "crystal": row_i["crystal"],
        "metal": row_i["metal"],
        "area": '{:.5e}'.format(row_i["area_2"]),

        # "u_mismatch": '{:.5e}'.format(row_i["u_mismatch"]),
        # "v_mismatch": '{:.5e}'.format(row_i["v_mismatch"]),

        "angle_mismatch": str(round(row_i["angle_mismatch"], 5)),

        # "angle_mismatch": '{:.5e}'.format(row_i["angle_mismatch"]),

        # "cell_x": str(['{:.5e}'.format(i) for i in row_i["atoms"].cell[0]]),
        # "cell_y": str(['{:.5e}'.format(i) for i in row_i["atoms"].cell[1]]),
        }

    str_repr_i = ""
    for key, value in dupl_prop_dict.items():
        str_repr_i += value + " | "

    return(str_repr_i)
    #__|
