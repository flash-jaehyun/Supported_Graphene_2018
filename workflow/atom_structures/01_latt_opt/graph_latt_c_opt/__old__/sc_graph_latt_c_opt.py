#| - Import Modules
import os
import numpy as np
import shutil
import pickle

from ase import io
from ase.build import graphene_nanoribbon
#__|


#| - Script Parameters
graph_bond_l = 1.42

bond_l_range = (1.3, 1.5)
resolution = 0.002
#__|


#| - Range of Bond Lengths
bond_l_lst = []
entry_i = bond_l_range[0]
while entry_i < bond_l_range[1]:
    bond_l_lst.append(entry_i)
    entry_i += resolution
bond_l_lst.append(bond_l_range[1])
#__|

"""
# Writing pickle file
with open("bond_l_lst.pickle", "w") as f:
    pickle.dump(bond_l_lst, f)

cwd = os.getcwd()
for i_cnt, bond_l in enumerate(bond_l_lst):

    # file_name = str(i_cnt).zfill(2) + "-" + '%.5f' % bond_l + "-jd/_1"
    file_name = str(i_cnt).zfill(2) + "-jd/_1"

    if os.path.exists(file_name):
        # shutil.rmtree(file_name)
        mess = "Folder already exists: " + str(file_name)
        print(mess)

    elif not os.path.exists(file_name):
        os.makedirs(file_name)


        graphene = graphene_nanoribbon(2, 1, type='zigzag', saturated=False,
        C_C=bond_l, sheet=True, vacuum=15.0)
        io.write(file_name + "/" + "POSCAR", graphene)
        shutil.copy2("model.py", file_name)

        os.chdir(file_name)
        comm = "/home/raul_ubuntu/matr.io/bin/trisub -q small"
        # os.system(comm)

        os.chdir(cwd)
"""
