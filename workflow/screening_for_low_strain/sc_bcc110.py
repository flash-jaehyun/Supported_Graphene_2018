from ase.build import bcc110



bcc_latt_const = 2.7576
graph_bond_d_real = 1.4237

atoms = bcc110(
    "Fe",
    size=(2,2,1),
    a=bcc_latt_const,
    vacuum=10.,
    orthogonal=True,
    )

atoms.write("temp.traj")
