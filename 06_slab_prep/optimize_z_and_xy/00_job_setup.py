#!/usr/bin/env python

"""Setup the jobs and job attributes.

Author: Raul A. Flores
"""

#| - IMPORT MODULES
from dft_job_automat.job_setup import DFT_Jobs_Setup
from methods import dir_setup
from create_master_job_list import master_job_list
#__|

#| - Instantiate DFT_Jobs_Setup
Jobs_S = DFT_Jobs_Setup()

Jobs_S.create_Jobs_from_dicts_and_paths(master_job_list)
Jobs_S.create_dir_struct()
Jobs_S.write_job_params_json_file()
#__|

#| - Job Setup
# print(25 * "*")
# atoms_list = []
# for Job_i in Jobs_S.Job_list:
#     path_i = Job_i.full_path
#     job_i_params = Job_i.job_params_dict
#
#     atoms_i = dir_setup(
#         path_i,
#         job_i_params,
#         )
#
#     atoms_list.append(atoms_i)
#__|
