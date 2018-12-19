#!/usr/bin/env python

"""Parse bulk optmization data for suported graphene project.

Author: Raul A. Flores
"""

#| - Import Modules
import os

import pickle

from dft_job_automat.job_analysis import DFT_Jobs_Analysis
from dft_job_automat.job_types_classes.dft_methods import DFT_Methods

from create_master_job_list import master_job_list
#__|


# | - Methods

def parse_info(path_i):
    """
    """
    #| - parse_info
    print(path_i); print("\n")

    pickle_file = pickle.load(
        open(
            os.path.join(
                path_i,
                "heterostructures.pickle",
                ),
            "rb",
            )
        )

    out_dict = {
        "sys_data_i": pickle_file,
        }

    return(out_dict)


    #| - __old__
    # from ase import io
    #
    # files_i = os.listdir(path_i)
    #
    # if "init_graphene.cif" in files_i:
    #     atoms_init_graph_i = io.read(
    #         os.path.join(
    #             path_i,
    #             "init_graphene.cif",
    #             )
    #         )
    # else:
    #     atoms_init_graph_i = None
    #
    # if "init_support.cif" in files_i:
    #     atoms_init_supp_i = io.read(
    #         os.path.join(
    #             path_i,
    #             "init_support.cif",
    #             )
    #         )
    # else:
    #     atoms_init_supp_i = None
    #
    # structures_found = os.path.isdir(
    #     os.path.join(
    #         path_i,
    #         "01_heterostructures",
    #         )
    #     )
    #
    # if structures_found:
    #     out_atoms_path_list = os.listdir(os.path.join(
    #         path_i,
    #         "01_heterostructures",
    #         ))
    #
    #     out_atoms_list = []
    #     for out_i in out_atoms_path_list:
    #         out_atoms_i = io.read(
    #             os.path.join(
    #                 path_i,
    #                 "01_heterostructures",
    #                 out_i,
    #                 )
    #             )
    #         out_atoms_list.append(out_atoms_i)
    # else:
    #     out_atoms_list = None
    #
    # out_dict = {
    #     "init_graph_atoms": atoms_init_graph_i,
    #     "init_support_atoms": atoms_init_supp_i,
    #     "out_atoms": out_atoms_list,
    #     }
    #__|

    #__|

def parse_out_for_mismatch(path_i):
    """
    """
    #| - parse_out_for_mismatch
    std_out_file = os.path.join(path_i, "job.out")

    if os.path.isfile(std_out_file):
        lines = [line.rstrip('\n') for line in open(std_out_file)]
        ind_i = lines.index("u,v & angle mismatches:")
        u_v_angle_mismatch = [float(i.replace(",", "")) for i in lines[ind_i + 1].split(" ")]

        u_mismatch = u_v_angle_mismatch[0]
        v_mismatch = u_v_angle_mismatch[1]
        angle_mismatch = u_v_angle_mismatch[2]

        out = {
            "u_mismatch": u_mismatch,
            "v_mismatch": v_mismatch,
            "angle_mismatch": angle_mismatch,
            }

    else:
        out = None

    return(out)
    #__|

#__|

#| - Instantiate Classes

# dft_inst = DFT_Methods(
#     methods_to_run=[
#         "elec_energy",
#         "init_atoms",
#         "atoms_object",
#         "dft_params",
#         ],
#
#     DFT_code="QE",
#     )

Jobs = DFT_Jobs_Analysis(
    indiv_job_dict_lst=master_job_list,
    working_dir=".",
    folders_exist=True,
    load_dataframe=False,
    # job_type_class=dft_inst,
    job_type_class=None,
    parse_all_revisions=False,
    methods_to_run=[
        parse_info,
        # parse_out_for_mismatch,
        ]
    )

df_all = Jobs.data_frame
df_m = Jobs.filter_early_revisions(Jobs.data_frame)
#__|


#| - __old__
# print(40 * "#")
#
# Jobs.add_data_column(
#     parse_info,
#     column_name="new_column",
#     revision="auto",
#     allow_failure=False,
#     )
#__|
