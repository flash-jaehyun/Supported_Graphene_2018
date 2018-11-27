"""Optimal translational configuratino of graphene on slab."""

#| - Import Modules
import os
import shutil
import itertools
import sys

from ase import io
from ase.visualize import view
from ase.build import add_adsorbate

# My Modules
from ase_modules.dft_params import Espresso_Params
from ase_modules.adsorbates import Adsorbate
from ase_modules.ase_methods import displace_overlayer

from dft_job_automat.job_dependencies import DFT_Jobs_Workflow
#__|

#| - Functions
def dir_setup(step_i, path_i, job_i_params, wf_vars):
    """
    Inputs:
        Everything needed to specify a job completely
        path_i,
        job_i_params,
    """
    #| - dir_setup
    from ase import io
    from ase_modules.adsorbates import Adsorbate

    #| - Parsing wf_vars
    master_root_dir = wf_vars["root_dir"]
    mod_dir = wf_vars["mod_dir"]
    model_names = wf_vars["model_names"]
    JobsAn = wf_vars["jobs_an_list"][step_i]
    atoms_list_names = wf_vars["atoms_list_names"]
    atoms_ext = wf_vars["atoms_ext"]
    atoms_dir = wf_vars["atoms_dir"]
    #__|

    #| - Copying Model Scripts
    model_dir = master_root_dir + "/" + mod_dir + "/" + model_names[step_i]
    shutil.copyfile(model_dir, path_i + "/model.py")
    #__|

    #| - DFT Parameters
    shutil.copy(master_root_dir + "/dft-params.json", path_i)
    #__|

    #| - Atoms Object
    x_size = len(JobsAn.level_entries["x_coord"])
    y_size = len(JobsAn.level_entries["y_coord"])

    x_coord = job_i_params["x_coord"]
    y_coord = job_i_params["y_coord"]

    atoms_file = atoms_list_names[step_i] + atoms_ext
    slab = io.read(master_root_dir + "/" + atoms_dir + "/" + atoms_file)
    slab = displace_overlayer(slab, x_coord, y_coord, x_size, y_size, save_file=True)

    slab.write(path_i + "/init.traj")
    #__|

    #| - Writing Ready File for First Step
    if step_i == 0:
        file = open(path_i + "/.READY", "w")
    #__|

    #__|

def job_maint(step_i, job_i, job_i_params, wf_vars, tally):
    """
    """
    #| - job_maint
    # tally = {"successes": 0, "failures": 0, "running": 0, "pending": 0}

    #| - Parsing wf_vars
    master_root_dir = wf_vars["root_dir"]
    mod_dir = wf_vars["mod_dir"]
    model_names = wf_vars["model_names"]
    Jobs = wf_vars["jobs_man_list"][step_i]
    atoms_list_names = wf_vars["atoms_list_names"]
    atoms_ext = wf_vars["atoms_ext"]
    atoms_dir = wf_vars["atoms_dir"]
    #__|

    path_i = Jobs.var_lst_to_path(job_i, job_rev="Auto", relative_path=False)

    #| - READY  | Not SUBMITTED
    if Jobs.job_ready(job_i):
        print("SUBMITTING" + " | " + path_i)  #PERM_PRINT

        Jobs.submit_job(
            path_i      = path_i,
            wall_time   = "1500"
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
        """

    else:
        pass
    #__|

    #| - FAILED | Rerun Job
    if Jobs.job_failed(job_i):
        print("FAILURE" + " | " + path_i)  #PERM_PRINT
        tally["failures"] += 1

        #| - Step 1 Restart
        if step_i == 0:
            prev_files = [
                "dft-params.json",
                "out.traj",
                "model.py",
                ".READY",
                ]

            sub_params = {
                "wall_time": "2400"
                }

            # Jobs.restart_job(job_i, prev_files, sub_params=sub_params)
        #__|

    #__|

    return(tally)
    #__|

#__|

#| - Script Parameters
mesh_size = 10

# inputdata = [
#     [0, 1, 2, 3, 4, 5,],
#     [0, 1, 2, 3, 4, 5,],
#     ]
#
# comb = itertools.product(*inputdata)
#
# value_list = []
# for comb_i in comb:
#     entry_i = str(comb_i[0]).zfill(2) + "_" + str(comb_i[1]).zfill(2)
#     value_list.append(entry_i)


#| - Parameters
atoms_prefix = ".traj"
atoms_list_names = ["init"]

tree_level_labels = [
    "x_coord",
    "y_coord"
    ]

tree_level_values = [
    range(mesh_size),
    range(mesh_size),
    ]

tree_level_labels_list = [tree_level_labels]
level_entries_dict_list = [tree_level_values]
#__|

#| - Script Behavior Flags
run_jobs = True  # Set to "False" to create directory structure only
run_trisync = False
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

#__|

# print(WF.jobs_an_list[0].job_var_lst)
