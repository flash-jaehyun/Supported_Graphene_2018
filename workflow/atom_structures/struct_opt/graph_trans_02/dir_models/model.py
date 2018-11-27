#!/usr/bin/env python

#| - IMPORT MODULES
import pickle
import json
import os
import sys

from ase.io import read, write, PickleTrajectory
from espresso import espresso
from ase.dft.kpoints import ibz_points, get_bandpath
from ase.optimize import QuasiNewton

# MY MODULES
sys.path.append("./PythonModules/")

from bader_charge.bader import bader
from ase_modules.ase_methods import (
    read_atoms_from_file,
    set_init_mag_moms,
    spin_pdos,
    an_pdos,
    an_bands,
    ionic_opt,
    )

from ase_modules.dft_params import Espresso_Params
#__|

#| - SCRIPT INPUTS ************************************************************
mode = "opt" # opt (ionic optimization) or sp (single-point calculation)
opt_fmax = 0.05 # max force convergence for optimizer

run_bader = True
run_pdos  = True
run_bands = True

# dos_kpts = (12, 12, 1)
dos_kpts = (3, 3, 1)
bands_kpts = (3, 3, 1)

#__| **************************************************************************

#| - Reading Atoms Object From File
print("Reading atoms object from file")
atoms = read_atoms_from_file()
#__|

#| - Calculation Parameters
print("Loading QE parameters from file")

espresso_params_inst = Espresso_Params(load_defaults=True)

if os.path.isfile("dft-params.json"):
    params_file = json.load(open("dft-params.json"))
    espresso_params_inst.update_params(params_file)

# espresso_params_inst.update_params(params)  # Create params dict if wanted

espresso_params_inst.test_check()
espresso_params_inst.write_params()
espresso_params = espresso_params_inst.params

calc = espresso(**espresso_params)
atoms.set_calculator(calc=calc)
#__|

#| - Setting Magnetic Moments
print("Setting inital magnetic moments")
set_init_mag_moms(atoms)
#__|

#| - Executing DFT
ionic_opt(atoms, calc, espresso_params, mode="easy_opt")
#__|

#| - Bader Analysis
print(atoms.get_initial_magnetic_moments())

#| - Don't Run Bader Executable on AWS
compenv = os.environ["COMPENV"]
if compenv == "slac" or compenv == "sherlock":
    run_exec = True
else:
    run_exec = False
#__|

if run_bader:
    bader(atoms, spinpol=espresso_params["spinpol"], run_exec=run_exec)
    write("dir_bader/bader.traj", atoms)
#__|

#| - PDOS Analysis
print(atoms.get_initial_magnetic_moments())
if run_pdos:
    atoms.set_calculator(calc=calc)
    an_pdos(atoms, dos_kpts, espresso_params)
print(atoms.get_initial_magnetic_moments())
#__|

#| - Band Structure Analaysis
if run_bands:
    an_bands(atoms, bands_kpts, espresso_params)
#__|

#| - Cleanup
with open(".FINISHED", "w") as fle:
    fle.write("\n")
#__|






#| - __old__

#| - __old__
# print("Executing Band Structure Analysis")
#
# espresso_params.update(
#     {
#         "kpts": (6, 6, 6),
#         "outdir": "dir_bands"
#         }
#     )
#
# atoms.calc = espresso(**espresso_params)
# atoms.get_potential_energy()
# atoms.calc.save_flev_chg("charge_den.tgz")
#
# atoms.calc.load_flev_chg("charge_den.tgz")
#
# ip = ibz_points["fcc"]
# points = ["Gamma", "X", "W", "K", "L", "Gamma"]
#
# bzpath = [ip[p] for p in points]
#
# kpts, x, X = get_bandpath(bzpath, atoms.cell, npoints=300)
# energies = atoms.calc.calc_bandstructure(kpts)
#
# f = open("band_disp.pickle", "w")
# pickle.dump((points, kpts, x, X, energies), f)
# f.close()
#__|

#| - __old__
# dos = calc.calc_pdos(
#     nscf=True,
#     kpts=dos_kpts,
#     Emin=-15.0,
#     Emax=15.0,
#     ngauss=0,
#     sigma=0.2,
#     DeltaE=0.01,
#     tetrahedra=False,
#     slab=True,
#     )
#
# if not os.path.exists("dir_pdos"):
#     os.makedirs("dir_pdos")
#
# pdos_out = "dir_pdos/dos.pickle"
# with open(pdos_out, "w") as fle:
#     pickle.dump(dos, fle)
#
# # Set Magnetic Moments To Atoms Object From PDOS Intergration
# spin_pdos(atoms, pdos_out, spinpol=espresso_params["spinpol"])
# write("dir_pdos/pdos.traj", atoms)
#__|

#| - __old__
# print("Running DFT calculation")
# atoms.set_calculator(calc)
# if mode == "opt":
#     qn = QuasiNewton(
#         atoms,
#         trajectory="out_opt.traj",
#         logfile="qn.log",
#         # restart="qn.pickle",
#         )
#
#     if os.path.exists("prev.traj"):
#         qn.replay_trajectory("prev.traj")
#
#     qn.run(fmax=opt_fmax)
#
# elif mode == "sp":
#     atoms.get_potential_energy()
#     write("out.traj", atoms)
#__|


#__|
