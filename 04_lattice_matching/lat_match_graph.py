#!/usr/bin/env python
#| - SLURM HEADER
#above line selects special python interpreter which knows all the paths
#SBATCH -p iric,owners
#################
#set a job name
#SBATCH --job-name=recon1
#################
#a file for job output, you can check job progress
#SBATCH --output=myjob.out
#################
# a file for errors from the job
#SBATCH --error=myjob.err
#################
#time you think you need; default is one hour
#in minutes in this case
#SBATCH --time=00:30:00
#################
#quality of service; think of it as job priority
#SBATCH --qos=normal
#################
#number of nodes you are requesting
#SBATCH --nodes=1
#################
#memory per node; default is 4000 MB per CPU
#SBATCH --mem-per-cpu=4000
#you could use --mem-per-cpu; they mean what we are calling cores
#################
#get emailed about job BEGIN, END, and FAIL
#SBATCH --mail-type=FAIL
#################
#who to send email to; please change to your email
#SBATCH  --mail-user=kkrempl@stanford.edu
#################
#task to run per node; each node has 16 cores
#SBATCH --ntasks-per-node=16
#################
#__|
"""Finds matching unit cells for graphene and a previously optimized bulk
crystal.


Author(s): Kevin Krempl, Raul Flores
"""

#| - Import Modules
from mpinterfaces.interface import Interface
from mpinterfaces.transformations import *
from mpinterfaces.utils import *

from pymatgen.io.ase import AseAtomsAdaptor

from ase.io import write

import pickle
#__|

#| - Inputs
# bulk_filename = 'Cobulk.POSCAR'
# graphene_filename = 'graph.POSCAR'

bulk_filename = 'Cobulk.cif'
graphene_filename = 'graph.cif'

surface_cut = [0,0,1]

separation = 3
nlayers_2d = 1
nlayers_substrate = 3

# Lattice matching algorithm parameters
# max_area = 1000
# max_mismatch = 5
# max_angle_diff = 1
# r1r2_tol = 0.01

max_area = 300
max_mismatch = 10
max_angle_diff = 3
r1r2_tol = 0.5
#__|

#| - Generate heterstructures
#impletment loop over a list of defined surface cuts

substrate_bulk = Structure.from_file(bulk_filename)
substrate_slab = Interface(
    substrate_bulk,
    hkl=surface_cut,
    min_thick=10,
    min_vac=25,
    primitive=False,
    from_ase=True,
    )

mat2d_slab = slab_from_file([0,0,1], graphene_filename)

# get aligned lattices
substrate_slab_aligned, mat2d_slab_aligned = get_aligned_lattices(
    substrate_slab,
    mat2d_slab,
    max_area=max_area,
    max_mismatch=max_mismatch,
    max_angle_diff=max_angle_diff,
    r1r2_tol=r1r2_tol,
    )

substrate_slab_aligned.to(filename='Substrate_opt.POSCAR')
mat2d_slab_aligned.to(filename='Graphene_opt.POSCAR')

# merge substrate and mat2d in all possible
# ways
hetero_interfaces = generate_all_configs(
    mat2d_slab_aligned,
    substrate_slab_aligned,
    nlayers_2d,
    nlayers_substrate,
    separation,
    )

#with open('hetero_interfaces', 'wb') as fle:
    #pickle.dump(hetero_interfaces, fle)

#| - Generate all poscars in new dir

mkdir 01_heterostructures

for i, iface in enumerate(hetero_interfaces):
    atoms = AseAtomsAdaptor.get_atoms(iface)
    write('./01_heterostructures/structure'+str(i)+'.traj', atoms)
#__|

# hetero_interfaces.to(filename='heterostructure.POSCAR')
#__|

#| - Main loop

#__|
