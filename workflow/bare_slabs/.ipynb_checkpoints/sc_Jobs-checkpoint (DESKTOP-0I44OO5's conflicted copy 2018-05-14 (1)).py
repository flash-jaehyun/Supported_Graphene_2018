#!/usr/bin/env python

"""Build a DFT_Jobs class from disorganized individual directories.

Author: Raul A. Flores
"""

#| - Import Modules
import pandas as pd
pd.options.mode.chained_assignment = None

# My Modules ******************************************************************
from dft_job_automat.job_types_classes.dft_methods import DFT_Methods
from dft_job_automat.job_analysis import DFT_Jobs_Analysis
#__|

#| - Script Inputs
dir_list = [

    # Bare Fe
    "/scratch/users/flores12/03_graph_N_Fe/01_opt_struct/Fe/slab/1-att/yes_spin/",
    "/scratch/users/flores12/03_graph_N_Fe/01_opt_struct/Fe/slab/1-att/no_spin/",

    # Bare Graphene
    "/scratch/users/flores12/03_graph_N_Fe/01_opt_struct/graphene/spinpol_True/",
    "/scratch/users/flores12/03_graph_N_Fe/01_opt_struct/graphene/spinpol_False/",

    # Fe-supported Graphene
    
    # NEW
    "/scratch/users/flores12/03_graph_N_Fe/01_opt_struct/combined-Fe-graph/02_relax_again/spinpol_True/",
    "/scratch/users/flores12/03_graph_N_Fe/01_opt_struct/combined-Fe-graph/02_relax_again/spinpol_False/",
    
    "/scratch/users/flores12/03_graph_N_Fe/01_opt_struct/combined-Fe-graph/FCC/5-att/1STEP/data/03-800/03-881/01-True/",
    "/scratch/users/flores12/03_graph_N_Fe/01_opt_struct/combined-Fe-graph/FCC/5-att/1STEP/data/03-800/03-881/02-False/",

    # Fe-supported N-Graphene
    "/scratch/users/flores12/03_graph_N_Fe/01_opt_struct/N_doped_graph_Fe/no_spin/01_N_trifold/",
    "/scratch/users/flores12/03_graph_N_Fe/01_opt_struct/N_doped_graph_Fe/no_spin/02_C_trifold/",
    ]

#__|

#| - Initialze Instances
dft_inst = DFT_Methods(
    methods_to_run=[
        "elec_energy",
        "pdos_data",
        "gibbs_correction",
        "atom_type_num_dict",
        "init_atoms",
        "atoms_object",
        "magmom_charge_history",
        ],
    )

Jobs = DFT_Jobs_Analysis(
    indiv_dir_lst=dir_list,
    working_dir=".",
    folders_exist=True,
    load_dataframe=False,
    job_type_class=dft_inst,
    # job_type_class=None,
    )

#__|

# Jobs.add_data_column(
#     dft_inst.pdos_data,
#     column_name="new_column",
#     revision="auto",
#     # allow_failure=True,
#     allow_failure=False,
#     )
#
# Job_l = Jobs.Job_list
