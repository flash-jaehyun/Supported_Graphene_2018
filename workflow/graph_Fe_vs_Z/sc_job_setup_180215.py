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
from ase.io.trajectory import Trajectory
# from ase.io.trajectory import write_traj

# from ase_modules.dft_params import VASP_Params

# My Modules

from ase_modules.ase_methods import highest_position_of_element, move_atoms_of_element_i
from ase_modules.adsorbates import Adsorbate

from ase_modules.add_adsorbate import add_adsorbate_centered

from dft_job_automat.job_setup import DFT_Jobs_Setup
from dft_job_automat.job_analysis import DFT_Jobs_Analysis
from dft_job_automat.job_manager import DFT_Jobs_Manager
import dft_job_automat.job_dependencies as jd

# from aws.aws_class import AWS_Queues
# from raman_dft import vasp_raman_job_methods as VR_meth
# from misc_modules.misc_methods import even_spaced_range
#__|

os.environ["COMPENV"] = "aws"

#| - FUNCTIONS
def create_atoms_list(atoms_name, file_ext, root_dir):
    """
    """
    #| - create_atoms_list
    atoms_dict = {}
    for atom in atoms_name:

        # atoms_i = Trajectory(root_dir + "/dir_atoms/" + atom + file_ext)
        # traj.set_description({"author": "Created by Raul Flores"})

        atoms_i = io.read(root_dir + "/dir_atoms/" + atom + file_ext)

        atoms_dict[atom] = atoms_i

    return(atoms_dict)
    #__|

#__|

#| - Script Parameters

#| - Atoms Object
print("Atoms Object")

atoms_prefix = ".traj"
atoms_list_names = ["init"]
atoms_dict = create_atoms_list(atoms_list_names, atoms_prefix, os.getcwd())
#__|

tree_level_labels = [
    "Z-spacing",
    ]

z_list = np.linspace(0.5, 6.5, num=40).tolist()

tree_level_values = [
    z_list,
    ]

run_jobs = False  # Set to "False" to create directory structure only
run_trisync = False
#__|

#| - MISC Parameters
mod_dir = "dir_models"
atoms_dir = "dir_atoms"

step_dir_names = ["1STEP"]
model_sc_names = ["model.py"]
#__|

#| - Under the  Hood ***********************************************************

#| - Root Directory
master_root_dir = os.getcwd()
root_dir_lst_full = master_root_dir.split("/")

# index = root_dir_lst_full.index("vasp")
# root_dir_beg = "/".join(root_dir_lst_full[0:index])
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

#| - Initializing Job Instances
print("Initializing Job Instance:")  #PERM_PRINT

dir_struct_file = master_root_dir + "/jobs_bin/dir_structure.json"

JobsAn = DFT_Jobs_Analysis(
    system="aws",
    tree_level=tree_level_labels,
    level_entries=tree_level_values,
    working_dir=master_root_dir,
    update_job_state=False,
    load_dataframe=True,
    )
#__|


#| - Placing Initial Files in Folders | LOOP OVER JOBS ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
print("Placing Initial Files in Folders | LOOP OVER JOBS")  #PERM_PRINT
files_placed_file = master_root_dir + "/.FILES_PLACED"

if not os.path.isfile(files_placed_file):

    #| - Create Step Folder Structure
    if not os.path.exists(master_root_dir + "/.FOLDERS_CREATED"):
        JobsAn.create_dir_struct(create_first_rev_folder="True")

        # aws_dir = os.environ["aws_dir"]
        # trysync_comm = aws_dir + "/matr.io/bin/trisync"
        # subprocess.call(trysync_comm)
        # print("")  #PERM_PRINT
    #__|

    for job_i in JobsAn.job_var_lst:
        path_i = JobsAn.var_lst_to_path(job_i, job_rev="Auto", relative_path=False)

        #| - Copying Model Scripts
        model_dir = master_root_dir + "/" + mod_dir + "/" + model_sc_names[0]
        shutil.copyfile(model_dir, path_i + "/model.py")
        #__|

        #| - Job_i Parameters
        job_i_params = {}
        for variable in JobsAn.tree_level_labels:
            job_i_params[variable] = JobsAn.extract_prop_from_var_lst(job_i, variable)
        #__|

        #| - Atoms Object
        atoms = atoms_dict[atoms_list_names[0]]
        atoms_i = copy.deepcopy(atoms)

        z_space = job_i_params["Z-spacing"]
        surface_z_coord = highest_position_of_element(atoms_i, "Fe")

        new_coord = surface_z_coord + z_space
        # print(new_coord)

        atoms_i = move_atoms_of_element_i(atoms_i, "C", new_coord)

        io.write("init.traj", atoms_i)

        shutil.move(master_root_dir + "/init.traj", path_i)
        #__|


    file = open(master_root_dir + "/.FILES_PLACED", "w")
file = open(master_root_dir + "/.FOLDERS_CREATED", "w")
#__|


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
            print(path_i)

            #| - READY  | Not SUBMITTED
            if Jobs.job_ready(job_i):
                print("SUBMITTING" + " | " + path_i)  #PERM_PRINT

                Jobs.submit_job(
                    path_i=path_i,
                    queue="large",
                    cpus=8,
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
                #
                # if step_num == 1:
                #     jd.copyfiles_onestep_up(job_i, step_num, Jobs_Inst_list,
                #         files_lst=[
                #             ["CONTCAR", "init.POSCAR"],
                #             # ".READY",
                #             ],
                #         root_dir_files=[".READY"]
                #         )
                #
                # elif step_num == 2:
                #     jd.copyfiles_onestep_up(job_i, step_num, Jobs_Inst_list,
                #         files_lst=[
                #             ["OUTCAR", "OUTCAR.phon"],
                #             ["POSCAR", "POSCAR.phon"],
                #             ],
                #         root_dir_files=[".READY"],
                #
                #         )
                #
                # elif step_num == 3:
                #     pass

            else:
                pass
            #__|

            #| - FAILED | Rerun Job
            if Jobs.job_failed(job_i):
                print("FAILURE" + " | " + path_i)  #PERM_PRINT
                tally["failures"] += 1
                #
                # #| - Step 1 Restart
                # prev_files = [
                #     ["CONTCAR", "init.POSCAR"],
                #     "model.py",
                #     "dft-params.json",
                #     # ".READY",
                #     ]
                #
                # sub_params = {
                #     "path_i": path_i,
                #     "queue": "large",
                #     "cpus": 48,
                #     }
                #
                # file_list = [
                #     ".READY",
                #     ]
                #
                # # Jobs.restart_job(
                # #     job_i,
                # #     prev_files,
                # #     sub_params=sub_params,
                # #     # source_rev=1,
                # #     )
                # #__|
                #
                # #| - Step 2 Restart | TEMP
                # # if step_num == 2:
                # #     print("Restarting step 2 job")
                # #
                # #     #| - Job_i Parameters
                # #     job_i_params = {}
                # #     for variable in Jobs.tree_level_labels:
                # #         job_i_params[variable] = Jobs.extract_prop_from_var_lst(job_i, variable)
                # #     #__|
                # #
                # #     #| - VASP Parameters
                # #     vasp_par = VASP_Params(load_defaults=True)
                # #
                # #     var = "force-cutoff"
                # #     if var in job_i_params:
                # #         vasp_par.update_params({"ediffg": job_i_params[var]})
                # #
                # #     var = "pw-cutoff"
                # #     if var in job_i_params:
                # #         vasp_par.update_params({"encut": job_i_params[var]})
                # #
                # #     var = "dft-functionals"
                # #     if var in job_i_params:
                # #         functional = job_i_params["dft-functionals"]
                # #         if functional == "hse06":
                # #             vasp_par.update_params({
                # #                 "algo":     "All",
                # #                 "time":     0.5,
                # #
                # #                 "ibrion": 6,
                # #
                # #                 "hfscreen": 0.2,
                # #                 "aexx":     0.25,
                # #                 "precfock": "Fast",
                # #                 "aldac":    1,
                # #                 "aggac":    1,
                # #                 "aggax":    0.75,
                # #                 "lhfcalc":  True,
                # #                 })
                # #
                # #         else:
                # #             vasp_par.update_params({
                # #                 "ibrion": 8,
                # #                 })
                # #     vasp_par.write_params(path=master_root_dir, overwrite=True)
                # #     #__|
                # #
                # #     prev_files = [
                # #         ["init.POSCAR", "init.POSCAR"],
                # #         ".READY"
                # #         ]
                # #
                # #     file_list = [
                # #         "dft-params.json",
                # #         ["dir_models/model_2.py", "model.py"]
                # #     ]
                # #
                # #     Jobs.restart_job(job_i, prev_files, file_list=file_list)
                # #__|
                #
                # #| - Step 3 Restart
                # if step_num == 3:
                #     prev_files = [
                #         # "3_vasp_raman_run_ibrion_n1.py",
                #         "model.py",
                #         "param_vasp_raman",
                #         "dft-params.json",
                #         "OUTCAR.phon",
                #         "POSCAR.phon",
                #         ]
                #
                #     sub_params = {
                #         "path_i": path_i,
                #         "queue": "small",
                #         "cpus": 4,
                #         }
                #
                #     file_list = [
                #         ".READY",
                #         ["dir_models/3_vasp_raman_run_ibrion_n1.py", "3_vasp_raman_run_ibrion_n1.py"]
                #         ]
                #
                #     Jobs.restart_job(
                #         job_i,
                #         prev_files,
                #         sub_params=sub_params,
                #         file_list=file_list,
                #         root_dir=master_root_dir,
                #         from_simulation_folder=False,
                #         source_rev=1,
                #         )
                #
                #     # sys.exit(0)
                #
                # #__|

            #__|


        print(tally)
    print("")
    #__|


#| - Reinitiating the Jobs Instances
print("")  #PERM_PRINT
print("Reinitiating the Jobs Instances")  #PERM_PRINT
Jobs_Inst_list = []
for step in range(len(step_dir_names)):
    step_num = step + 1

    # print("Initializing Job Instance: " + str(step_num))
    Jobs = DFT_Jobs_Analysis(
        system="aws",
        tree_level=tree_level_labels_list[step],
        level_entries=level_entries_dict_list[step],
        working_dir=master_root_dir + "/" + step_dir_names[step],
        load_dataframe=False,
        )

    Jobs_Inst_list.append(Jobs)
#__|


# __| ***************************************************************************
