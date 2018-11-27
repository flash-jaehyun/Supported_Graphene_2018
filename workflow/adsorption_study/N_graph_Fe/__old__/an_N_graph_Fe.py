
# coding: utf-8

# # Nitrogen-doped Graphene Supported on FCC Iron 111 Surface <a name="head"></a>
# ***

# #### Table of Contents
# 
# -   [Import Python Modules](#import-modules)
# -   [Reference Energies & Misc Parameters](#ref_e_&_params)
# -   [Initialize Instances](#init_instances)
# -   [Lowest Energy Pathway](#lowest_e_pathway)
# -   [All Binding Site States](#all_states)

# ## Import Modules <a name="import-modules"></a>

# In[1]:


import sys
import copy

import numpy as np
import pandas as pd

import plotly
from plotly.graph_objs import Figure
import plotly.plotly as py

# My Modules ******************************************************************
from dft_job_automat.job_analysis import DFT_Jobs_Analysis
from dft_job_automat.job_types_classes.dft_methods import DFT_Methods
from orr_reaction.orr_methods import ORR_Free_E_Plot, calc_ads_e

from orr_reaction.orr_methods import lowest_e_path, df_calc_adsorption_e, plot_all_states

pd.options.mode.chained_assignment = None

# iPython Settings
# get_ipython().run_line_magic('load_ext', 'autoreload')
# get_ipython().run_line_magic('autoreload', '2')


# ## Reference Energies & Misc Parameters <a name="ref_e_&_params"></a>

# In[2]:


bare_slab = -31839.06523325643

# R21 From Pourbaix Papers
dG_rxn_h2o = -2.4583

# /scratch/users/flores12/gas_phase_molec/BEEF-vdW
H2_dft = -32.9563981542851
O2_dft = -883.190570481887
H2O_dft = -476.544109028354

hyd_ref = H2_dft / 2.

ref_scheme = "h2o"
if ref_scheme == "h2o":
    oxy_ref = H2O_dft - H2_dft
elif ref_scheme == "o2":
    oxy_ref = dG_rxn_h2o + O2_dft / 2.
    
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


# ## Initialize Instances <a name="init_instances"></a>

# In[3]:


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
df_calc_adsorption_e(df, bare_slab, oxy_ref, hyd_ref)
df_master = df.copy()


# ## All Binding Site States <a name="all_states"></a>

# In[6]:


dat_lst1, layout1 = plot_all_states(df_master, Jobs.tree_level_labels, color_list, bias=0.)

py.iplot(
    {
        "data": dat_lst1,
        "layout": layout1,
        },
    filename="pl_fed_supp_graph_01.html"
    )


# ## Lowest Energy Pathway <a name="lowest_e_pathway"></a>

# In[4]:


dat_lst, layout = lowest_e_path(df, Jobs.tree_level_labels, color_list, bias=0.)

py.iplot(
    {
        "data": dat_lst,
        "layout": layout,
        },
    filename="pl_fed_supp_graph_02.html"
    )


# [(Back to top)](#head)
