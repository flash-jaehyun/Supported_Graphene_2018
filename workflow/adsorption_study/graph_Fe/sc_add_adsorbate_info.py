"""Add adsorbate info to atoms.info["adsorbates"]."""

#| - IMPORT MODULES
import shutil

# import sys
import copy
# import traceback

import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None

import plotly
from plotly.graph_objs import Figure

# My Modules ******************************************************************

from dft_job_automat.job_analysis import DFT_Jobs_Analysis
from dft_job_automat.job_types_classes.dft_methods import DFT_Methods

from orr_reaction.orr_methods import ORR_Free_E_Plot, calc_ads_e
#__|

#| - METHODS
def adsorbate_index_list(atoms, adsorbate_atoms_list=["O", "H"]):
    """
    """
    #| - adsorbate_index_list
    # NOTE This only works when there is no other adsorbate atom type
    # already in the atoms object.
    ads_atom_ind_list = []
    for atom in atoms:
        if atom.symbol in adsorbate_atoms:
            ads_atom_ind_list.append(atom.index)

    return(ads_atom_ind_list)
    #__|


#__|

#| - Initiate Instance
dft_inst = DFT_Methods(
    methods_to_run=[
        "elec_energy",
        "atom_type_num_dict",
        "init_atoms",
        "atoms_object",
        ],
    )

Jobs = DFT_Jobs_Analysis(
    update_job_state=False,
    job_type_class=dft_inst,
    load_dataframe=True,
    working_dir="1STEP",
    )

df = Jobs.filter_early_revisions(Jobs.data_frame)

# from dft_job_automat.job_types_classes.data_frame_methods import \
#     DataFrame_Methods
# DF = DataFrame_Methods(df)
# DF.create_atoms_objects(atoms_row="atoms_object")
#__|

#| - Data Processing
for index, row in df.iterrows():
    path_i = Jobs.root_dir + "/" + row["path"] + "_" + str(row["revision_number"])
    print(path_i)

    #| - Atoms Object
    try:
        atoms = row["atoms_object"][-1]

    except TypeError:
        print("No atoms object here!!!!!!!!!!!!!!!!!!!")
        continue
    #__|

    adsorbate_type = row["adsorbate"]
    adsorbate_atoms = ["O", "H"]

    ads_atom_ind_list = adsorbate_index_list(
        atoms,
        adsorbate_atoms_list=adsorbate_atoms,
        )

    print(ads_atom_ind_list)

    atoms.info["adsorbates"] = ads_atom_ind_list

    atoms.write("new.traj")
    shutil.move("./new.traj", path_i)

    import sys; sys.exit()
#__|
