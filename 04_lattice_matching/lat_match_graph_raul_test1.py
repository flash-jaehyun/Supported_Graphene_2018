#!/usr/bin/env python

"""Create heterointerfaces between graphene and slab surface.

I'm working on this in my personal branch - Raul Flores

Todo:
    # Impletment loop over a list of defined surface cuts

Author(s): Kevin Krempl, Raul Flores
"""

#| - Import Modules
from mpinterfaces.transformations import (
    Structure,
    get_aligned_lattices,
    generate_all_configs,
    )

from mpinterfaces.utils import slab_from_file
from mpinterfaces.interface import Interface

from pymatgen.io.ase import AseAtomsAdaptor
from ase.io import write

import pickle

import os
#__|

#| - Script Inputs
bulk_filename = 'Cobulk.cif'
graphene_filename = 'graph.cif'

surface_cut = [0, 0, 1]

separation = 3
nlayers_2d = 1
nlayers_substrate = 3

# Lattice matching algorithm parameters
max_area = 40
max_mismatch = 10
max_angle_diff = 3
r1r2_tol = 0.5
#__|

#| - Generate heterstructures
substrate_bulk = Structure.from_file(bulk_filename)
substrate_slab = Interface(
    substrate_bulk,
    hkl=surface_cut,
    min_thick=10,
    min_vac=25,
    primitive=False,
    from_ase=True,
    )
mat2d_slab = slab_from_file([0, 0, 1], graphene_filename)

print(60 * "*")
print("get_aligned_lattices")
mat2d_slab_aligned, substrate_slab_aligned = get_aligned_lattices(
    mat2d_slab,
    substrate_slab,
    max_area=max_area,
    max_mismatch=max_mismatch,
    max_angle_diff=max_angle_diff,
    r1r2_tol=r1r2_tol,
    )
print(60 * "*")
print("")
print("")

#| - Writing hetero_interfaces to pickle file
with open('aligned_latt_materials.pickle', 'wb') as fle:
    pickle.dump((substrate_slab_aligned, mat2d_slab_aligned), fle)
#__|

substrate_slab_aligned.to(filename='00_substrate_opt.POSCAR')
mat2d_slab_aligned.to(filename='00_graphene_opt.POSCAR')

# merge substrate and mat2d in all possible ways
print(60 * "*")
print("generate_all_configs")
hetero_interfaces = generate_all_configs(
    mat2d_slab_aligned,
    substrate_slab_aligned,
    nlayers_2d,
    nlayers_substrate,
    separation,
    )
print(60 * "*")
print("")
print("")

#| - Writing hetero_interfaces to pickle file
with open('hetero_interfaces.pickle', 'wb') as fle:
    pickle.dump(hetero_interfaces, fle)
#__|

#__|

#| - Write all heterostructures to file
os.mkdir('01_heterostructures')
for i, iface in enumerate(hetero_interfaces):
    atoms = AseAtomsAdaptor.get_atoms(iface)
    write(
        os.path.join(
            '.',
            '01_heterostructures',
            'structure_' + str(i + 1).zfill(2) + '.traj',
            ),
        atoms,
        )
#__|
