#!/usr/bin/env python

"""Sandbox script.

Author: Raul A. Flores
"""

#| - Import Modules
from dft_job_automat.job_types_classes.data_frame_methods import DataFrame_Methods
from dft_job_automat.job_analysis import DFT_Jobs_Analysis, DFT_Jobs_Setup

from dft_job_automat.job_types_classes.dft_methods import DFT_Methods
#__|


# Jobs = DFT_Jobs_Setup(
#         working_dir="1STEP",
#         )
#
# df = Jobs.data_frame
# # Jobs.__gen_datatable__()

dft_meth = DFT_Methods(
    methods_to_run=[
        "init_atoms",
        ]
    )

Jobs = DFT_Jobs_Analysis(
    working_dir="1STEP",
    load_dataframe=False,
    job_type_class=dft_meth,
    )

df = Jobs.data_frame



DFM = DataFrame_Methods(df)

DFM.create_atoms_objects(
    outdir="atoms_objects",
    atoms_row="init_atoms",
    # atoms_row="atoms_object",
    image=-1,
    )
