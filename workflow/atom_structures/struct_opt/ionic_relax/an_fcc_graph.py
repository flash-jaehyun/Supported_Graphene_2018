"""Electronic energy convergence of FCC Fe supported graphene."""

#| - IMPORT MODULES
import os
import sys
import copy
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

import plotly
from plotly.graph_objs import Scatter, Layout

# My Modules
from dft_job_automat.job_analysis import DFT_Jobs_Analysis
from raman_dft.vasp_raman_job_methods import to_plot
from  dft_job_automat.job_types_classes.dft_methods import DFT_Methods
#__|

#| - Initializing Class Instances

#| - Iron + Graphene Slab
compenv = os.environ["COMPENV"]
if compenv == "wsl":
    working_dir = "."
    load_dataframe = True
elif compenv == "sherlock":
    working_dir = "./1STEP"
    load_dataframe = False

dft_inst = DFT_Methods(
    methods_to_run=[
        "elec_energy",
        "atom_type_num_dict",
        ],
    )

Jobs = DFT_Jobs_Analysis(
    # system="aws",
    update_job_state=False,
    job_type_class=dft_inst,
    load_dataframe=load_dataframe,
    working_dir=working_dir,
    )

df = Jobs.data_frame
#__|

#| - Bulk Iron
# data_dir = os.environ["sc"] + "/05_fe_graph_proj/workflow/bulk_struct_opt/Fe_FCC_bulk"
#
# dft_inst = DFT_Methods(
#     methods_to_run=["elec_energy"],
#     )
#
# Jobs_2 = DFT_Jobs_Analysis(
#     # system="aws",
#     update_job_state=False,
#     # job_type_class=dft_inst,
#     load_dataframe=True,
#     working_dir=data_dir,
#     )
#
# df_fe = Jobs_2.data_frame
#__|

#| - Bulk Graphene


#__|


#__|

#| - Discarded Non-Finished Jobs
finite_e = np.isfinite(df["elec_energy"]) == True
df = df[finite_e]

min_e = df["elec_energy"].min()
df["norm_e"] = df["elec_energy"] - min_e

booleanDictionary = {True: "TRUE", False: "FALSE"}
df = df.replace(booleanDictionary)



df["data_label"] = "magmom: " + df["magmom"]
df["hover_lab"] = "kpoints: " + df["kpoints"].astype(str)


# tmp = df.loc[df["magmom"] == "TRUE"]

#| - Color Palettes
color_palette_1 = [
"rgb(198,158,61)",
"rgb(103,76,204)",

"rgb(236,186,51)",
"rgb(237,101,67)",
"rgb(222,134,54)",
]

color_palette_2 = [
"rgb(181,149,213)",
"rgb(103,76,204)",
"rgb(97,166,201)",
"rgb(185,76,198)",
"rgb(93,80,139)",
]
#__|


# fig, ax = plt.subplots()
data_lst = []
for key, grp in df.groupby(["magmom"]):
    label_i = grp["data_label"].unique()
    if len(label_i) == 1:
        series_label = label_i[0]

    data_i = Scatter(
        x = grp["pw-cutoff"],
        y = grp["norm_e"],
        name = series_label,
        mode = "markers",
        marker = dict(
            size = 10,
            ),
        text= df["hover_lab"].tolist(),
        )
    data_lst.append(data_i)
#__|

#| - Plotting

#| - Font Size
plot_title_size = 20
tick_lab_size = 16
axes_lab_size = 18
legend_size = 18
#__|


#| - layout
layout = {
    "title": "Convergence of FCC-Iron Supported Graphene",

    "font": {
        "family": "Courier New, monospace",
        "size": plot_title_size,
        "color": "black",
        },

    "yaxis": {
        "title": "Electronic Energy [eV]",
        "zeroline": True,
        "showgrid": False,

        "tickfont":dict(
            size=tick_lab_size,
            ),

        },

    "xaxis": {
        "title": "pw-cutoff [eV]",
        "zeroline": True,
        "showgrid": False,

        "tickfont":dict(
            size=tick_lab_size,
            ),

        "ticks": "outside",
        "tick0": 0,
        "dtick": 100,
        "ticklen": 5,
        "tickwidth": 1,
        "tickcolor": "black",


        },

    "autosize": False,
    "width": 800,
    "height": 600,

    # "autosize": True,

    #| - Legend ---------------------------------------------------------------
    "legend": {
        "traceorder": "normal",
        "font": dict(size=legend_size)
        },

    #__| ----------------------------------------------------------------------

    }
#__|

plotly.offline.plot(
    {
        "data": data_lst,
        "layout": layout,
        },
    filename="pl_Fe_fcc_graph_convergence.html"
    )
#__|
