#!/usr/bin/env python

"""Submit and 'manage' all jobs in data dir.

Intended behavior upon rerunning this script is to rerun failed jobs

Author: Raul A. Flores
"""

#| - IMPORT MODULES
import os
import sys

from create_master_job_list import master_job_list

from dft_job_automat.job_manager import DFT_Jobs_Manager
#__|

Jobs_M = DFT_Jobs_Manager(
    load_dataframe=False,
    )

Jobs_M.create_Jobs_from_dicts_and_paths(master_job_list)

for Job_i in Jobs_M.Job_list:
    print(Job_i.full_path)
    print("-_____-___---__")

    Jobs_M.submit_job(**{
        "path_i": Job_i.full_path,
        "nodes": "1",  # --nodes
        "cpus": "2",  # --ntasks-per-node
        "memory": "2000",  # --mem-per-cpu
        "wall_time": "20",  # --time (720min -> 12hrs)

#         "queue": "owners,iric,normal",  # -p flag
#         "job_name": "Default",  # --job-name
#         "priority": "normal",  # --qos
        # "email": "flores12@stanford.edu",  # --mail-user
#         "email": self.username + "@stanford.edu",  # --mail-user
#         "email_mess": "FAIL",  # --mail-type
        })
