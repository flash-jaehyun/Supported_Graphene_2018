"""Lattice-constant optimization Fe-BCC """

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
ram_inst = DFT_Methods(
    methods_to_run=["elec_energy"],
    )

Jobs = DFT_Jobs_Analysis(
    system="aws",
    update_job_state=False,
    job_type_class=ram_inst,
    load_dataframe=False,
    )

df = Jobs.data_frame
#__|

#| - Discarded Non-Finished Jobs
finite_alpha_rows = np.isfinite(df["elec_energy"]) == True
df = df[finite_alpha_rows]

# df = df[df["force-cutoff"] == 0.001]

df.to_csv("dataframe_out.csv")
#__|

#| - Normalize Energy
min_e = df.loc[df["elec_energy"].idxmin()]["elec_energy"]

df["elec_energy"] = df["elec_energy"].apply(lambda x: x - min_e)
# df["elec_energy"]
#__|

# ###############################################################################

#| - Data Collection
data_sets = Jobs.create_data_sets(df, "lattice-parameter")

plot_data_list = []
for data_series in data_sets:
    data_i_labels = data_series["label"]
    x_dat = data_series["data"]["lattice-parameter"].tolist()
    y_dat = data_series["data"]["elec_energy"].tolist()

    data_i = Scatter(
        x = x_dat,
        y = y_dat,

        name = data_i_labels,
        mode = "lines",
        )

    plot_data_list.append(data_i)
#__|

#| - Plotting
layout = {

    "title": "Lattice-Constant Optimization for Iron BCC",

    "yaxis": {
        "title": "Electronic Energy [eV]",
        "zeroline": False,
        "showgrid": False,
        },

    "xaxis": {
        "title": "Lattice-Constant [A]",
        "zeroline": False,

        # "autotick": False,
        # # "tick0": 0,
        # # "dtick": 100,
        # "showgrid": False,
        },

    # "autosize": False,
    # "width": 1200,
    # "height": 800,
    # "legend": {
    #     "xanchor":"center",
    #     "yanchor":"top",
    #     "y":-0.2,
    #     "x":0.5,
    #     },
    }

plotly.offline.plot(
    {
        "data": plot_data_list,
        "layout": layout,
        },
    filename="Fe_bcc_latt_opt.html"

    )
#__|
