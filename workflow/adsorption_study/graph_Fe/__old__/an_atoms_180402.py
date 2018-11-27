"""Processing ORR Adsorption Energetics."""

#| - IMPORT MODULES
import pandas as pd
pd.options.mode.chained_assignment = None

# My Modules ******************************************************************

from dft_job_automat.job_analysis import DFT_Jobs_Analysis
from dft_job_automat.job_types_classes.dft_methods import DFT_Methods
#__|

#| - SCRIPT INPUTS

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
#__|

for index, row in df.iterrows():
    print(str(row["revision_number"]) + " | " + row["path"])
