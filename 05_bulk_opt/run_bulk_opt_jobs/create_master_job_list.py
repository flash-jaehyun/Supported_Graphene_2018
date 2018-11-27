#!/usr/bin/env python

"""Create the master_job_list variable.

Author: Raul A. Flores
"""

#| - IMPORT MODULES
import os

import numpy as np

import json
import itertools

from systems_data import (
    most_stable_crystal_structure_dict,
    exp_latt_const_dict,
    )

from dft_job_automat.job_setup import DFT_Jobs_Setup

from methods import dir_setup
#__|

#| - Script Inputs
latt_const_array_len = 30

latt_const_range_perc = 0.02

element_list = [

    # Raul Materials
    "Ni",
    "Co",
    "Mo",

    # Kevin Materials
    # "Ru",
    # "Rh",
    # "W",

    ]
#__|

#| - Methods
def create_latt_const_range(latt_const_0, latt_const_range_perc=0.05, num=100):
    d_lc = latt_const_range_perc * latt_const_0
    latt_const_range = np.linspace(
        latt_const_0 - d_lc,
        latt_const_0 + d_lc,
        num=num,
        endpoint=True,
        )

    return(latt_const_range)
#__|

#| - Creating Master Job List
master_job_list = []
for elem_i in element_list:
    latt_const_dict_i = exp_latt_const_dict[elem_i]
    crys_struct_i = most_stable_crystal_structure_dict[elem_i]
    exp_lattices_i = latt_const_dict_i[crys_struct_i]

    #| - Creating permutations of all lattice constants
    lattice_constant_array_dict = {}
    for key, value in exp_lattices_i.items():
        latt_const_range_j = create_latt_const_range(
            value,
            latt_const_range_perc=latt_const_range_perc,
            num=latt_const_array_len,
            )
        latt_const_range_j = np.round(
            latt_const_range_j,
            decimals=5
            )
        lattice_constant_array_dict[key] = latt_const_range_j

    latt_const_permut_i = list(
        itertools.product(
            *list(
                lattice_constant_array_dict.values()
                )
            )
        )
    #__|

    for lattice_constants_k in latt_const_permut_i:
        for spinpol in [True, False]:
            job_dict_i = dict(
                zip(
                    list(exp_lattices_i.keys()),
                    list(lattice_constants_k),
                    )
                )

            job_dict_i["support_metal"] = elem_i
            job_dict_i["crystal_structure"] = crys_struct_i
            job_dict_i["spinpol"] = spinpol

            path_1_i = os.path.join(
                job_dict_i.get("support_metal", "nan"),
                job_dict_i.get("crystal_structure", "nan"),
                str(job_dict_i.get("spinpol", "nan")),
                )

            path_i = os.path.join(
                "data",
                path_1_i,
                str(job_dict_i.get("a", "nan")) + "-" + str(job_dict_i.get("c", "nan")),
                )

            master_job_list.append(
                {
                    "properties": job_dict_i,
                    "path": path_i,
                    }
                )

#__|
