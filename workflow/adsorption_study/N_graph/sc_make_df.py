#!/usr/bin/env python

"""IrOx Project.

Author: Raul A. Flores
"""

#| - Import Modules
from os.path import join as join
import sys
sys.path.append(".")

import pandas as pd
pd.options.mode.chained_assignment = None

from sc_methods import job_maint
from dft_job_automat.job_analysis import DFT_Jobs_Analysis
from dft_job_automat.job_types_classes.dft_methods import DFT_Methods
#__|

#| - Script Parameters

#__|

#| - Instantiate Classes
tree_level_labels = [
    "adsorbate",
    "site",
    "spinpol",
    ]

adsorbates = [
    "ooh",
    "o",
    "oh",
    "h2o",
    ]

# C1 is adjacent to N, C2 is non-adjacent to N
sites = [
    "ring-center",
    "C1-ontop",
    "C2-ontop",
    "N-ontop",
    "C-N-bridged",
    "C-C bridged",
    ]

tree_level_values = [
    adsorbates,
    sites,
    [True, False],
    ]

dft_inst = DFT_Methods(
    methods_to_run=[
        "elec_energy",
        "pdos_data",
        "gibbs_correction",
        "atom_type_num_dict",
        "init_atoms",
        "atoms_object",
        # "incar",
        ],
    DFT_code="QE",
    )

Jobs = DFT_Jobs_Analysis(
    tree_level=tree_level_labels,
    level_entries=tree_level_values,

    # indiv_dir_lst=dir_list,

    working_dir="1STEP",
    folders_exist=True,
    load_dataframe=False,
    job_type_class=dft_inst,
    )

#__|

# Jobs.add_data_column(
#     dft_inst.atom_type_num_dict,
#     column_name="new_column",
#     revision="auto",
#     allow_failure=False,
#     )

df_all = Jobs.data_frame
df_m = Jobs.filter_early_revisions(Jobs.data_frame)



#| - Job Maintance
# print(25 * "*")
#
# tally = {"successes": 0, "failures": 0, "running": 0, "pending": 0}
#
# for Job_i in Jobs.Job_list:
#     path_i = Job_i.full_path
#     job_i_params = Job_i.job_params
#
#     print(path_i)
#
#     tally = job_maint(
#         0,
#         path_i,
#         job_i_params,
#         {"jobs_man_list": [Jobs]},
#         tally,
#         file_ops=False,
#         )
#__|
