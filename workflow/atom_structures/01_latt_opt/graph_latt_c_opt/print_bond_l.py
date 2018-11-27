import pickle

bond_l_lst = pickle.load(open("bond_l_lst.pickle", "r"))

for i, val in enumerate(bond_l_lst):

    print(str(i) + " | " + str(val))
