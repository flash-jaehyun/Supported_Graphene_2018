#!/usr/bin/env python

"""Preprocess data from various sources.

Author: Raul A. Flores
"""

#| - Import Modules
import pickle
import pandas as pd

# My Modules **********************************************************
from dft_job_automat.job_analysis import DFT_Jobs_Analysis
from orr_reaction.orr_methods import df_calc_adsorption_e
from energetics.dft_energy import Element_Refs
#__|

#| - Script Inputs
# bias = 0.  # Not used

# Bare Fe
bare_slab_False = -30772.862053560006
bare_slab_True = -30774.394355700322
bare_slab_dict_Fe = {True: bare_slab_True, False: bare_slab_False}

# Bare Graphene
bare_slab_False = -947.9120007283367
bare_slab_True = -947.9121850854704
bare_slab_dict_Graphene = {True: bare_slab_True, False: bare_slab_False}

# Fe-supported Graphene
bare_slab_True = -31722.43520417364
bare_slab_False = -31721.412152900266
bare_slab_dict_Fe_Graph = {True: bare_slab_True, False: bare_slab_False}

# Fe-supported N-Graphene
# /scratch/users/flores12/03_graph_N_Fe/01_opt_struct/N_doped_graph_Fe/no_spin/01_N_trifold/_4
# N in trifold site
bare_slab_NGraph_Fe = -31839.06523325643

# C in trifold site
tmp = -31838.6148526

Refs = Element_Refs()
oxy_ref = Refs.E_O_ref.gibbs_e
hyd_ref = Refs.E_H_ref.gibbs_e

fe_corr_dict = {
    "h2o": 0.528688009,
    "o": 0.068715186,
    "oh": 0.265727434,
    "ooh": 0.351189818,
    }

dir_list = ["Fe_slab", "graphene", "graph_Fe", "N_graph_Fe"]

sys_dict = [
    {"folder": "Fe_slab", "bare_ref": bare_slab_dict_Fe},
    {"folder": "graphene", "bare_ref": bare_slab_dict_Graphene},
    {"folder": "graph_Fe", "bare_ref": bare_slab_dict_Fe_Graph},
    {"folder": "N_graph_Fe", "bare_ref": bare_slab_NGraph_Fe},
    ]
#__|

def load_df(
    from_file=True,

    file_name="df_master.pickle",
    ):
    """

    Args:
        from_file:
    """
    #| - load_df
    if from_file:

        #| - From Saved Pickle File
        print("Attempting to load df from pickle")
        with open(file_name, "rb") as fle:
            df_master = pickle.load(fle)
        return(df_master)
        #__|

    else:

        #| - Process Data Frame

        #| - Process Dataframe
        df_sys = pd.DataFrame(sys_dict)

        df_list = []
        Jobs_list = []
        for index, row in df_sys.iterrows():
            folder_name = row["folder"]

            Jobs = DFT_Jobs_Analysis(
                update_job_state=False,
                job_type_class=None,
                load_dataframe=True,
                working_dir=folder_name + "/1STEP",
                )

            tree_level_labels = Jobs.tree_level_labels

            df = Jobs.filter_early_revisions(Jobs.data_frame)

            if folder_name == "N_graph_Fe":
                df_calc_adsorption_e(
                    df,
                    oxy_ref,
                    hyd_ref,
                    row["bare_ref"],
                    bare_slab_var="spinpol",
                    )
            else:
                df_calc_adsorption_e(
                    df,
                    oxy_ref,
                    hyd_ref,
                    row["bare_ref"],
                    bare_slab_var="spinpol",
                    corrections_mode="corr_dict",
                    corrections_dict=fe_corr_dict,
                    )

            df["system"] = folder_name

            # tmp = [tree_level_labels for i in range(len(df))]
            df["tree_level_labels"] = [tree_level_labels for i in range(len(df))]

            # Jobs.df = df
            # Jobs_list.append(Jobs)
            df_list.append(df)

        df_master = pd.concat(df_list)
        df_master.reset_index(drop=True, inplace=True)

        if "NA" in list(df_master):
            df_master.drop("NA", axis=1, inplace=True)
        #__|

        #| - Saving Dataframe to Pickle

        with open(file_name, "wb") as fle:
            pickle.dump(df_master, fle)
        #__|

        return(df_master)
    #__|

    #__|
