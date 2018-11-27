#!/usr/bin/env python

"""ORR adsorption on N-doped graphene layered on FCC 111 Fe.

Author: Raul A. Flores
"""

#| - Import Modules
from dft_job_automat.job_dependencies import DFT_Jobs_Workflow
from sc_methods import dir_setup, job_maint
#__|

#| - Script Parameters
atoms_list_names = ["init_true", "init_false"]

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
#__|

#| - TEMP - 180602
# from dft_job_automat.job_setup import DFT_Jobs_Setup
# Jobs = DFT_Jobs_Setup(
#     tree_level=tree_level_labels,
#     level_entries=tree_level_values,
#     working_dir="1STEP",
#     )
# job_var_i = Jobs.job_var_lst[1]
#__|

#| - Initialize Instance
WF = DFT_Jobs_Workflow(
    # atoms_prefix=atoms_prefix,
    atoms_list_names=atoms_list_names,
    tree_level_labels_list=[tree_level_labels],
    tree_level_values_list=[tree_level_values],
    model_names=["model.py"],
    setup_function=dir_setup,
    maint_function=job_maint,
    run_jobs=True,
    )
#__|
