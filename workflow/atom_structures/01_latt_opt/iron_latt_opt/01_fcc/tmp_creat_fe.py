"""Temp docstring."""

#| - Import Modules
import os

from ase import io
from ase.build import bulk
#__|

#| - Lattice Parameters
metal = "Fe"

latt_const = 3.4741
supp_latt_units = 2
#__|

#| - Bulk
bulk_fe = bulk(metal, "fcc", a=latt_const, cubic=True)
io.write("bulk.traj", bulk_fe)
#__|

#| - Metal Surface
# slab = fcc111(metal, size=(supp_latt_units, supp_latt_units, 3), a=latt_const)
# io.write("slab.traj", slab)
#__|
