#!/usr/bin/env python

"""Create heterointerfaces between graphene and slab surface.

TEST 181121 - RF
I'm working on this in my personal branch - Raul Flores

Todo:
    # Impletment loop over a list of defined surface cuts

Author(s): Kevin Krempl, Raul Flores
"""

#| - Import Modules
import pickle
import os

import json

from mpinterfaces.transformations import (
    Structure,
    get_aligned_lattices,
    generate_all_configs,
    )

from mpinterfaces.utils import slab_from_file
from mpinterfaces.interface import Interface

from pymatgen.io.ase import AseAtomsAdaptor

from ase import io
#__|

#| - Script Inputs
strain_sys = "support"  # 'support' or 'overlayer'
# strain_sys = "overlayer"  # 'support' or 'overlayer'

bulk_filename = "init_support.cif"
graphene_filename = "init_graphene.cif"

# surface_cut = [0, 0, 1]

separation = 3
nlayers_2d = 1
nlayers_substrate = 3

# Lattice matching algorithm parameters
max_area = 100
max_mismatch = 1
max_angle_diff = 0.1
r1r2_tol = 0.01
#__|

#| - METHODS ******************************************************************

def create_heterostructure(
    bulk_structure=None,
    slab_structure=None,

    strain_sys="overlayer",  # 'support' or 'overlayer'

    surface_cut=[0, 0, 1],
    separation=3,
    nlayers_2d=1,
    nlayers_substrate=4,

    # Lattice matching algorithm parameters
    max_area=40,
    max_mismatch=1,
    max_angle_diff=0.1,
    r1r2_tol=0.01,
    ):
    """

    bulk_structure:
        ase atoms object for the support material
    slab_structure:
        overlayer material

    strain_sys:
    surface_cut:
    separation:
    nlayers_2d:
    nlayers_substrate:
    max_area:
    max_mismatch:
    max_angle_diff:
    r1r2_tol:

    """
    #| - create_heterostructure

    #| - Generate Heterostructures
    # substrate_bulk = Structure.from_file(bulk_filename)

    substrate_slab = Interface(
        bulk_structure,
        # substrate_bulk,
        hkl=surface_cut,
        min_thick=20,
        min_vac=30,
        primitive=False,
        from_ase=True,
        )

    # mat2d_slab = slab_from_file([0, 0, 1], graphene_filename)
    mat2d_slab = slab_structure

    if strain_sys == "support":
        lower_mat = mat2d_slab
        upper_mat = substrate_slab
    elif strain_sys == "overlayer":
        lower_mat = substrate_slab
        upper_mat = mat2d_slab

    # mat2d_slab_aligned, substrate_slab_aligned = get_aligned_lattices(
    lower_mat_aligned, upper_mat_aligned = get_aligned_lattices(
        lower_mat,
        upper_mat,
        max_area=max_area,
        max_mismatch=max_mismatch,
        max_angle_diff=max_angle_diff,
        r1r2_tol=r1r2_tol,
        )

    if strain_sys == "support":
        mat2d_slab_aligned = lower_mat_aligned
        substrate_slab_aligned = upper_mat_aligned
    elif strain_sys == "overlayer":
        mat2d_slab_aligned = upper_mat_aligned
        substrate_slab_aligned = lower_mat_aligned


    # Writing hetero_interfaces to pickle file
    with open('aligned_latt_materials.pickle', 'wb') as fle:
        pickle.dump((substrate_slab_aligned, mat2d_slab_aligned), fle)

    substrate_slab_aligned.to(filename='00_substrate_opt.POSCAR')
    mat2d_slab_aligned.to(filename='00_graphene_opt.POSCAR')

    # merge substrate and mat2d in all possible ways
    hetero_interfaces = generate_all_configs(
        mat2d_slab_aligned,
        substrate_slab_aligned,
        nlayers_2d,
        nlayers_substrate,
        separation,
        )

    # Writing hetero_interfaces to pickle file
    with open('hetero_interfaces.pickle', 'wb') as fle:
        pickle.dump(hetero_interfaces, fle)
    #__|

    return(hetero_interfaces)

    #__|

#__| **************************************************************************


# | - __main__

surface_cut = json.load(open("facet.json", "r"))["facet"]

bulk_structure = Structure.from_file(bulk_filename)

slab_structure = slab_from_file([0, 0, 1], graphene_filename)
slab_structure.to(filename='tmp.POSCAR')

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

out_dir = '01_heterostructures'

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

for i, iface in enumerate(hetero_interfaces_i):
    atoms = AseAtomsAdaptor.get_atoms(iface)
    io.write(
        os.path.join(
            out_dir,
            'out_' + str(i).zfill(2) + '.traj',
            ),
        atoms,
        )
#__|
