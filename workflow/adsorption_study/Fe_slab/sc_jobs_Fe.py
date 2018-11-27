#!/usr/bin/env python

"""ORR adsorption on FCC 111 Fe slab.

Author: Raul A. Flores
"""

#| - Import Modules
from dft_job_automat.job_dependencies import DFT_Jobs_Workflow
from job_methods import dir_setup, job_maint
#__|

run_jobs = True

#| - Parameters
atoms_prefix = ".traj"
atoms_list_names = ["init"]

tree_level_labels = ["adsorbate", "site", "spinpol"]

tree_level_values = [
    ["ooh", "o", "oh", "h2o"],
    ["ontop", "bridge", "trifold"],
    [True, False]
    ]

tree_level_labels_list = [tree_level_labels]
level_entries_dict_list = [tree_level_values]
#__|

#| - Initialize Instance
WF = DFT_Jobs_Workflow(
    atoms_prefix=atoms_prefix,
    atoms_list_names=atoms_list_names,
    tree_level_labels_list=tree_level_labels_list,
    tree_level_values_list=level_entries_dict_list,
    model_names=["model.py"],
    setup_function=dir_setup,
    maint_function=job_maint,

    run_jobs=run_jobs,
    )
#__|
