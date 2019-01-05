#!/usr/bin/env python

"""DFT relaxation w/ additional anaylsis.

Author: Raul A. Flores
"""

#| - IMPORT MODULES
import os
import sys
import pickle

# MY MODULES
from ase_modules.ase_methods import (
    thermochem_harm_corr,
    )
#__|


root_dir = os.getcwd()
for dirName, subdirList, fileList in os.walk(root_dir):
    if "vib_modes.pickle" in fileList:
        # print(fileList)

    # if "gibbs_corr.out" in fileList:
    #     print(dirName)
    #     os.system("rm -r " + dirName)
    #     print("found gibbs_corr.out ######")


        os.chdir(dirName)

        os.system("pwd")
        os.chdir("..")
        # os.system("cd ..")
        # os.system("ls")
        os.system("pwd")

        print(20 * "_")

        vib_modes = pickle.load(open("dir_vib/vib_modes.pickle", "r"))
        tmp = thermochem_harm_corr(vib_modes)
        os.chdir(root_dir)
