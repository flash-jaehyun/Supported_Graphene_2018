"""Processing ORR Adsorption Energetics."""

#| - IMPORT MODULES
# import sys
import copy

import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None

import plotly
from plotly.graph_objs import Figure

# My Modules
from dft_job_automat.job_types_classes.data_frame_methods import \
    DataFrame_Methods

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

run_an_0 = False
run_an_1 = True

bias = 0.
#__|

#| - Reference Energies
bare_slab = -31722.653798

# Using Water for Oxygen Reference
hyd_ref = -32.920360 / 2.
h2o_ref = -476.63
oxy_ref = h2o_ref - 2. * hyd_ref
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

# DF = DataFrame_Methods(df)
# DF.create_atoms_objects(atoms_row="atoms_object")
#__|

#| - Data Processing

#| - Filtering Data
# tmp = df[np.isfinite(df["elec_energy"]) == True]
# tmp = df[np.isfinite(df["elec_energy"]) == True]
# # df = df[df["job_state"] == "SUCCEEDED"]
# finite_e_rows = np.isfinite(df["elec_energy"]) == True
# df = df[finite_e_rows]
#__|

#| - Adsorption Energies
ads_e_list = []
for index, row in df.iterrows():
    ads_e_i = calc_ads_e(
        row,
        bare_slab,
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

        #| - Removing Old Versions
        latest_entry_list = []
        for entry_i in group_i[1].groupby("adsorbate"):
            filt_i = entry_i[1].loc[entry_i[1]["revision_number"].idxmax()]
            filt_i = pd.DataFrame(filt_i)

            filt_i_dict = filt_i.to_dict()
            filt_i_dict = filt_i_dict[filt_i_dict.keys()[0]]

            latest_entry_list.append(filt_i_dict)

        group_i_filt = pd.DataFrame(latest_entry_list)
        #__|

        ads_e_dict_i = dict(zip(
            group_i_filt["adsorbate"],
            group_i_filt["ads_e"],
            ))
        ads_e_dict_i["bulk"] = 0.

        data_master[group_i[0]] = ads_e_dict_i
    #__|

    #| - Creating Data Sets

    #| - Creating FED Datasets
    data_list = []
    i_cnt = 0
    for key, fe_dict in data_master.iteritems():
        i_cnt += 1
        ORR = ORR_Free_E_Plot(fe_dict)
        e_list = ORR.energy_lst
        e_list = ORR.apply_bias(bias, e_list)

        for n, i in enumerate(e_list):
            if np.isnan(i) is True:
                e_list[n] = None

        name_i = "_".join([str(i) for i in key])

        print("Creating plotly series")
        dat_lst = ORR.create_plotly_series(
            e_list,
            group=name_i,
            name=name_i,
            color=color_list[i_cnt - 1],
            # plot_mode="full_lines",
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
        filename="pl_fed_supp_graph.html"
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

    # data_sets = copy.deepcopy(groupby)
    # data_sets.remove("adsorbate")

    data_master = {}
    site_data = {}
    for group_i in df.groupby(groupby):

        ads_e_dict_i = {}
        site_dict_i = {}
        for ads_i in group_i[1].groupby("adsorbate"):

            min_e_row = ads_i[1].loc[ads_i[1]["ads_e"].idxmin()]
            min_e = min_e_row["ads_e"]

            site_i = min_e_row["site"]
            site_dict_i[ads_i[0]] = site_i

            ads_e_dict_i[ads_i[0]] = min_e

        ads_e_dict_i["bulk"] = 0.
        site_dict_i["bulk"] = ""

        data_master[group_i[0]] = ads_e_dict_i
        site_data[group_i[0]] = site_dict_i
    #__|

    #| - Creating Site List
    rxn_path_list = ["bulk", "ooh", "o", "oh", "bulk"]

    site_list_dict = {}
    for key_i, value_i in site_data.iteritems():

        site_list_i = []
        for ads_i in rxn_path_list:
            for key_j, value_j in value_i.iteritems():
                if key_j == ads_i:
                    # print("!@#!@)#*!()@*")
                    site_list_i.append(value_j)

        site_list_dict[key_i] = site_list_i

    # Changed spinpol:False, *OH, entry from "bridge" to "ontop-trifold" because
    # the relaxation restructured the adsorption site
    site_list_dict[False][3] = "ontop-trifold"
    #__|

    #| - Creating Data Sets

    #| - Creating FED Datasets
    data_list = []
    i_cnt = 0
    for key, fe_dict in data_master.iteritems():
        i_cnt += 1
        ORR = ORR_Free_E_Plot(fe_dict)
        e_list = ORR.energy_lst
        e_list = ORR.apply_bias(bias, e_list)

        overpot_i = ORR.overpotential

        for n, i in enumerate(e_list):
            if np.isnan(i) is True:
                e_list[n] = None

        if type(key) == tuple:
            name_i = "_".join([str(i) for i in key]) + " (OP: " + str(round(overpot_i, 2)) + ")"
        else:
            name_i = str(key) + " (OP: " + str(round(overpot_i, 2)) + ")"

        print("Creating plotly series")
        dat_lst = ORR.create_plotly_series(
            e_list,
            group=name_i,
            name=name_i,
            hover_text=site_list_dict[key],
            color=color_list[i_cnt - 1],
            # plot_mode="full_lines",
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
        filename="pl_fed_supp_graph_02.html"
        )
    # tmp = plotly.plotly.image.plot(data, filename="pl_fed_180314.png")
    #__|

#__|

#__|
