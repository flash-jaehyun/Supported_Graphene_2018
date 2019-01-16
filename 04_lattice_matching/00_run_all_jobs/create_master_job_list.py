# coding: utf-8
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
    surface_facets,
    )

from ase import io
from ase import build

from ase.visualize import view

from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

from pymatgen.io.ase import AseAtomsAdaptor
#__|


elem_to_run = ["Fe"]

master_job_list = []

atoms_list = []
for metal_i, cryst_dict_i in dft_latt_const_dict.items():
    if metal_i in elem_to_run:
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

                for facet in surface_facets:

                    job_dict_i = {}

                    job_dict_i["metal"] = metal_i
                    job_dict_i["crystal"] = cryst_j
                    job_dict_i["atoms"] = atoms_i
                    job_dict_i["facet"] = facet


                    "".join(list(map(str, facet)))

                    path_i = "/".join([
                        "data",
                        str(job_dict_i.get("metal", "nan")),
                        str(job_dict_i.get("crystal", "nan")),
                        "".join(list(map(str, facet))),
                        # str(job_dict_i.get("facet", "nan")),
                        ])


                    master_job_list.append(
                        {
                            "properties": job_dict_i,
                            "path": path_i,
                            }
                        )
