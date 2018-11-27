"""Processing ORR Adsorption Energetics.

Author: Raul A. Flores
"""

#| - IMPORT MODULES
import sys
import copy
# import traceback

import numpy as np
import pandas as pd

import plotly
from plotly.graph_objs import Figure

# My Modules ******************************************************************
from dft_job_automat.job_analysis import DFT_Jobs_Analysis
from dft_job_automat.job_types_classes.dft_methods import DFT_Methods
from orr_reaction.orr_methods import ORR_Free_E_Plot, calc_ads_e

pd.options.mode.chained_assignment = None
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
bare_slab = -31839.06523325643
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
        "gibbs_correction",
        "atom_type_num_dict",
        "init_atoms",
        "atoms_object",
        # "magmom_charge_history",
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

from dft_job_automat.job_types_classes.data_frame_methods import \
    DataFrame_Methods
DF = DataFrame_Methods(df)
# DF.create_atoms_objects(atoms_row="init_atoSms")
#__|


# groupby = copy.deepcopy(Jobs.tree_level_labels)
# groupby.remove("adsorbate")

groupby = ["adsorbate"]

data_master = {}
for group_i in df.groupby(groupby):

    print(group_i[0])
    # data_master[group_i[0]] = group_i[1]
    mean_fe_corr = group_i[1]["gibbs_correction"].mean()

    print(mean_fe_corr)

    print(20 * "_")
