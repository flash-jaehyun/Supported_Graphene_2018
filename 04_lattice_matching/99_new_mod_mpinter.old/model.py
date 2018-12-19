#!/usr/bin/env python

"""
Create heterointerfaces between graphene and slab surface.


I'm working on this in my personal branch - Raul Flores

Todo:
    # Impletment loop over a list of defined surface cuts

Author(s): Kevin Krempl, Raul Flores
"""

#| - Import Modules
import os
import sys

sys.path.append(
    os.path.join(
        os.environ["PROJ_fe_graph"],
        "04_lattice_matching",
        )
    )
from new_methods import create_heterostructure

# #############################################################################

import json
import pickle

from ase import io
from mpinterfaces.utils import slab_from_file

from pymatgen.core.structure import Structure
from pymatgen.io.ase import AseAtomsAdaptor
#__|

#| - Script Inputs
strain_sys = "support"  # 'support' or 'overlayer'
# strain_sys = "overlayer"  # 'support' or 'overlayer'

bulk_filename = "init_support.cif"
graphene_filename = "init_graphene.cif"

separation = 3
nlayers_2d = 1
nlayers_substrate = 3

# Lattice matching algorithm parameters
max_area = 250
max_mismatch = 0.05
max_angle_diff = 0.05
r1r2_tol = 0.05
#__|

#| - __main__
surface_cut = json.load(open("facet.json", "r"))["facet"]
bulk_structure = Structure.from_file(bulk_filename)
slab_structure = slab_from_file([0, 0, 1], graphene_filename)


# lower_mat_aligned, upper_mat_aligned = create_heterostructure(
hetero_interfaces_i = create_heterostructure(
    bulk_structure=bulk_structure,
    slab_structure=slab_structure,
    strain_sys=strain_sys,
    surface_cut=surface_cut,
    separation=separation,
    nlayers_2d=nlayers_2d,
    nlayers_substrate=nlayers_substrate,
    max_area=max_area,
    max_mismatch=max_mismatch,
    max_angle_diff=max_angle_diff,
    r1r2_tol=r1r2_tol,
    )

out_dir = '01_heterostructures_outdir'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

for i, sys_i in enumerate(hetero_interfaces_i):
    struct_i = sys_i["heterointerface"]
    atoms = AseAtomsAdaptor.get_atoms(struct_i)

    io.write(
        os.path.join(
            out_dir,
            'out_' + str(i).zfill(2) + '.traj',
            ),
        atoms,
        )

pickle.dump(
    hetero_interfaces_i,
    open("heterostructures.pickle", "wb")
    )
#__|
