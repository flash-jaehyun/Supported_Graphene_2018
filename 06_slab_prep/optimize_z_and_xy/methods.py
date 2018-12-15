#!/usr/bin/env python

"""Job maintance methods.

Author: Raul A. Flores
"""

#| - Import Modules
import os

import shutil
import json

# from ase import io
# from ase import build
#__|

def dir_setup(
    path_i,
    job_params_i,
    ):
    """Everything needed to specify a job completely.

    # step_i,
    # wf_vars,

    Args:
        step_i:
        path_i:
        job_i_params:
        wf_vars:
    """
    #| - dir_setup ************************************************************

    #| - Checking for '.READY' file
    # If the .READY file exists in a dir, don't do anything
    if os.path.exists(os.path.join(path_i, ".READY")):
        return(None)
    #__|

    #| - Copying Model Scripts
    model_dir = "./model.py"
    shutil.copyfile(
        model_dir,
        os.path.join(
            path_i,
            "model.py"
            )
        )
    #__|

    #| - Creating Atoms Object
    atoms_i = job_params_i["atoms_new"]

    atoms_i.write(
        os.path.join(
            path_i,
            "init.traj"
            )
        )
    #__|

    #| - DFT Params File
    # dft_params_dir = os.path.join(
    #     os.environ["git_fe_graph_proj"],
    #     "03_dft_calcs",
    #     "dft-params_bulk.json",
    #     )

    dft_params_dir = "./dft-params_bulk.json"
    dft_params_dict = json.load(open(dft_params_dir, "r"))
    dft_params_dict["spinpol"] = job_params_i.get("spinpol", True)


    dft_params_path_i = os.path.join(
        path_i,
        "dft-params.json",
        )

    with open(dft_params_path_i, 'w') as outfile:
        json.dump(dft_params_dict, outfile, indent=2)
    #__|

    # ###### last thing #######
    #| - Writing Ready File for First Step
    open(path_i + "/.READY", "w")
    #__|

    return(atoms_i)

    #__| **********************************************************************





#| - __old__

# def job_maint(
#     step_i,
#     job_i,
#     job_i_params,
#     wf_vars,
#     tally,
#     file_ops=False,
#     ):
#     """Job maintance, rerunning jobs, continuning jobs, etc.
#
#     Args:
#         step_i:
#         job_i:
#         job_i_params:
#         wf_vars:
#         tally:
#         file_ops:
#             If False will not create new revision folders and copy files into
#             them.
#     """
#     #| - job_maint ************************************************************
#
#     #| - Parsing wf_vars
#     # master_root_dir = wf_vars["root_dir"]
#     # mod_dir = wf_vars["mod_dir"]
#     # model_names = wf_vars["model_names"]
#
#     Jobs = wf_vars["jobs_man_list"][step_i]
#
#     # atoms_list_names = wf_vars["atoms_list_names"]
#     # atoms_ext = wf_vars["atoms_ext"]
#     # atoms_dir = wf_vars["atoms_dir"]
#     #__|
#
#     import copy
#     # path_i = Jobs.var_lst_to_path(job_i, job_rev="Auto", relative_path=False)
#     path_i = copy.deepcopy(job_i)
#
#     #| - Not READY | Job Dir Not Set Up
#     # if Jobs._job_setup(job_i):
#         # print("SUBMITTING" + " | " + path_i)
#     #__|
#
#     #| - READY  | Not SUBMITTED
#     if Jobs._job_ready(job_i):
#         print("SUBMITTING" + " | " + path_i)
#
#         # Jobs.submit_job(
#         #     path_i=path_i,
#         #     wall_time="400",
#         #     queue="regular",
#         #     )
#     #__|
#
#     #| - PENDING | Leave Alone
#     # print("Is job pending:")
#     # print(Jobs._job_pending(job_i))
#
#     if Jobs._job_pending(job_i):
#         print("PENDING" + " | " + path_i)  # PERM_PRINT
#
#         tally["pending"] += 1
#     #__|
#
#     #| - RUNNING
#     if Jobs._job_running(job_i):
#         print("RUNNING" + " | " + path_i)  # PERM_PRINT
#
#         tally["running"] += 1
#     #__|
#
#     #| - SUCCEEDED | Copy Files to Next Step
#     if Jobs._job_succeeded(job_i):
#         print("SUCCESS" + " | " + path_i)  # PERM_PRINT
#
#         tally["successes"] += 1
#
#         if file_ops:
#             tmp = 42
#             print(tmp)
#
#             # if step_num == 1:
#             #     jd.copyfiles_onestep_up(job_i, step_num, Jobs_Inst_list,
#             #         files_lst=[
#             #             ["CONTCAR", "init.POSCAR"],
#             #             ".READY",
#             #             ]
#             #         )
#
#     # else:
#     #     pass
#     #__|
#
#     #| - FAILED | Rerun Job
#     if Jobs._job_failed(job_i):
#         print("FAILURE" + " | " + path_i)  # PERM_PRINT
#         tally["failures"] += 1
#
#         #| - Step 1 Restart
#         if step_i == 0:
#             prev_files = [
#                 "dft-params.json",
#                 "out_opt.traj",
#                 "model.py",
#                 ".READY",
#                 ]
#
#             sub_params = {
#                 "wall_time": "2000"
#                 }
#
#             if file_ops:
#                 Jobs.restart_job(job_i, prev_files, sub_params=sub_params)
#         #__|
#
#     #__|
#
#
#
#     return(tally)
#     #__| **********************************************************************

#__|
