#| - IMPORT MODULES
import os
import sys
import pickle
import operator
import matplotlib.pyplot as plt
#__|


#| - Opening Bond Length List File
with open("bond_l_lst.pickle", "r") as f:
    bond_l_lst = pickle.load(f)
#__|


#| - TEMP
data_lst = []
for index, bond_l in enumerate(bond_l_lst):
    # print(str(index) + ": " + str(bond_l))

    fold_name = str(index).zfill(2) + "-jd"
    # print(tmp)

    prop_lst = {}
    # prop_lst["energy"] = []

    prop_lst["bond_l"] = bond_l

    e_lst = []
    f_lst = []
    # with open("./" + fold_name + "/_1/simulation/qn.log") as f:
    with open("./" + fold_name + "/_1/qn.log") as f:
        content = f.readlines()

        for line in content:

            e_lst.append(float(line.split()[4]))
            f_lst.append(float(line.split()[5]))

        prop_lst["forces"] = f_lst
        prop_lst["energies"] = e_lst


    data_lst.append(prop_lst)
#__|


tmp = [x["energies"][-1] for x in data_lst]
tmp2 = [x["bond_l"] for x in data_lst]


#| - Writing Energy and Bond Length to CSV
import csv

with open('e_vs_bondl.csv', 'w') as f:
    writer = csv.writer(f, delimiter=' ')
    writer.writerows(zip(tmp,tmp2))

#__|


min_index, min_value = min(enumerate(tmp), key=operator.itemgetter(1))


#| - Plotting
# plt.plot(norm_data[0], norm_data[1])
plt.plot(tmp2, tmp, linestyle="",marker="o")
# plt.show()
#__|
