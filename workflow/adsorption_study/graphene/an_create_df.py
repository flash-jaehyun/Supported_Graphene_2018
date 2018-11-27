#!/usr/bin/env python

"""Processing ORR Adsorption Energetics.

Author: Raul A. Flores
"""

#| - IMPORT MODULES
# import sys

import pandas as pd
pd.options.mode.chained_assignment = None

# My Modules ******************************************************************
from dft_job_automat.job_analysis import DFT_Jobs_Analysis
from dft_job_automat.job_types_classes.dft_methods import DFT_Methods
#__|

#| - Initiate Instance
dft_inst = DFT_Methods(
    methods_to_run=[
        "elec_energy",
        "pdos_data",
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
    # load_dataframe=True,
    load_dataframe=False,
    working_dir="1STEP",
    )

df = Jobs.filter_early_revisions(Jobs.data_frame)

from dft_job_automat.job_types_classes.data_frame_methods import \
    DataFrame_Methods
DF = DataFrame_Methods(df)
# DF.create_atoms_objects(atoms_row="init_atoSms")

#__|

#| - Checking Atoms Objects Adsorbate Indices
# for atoms_i in df["init_atoms"]:
#     ads_indices = atoms_i.info["adsorbates"]
#     print(ads_indices)
#
#     tmp1 = atoms_i[ads_indices]
#     print(tmp1.get_chemical_symbols())
#__|
