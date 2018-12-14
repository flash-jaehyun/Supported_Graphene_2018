#!/usr/bin/env pytfehon

"""Create heterointerfaces between graphene and slab surface.

Author(s): Raul Flores
"""

#| - Import Modules
import os
import sys

sys.path.insert(0, os.path.join(
        os.environ["PROJ_fe_graph"],
        "data"))

from proj_data_fe_graph import (
    most_stable_crystal_structure_dict,
    dft_latt_const_dict,
    )

from ase import io
from ase import build

from ase.visualize import view

from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

from pymatgen.io.ase import AseAtomsAdaptor
#__|


#| - TEMP
atoms_list = []
for metal_i, cryst_dict_i in dft_latt_const_dict.items():
    for cryst_j, latt_params_j in cryst_dict_i.items():

        #| - Testing for the completness of the latt_const dict
        make_atoms = True
        if len(list(latt_params_j.keys())) == 1:
            if "a" in list(latt_params_j.keys()):
                if latt_params_j.get("a", None) is None:
                    make_atoms = False

        if len(list(latt_params_j.keys())) == 2:
            if "a" in list(latt_params_j.keys()):
                 if "c" in list(latt_params_j.keys()):
                    if latt_params_j.get("a", None) is None:
                        make_atoms = False
                    if latt_params_j.get("c", None) is None:
                        make_atoms = False
        #__|

        if make_atoms:
            atoms_i = build.bulk(
                metal_i,
                crystalstructure=cryst_j,
                a=latt_params_j.get("a", None),
                c=latt_params_j.get("c", None),
                covera=None,
                u=None,
                orthorhombic=False,
                cubic=False,
                )

            structure_i = AseAtomsAdaptor.get_structure(atoms_i)
            analyzer = SpacegroupAnalyzer(structure_i)
            struct_conv_std_i = analyzer.get_conventional_standard_structure()
            atoms_i = AseAtomsAdaptor.get_atoms(struct_conv_std_i)

            atoms_list.append(atoms_i)

        #| - __old__
        # latt_params_keys = list(latt_params_j.keys())
        # if "a" in latt_params_keys and "c" not in latt_params_keys:
        #     tmp = 42
        #
        #
        # elif "a" in latt_params_keys and "c" in latt_params_keys:
        #     tmp = 42
        #__|


#__|
