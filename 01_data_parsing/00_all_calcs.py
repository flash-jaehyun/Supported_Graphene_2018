#!/usr/bin/env python

"""Book keeping script for supported-graphene project.

Essentially just a list of paths to your jobs.


Author: Raul A. Flores
"""

#| - Import Modules
from os.path import join as join
import sys
sys.path.append(".")

import pandas as pd
from methods import job_maint
from dft_job_automat.job_analysis import DFT_Jobs_Analysis
from dft_job_automat.job_types_classes.dft_methods import DFT_Methods

pd.options.mode.chained_assignment = None
#__|

#| - Script Parameters
# Old path from $HOME dir
# rt = "/home/users/kkrempl/01_Fe_graphene_system"
rt = "/scratch/users/kkrempl/01_Supported_Graphene_2018"
fcc_fe_111 = "01_Fe_graphene_system/01_FCC_Fe_111"

dir_list = [

    #| - IrO2 *****************************************************************
    join(rt, fcc_fe_111, "02_2x_Graphen/02_AB_stacking/o"),
    join(rt, fcc_fe_111, "02_2x_Graphen/02_AB_stacking/bare"),
    join(rt, fcc_fe_111, "02_2x_Graphen/02_AB_stacking/oh"),
    join(rt, fcc_fe_111, "02_2x_Graphen/02_AB_stacking/ooh"),
    #__| **********************************************************************

    ]

#__|

#| - Instantiate Classes
dft_inst = DFT_Methods(
    methods_to_run=[
        "elec_energy",
        "init_atoms",
        "atoms_object",
        "dft_params",
        # "incar",
        # "outcar"
        ],
    DFT_code="QE",
    )

Jobs = DFT_Jobs_Analysis(
    indiv_dir_lst=dir_list,
    working_dir=".",
    folders_exist=True,
    load_dataframe=False,
    job_type_class=dft_inst,
    )
#__|

df_all = Jobs.data_frame
df_m = Jobs.filter_early_revisions(Jobs.data_frame)

#| - Job Maintance
print(25 * "*")

tally = {"successes": 0, "failures": 0, "running": 0, "pending": 0}

for Job_i in Jobs.Job_list:
    path_i = Job_i.full_path
    job_i_params = Job_i.job_params

    print(path_i)

    tally = job_maint(
        0,
        path_i,
        job_i_params,
        {"jobs_man_list": [Jobs]},
        tally,
        file_ops=False,
        )
#__|

#| - __old__
Jobs.add_data_column(
    dft_inst.dft_params,
    column_name="new_column",
    revision="auto",
    allow_failure=False,
    )
#__|
