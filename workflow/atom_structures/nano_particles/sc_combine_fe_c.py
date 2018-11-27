from ase import io

atoms_c = io.read("fe_bulk_03.cif")
atoms_fe = io.read("c_60.cif")

atoms_combined = atoms_c + atoms_fe

atoms_combined.write("out_02.cif")
