#!/usr/bin/env python

"""Miscellaneous Data and formatting templates.

Author: Raul A. Flores
"""

#| - Import Modules
import pandas as pd

from statistics import mean
#__|

#| - Formatting ***************************************************************

#| - Color Scheme

system_color_map = {
    "Fe_slab_False_nan": "#b94663",
    "Fe_slab_True_nan": "#b94663",

    "N_graph_False_nan": "#000000",
    "N_graph_True_nan": "#000000",

    "N_graph_Fe_False_C-trifold": "#6fac5d",
    "N_graph_Fe_False_N-trifold": "#6fac5d",

    "graph_Fe_False_nan": "#bc7d39",
    "graph_Fe_True_nan": "#bc7d39",

    "graphene_False_nan": "#697ed5",
    "graphene_True_nan": "#697ed5",
    }

# Pt_NaN_1
# graphene_NaN_1
# Fe3C/graphene_NaN_1
# graph_Fe_NaN_1
# N_graph_Fe_NaN_1
# N_graph_1.0_1
# N_graph_2.0_1
# N_graph_NaN_2
# N_graph_NaN_3
# Fe3C/N-graphene_NaN_1
# Fe3C/N-graphene_2.0_1
# Fe3C/N-graphene_NaN_2
# Fe3C/N-graphene_NaN_3

# system_color_map_vegge = {
#     "Pt_NaN_1": "#ff0000",
#     "graphene_NaN_1": "#697ed5",
#     "Fe3C/graphene_NaN_1": "#ffb830",
#
#     "Fe/graphene_NaN_1": "#bc7d39",
#     "Fe/N-graphene_NaN_1": "#6fac5d",
#
#
#     "N-graphene_1.0_1": "#000000",
#     "N-graphene_2.0_1": "#000000",
#     "N-graphene_NaN_2": "#000000",
#     "N-graphene_NaN_3": "#000000",
#
#     "Fe3C/N-graphene_NaN_1": "#90f473",
#     "Fe3C/N-graphene_2.0_1": "#90f473",
#     "Fe3C/N-graphene_NaN_2": "#90f473",
#     "Fe3C/N-graphene_NaN_3": "#90f473",
#     }


system_color_map_vegge = {
    "Pt_NaN_1": "#ff0000",
    "graphene_NaN_1": "#697ed5",
    "Fe3C/graphene_NaN_1": "#ffb830",
    "graph_Fe_NaN_1": "#bc7d39",
    "N_graph_Fe_NaN_1": "#6fac5d",
    "N_graph_1.0_1": "#000000",
    "N_graph_2.0_1": "#000000",
    "N_graph_NaN_2": "#000000",
    "N_graph_NaN_3": "#000000",
    "Fe3C/N-graphene_NaN_1": "#90f473",
    "Fe3C/N-graphene_2.0_1": "#90f473",
    "Fe3C/N-graphene_NaN_2": "#90f473",
    "Fe3C/N-graphene_NaN_3": "#90f473",
    }


#__|

#| - Smart Format Dict

# Smart Formatting
smart_format_dict_volcano_scaling = [

    [
        {"system": "Fe_slab"},
        {"color2": "#b94663"},
        ],

    [
        {"system": "N_graph_Fe"},
        {"color2": "#6fac5d"},
        ],

    [
        {"system": "graph_Fe"},
        {"color2": "#bc7d39"},
        ],

    [
        {"system": "graphene"},
        {"color2": "#697ed5"},
        ],

    [
        {"system": "N_graph"},
        {"color2": "#000000"},
        ],

    # Vegge specific systems
    [
        {"system": "Fe3C/N-graphene"},
        {"color2": "#90f473"},
        ],

    [
        {"system": "Fe3C/graphene"},
        {"color2": "#ffb830"},
        ],



    [
        {"author_short": "vegge"},
        {"symbol": "circle"},
        ],

    [
        {"author_short": "norskov"},
        {"symbol": "triangle-up"},
        ],

    ]

smart_format_dict = [

    # [
    #     {"spinpol": True},
    #     {"dash": "dot"},
    #     ],

    [
        {"system": "Fe_slab"},
        {"dash": "dashdot"},
        ],

    [
        {"system": "N_graph_Fe"},
        {"dash": "dot"},
        ],

    [
        {"system": "graph_Fe"},
        {"dash": "dash"},
        ],

    [
        {"system": "graphene"},
        {"dash": None},
        ],

    ]

#__|

#__| **************************************************************************

#| - Energetics ***************************************************************

#| - Scaling Data

# g_h2 = 0.
# g_h2o = 0
# g_o2 = 4.92

gas_molec_dict = {
    "h2": 0.,
    "o2": 4.92,
    "h2o": 0,
    }

# Ideal scaling
scaling_dict_ideal = {

    "ooh": {
        "m": 1.,
        "b": 3.2,
        },

    "o": {
        "m": 2.,
        "b": 0.,
        },

    "oh": {
        "m": 1.,
        "b": 0.,
        },

    }

# OOH Fit
# intercept (b) and slope (m) coefficients:
# 2.917714890331197
# 1.298834518086638
# O Fit
# intercept (b) and slope (m) coefficients:
# 0.5017142485515365
# 1.8144171589792406

scaling_dict = {

    "ooh": {
        "m": 1.298834518086638,
        "b": 2.917714890331197,
        },

    "o": {
        "m": 1.8144171589792406,
        "b": 0.5017142485515365,
        },

    "oh": {
        "m": 1.,
        "b": 0.,
        },

    }

#__|

#| - Raw Bare Slab DFT Energies

# Bare Fe
# /scratch/users/flores12/03_graph_N_Fe/01_opt_struct/Fe/slab/1-att/yes_spin/_1
# /scratch/users/flores12/03_graph_N_Fe/01_opt_struct/Fe/slab/1-att/no_spin/_2
bare_slab_False = -30772.8620536
bare_slab_True = -30774.3943557
bare_slab_dict_Fe = {True: bare_slab_True, False: bare_slab_False}

# Bare Graphene

# /scratch/users/flores12/03_graph_N_Fe/01_opt_struct/graphene/spinpol_False/_1
# /scratch/users/flores12/03_graph_N_Fe/01_opt_struct/graphene/spinpol_True
bare_slab_False = -947.9120007283367
bare_slab_True = -947.912185085
bare_slab_dict_Graphene = {True: bare_slab_True, False: bare_slab_False}

# Fe-supported Graphene
# /scratch/users/flores12/03_graph_N_Fe/01_opt_struct/combined-Fe-graph/FCC/5-att/1STEP/data/03-800/03-881/01-True/_1
# /scratch/users/flores12/03_graph_N_Fe/01_opt_struct/combined-Fe-graph/FCC/5-att/1STEP/data/03-800/03-881/02-False/_1
bare_slab_True = -31722.4352042
bare_slab_False = -31721.4121808
bare_slab_dict_Fe_Graph = {True: bare_slab_True, False: bare_slab_False}

# Fe-supported N-Graphene
# /scratch/users/flores12/03_graph_N_Fe/01_opt_struct/N_doped_graph_Fe/no_spin/01_N_trifold/_4
# N in trifold site
bare_slab_NGraph_Fe = -31839.06523325643

# C in trifold site
bare_slab_NGraph_False = -1065.40841793
bare_slab_NGraph_True = -1065.40843888
bare_slab_dict_NGraph = {
    True: bare_slab_NGraph_True,
    False: bare_slab_NGraph_False,
    }

# tmp = -31838.6148526

# Refs = Element_Refs()
# oxy_ref = Refs.E_O_ref.gibbs_e
# hyd_ref = Refs.E_H_ref.gibbs_e

fe_corr_dict = {
    "h2o": 0.528688009,
    "o": 0.068715186,
    "oh": 0.265727434,
    "ooh": 0.351189818,
    }

#__|

#__| **************************************************************************

#| - 2018_Vegge_Paper *********************************************************

#| - Solvent Energetics
oh_ooh_solv_corr_range = [-0.18, -0.35]

oh_solv_corr_range = oh_ooh_solv_corr_range
ooh_solve_corr_range = oh_ooh_solv_corr_range
o_solv_corr_range = [-0.63, -0.95]

oh_solv_corr_ave = mean(oh_solv_corr_range)
ooh_solv_corr_ave = mean(ooh_solve_corr_range)
o_solv_corr_ave = mean(o_solv_corr_range)
#__|

#| - Free Energy Corrections

n_graph_orr_ads_corr_dict = {
    "ooh": 0.445,
    "o": 0.074,
    "oh": 0.394,
    }

fe_carb_graph_orr_ads_corr_dict = {
    "ooh": 0.437,
    "o": 0.069,
    "oh": 0.389,
    }

gas_molec_corr_dict = {
    "h2": -0.043,
    "h2o": -0.011,
    }
#__|

#| - Adsorbate Energetics

# Energetics includes free energy corrections, water solvation corrections,
# and the Christensen correction scheme.

vegge_paper = [

    #| - Pt(111)
    {
        "system": "Pt",
        "facet": "111",
        "graphene_layers": 1,
        "cell": "3x3",
        "dg_ads_ooh": 3.98,
        "dg_ads_o": 1.37,
        "dg_ads_oh": 0.58,
        "overpotential": 0.65,
        },
    #__|

    #| - Graphene
    {
        "system": "graphene",
        "graphene_layers": 1,
        "cell": "r2xr2",
        "dg_ads_ooh": 5.98,
        "dg_ads_o": 3.65,
        "dg_ads_oh": 2.58,
        "overpotential": 2.19,
        },
    #__|

    #| - Fe3C/Graphene
    {
        "system": "Fe3C/graphene",
        "graphene_layers": 1,
        "cell": "r2xr2",
        "dg_ads_ooh": 4.79,
        "dg_ads_o": 1.96,
        "dg_ads_oh": 1.51,
        "overpotential": 1.10,
        },
    #__|

    #| - Fe/Graphene
    {
        "system": "graph_Fe",
        "cell": "1x1",
        "graphene_layers": 1,
        "dg_ads_ooh": 4.41,
        "dg_ads_o": 1.28,
        "dg_ads_oh": 1.01,
        "overpotential": 0.96,
        },
    #__|

    #| - N-graphene
    {
        "system": "N_graph",
        "n_per_ads": 1,
        "graphene_layers": 1,
        "cell": "r2xr3",
        "dg_ads_ooh": 4.63,
        "dg_ads_o": 2.50,
        "dg_ads_oh": 1.20,
        "overpotential": 0.94,
        },
    #__|

    #| - Fe3C/N-graphene
    {
        "system": "Fe3C/N-graphene",
        "graphene_layers": 1,
        "cell": "r2xr3",
        "dg_ads_ooh": 4.47,
        "dg_ads_o": 1.45,
        "dg_ads_oh": 0.98,
        "overpotential": 0.78,
        },
    #__|

    #| - Fe/N-graphene
    {
        "system": "N_graph_Fe",
        "graphene_layers": 1,
        "cell": "1x1",
        "dg_ads_ooh": 4.36,
        "dg_ads_o": 0.78,
        "dg_ads_oh": 0.78,
        "overpotential": 1.23,
        },
    #__|


    # N-graphene

    #| - N-graphene (2N/ads)
    {
        "system": "N_graph",
        "n_per_ads": 2,
        "graphene_layers": 1,
        "cell": "r2xr2",
        "dg_ads_ooh": 4.51,
        "dg_ads_o": 1.18,
        "dg_ads_oh": 1.10,
        "overpotential": 1.14,
        },
    #__|

    #| - 2 x N-graphene
    {
        "system": "N_graph",
        "graphene_layers": 2,
        "cell": "r2xr3",
        "dg_ads_ooh": 4.61,
        "dg_ads_o": 2.26,
        "dg_ads_oh": 1.18,
        "overpotential": 0.92,
        },
    #__|

    #| - 3 x N-graphene
    {
        "system": "N_graph",
        "graphene_layers": 3,
        "cell": "r2xr3",
        "dg_ads_ooh": 4.62,
        "dg_ads_o": 2.28,
        "dg_ads_oh": 1.19,
        "overpotential": 0.93,
        },
    #__|


    # Fe3C/N-graphene

    #| - Fe3C/N-graphene (2N/ads)
    {
        "system": "Fe3C/N-graphene",
        "n_per_ads": 2,
        "graphene_layers": 1,
        "cell": "r2xr2",
        "dg_ads_ooh": 4.51,
        "dg_ads_o": 1.10,
        "dg_ads_oh": 1.06,
        "overpotential": 1.20,
        },
    #__|

    #| - Fe3C/2 x N-graphene
    {
        "system": "Fe3C/N-graphene",
        "graphene_layers": 2,
        "cell": "r2xr3",
        "dg_ads_ooh": 4.66,
        "dg_ads_o": 2.31,
        "dg_ads_oh": 1.21,
        "overpotential": 0.97,
        },
    #__|

    #| - Fe3C/3 x N-graphene
    {
        "system": "Fe3C/N-graphene",
        "graphene_layers": 3,
        "cell": "r2xr3",
        "dg_ads_ooh": 4.62,
        "dg_ads_o": 2.28,
        "dg_ads_oh": 1.19,
        "overpotential": 0.93,
        },
    #__|


    ]

#__|

df_vegge = pd.DataFrame(vegge_paper)

df_vegge["authors"] = "reda_hansen_vegge"
df_vegge["author_short"] = "vegge"
#__| **************************************************************************


#| - Bulk Metal Experimental Properties

most_stable_crystal_structure_dict = {
    "Ni": "fcc",
    "Co": "hcp",
    "Ru": "hcp",
    "Rh": "fcc",
    "Mo": "bcc",
    "W": "bcc",
    }

#| - Experimental Lattice Constants
# All lattice constants are in A
exp_latt_const_dict = {

    #| - Nickel
    "Ni": {
        # Most stable <--------------------------------------------------------
        "fcc": {
            "a": 3.524,
            },

        # Article title:
        # Structure transition and magnetism of bcc-Ni nanowires
        "bcc": {
            "a": 2.88,
            },

        "hcp": {
            "a": None,
            "c": None,
            },
        },
    #__|

    #| - Cobalt
    "Co": {
        "fcc": {
            "a": None,
            },

        "bcc": {
            "a": None,
            },

        # Most stable <--------------------------------------------------------
        "hcp": {
            "a": 2.5071,
            "c": 4.0695,
            },
        },
    #__|

    #| - Ruthenium
    "Ru": {
        "fcc": {
            "a": None,
            },

        "bcc": {
            "a": None,
            },

        # Most stable <--------------------------------------------------------
        "hcp": {
            "a": 2.7059,
            "c": 4.2815,
            },
        },
    #__|

    #| - Rhodium
    "Rh": {
        "fcc": {
            "a": 3.8034,
            },

        "bcc": {
            "a": None,
            },

        # Most stable <--------------------------------------------------------
        "hcp": {
            "a": None,
            "c": None,
            },
        },
    #__|

    #| - Molybdenum
    "Mo": {
        "fcc": {
            "a": None,
            },

        # Most stable <--------------------------------------------------------
        "bcc": {
            "a": 3.147,
            },

        "hcp": {
            "a": None,
            "c": None,
            },
        },
    #__|

    #| - Tungsten
    "W": {

        # FACE‐CENTERED‐CUBIC TUNGSTEN FILMS OBTAINED BY
        "fcc": {
            "a": 4.15,
            },

        # Most stable <--------------------------------------------------------
        "bcc": {
            "a": 3.1652,
            },

        "hcp": {
            "a": None,
            "c": None,
            },
        },
    #__|

    }

#__|

#| - Optimized Lattice Constants

dft_latt_const_dict = {

    #| - Nickel
    "Ni": {
        # Most stable <--------------------------------------------------------
        "fcc": {
            "a": 3.528057,  # spinpol: True
            "a1": 3.526998,  # spinpol: False
            "a1": 3.527580,  # Kevin
            },

        "bcc": {
            "a": None,
            },

        "hcp": {
            "a": None,
            "c": None,
            },
        },
    #__|

    #| - Cobalt
    "Co": {
        "fcc": {
            "a": None,
            },

        "bcc": {
            "a": None,
            },

        # Most stable <--------------------------------------------------------
        "hcp": {

            # spinpol: True
            "a": 2.488106,
            "c": 4.120884,

            # spinpol: False
            "a2": 2.472911,
            "c2": 3.964677,

            # Kevin | spinpol: True
            "a3": 2.472911,
            "c3": 3.964677,
            },
        },
    #__|

    #| - Ruthenium
    "Ru": {
        "fcc": {
            "a": None,
            },

        "bcc": {
            "a": None,
            },

        # Most stable <--------------------------------------------------------
        "hcp": {
            # spinpol: True
            "a": 2.738153,
            "c": 4.280635,

            # spinpol: False
            "a2": 2.73706,
            "c2": 4.28237,

            # Kevin
            "a3": 2.728156,
            "c3": 4.3,

            },
        },
    #__|

    #| - Rhodium
    "Rh": {
        "fcc": {
            "a": 3.861584,  # spinpol: True
            "a2": 3.86089,  # spinpol: False
            "a3": 3.861137,  # Kevin
            },

        "bcc": {
            "a": None,
            },

        # Most stable <--------------------------------------------------------
        "hcp": {
            "a": None,
            "c": None,
            },
        },
    #__|

    #| - Molybdenum
    "Mo": {
        "fcc": {
            "a": None,
            },

        # Most stable <--------------------------------------------------------
        "bcc": {
            "a": 3.161018,  # spinpol: True
            "a2": 3.161018,  # spinpol: False
            "a3": 3.147,  # Kevin
            },

        "hcp": {
            "a": None,
            "c": None,
            },
        },
    #__|

    #| - Tungsten
    "W": {

        # FACE‐CENTERED‐CUBIC TUNGSTEN FILMS OBTAINED BY
        "fcc": {
            "a": None,
            },

        # Most stable <--------------------------------------------------------
        "bcc": {
            "a": 3.182625,  # spinpol: True
            "a2": 3.182625,  # spinpol: False
            "a3": 3.1819781,  # Kevin
            },

        "hcp": {
            "a": None,
            "c": None,
            },
        },
    #__|

    }

#__|

#__|

#| - Surface Facets
tmp_dict = {

    #| - Nickel
    "Ni": {
        # Most stable <--------------------------------------------------------
        "fcc": {
            "a": 3.528057,  # spinpol: True
            "a1": 3.526998,  # spinpol: False
            "a1": 3.527580,  # Kevin
            },

        "bcc": {
            "a": None,
            },

        "hcp": {
            "a": None,
            "c": None,
            },
        },
    #__|

    #| - Cobalt
    "Co": {
        "fcc": {
            "a": None,
            },

        "bcc": {
            "a": None,
            },

        # Most stable <--------------------------------------------------------
        "hcp": {

            # spinpol: True
            "a": 2.488106,
            "c": 4.120884,

            # spinpol: False
            "a2": 2.472911,
            "c2": 3.964677,

            # Kevin | spinpol: True
            "a3": 2.472911,
            "c3": 3.964677,
            },
        },
    #__|

    #| - Ruthenium
    "Ru": {
        "fcc": {
            "a": None,
            },

        "bcc": {
            "a": None,
            },

        # Most stable <--------------------------------------------------------
        "hcp": {
            # spinpol: True
            "a": 2.738153,
            "c": 4.280635,

            # spinpol: False
            "a2": 2.73706,
            "c2": 4.28237,

            # Kevin
            "a3": 2.728156,
            "c3": 4.3,

            },
        },
    #__|

    #| - Rhodium
    "Rh": {
        "fcc": {
            "a": 3.861584,  # spinpol: True
            "a2": 3.86089,  # spinpol: False
            "a3": 3.861137,  # Kevin
            },

        "bcc": {
            "a": None,
            },

        # Most stable <--------------------------------------------------------
        "hcp": {
            "a": None,
            "c": None,
            },
        },
    #__|

    #| - Molybdenum
    "Mo": {
        "fcc": {
            "a": None,
            },

        # Most stable <--------------------------------------------------------
        "bcc": {
            "a": 3.161018,  # spinpol: True
            "a2": 3.161018,  # spinpol: False
            "a3": 3.147,  # Kevin
            },

        "hcp": {
            "a": None,
            "c": None,
            },
        },
    #__|

    #| - Tungsten
    "W": {

        # FACE‐CENTERED‐CUBIC TUNGSTEN FILMS OBTAINED BY
        "fcc": {
            "a": None,
            },

        # Most stable <--------------------------------------------------------
        "bcc": {
            "a": 3.182625,  # spinpol: True
            "a2": 3.182625,  # spinpol: False
            "a3": 3.1819781,  # Kevin
            },

        "hcp": {
            "a": None,
            "c": None,
            },
        },
    #__|

    }


#__|


#| - __misc__
proj_dir_name = "01_fe_graph"
#__|
