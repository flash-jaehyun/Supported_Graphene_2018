"""ORR adsorption on graphene.

TEMP TEMP TEMP

Author: Raul A. Flores
"""

#| - Import Modules
import os
import shutil

from ase import io
from ase.visualize import view
from ase.build import add_adsorbate

from ase_modules.dft_params import DFT_Params

# My Modules
from ase_modules.dft_params import Espresso_Params
from ase_modules.adsorbates import Adsorbate
from dft_job_automat.job_dependencies import DFT_Jobs_Workflow

from ase_modules.ase_methods import find_diff_between_atoms_objects
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


    # print(atoms_list_names)
    # print(atoms_ext)
    # print(atoms_dir)


    #| - Copying Model Scripts
    model_dir = master_root_dir + "/" + mod_dir + "/" + model_names[step_i]
    shutil.copyfile(model_dir, path_i + "/model.py")
    #__|

    #| - DFT Parameters
    dft_par = Espresso_Params(load_defaults=True)
    dft_par.load_params(dir=master_root_dir)

    var = "spinpol"
    if var in job_i_params:
        dft_par.update_params({"spinpol": job_i_params[var]})

    dft_par.write_params(path_i=path_i, overwrite=True)
    #__|

    #| - Atoms Object
    ads_i = job_i_params["adsorbate"]
    site_i = job_i_params["site"]

    site_coords_dict = {
        "ontop":        [2.481, 0.614, 1.45],
        "bridged":      [3.181, 0.614, 1.45],
        "ring-center":  [3.181, 1.814, 1.15],
        }

    Ads = Adsorbate()
    ads = Ads.get_adsorbate(ads_i)

    print(job_i_params)

    if job_i_params["spinpol"] is False:
        ind_atoms_list = 0

    elif job_i_params["spinpol"] is True:
        ind_atoms_list = 1

    # dft_par.params["spinpol"]

    atoms_file = atoms_list_names[ind_atoms_list] + atoms_ext
    slab = io.read(master_root_dir + "/" + atoms_dir + "/" + atoms_file)


    z_space = site_coords_dict[site_i][2]
    slab_before_adsorbate = slab.copy()

# slab, adsorbate, ads_height, position=ads_pos
    add_adsorbate(slab, ads, z_space, position=site_coords_dict[site_i][0:2])

    tmp1, tmp2 = find_diff_between_atoms_objects(slab_before_adsorbate, slab)
    slab.info["adsorbates"] = tmp2

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
        print("SUBMITTING" + " | " + path_i)

        Jobs.submit_job(
            path_i      = path_i,
            wall_time   = "1000",
            queue       = "iric",
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
                "init.traj",
                "model.py",
                ".READY",
                ]

            sub_params = {
                "wall_time": "1400"
                }

            # Jobs.restart_job(job_i, prev_files, sub_params=sub_params)
        #__|

    #__|

    return(tally)
    #__|

#__|

#| - Script Parameters

#| - Parameters
atoms_prefix = ".traj"
atoms_list_names = ["01_false", "02_true"]

tree_level_labels = [
    "adsorbate",
    "site",
    "spinpol"
    ]

adsorbates = [
    "ooh",
    "o",
    "oh",
    "h2o",
    ]

sites = [
    "ontop",
    "bridged",
    "ring-center",
    ]

tree_level_values = [
    adsorbates,
    sites,
    [True, False],
    ]

tree_level_labels_list = [tree_level_labels]
level_entries_dict_list = [tree_level_values]
#__|

#| - Script Behavior Flags
run_jobs = True  # Set to "False" to create directory structure only
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
