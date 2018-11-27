#!/usr/bin/env python

"""."""

#| - IMPORT MODULES
import os
import sys

sys.path.insert(0, "./PythonPackages")
sys.path.insert(0, "./PythonModules")

# MY MODULES
from bader_charge.bader import bader
from ase_modules.ase_methods import (
    read_atoms_from_file,
    set_init_mag_moms,
    ionic_opt,
    an_pdos,
    an_bands,
    an_beef_ensemble,
    set_QE_calc_params,
    an_ads_vib,
    clean_up_dft,
    )
#__|

#| - SCRIPT INPUTS ************************************************************
atoms_filename = "init.traj"

# opt (ionic optimization), easy_opt, or sp (single-point calculation)
mode = "opt"
opt_fmax = 0.01  # max force convergence for optimizer
maxsteps = 10000

run_opt             = True
run_pdos            = False
run_bader           = False
run_bands           = False
run_beef_ensemble   = False
run_vib             = False

dos_kpts = (6, 6, 6)
bands_kpts = (6, 6, 6)
#__| **************************************************************************

#| - Setup


layer_dict = {
    1: {"magmom": -4, "atom_indices": [0, 1, 2]},
    2: {"magmom": 4, "atom_indices": [3, 4, 5]},
    3: {"magmom": -4, "atom_indices": [6, 7, 8]},
    4: {"magmom": 4, "atom_indices": [9, 10, 11, 12, 13, 14]},

    # 2: [3, 4, 5],
    # 3: [6, 7, 8],
    # 4: [9, 10, 11, 12, 13, 14],

    }


atoms, traj = read_atoms_from_file(filename=atoms_filename)

# magmom_list = []
# for layer_i, layer_dict_i in layer_dict.items():
    # print(layer_i)

    # for atom_ind in atom_indices:
        # print(atom_inds)

for atom in atoms:

    for layer_i, layer_dict_i in layer_dict.items():
        if atom.index in layer_dict_i["atom_indices"]:
            print("WWWOOOOOOOOO")

#__|


#| - __old__

# calc, espresso_params = set_QE_calc_params(
#     atoms,
#     load_defaults=True,
#     )
#
# set_init_mag_moms(
#     atoms,
#     read_from_file=True,
#     # magmoms=magmom_list,
#     )


#
# #| - Ionic Optimization
# if run_opt:
#     ionic_opt(
#         atoms,
#         calc,
#         traj=traj,
#         mode=mode,
#         fmax=opt_fmax,
#         maxsteps=maxsteps,
#         )
# #__|
#
# #| - Additional Analysis
# if run_beef_ensemble:
#     an_beef_ensemble(atoms)
#
# #| - Bader Analysis
#
# #| - Don't Run Bader Executable on AWS
# if "COMPENV" in os.environ:
#     run_exec = True
# else:
#     run_exec = False
# #__|
#
# if run_bader:
#     bader(atoms, spinpol=espresso_params["spinpol"], run_exec=run_exec)
# #__|
#
# if run_pdos:
#     atoms.set_calculator(calc=calc)
#     an_pdos(atoms, dos_kpts, espresso_params)
#
# if run_bands:
#     an_bands(atoms, bands_kpts, espresso_params)
#
# if run_vib:
#     atoms.set_calculator(calc=calc)
#
#     an_ads_vib(
#         atoms,
#         thermochem_corrections="thermochem_corrections",
#         Temperature=300.0,
#         Pressure=100000.0,
#         symmetrynumber=2,  # symmetry numbers from point group
#         spin=0,  # 1 for O2, 0 for H2O and H2
#         linear=True,
#         )
# #__|
#
# atoms.write("out.traj")
#
# clean_up_dft()
#__|
