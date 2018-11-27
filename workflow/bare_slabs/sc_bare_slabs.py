#!/usr/bin/env python

"""Build a DFT_Jobs class from disorganized individual directories.

Author: Raul A. Flores
"""

#| - Import Modules
import pandas as pd

# My Modules ******************************************************************
from dft_job_automat.job_types_classes.dft_methods import DFT_Methods
from dft_job_automat.job_analysis import DFT_Jobs_Analysis

pd.options.mode.chained_assignment = None
#__|

#| - Script Inputs
root_dir = "/scratch/users/flores12/03_graph_N_Fe/01_opt_struct/"
dir_list = [

    #| - Bare Fe
    root_dir + "Fe/slab/1-att/yes_spin/",
    root_dir + "Fe/slab/1-att/no_spin/",

    root_dir + "Fe/bulk/02_FM/",
    #__|

    #| - Bare Graphene
    root_dir + "graphene/spinpol_True/",
    root_dir + "graphene/spinpol_False/",
    #__|

    #| - Fe-supported Graphene
    root_dir + "combined-Fe-graph/02_relax_again/spinpol_True/",
    root_dir + "combined-Fe-graph/02_relax_again/spinpol_False/",
    #__|

    #| - Fe-supported N-Graphene
    root_dir + "N_doped_graph_Fe/no_spin/01_N_trifold/",
    root_dir + "N_doped_graph_Fe/no_spin/02_C_trifold/",
    #__|

    #| - N-Graphene
    root_dir + "N_graph/spinpol_True/",
    root_dir + "N_graph/spinpol_False/",
    #__|
    ]

#__|

#| - Initialze Instances
dft_inst = DFT_Methods(
    methods_to_run=[
        "elec_energy",
        "pdos_data",
        "bands_data",
        "gibbs_correction",
        "atom_type_num_dict",
        "init_atoms",
        "atoms_object",
        # "magmom_charge_history",
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

df = Jobs.data_frame
df = Jobs.filter_early_revisions(df)

#| - Test - add_data_column
def add_col(funct):
    Jobs.add_data_column(
        funct,
        # dft_inst.pdos_data,
        column_name="new_column",
        revision="auto",
        allow_failure=True,
        # allow_failure=False,
        )
#__|
