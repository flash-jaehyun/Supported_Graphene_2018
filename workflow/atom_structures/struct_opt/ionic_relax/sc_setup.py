"""FCC 111 + Graphene Overlayer  """

#| - Import Modules
import os
import  sys
import shutil
import copy
import subprocess

import numpy as np
import pandas as pd
pd.options.display.max_colwidth = 250

# ASE
from ase import io
# from ase.io.trajectory import Trajectory
# from ase.build import bulk

# My Modules
from ase_modules.adsorbates import Adsorbate
#from ase_modules.add_adsorbate import add_adsorbate_centered
from ase_modules.dft_params import Espresso_Params


from dft_job_automat.job_setup import DFT_Jobs_Setup
from dft_job_automat.job_analysis import DFT_Jobs_Analysis
from dft_job_automat.job_manager import DFT_Jobs_Manager
import dft_job_automat.job_dependencies as jd

# from dft_job_automat.job_dependencies import DFT_Jobs_Workflow

#__|

#| - Script Parameters

#| - Atoms Object
atoms_prefix = ".traj"
atoms_list_names = ["init"]
# atoms_dict = jd.create_atoms_list(atoms_list_names, atoms_prefix, os.getcwd())
#__|

#| - Parameters
tree_level_labels = [
    "pw-cutoff",
    "kpoints",
    "magmom",
    ]

tree_level_values = [
    [400, 600, 800, 1000],
    ["441", "661", "881"],
    [True, False],
    ]

tree_level_labels_list = [tree_level_labels]
level_entries_dict_list = [tree_level_values]
#__|

# Workflow = DFT_Jobs_Workflow(
#     atoms_prefix=atoms_prefix,
#     atoms_list_names=atoms_list_names,
#     tree_level_labels_list=tree_level_labels_list,
#     tree_level_values_list=tree_level_values_list,
#     )

#| - Script Behavior Flags
run_jobs = True  # Set to "False" to create directory structure only
run_trisync = False
#__|


# sys.exit(0)
#__|

#| - MISC Parameters
step_dir_names = ["1STEP"]
model_sc_names = ["model.py"]

mod_dir = "dir_models"
atoms_dir = "dir_atoms"
#__|


#| - Under the  Hood ***********************************************************

#| - Root Directory
master_root_dir = os.getcwd()
root_dir_lst_full = master_root_dir.split("/")
#__|

#| - trisync folders
if os.path.exists(master_root_dir + "/.FOLDERS_CREATED") and run_trisync:
    aws_dir = os.environ["aws_dir"]
    trysync_comm = aws_dir + "/matr.io/bin/trisync"
    subprocess.call(trysync_comm)
    print("")  #PERM_PRINT
#__|

#__| ***************************************************************************

#| - PREPARING EXTENDED FOLDER SYSTEM ******************************************
print("PREPARING EXTENDED FOLDER SYSTEM")  #PERM_PRINT
Jobs_Inst_list = []
for step in range(len(step_dir_names)):
    step_num = step + 1

    #| - Initializing Job Instances
    print("Initializing Job Instance: " + str(step_num))  #PERM_PRINT

    dir_struct_file = master_root_dir + "/" + step_dir_names[step] + "/jobs_bin/dir_structure.json"

    level_labels_tmp = tree_level_labels_list[step]
    level_entries_tmp = level_entries_dict_list[step]

    JobsAn = DFT_Jobs_Analysis(
        system="aws",
        tree_level=level_labels_tmp,
        level_entries=level_entries_tmp,
        working_dir=master_root_dir + "/" + step_dir_names[step],
        update_job_state=False,
        load_dataframe=False,
        )

    Jobs_Inst_list.append(JobsAn)
    #__|

    #| - Creating Parent Step Folders
    step_folder = master_root_dir + "/" + step_dir_names[step]
    if not os.path.isdir(step_folder):
        os.makedirs(step_dir)
    #__|

    #| - Placing Initial Files in Folders | LOOP OVER JOBS ^^^^^^^^^^^^^^^^^^^^
    print("Placing Initial Files in Folders | LOOP OVER JOBS")  #PERM_PRINT
    files_placed_file = master_root_dir + "/" + step_dir_names[step] + "/.FILES_PLACED"

    if not os.path.isfile(files_placed_file):

        #| - Create Step Folder Structure
        JobsAn.create_dir_struct(create_first_rev_folder="True")
        #__|

        for job_i in JobsAn.job_var_lst:
            path_i = JobsAn.var_lst_to_path(job_i, job_rev="Auto", relative_path=False)

            #| - Copying Model Scripts
            model_dir = master_root_dir + "/" + mod_dir + "/" + model_sc_names[step]
            shutil.copyfile(model_dir, path_i + "/model.py")
            #__|

            #| - Job_i Parameters
            job_i_params = {}
            for variable in JobsAn.tree_level_labels:
                job_i_params[variable] = JobsAn.extract_prop_from_var_lst(job_i, variable)
            #__|

            #| - DFT Parameters
            qe_par = Espresso_Params(load_defaults=False)

            var = "pw-cutoff"
            if var in job_i_params:
                pw_cutoff = job_i_params[var]
                qe_par.update_params({"pw": pw_cutoff})
                qe_par.update_params({"dw": 10. * pw_cutoff})

            var = "kpoints"
            if var in job_i_params:
                kpts_str = job_i_params[var]
                kpts = (kpts_str[0], kpts_str[1], kpts_str[2])
                qe_par.update_params({"kpts": kpts})

            var = "magmom"
            if var in job_i_params:
                qe_par.update_params({"spinpol": job_i_params[var]})

            qe_par.write_params(path=path_i)
            #__|

            #| - Atoms Object

            atoms_file = atoms_list_names[0] + atoms_prefix
            shutil.copy(master_root_dir + "/dir_atoms/" + atoms_file, path_i)
            #__|

            #| - Writing Ready File for First Step
            if step_num == 1:
                file = open(path_i + "/.READY", "w")
            #__|

            file_name = master_root_dir + "/" + step_dir_names[step]
            file = open(file_name + "/.FILES_PLACED", "w")

    file = open(master_root_dir + "/.FOLDERS_CREATED", "w")

    #__| ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#__| ***************************************************************************

#| - MONITERING JOBS ***********************************************************
print("MONITERING JOBS")  #PERM_PRINT

#| - Reinitiating the Jobs Instances
print("")  #PERM_PRINT
print("Reinitiating the Jobs Instances")  #PERM_PRINT
Jobs_Inst_list = []
for step in range(len(step_dir_names)):
    step_num = step + 1

    Jobs = DFT_Jobs_Manager(
        system="aws",
        tree_level=tree_level_labels_list[step],
        level_entries=level_entries_dict_list[step],
        working_dir=master_root_dir + "/" + step_dir_names[step],
        load_dataframe=False,
        )

    Jobs_Inst_list.append(Jobs)
#__|

print("")  #PERM_PRINT
root_dir_beg = master_root_dir
for step in range(len(step_dir_names)):
    step_num = step + 1
    Jobs = Jobs_Inst_list[step]
    df = Jobs.data_frame
    tally = {"successes": 0, "failures": 0, "running": 0, "pending": 0}

    #| - PRINT
    print("")  #PERM_PRINT
    print("###################################################################")
    print("############################ STEP " + str(step_num) + " ###############################")
    print("###################################################################")
    print("Total Jobs: " + str(Jobs.num_jobs))  #PERM_PRINT
    #__|

    #| - LOOP OVER JOBS
    if run_jobs:
        for job_i in Jobs.job_var_lst:
            path_i = Jobs.var_lst_to_path(job_i, job_rev="Auto", relative_path=False)

            #| - READY  | Not SUBMITTED
            if Jobs.job_ready(job_i):
                print("SUBMITTING" + " | " + path_i)  #PERM_PRINT

                Jobs.submit_job(
                    path_i =    path_i,
                    wall_time = "2800"
                    )
            else:
                pass
            #__|

            #| - PENDING | Leave Alons
            if Jobs.job_pending(job_i):
                print("PENDING" + " | " + path_i)  #PERM_PRINT

                tally["pending"] += 1
            #__|

            #| - RUNNING
            if Jobs.job_running(job_i):
                print("RUNNING" + " | " + path_i)  #PERM_PRINT

                tally["running"] += 1
            #__|

            #| - SUCCEEDED | Copy Files to Next Step
            if Jobs.job_succeeded(job_i):
                print("SUCCESS" + " | " + path_i)  #PERM_PRINT

                tally["successes"] += 1

                """
                if step_num == 1:
                    jd.copyfiles_onestep_up(job_i, step_num, Jobs_Inst_list,
                        files_lst=[
                            ["CONTCAR", "init.POSCAR"],
                            ".READY",
                            ]
                        )
                elif step_num == 2:
                    jd.copyfiles_onestep_up(job_i, step_num, Jobs_Inst_list,
                        files_lst=[
                            ["OUTCAR", "OUTCAR.phon"],
                            ["POSCAR", "POSCAR.phon"],
                            ".READY",
                            ]
                        )

                elif step_num == 3:
                    pass
                """

            else:
                pass
            #__|

            #| - FAILED | Rerun Job
            if Jobs.job_failed(job_i):
                print("FAILURE" + " | " + path_i)  #PERM_PRINT
                tally["failures"] += 1

                #| - Step 1 Restart
                if step_num == 1:
                    prev_files = [
                        "dft-params.json",
                        "init.traj",
                        "model.py",
                        ".READY",
                        ]

                    sub_params = {
                        "wall_time": "2400"
                        }

                    # Jobs.restart_job(job_i, prev_files, sub_params=sub_params)
                #__|

                """
                #| - Step 2 Restart | TEMP
                # if step_num == 2:
                #     print("Restarting step 2 job")
                #
                #     #| - Job_i Parameters
                #     job_i_params = {}
                #     for variable in Jobs.tree_level_labels:
                #         job_i_params[variable] = Jobs.extract_prop_from_var_lst(job_i, variable)
                #     #__|
                #
                #     #| - VASP Parameters
                #     vasp_par = VASP_Params(load_defaults=True)
                #
                #     var = "force-cutoff"
                #     if var in job_i_params:
                #         vasp_par.update_params({"ediffg": job_i_params[var]})
                #
                #     var = "pw-cutoff"
                #     if var in job_i_params:
                #         vasp_par.update_params({"encut": job_i_params[var]})
                #
                #     var = "dft-functionals"
                #     if var in job_i_params:
                #         functional = job_i_params["dft-functionals"]
                #         if functional == "hse06":
                #             vasp_par.update_params({
                #                 "algo":     "All",
                #                 "time":     0.5,
                #
                #                 "ibrion": 6,
                #
                #                 "hfscreen": 0.2,
                #                 "aexx":     0.25,
                #                 "precfock": "Fast",
                #                 "aldac":    1,
                #                 "aggac":    1,
                #                 "aggax":    0.75,
                #                 "lhfcalc":  True,
                #                 })
                #
                #         else:
                #             vasp_par.update_params({
                #                 "ibrion": 8,
                #                 })
                #     vasp_par.write_params(path=master_root_dir, overwrite=True)
                #     #__|
                #
                #     prev_files = [
                #         ["init.POSCAR", "init.POSCAR"],
                #         ".READY"
                #         ]
                #
                #     file_list = [
                #         "dft-params.json",
                #         ["dir_models/model_2.py", "model.py"]
                #     ]
                #
                #     Jobs.restart_job(job_i, prev_files, file_list=file_list)
                #__|
                """

            #__|

        print(tally)
    print("")
    #__|


#| - Reinitiating the Jobs Instances
# print("")  #PERM_PRINT
# print("Reinitiating the Jobs Instances")  #PERM_PRINT
# Jobs_Inst_list = []
# for step in range(len(step_dir_names)):
#     step_num = step + 1
#
#     # print("Initializing Job Instance: " + str(step_num))
#     Jobs = DFT_Jobs_Analysis(
#         system="aws",
#         tree_level=tree_level_labels_list[step],
#         level_entries=level_entries_dict_list[step],
#         working_dir=master_root_dir + "/" + step_dir_names[step],
#         load_dataframe=False,
#         )
#
#     Jobs_Inst_list.append(Jobs)
#__|


#__| ***************************************************************************
