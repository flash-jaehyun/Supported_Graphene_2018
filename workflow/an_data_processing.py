#!/usr/bin/env python

"""Preprocess data for supported graphene project.

Author: Raul A. Flores
"""

#| - Import Modules
import os
import sys

sys.path.insert(
    0,
    os.path.join(
        os.environ["PROJ_fe_graph"],
        "data",
        ),
    )

import pickle

import numpy as np

import pandas as pd
pd.set_option("display.max_columns", None)
pd.set_option('display.max_rows', None)

# My Modules **********************************************************
from misc_modules.pandas_methods import reorder_df_columns

from dft_job_automat.job_analysis import DFT_Jobs_Analysis
from orr_reaction.orr_methods import df_calc_adsorption_e
from energetics.dft_energy import Element_Refs

from proj_data_fe_graph import (
    bare_slab_dict_Fe,
    bare_slab_dict_Graphene,
    bare_slab_dict_Fe_Graph,
    bare_slab_NGraph_Fe,
    bare_slab_dict_NGraph,
    fe_corr_dict,
    )
#__|

data_pre_dir = os.path.join(
    os.environ["norskov_research"],
    "04_comp_clusters/02_DATA/01_fe_graph_proj/adsorption_study",
    )

#| - Script Inputs

#| - Energetics
Refs = Element_Refs()
oxy_ref = Refs.E_O_ref.gibbs_e
hyd_ref = Refs.E_H_ref.gibbs_e

#__|

# dir_list = ["Fe_slab", "graphene", "graph_Fe", "N_graph_Fe"]

sys_dict = [
    {
        "folder": "Fe_slab",
        "bare_ref": bare_slab_dict_Fe,
        "df_dir": data_pre_dir + "/Fe_slab",
        },

    {
        "folder": "graphene",
        "bare_ref": bare_slab_dict_Graphene,
        "df_dir": data_pre_dir + "/graphene",
        },

    {
        "folder": "graph_Fe",
        "bare_ref": bare_slab_dict_Fe_Graph,
        "df_dir": data_pre_dir + "/graph_Fe",
        },

    {
        "folder": "N_graph_Fe",
        "bare_ref": bare_slab_NGraph_Fe,
        "df_dir": data_pre_dir + "/N_graph_Fe",
        },

    {
        "folder": "N_graph",
        "bare_ref": bare_slab_dict_NGraph,
        "df_dir": data_pre_dir + "/N_graph",
        },
    ]
#__|

def load_df(
    from_file=True,
    root_dir=".",
    data_dir=data_pre_dir,
    file_name="df_master.pickle",
    filter_columns=None,
    save_df=False,
    ):
    """Load dataframe and perform some preprocessing.

    Args:
        from_file:
    """
    #| - load_df

    if from_file:

        #| - From Saved Pickle File
        print("Attempting to load df from pickle")

        file_path = os.path.join(data_dir, file_name)
        with open(file_path, "rb") as fle:
            df_master = pickle.load(fle)

        return(df_master)
        #__|

    else:

        #| - Process Data Frame

        #| - Process Dataframe

        #| - Collecting Jobs instances from different locations
        df_sys = pd.DataFrame(sys_dict)

        df_list = []
        for index, row in df_sys.iterrows():
            folder_name = row["folder"]

            Jobs = DFT_Jobs_Analysis(
                update_job_state=False,
                job_type_class=None,
                load_dataframe=True,
                working_dir=root_dir + "/" + folder_name + "/1STEP",
                dataframe_dir=row["df_dir"],
                )

            tree_level_labs = Jobs.tree_level_labels

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

            df["tree_level_labels"] = [tree_level_labs for i in range(len(df))]
            df_list.append(df)

        df_master = pd.concat(df_list)
        df_master.reset_index(drop=True, inplace=True)
        #__|

        #| - TEMP | Dropping N-graph C-C bridged dat
        # The jobs were never run because of a space in variable parameter
        # that resulted in a space in the path.

        df_ngraph_ccbridged = df_master[
            (df_master["system"] == "N_graph") &
            (df_master["site"] == "C-C bridged")
            # (df_m[""] == "") & \
            ]

        index_list = list(df_ngraph_ccbridged.index.values)

        df_master.drop(index_list, inplace=True)
        #__|

        # Removing 'NA' for some reason
        if "NA" in list(df_master):
            df_master.drop("NA", axis=1, inplace=True)

        # Adding spinpol=False for N_graph_Fe data
        df_master.loc[df_master["system"] == "N_graph_Fe", "spinpol"] = False

        # Changing NAN values for 'graph_site' column to a string literal 'nan'
        df_master.loc[df_master["graph_site"].isnull(), "graph_site"] = "nan"

        #| - Removing Certain Columns
        if filter_columns is not None:
            all_columns = set(list(df_master))

            exclude_columns = set(filter_columns)
            columns_to_keep = list(all_columns - exclude_columns)

            df_master = df_master[columns_to_keep]
        #__|

        #| - Adding Additional Columns
        df_master["authors"] = "flores_norskov"
        df_master["author_short"] = "norskov"
        #__|

        #| - Ordering Columns

        col_order_list = [
            'system',
            'adsorbate',
            'site',
            'final_site',
            'spinpol',
            'graph_site',
            'ads_e',
            'gibbs_correction',
            'elec_energy',
            'notes_processed',
            'author_short',
            'path',
            'notes',
            'atom_type_num_dict',

            # Low priority
            'variable_list',
            'full_path',
            'authors',
            'Job',
            'atoms_object',
            'init_atoms',
            'tree_level_labels',
            'revision_number',
            'max_revision',

            ]

        # TEMP | Made df_reorder into a method
        df_master = reorder_df_columns(col_order_list, df_master)

        #| - __old__
        # col_order_list = [
        #     "system",
        #     "adsorbate",
        #     "site",
        #     "final_site",
        #     "spinpol",
        #     "graph_site",
        #
        #     "ads_e",
        #     "gibbs_correction",
        #     "elec_energy",
        #
        #     "path",
        #     "full_path",
        #
        #     "notes",
        #     "variable_list",
        #     "atom_type_num_dict",
        #     "tree_level_labels",
        #
        #     "revision_number",
        #     "max_revision",
        #
        #     "init_atoms",
        #     "atoms_object",
        #
        #     "Job",
        #     ]
        #
        # col_order_list.reverse()
        #
        # df_col_list = list(df_master)
        # for col_i in col_order_list:
        #     df_col_list.remove(col_i)
        #
        #     df_col_list.insert(0, col_i)
        #
        # df_master = df_master[df_col_list]
        #__|

        #__|


        #| - Processing 'notes' column
        df_master["notes_processed"] = df_master["notes"]
        df_master.loc[df_master["notes"] == "", "notes_processed"] = np.nan

        def parse_notes(row_i):
            """
            """
            #| - get_sum_force
            assert "notes" in list(row_i.keys()), "skjfksddf"
            assert "notes_processed" in list(row_i.keys()), "skjfksddf_2"

            if row_i["notes_processed"] is not np.nan:
                if "Reconfig" in row_i["notes_processed"]:
                    out = "reconfigured"
                else:
                    out = row_i["notes_processed"]
            else:
                out = row_i["notes_processed"]

            return(out)
            #__|

        df_master["notes_processed_tmp"] = df_master.apply(
            parse_notes,
            axis=1,
            )

        df_master["notes_processed"] = df_master["notes_processed_tmp"]

        # Dropping temporary column
        if "notes_processed_tmp" in list(df_master.columns):
            df_master.drop(labels=["notes_processed_tmp"], axis=1)


        #__|

        #| - Saving Dataframe to Pickle
        if save_df:
            with open(data_dir + "/" + file_name, "wb") as fle:
                pickle.dump(df_master, fle)
        #__|

        return(df_master)

        #__|

    #__|

    #__|


def load_vegge_data(
    ads_e_mode="w_solvent_correction",

    ):
    """Load Tejs Vegge supported graphene DFT data.

    # from_file=True,
    # root_dir=".",
    # data_dir=data_pre_dir,
    # file_name="df_master.pickle",
    # filter_columns=None,
    # save_df=False,

    Args:
        ads_e_mode:
            'w_solvent_correction'
                    or
            'wo_solvent_correction'

    """
    #| - load_vegge_data
    from proj_data_fe_graph import (
        vegge_paper,
        oh_solv_corr_ave,
        ooh_solv_corr_ave,
        o_solv_corr_ave,
        )

    df_vegge = pd.DataFrame(vegge_paper)

    df_vegge["authors"] = "reda_hansen_vegge"
    df_vegge["author_short"] = "vegge"

    dg_ads_o_2_list = []
    dg_ads_oh_2_list = []
    dg_ads_ooh_2_list = []
    for i_cnt, row_i in df_vegge.iterrows():
        dg_ads_o_2_list.append(row_i["dg_ads_o"] - o_solv_corr_ave)
        dg_ads_oh_2_list.append(row_i["dg_ads_oh"] - oh_solv_corr_ave)
        dg_ads_ooh_2_list.append(row_i["dg_ads_ooh"] - ooh_solv_corr_ave)

    df_vegge["dg_ads_o_2"] = dg_ads_o_2_list
    df_vegge["dg_ads_oh_2"] = dg_ads_oh_2_list
    df_vegge["dg_ads_ooh_2"] = dg_ads_ooh_2_list

    #| - Expanding the Dataframe so that each adsorbate has its' own row

    if ads_e_mode == "w_solvent_correction":
        ads_e_keys = {
            "o": "dg_ads_o",
            "oh": "dg_ads_oh",
            "ooh": "dg_ads_ooh",
            }

    elif ads_e_mode == "wo_solvent_correction":
        ads_e_keys = {
            "o": "dg_ads_o_2",
            "oh": "dg_ads_oh_2",
            "ooh": "dg_ads_ooh_2",
            }

    data_frame_list = []
    for i_cnt, row_i in df_vegge.iterrows():

        df_list_i = [
            {
                "adsorbate": "o",
                "ads_e": row_i[ads_e_keys["o"]],
                },

            {
                "adsorbate": "oh",
                "ads_e": row_i[ads_e_keys["oh"]],
                },

            {
                "adsorbate": "ooh",
                "ads_e": row_i[ads_e_keys["ooh"]],
                },

            ]

        for row_j in df_list_i:
            for key_k, value_k in row_i.iteritems():

                if key_k == ads_e_keys["o"]:
                    continue
                elif key_k == ads_e_keys["oh"]:
                    continue
                elif key_k == ads_e_keys["ooh"]:
                    continue

                row_j[key_k] = value_k

        df_i = pd.DataFrame(df_list_i)
        data_frame_list.append(df_i)

    df_vegge_new = pd.concat(data_frame_list)

    df_vegge = df_vegge_new
    #__|

    # I hate how pandas handles NaN, just replace with string
    df_vegge = df_vegge.replace(np.nan, 'NaN', regex=True)

    return(df_vegge)
    #__|
