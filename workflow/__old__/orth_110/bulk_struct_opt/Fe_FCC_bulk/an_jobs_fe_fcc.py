#| - IMPORT MODULES
from dft_job_automat.job_analysis import DFT_Jobs_Analysis

import sys

from ase import io
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
#__|

#| - SCRIPT INPUTS
regr_fit_order = 3
length_var = "lattice_parameter"

# Mitigate discontinuity in V vs bondlength
bond_length_cutoff = 3.43
#__|

Jobs = DFT_Jobs_Analysis(system="aws", update_job_state=False)

df = Jobs.data_frame
df.to_csv("out.csv")

#| - Regression
x_min = df.loc[df[length_var].idxmin()][length_var]
x_max =df.loc[df[length_var].idxmax()][length_var]
bounds = [x_min, x_max]

finite_e = np.isfinite(df["elec_energy"]) == True
df = df[finite_e]

# df = df[df.job_state == "complete"]
df = df.drop(df[df.bond_length < bond_length_cutoff].index)

min_e = df["elec_energy"].min()
df["elec_energy"] = df["elec_energy"] - min_e

regr_dict = {}
for key, grp in df.groupby(["kpoints"]):
    x_arr = grp.loc[: , length_var]
    y_arr = grp.loc[: , "elec_energy"]
    idx = np.isfinite(x_arr) & np.isfinite(y_arr)
    regr_coef = np.poly1d(np.polyfit(x_arr[idx], y_arr[idx], regr_fit_order))
    regr_dict[key] = regr_coef

# Taking derivatives polynomial regression and finding curve minimum
for kpoints, coefficients in regr_dict.iteritems():
    crit_points = [x for x in coefficients.deriv().r if x.imag == 0 and bounds[0] < x.real < bounds[1]]
    print(kpoints)
    print(crit_points)
#__|


#| - Plotting
# df = df[df.lattice_parameter == df.lattice_parameter.values[13]]

fig, ax = plt.subplots()
labels = []
for key, grp in df.groupby(["kpoints"]):
    ax = sns.regplot(length_var, "elec_energy", data=grp, ax=ax, label=key, fit_reg=False, marker=".", scatter_kws={'s':60})
    labels.append(key)

lines, _ = ax.get_legend_handles_labels()
ax.legend(lines, labels, loc="best")
plt.show()
#__|
