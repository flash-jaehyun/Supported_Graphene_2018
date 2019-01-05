#!/usr/bin/env python

"""Searching for surface graphene systems which minimize lattice strain."""

#| - Import Modules
import sys
import os
import numpy as np
import itertools
import math
import pickle
import json

import pandas as pd

from ase import io
from ase.build import fcc100, fcc110, fcc111, fcc211
from ase.build import bcc100, bcc110, bcc111

from ase.build import graphene_nanoribbon
from ase import Atoms
from ase.build import root_surface, add_adsorbate

from misc_modules.numpy_methods import angle_between
from ase_modules.add_adsorbate import add_graphene_layer
from ase_modules.ase_methods import angle_between_lattice_vectors, magnitude_of_lattice_vectors
#__|

#| - SCRIPT INPUTS
metal = "Fe"
fcc_latt_const = 3.4741 # Value obtained from lattice constant optimization
bcc_latt_const = 2.7576 # Value obtained from lattice constant optimization
graph_bond_d_real = 1.4237
layers_z = 3
vacuum = 10.

###############################################################################
max_strain = 100.0
max_area = 2000.

# supp_latt_size = range(3)[1:]
# supp_latt_size = [3, 4, 5, 6]
supp_latt_size = [1, 2, 3]
graph_latt_size = supp_latt_size

roots = range(4)[3:]

structures = [
    # {"bulk": "fcc", "surface": "100", "function": fcc100},
    # {"bulk": "fcc", "surface": "110", "function": fcc110},
    {"bulk": "fcc", "surface": "111", "function": fcc111},

    # {"bulk": "bcc", "surface": "100", "function": bcc100},
    # {"bulk": "bcc", "surface": "110", "function": bcc110},  # Doesn't work, weird angle
    # {"bulk": "bcc", "surface": "111", "function": bcc111},
    ]
#__|

#| - MISC PARAMETERS
data_dir = "01_data"
load_data = False
#__|

#| - Orthogonal Graphene
graph = graphene_nanoribbon(2, 2, C_C=graph_bond_d_real, sheet=True)

x_vect = graph.cell[0][0]
y_vect = graph.cell[2][2]
#__|

#| - FUNCTIONS

def create_comb_sys(slab_i, graph_n_x, graph_n_y, out_file=None):
    """

    """
    #| - create_comb_sys
    graph_n_x = int(graph_n_x)
    graph_n_y = int(graph_n_y)


    x_vect = slab_i.cell[0][0]
    y_vect = slab_i.cell[1][1]

    new_CC_x = x_vect / (graph_n_x * 3.)
    new_CC_y = y_vect / (graph_n_y * 2. * 3. ** (1. / 2.))

    pos = slab_i.positions
    max_z_pos = pos.max(axis=0)[2]

    #| - TEMP - Creating Rectangular Graphene
    from ase.build import graphene_nanoribbon

    # graph = graphene_nanoribbon(2, 2, C_C=new_CC_x, sheet=True)
    # print(2 * graph_n_x)
    # print(2 * graph_n_y)

    graph = graphene_nanoribbon(2 * graph_n_x, 2 * graph_n_y, C_C=new_CC_x, sheet=True)

    # graph.write("graph.traj")

    graph.rotate(90, "x", center=(0,0,0))
    graph.rotate(180, "z", center=(0,0,0))
    graph.wrap()

    x_vect = graph.cell[0][0]
    y_vect = graph.cell[2][2]

    new_cell = np.array([
        [x_vect, 0., 0.],
        [0., y_vect, 0.],
        [0., 0., 2.],
        ])
    graph.set_cell(new_cell)
    graph.set_pbc((True, True, True))

    graph.positions[:, 2] = graph.positions[:, 2] + max_z_pos + 3.
    # print(new_CC_y / new_CC_x)
    graph.positions[:, 1] = graph.positions[:, 1] * (new_CC_y / new_CC_x)

    new_pos = graph.positions
    graph.set_positions(new_pos)

    # graph.write("graph.traj")
    #__|

    #| - TEMP -  Adding Graphene to Slab
    interface = slab_i.copy()
    interface.extend(graph)
    # interface.center
    # print(out_file)

    if out_file is None:
        pass
    else:
        interface.write(out_file)
    #__|

    return(interface)
    #__|

def find_low_strain_comb(
    graph_latt_c,
    latt_vector_2,
    graph_cc_ideal=1.42,
    dir="y",
    cell_geom="ortho",
    ):
    """

    Args:
        graph_cc_ideal
        dir:
            "x", "y"
        cell_geom:
            "ortho", "hex"
    """
    #| - find_low_strain_comb
    strain_list = []
    for i_ind in range(5)[1:]:
        slab_j = latt_vector_2

        if cell_geom == "ortho":
            #| - Orthogonl Unit Cell
            graph_i = i_ind * graph_latt_c

            if dir == "y":
                new_CC = slab_j / (i_ind * 2. * 3. ** (1. / 2.))
                graph_cc_ideal = graph_i / (i_ind * 2. * 3. ** (1. / 2.))

            elif dir == "x":
                new_CC = slab_j / (i_ind * 3.)
                graph_cc_ideal = graph_i / (3. * i_ind)

            #__|

        elif cell_geom == "hex":
            #| - Hexagonal Unit Cell
            new_CC = 1. * slab_j / (3 * i_ind)

            #__|

        strain =100. * (new_CC - graph_cc_ideal) / graph_cc_ideal
        entry_i = {"strain": strain, "graph_rep": i_ind, "new_CC": new_CC}
        strain_list.append(entry_i)

    return(strain_list)
    #__|

#__|

#| - MAIN LOOP ****************************************************************
if not load_data:
    master_list = []

    iter_list = [range(len(structures)), supp_latt_size, supp_latt_size, roots]

    prod = 1
    for ind_i in [len(i) for i in iter_list]:
        prod *= ind_i
    print(prod)
    all_comb = itertools.product(*iter_list)
    for idx, iterand in enumerate(all_comb):
        print("_____________________________________")

        skip_i = False
        print(100. * idx / prod)

        #| - Parameters
        structure = structures[iterand[0]]
        supp_latt_unit_1 = iterand[1]
        supp_latt_unit_2 = iterand[2]
        root_i = iterand[3]

        bulk = structure["bulk"]
        surf = structure["surface"]
        func = structure["function"]

        if bulk == "fcc":
            lattice_constant_i = fcc_latt_const
        elif bulk == "bcc":
            lattice_constant_i = bcc_latt_const
        #__|

        #| - TEMP - Skipping
        # if bulk != "bcc":
        #     continue
        # elif surf != "111":
        #     continue

        # elif supp_latt_unit_1 != 1:
        #     continue
        # elif supp_latt_unit_2 != 6:
        #     continue

        # print(str(supp_latt_unit_1) + " | " + str(supp_latt_unit_2))
        #__|

        mess_i = "Starting " + bulk + "-" + surf + " (" + str(supp_latt_unit_1) \
        + "x" + str(supp_latt_unit_2) + ")" + " root: " + str(root_i) + " structure"
        print(mess_i)
        sys.stdout.flush()

        #| - Creating Slab
        orth_cell = False
        if bulk == "bcc" and surf == "110":
            orth_cell = True
            # print("WOOOP")

        try:
            slab_i = func(
                metal,
                size=(supp_latt_unit_1, supp_latt_unit_2, layers_z),
                a=lattice_constant_i,
                vacuum=vacuum,
                orthogonal=orth_cell,
                )
        except:
            print("Couldn't create slab")
            continue

        if root_i == 0:
            slab_i = slab_i
        else:
            try:
                root_slab_i = root_surface(slab_i, root_i)
            except:
                print("This root surface doesn't exist!!!!")
                continue

            slab_i = root_slab_i

        num_atoms = len(slab_i.get_atomic_numbers())
        #__|

        #| - Angle Between Unit Vectors
        angle = angle_between_lattice_vectors(slab_i)
        mag1, mag2, mag3 = magnitude_of_lattice_vectors(slab_i)
        print("Angle: " + str(angle))
        #__|

        #| - ENTRY_i DICT
        entry_i = {
            "bulk": bulk,
            "surface": surf,
            "latt_vect_1": mag1,
            "latt_vect_2": mag2,
            "angle": angle,
            "root_cut": root_i,
            "ase_slab_function": func,
            "lattice_constant": lattice_constant_i,
            "supp_rep_1": supp_latt_unit_1,
            "supp_rep_2": supp_latt_unit_2,
            "num_M_atoms": num_atoms,
            "slab": slab_i,
            }
        #__|

        #| - Analysing Normal Slab
        if round(angle, 5) == 60.0:
            #| - Hexagonal Unit Cell
            print("Hexagonal cell - Good!")
            if round(mag1, 5) == round(mag2, 5):

                strain_1 = find_low_strain_comb(
                    None,
                    mag1,
                    graph_cc_ideal=graph_bond_d_real,
                    cell_geom="hex",
                    )

                low_strain_x = min(strain_1, key=lambda x:abs(x["strain"]))

                entry_i.update(
                    {
                        "cell_geom": "hex",

                        "strain_1": low_strain_x["strain"],
                        "strain_2": low_strain_x["strain"],

                        "graph_rep_1": low_strain_x["graph_rep"],
                        "graph_rep_2": low_strain_x["graph_rep"],
                        }
                    )

            else:
                print("hmm, hexagonal lattice with different lattice vectors")
                skip_i = True
                continue
            #__|

        elif round(angle, 5) == 90.0:
            #| - Orthogonal Square Lattice
            print("Orthogonl cell - Good!")

            slab_latt_vect_x = slab_i.cell[0][0]
            slab_latt_vect_y = slab_i.cell[1][1]

            strain_1 = find_low_strain_comb(x_vect, slab_latt_vect_x, graph_cc_ideal=graph_bond_d_real, dir="x")
            strain_2 =find_low_strain_comb(y_vect, slab_latt_vect_y, graph_cc_ideal=graph_bond_d_real, dir="y")

            low_strain_x = min(strain_1, key=lambda x:abs(x["strain"]))
            low_strain_y = min(strain_2, key=lambda x:abs(x["strain"]))

            entry_i.update(
                {
                    "cell_geom": "ortho",

                    "graph_rep_1": low_strain_x["graph_rep"],
                    "graph_rep_2": low_strain_y["graph_rep"],

                    "strain_1": low_strain_x["strain"],
                    "strain_2": low_strain_y["strain"],
                    }
                )
            #__|

        else:
            #| - Neither Hex or Orth (Don't know what to do)
            print("Skip - Bad!!")
            continue
            #__|

        if skip_i:
            continue

        tot_strain = abs(entry_i["strain_1"]) + abs(entry_i["strain_2"])
        print("Tot Strain: " + str(tot_strain))
        supp_area = entry_i["supp_rep_1"] * entry_i["latt_vect_1"] + entry_i["supp_rep_2"] * entry_i["latt_vect_2"]
        print("Area: " + str(supp_area))

        # if supp_area < max_area and tot_strain < max_strain:
        # else:
        #     continue
        master_list.append(entry_i)
        #__|

        # sys.exit(0)

    pickle.dump(master_list, open("master_data.pickle", "wb"))
#__| **************************************************************************

#| - Pandas Dataframe *********************************************************

#| - Creating DataFrame
if load_data:
    master_list = pickle.load(open("master_data.pickle", "rb"))

df = pd.DataFrame(master_list)
#__|

#| - Adding Derived Columns
df["abs_strain_x"] = abs(df["strain_1"])
df["abs_strain_y"] = abs(df["strain_2"])

df["supp_area"] = df["latt_vect_1"] * df["latt_vect_2"]
df["tot_strain"] = df["abs_strain_y"] + df["abs_strain_x"]

df["temp"] = df["bulk"].astype(str) + df["cell_geom"].astype(str) + \
             df["strain_1"].astype(str) + df["strain_2"].astype(str) + \
             df["surface"].astype(str)

# df.to_csv("data.csv")

col_order = list(df)


col_list = ["tot_strain", "surface", "bulk", "supp_area", "root_cut"]
col_list = list(reversed(col_list))

for col_name in col_list:
    if  col_name in col_order:
        col_order.remove(col_name)
        col_order.append(col_name)
        # col_order.insert(0, col_name)

df = df[col_order]
#__|

#| - Creating Atoms Files Directory
if not os.path.exists("atoms_files"):
    os.makedirs("atoms_files")
#__|

grouped = df.groupby(["bulk", "surface"])
for name, group_i in grouped:
    print(name)

    #| - Filteriing DataFrame For Low Strain and Low Area
    filt_i = group_i
    filt_i = filt_i.loc[filt_i["tot_strain"] < max_strain]
    filt_i = filt_i.loc[filt_i["supp_area"] < max_area]
    filt_i = filt_i.sort_values("supp_area").drop_duplicates("temp").sort_index()
    #__|

    for index, row_i in filt_i.iterrows():

        #| - Parameters_i
        g_x = row_i["graph_rep_1"]
        g_y = row_i["graph_rep_2"]
        s_x = row_i["supp_rep_1"]
        s_y = row_i["supp_rep_2"]
        supp_latt_unit_1 = row_i["supp_rep_1"]
        supp_latt_unit_2 = row_i["supp_rep_2"]
        latt_geom = row_i["cell_geom"]
        func = row_i["ase_slab_function"]
        lattice_constant_i = row_i["lattice_constant"]
        #__|

        #| - Create Atoms Object
        # layers_z, vacuum

        def create_comb_atoms(df_series, layers_z, vacuum):
            """
            """
            #| - create_comb_sys

            #| - Parameters_i
            g_x = df_series["graph_rep_1"]
            g_y = df_series["graph_rep_2"]
            s_x = df_series["supp_rep_1"]
            s_y = df_series["supp_rep_2"]
            supp_latt_unit_1 = df_series["supp_rep_1"]
            supp_latt_unit_2 = df_series["supp_rep_2"]
            latt_geom = df_series["cell_geom"]
            func = df_series["ase_slab_function"]
            lattice_constant_i = df_series["lattice_constant"]
            #__|

            #| - Creating Bare Slab

            orth_cell = False
            print("TEMP TEMP TEMP - 180301")
            if bulk == "bcc" and surf == "110":
                orth_cell = True

            slab_i = func(
                metal,
                size=(supp_latt_unit_1, supp_latt_unit_2, layers_z),
                a=lattice_constant_i,
                vacuum=vacuum,
                orthogonal=orth_cell,
                )

            root_i = row_i["root_cut"]
            if root_i == 0:
                slab_i = slab_i
            else:
                slab_i = root_surface(slab_i, root_i)
            #__|

            #| - Adding Graphene
            if latt_geom == "ortho":
                out_atoms_i = create_comb_sys(slab_i, g_x, g_y, out_file=None)

            elif latt_geom == "hex":
                out_atoms_i = add_graphene_layer(slab_i, graphene_units=g_x, graph_surf_d=1.885)
            #__|

            #| - Atoms File Name
            atom_name = [
                str(df_series["bulk"]),
                str(df_series["surface"]),
                "root-" + str(df_series["root_cut"]),
                str(df_series["cell_geom"]),
                str(df_series["supp_rep_1"]),
                str(df_series["supp_rep_2"]),
                "strain-" + str(round(df_series["tot_strain"], 3)),
                "area-" + str(round(df_series["supp_area"], 3)),
                ]

            atom_name = "_".join(atom_name) + ".traj"
            #__|

            out_atoms_i.write("atoms_files/" + atom_name)

            #__|

        create_comb_atoms(row_i, layers_z, vacuum=10)
        #__|

#__| **************************************************************************
