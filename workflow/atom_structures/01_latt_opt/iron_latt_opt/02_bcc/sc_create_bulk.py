"""Temp docstring."""

#| - Import Modules
from ase import io
from ase.build import bulk
#__|

#| - Lattice Parameters
latt_const = 2.856
supp_latt_units = 2
#__|

#| - Create Bulk Structure
atoms = bulk("Fe", "bcc", a=latt_const)
io.write("fe_bcc.POSCAR", atoms)
#__|
