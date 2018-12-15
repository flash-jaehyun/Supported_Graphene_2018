#!/usr/bin/env python

"""Create the master_job_list variable.

Author: Raul A. Flores
"""

#| - IMPORT MODULES
import os
import sys

import copy

import pickle

import numpy as np

from ase.visualize import view
#__|

#| - Script Inputs
# latt_const_array_len = 30
#
# latt_const_range_perc = 0.02
#
# element_list = [
#
#     # Raul Materials
#     "Ni",
#     "Co",
#     "Mo",
#
#     # Kevin Materials
#     # "Ru",
#     # "Rh",
#     # "W",
#
#     ]
#__|

#| - Methods
# def create_latt_const_range(latt_const_0, latt_const_range_perc=0.05, num=100):
#     d_lc = latt_const_range_perc * latt_const_0
#     latt_const_range = np.linspace(
#         latt_const_0 - d_lc,
#         latt_const_0 + d_lc,
#         num=num,
#         endpoint=True,
#         )
#
#     return(latt_const_range)
#__|

#| - Creating Master Job List

with open("../slab_df.pickle", "rb") as fle:
    df = pickle.load(fle)

master_job_list = []

path_list = []
for i_cnt, row_i in df.iterrows():

    atoms = row_i["atoms"]

    elem_list_i = list(set(atoms.get_chemical_symbols()))
    try:
        elem_list_i.remove("C")
        metal_elem_i = elem_list_i[0]
    except:
        pass

    assert len(elem_list_i) == 1, "More than 1 non-C element!"

    metal_ind_list = []
    for atom in atoms:
        if atom.symbol == metal_elem_i:
            metal_ind_list.append(atom.index)

    support_atoms = atoms[metal_ind_list]
    z_positions = support_atoms.get_positions()[:,2]
    z_min = z_positions.min()
    z_max = z_positions.max()

    graphene_z_pos_list = np.linspace(z_max + 1., z_max + 6., num=30, endpoint=True)
    for graph_z_j in graphene_z_pos_list:
        atoms_j = copy.deepcopy(atoms)
        for atom in atoms_j:
            if atom.symbol == "C":
                atom.position[2] = graph_z_j


        job_dict_i = row_i.to_dict()

        job_dict_i["graphene_pos_above_support"] = graph_z_j - z_max
        job_dict_i["atoms_new"] = atoms_j
        job_dict_i["job_type"] = "opt_z_spacing"

        path_i = "/".join([
            "data",
            str(job_dict_i.get("job_type", "nan")),
            str(job_dict_i.get("element", "nan")),
            str(job_dict_i.get("crystal_structure", "nan")),
            str(job_dict_i.get("facet", "nan")),
            '{:.5f}'.format(
                round(job_dict_i.get("graphene_pos_above_support", "nan"), 5)
                ),
            ])

        master_job_list.append(
            {
                "properties": job_dict_i,
                "path": path_i,
                }
            )
#__|
