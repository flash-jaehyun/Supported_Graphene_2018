#!/usr/bin/env python

"""DFT relaxation w/ additional anaylsis.

Author: Raul A. Flores
"""

#| - IMPORT MODULES
import sys
sys.path.insert(0, "./PythonPackages"); sys.path.insert(0, "./PythonModules")
from ase_modules.ase_methods import (
    read_atoms_from_file, set_QE_calc_params,
    set_init_mag_moms, read_magmoms_from_file,
    ionic_opt, an_pdos,
    an_bands, an_ads_vib, clean_up_dft)
#__|

#| - SCRIPT INPUTS ************************************************************
mode = "sp"  # opt (ionic optimization), easy_opt, or sp (single-point calc)
fmax = 0.01  # max force convergence for optimizer

run_opt             = True
run_beef_ensemble   = True
run_bader           = False
run_pdos            = False
run_bands           = False
run_vib             = False

# kpts = (12, 12, 12)
kpts = 3 * (6,)

dos_kpts   = kpts
bands_kpts = kpts

# dos_kpts   = tuple(3 * [12])
# bands_kpts = tuple(3 * [12])
#__| **************************************************************************

#| - Setup
atoms, traj = read_atoms_from_file(filename="init.traj")

calc, espresso_params = set_QE_calc_params(
    atoms=None, params={},
    load_defaults=True, init_inst=False)

magmoms = read_magmoms_from_file(file_name="magmom_init.in")

set_init_mag_moms(atoms, espresso_params=espresso_params,
    read_from_file=True, inc_val_magmoms=False, magmoms=magmoms)
#__|

#| - Protocols
if run_opt:
    ionic_opt(
        atoms,
        traj=traj, espresso_params=espresso_params, mode=mode, fmax=fmax,
        run_beef_an=run_beef_ensemble, run_bader_an=run_bader)

if run_pdos:
    an_pdos(atoms, dos_kpts, espresso_params)

if run_bands:
    an_bands(atoms, bands_kpts, espresso_params)

if run_vib:
    an_ads_vib(atoms, thermochem_corrections="harmonic")
#__|

atoms.write("out.traj")
clean_up_dft()
