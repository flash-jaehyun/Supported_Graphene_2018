"""Create Iron bulk lattice with varying k-points and lattice constant. """

#| - Import Modules
import os
import numpy as np
import shutil
import pickle

from ase import io
# from ase.build import graphene_nanoribbon
from ase.build import bulk

from ase_modules.espresso_params import Espresso_Params
from dft_job_automat.job_setup import DFT_Jobs_Setup
#__|


#| - Script Parameters
metal = "Fe"

bond_l_range = (2.0, 3.0)
resolution = 0.1
#__|


#| - Range of Bond Lengths
bond_l_lst = []
entry_i = bond_l_range[0]
while entry_i < bond_l_range[1]:
    bond_l_lst.append(entry_i)
    entry_i += resolution
bond_l_lst.append(bond_l_range[1])
#__|


#| - Read Directory Structure File
tree_level_labels     = ["kpoints", "lattice_parameter"]

# Define descriptors at each level of the directory tree
level_entries_dict    = {}
level_entries_dict[tree_level_labels[0]]    = ["221", "441", "661", "881"]
level_entries_dict[tree_level_labels[1]]    = bond_l_lst
#__|


#| - Initializing the Jobs Class Instance
Jobs = DFT_Jobs_Setup(system="aws")
Jobs.load_dir_struct(tree_level_labels, level_entries_dict)
Jobs.create_dir_struct()
#__|


for i in Jobs.job_var_lst:

    #| - KPoints
    kp = Jobs.extract_prop_from_var_lst(i, "kpoints")
    kpoints = (kp[0], kp[1], kp[2])
    #__|

    Jobs.create_job_dir(i, revision="Auto")

    #| - Quantum Espresso Parameters
    qe_params = Espresso_Params()
    qe_params.update_params({"kpts": kpoints})
    qe_params.write_params()
    #__|


    #| - Graphene Atoms Object
    bond_l = Jobs.extract_prop_from_var_lst(i, "lattice_parameter")
    # print(bond_l)
    bulk_fe = bulk(metal, "fcc", a=bond_l, cubic=True)
    io.write("POSCAR", bulk_fe)
    #__|


    # os.system("ase gui POSCAR")
    Jobs.copy_files_jd(["model.py", "POSCAR", "dft-params.json"], i, revision="Auto")
