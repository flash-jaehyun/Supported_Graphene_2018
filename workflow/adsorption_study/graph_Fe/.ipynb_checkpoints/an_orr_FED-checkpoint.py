"""Processing ORR Adsorption Energetics.


TEMP
"""

#| - IMPORT MODULES
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

#| - SCRIPT INPUTS

#| - Colors
color_list = [
    "rgb(37,69,0)",
    "rgb(0,76,214)",
    "rgb(168,0,15)",
    "rgb(0,85,162)",
    "rgb(255,113,196)",
    ]

color_list = [
    "rgb(113,166,190)",
    "rgb(145,209,79)",
    "rgb(124,78,196)",
    "rgb(203,169,87)",
    "rgb(200,72,150)",
    "rgb(130,204,159)",
    "rgb(190,82,63)",
    "rgb(80,51,82)",
    "rgb(81,92,54)",
    "rgb(192,151,188)",
    ]
#__|

#| - Free Energy Corrections
# COMBAK I'm doing it manually for now

fe_corr_dict = {
    "h2o": 0.,
    "ooh": 0.,
    # "o": 0.,
    "o": 0.01,
    # "oh": 0.,
    "oh": -0.25,
    }
#__|

run_an_0 = True
run_an_1 = True

ref_scheme = "h2o"  # o2 or h2o

bias = 0.
#__|

#| - Reference Energies

#| - Slab Energy
# /scratch/users/flores12/03_graph_N_Fe/01_opt_struct/
# combined-Fe-graph/FCC/5-att/1STEP/data/03-800/03-881/01-True/_1

# /scratch/users/flores12/03_graph_N_Fe/01_opt_struct/
#  combined-Fe-graph/FCC/5-att/1STEP/data/03-800/03-881/02-False/_1

bare_slab = -31722.43520417364
bare_slab_SP_t = -31722.43520417364
bare_slab_SP_f = -31721.412152900266

bare_slab_dict = {
    False: bare_slab_SP_f,
    True: bare_slab_SP_t,
    }
#__|

# R21 From Pourbaix Papers
dG_rxn_h2o = -2.4583

# /scratch/users/flores12/gas_phase_molec/BEEF-vdW
H2_dft = -32.9563981542851
O2_dft = -883.190570481887
H2O_dft = -476.544109028354

hyd_ref = H2_dft / 2.

if ref_scheme == "h2o":
    oxy_ref = H2O_dft - H2_dft
elif ref_scheme == "o2":
    oxy_ref = dG_rxn_h2o + O2_dft / 2.
#__|

#| - Initiate Instance
dft_inst = DFT_Methods(
    methods_to_run=[
        "elec_energy",
        "atom_type_num_dict",
        "init_atoms",
        "atoms_object",
        "magmom_charge_history",
        ],
    )

Jobs = DFT_Jobs_Analysis(
    update_job_state=False,
    job_type_class=dft_inst,
    load_dataframe=True,
    # load_dataframe=False,
    working_dir="1STEP",
    )

df = Jobs.filter_early_revisions(Jobs.data_frame)

# from dft_job_automat.job_types_classes.data_frame_methods import \
#     DataFrame_Methods
# DF = DataFrame_Methods(df)
# DF.create_atoms_objects(atoms_row="atoms_object")
#__|

#| - Data Processing

#| - Filtering Data
# tmp = df[np.isfinite(df["elec_energy"]) == True]
# tmp = df[np.isfinite(df["elec_energy"]) == True]
# # df = df[df["job_state"] == "SUCCEEDED"]
#
# finite_e_rows = np.isfinite(df["elec_energy"]) == True
# df = df[finite_e_rows]



# df = df[df["spinpol"] == True]
# df = df[df["notes"] != "Desorbed"]
#__|

#| - Removing Unnecessary Columns
col_to_remove = [
    "variable_list",
    "init_atoms",
    "atoms_object",
    ]

df = df.drop(col_to_remove, axis=1)
#__|

#| - Adsorption Energies
ads_e_list = []
for index, row in df.iterrows():

    corr = fe_corr_dict[row["adsorbate"]]
    bare_e = bare_slab_dict[row["spinpol"]]

    ads_e_i = calc_ads_e(
        row,
        # bare_slab,
        bare_e,
        correction=corr,
        oxy_ref_e=oxy_ref,
        hyd_ref_e=hyd_ref,
        )

    ads_e_list.append(ads_e_i)

df["ads_e"] = np.array(ads_e_list)
df_master = copy.deepcopy(df)
#__|

#__|

#| - Data Analysis

###############################################################################
# ######################## All Free Energy Pathways ###########################
###############################################################################
#| - All Free Energy Pathways
if run_an_0:

    #| - Grouping By Adsorbate Type
    groupby = copy.deepcopy(Jobs.tree_level_labels)
    groupby.remove("adsorbate")

    data_master = {}
    for group_i in df.groupby(groupby):

        data_master[group_i[0]] = group_i[1]
    #__|

    #| - Creating Data Sets

    #| - Creating FED Datasets
    data_list = []
    # for i_cnt, (key, fe_dict) in enumerate(data_master.iteritems()):
    for i_cnt, (key, fe_dict) in enumerate(data_master.items()):
        ORR = ORR_Free_E_Plot(
            free_energy_df=fe_dict,
            )

        dat_lst = ORR.plot_fed_series(
            bias=bias,
            properties=key,
            color_list=color_list,
            i_cnt=i_cnt,
            # hover_text_col="site"
            hover_text_col="notes",
            plot_mode="states_only",
            )

        data_list.extend(dat_lst)
    #__|

    #| - Creating Ideal FED Dataset
    e_list_ideal = ORR.apply_bias(bias, ORR.ideal_energy)

    dat_ideal = ORR.create_plotly_series(
        e_list_ideal,
        group="Ideal",
        name="Ideal",
        color="red",
        plot_mode="full_lines",
        )
    #__|

    dat_lst = data_list + dat_ideal
    #__|

    #| - Plotting

    #| - Plot Settings
    plot_title_size = 18
    tick_lab_size = 16
    axes_lab_size = 18
    legend_size = 12
    #__|

    #| - Plot Layout
    xax_labels = ["O2", "OOH", "O", "OH", "H2O"]
    layout = {

        "title": "FED of ORR Mechanism For Iron-Supported-Graphene",

        "font": {
            "family": "Courier New, monospace",
            "size": plot_title_size,
            "color": "black",
            },

        #| - Axes --------------------------------------------------------------
        "yaxis": {
            "title": "Free Energy [eV]",
            "zeroline": True,
            "titlefont": dict(size=axes_lab_size),
            "showgrid": False,
            "tickfont": dict(
                size=tick_lab_size,
                ),
            },

        "xaxis": {
            "title": "Reaction Coordinate",
            "zeroline": True,
            "titlefont": dict(size=axes_lab_size),
            "showgrid": False,

            # "showticklabels": False,

            "ticktext": xax_labels,
            "tickvals": [1.5 * i + 0.5 for i in range(len(xax_labels))],

            "tickfont": dict(
                size=tick_lab_size,
                ),
            },
        #__| -------------------------------------------------------------------

        #| - Legend ------------------------------------------------------------
        "legend": {
            "traceorder": "normal",
            "font": dict(size=legend_size)
            },
        #__| -------------------------------------------------------------------

        #| - Plot Size
        "width": 200 * 4.,
        "height": 200 * 3.,
        #__|

        }
    #__|

    fig = Figure(data=dat_lst, layout=layout)
    # plotly.plotly.image.save_as(fig, filename="pl_hab_opda_raman.png")

    plotly.offline.plot(
        {
            "data": dat_lst,
            "layout": layout,
            },
        filename="plots/pl_fed_supp_graph_01.html"
        )
    # tmp = plotly.plotly.image.plot(data, filename="pl_fed_180314.png")
    #__|

#__|

###############################################################################
# ####################### Lowest Free Energy Pathway ##########################
###############################################################################
#| - Lowest Free Energy Pathway
if run_an_1:

    #| - Grouping By Adsorbate Type
    df = copy.deepcopy(df_master)

    groupby = copy.deepcopy(Jobs.tree_level_labels)
    groupby.remove("site")
    groupby.remove("adsorbate")

    data_master = {}
    for group_i in df.groupby(groupby):
        series_list = []
        for ads_i in group_i[1].groupby("adsorbate"):

            min_e_row = ads_i[1].loc[ads_i[1]["ads_e"].idxmin()]
            series_list.append(min_e_row)

        df_i = pd.DataFrame.from_items([(s.name, s) for s in series_list]).T
        data_master[group_i[0]] = df_i
    #__|

    #| - Creating Data Sets

    #| - Creating FED Datasets
    data_list = []
    # for i_cnt, (key, fe_dict) in enumerate(data_master.iteritems()):
    for i_cnt, (key, fe_dict) in enumerate(data_master.items()):
        ORR = ORR_Free_E_Plot(
            free_energy_df=fe_dict,
            )

        dat_lst = ORR.plot_fed_series(
            bias=bias,
            properties=key,
            color_list=color_list,
            i_cnt=i_cnt,
            hover_text_col="site"
            )

        data_list.extend(dat_lst)
    #__|

    #| - Creating Ideal FED Dataset
    e_list_ideal = ORR.apply_bias(bias, ORR.ideal_energy)

    dat_ideal = ORR.create_plotly_series(
        e_list_ideal,
        group="Ideal",
        name="Ideal",
        color=color_list[-1],
        plot_mode="full_lines",
        )
    #__|

    dat_lst = data_list + dat_ideal
    #__|

    #| - Plotting

    #| - Plot Settings
    plot_title_size = 18
    tick_lab_size = 16
    axes_lab_size = 18
    legend_size = 18
    #__|

    #| - Plot Layout
    xax_labels = ["O2", "OOH", "O", "OH", "H2O"]
    layout = {

        "title": "FED of ORR Mechanism For Iron-Supported-Graphene",

        "font": {
            "family": "Courier New, monospace",
            "size": plot_title_size,
            "color": "black",
            },

        #| - Axes --------------------------------------------------------------
        "yaxis": {
            "title": "Free Energy [eV]",
            "zeroline": True,
            "titlefont": dict(size=axes_lab_size),
            "showgrid": False,
            "tickfont": dict(
                size=tick_lab_size,
                ),
            },

        "xaxis": {
            "title": "Reaction Coordinate",
            "zeroline": True,
            "titlefont": dict(size=axes_lab_size),
            "showgrid": False,

            # "showticklabels": False,

            "ticktext": xax_labels,
            "tickvals": [1.5 * i + 0.5 for i in range(len(xax_labels))],

            "tickfont": dict(
                size=tick_lab_size,
                ),
            },
        #__| -------------------------------------------------------------------

        #| - Legend ------------------------------------------------------------
        "legend": {
            "traceorder": "normal",
            "font": dict(size=legend_size)
            },
        #__| -------------------------------------------------------------------

        #| - Plot Size
        "width": 200 * 4.,
        "height": 200 * 3.,
        #__|

        }
    #__|

    fig = Figure(data=dat_lst, layout=layout)
    # plotly.plotly.image.save_as(fig, filename="pl_hab_opda_raman.png")

    plotly.offline.plot(
        {
            "data": dat_lst,
            "layout": layout,
            },
        filename="plots/pl_fed_supp_graph_02.html"
        )
    # tmp = plotly.plotly.image.plot(data, filename="pl_fed_180314.png")
    #__|

#__|

#__|
