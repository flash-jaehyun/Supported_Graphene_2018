#!/usr/bin/env python

"""Parse bulk optmization data for suported graphene project.

Author: Raul A. Flores
"""

#| - Import Modules
from dft_job_automat.job_analysis import DFT_Jobs_Analysis
from dft_job_automat.job_types_classes.dft_methods import DFT_Methods

from create_master_job_list import master_job_list
#__|

#| - Instantiate Classes
dft_inst = DFT_Methods(
    methods_to_run=[
        "elec_energy",
        "init_atoms",
        "atoms_object",
        "dft_params",
        ],

    DFT_code="QE",
    )

Jobs = DFT_Jobs_Analysis(
    indiv_job_dict_lst=master_job_list,
    working_dir=".",
    folders_exist=True,
    load_dataframe=False,
    job_type_class=dft_inst,
    parse_all_revisions=False,
    )

df_all = Jobs.data_frame
df_m = Jobs.filter_early_revisions(Jobs.data_frame)
#__|


#| - __old__
# Jobs.add_data_column(
#     dft_inst.elec_energy,
#     column_name="new_column",
#     revision="auto",
#     allow_failure=False,
#     )
#__|
