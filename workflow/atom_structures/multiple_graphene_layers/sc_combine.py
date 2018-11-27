from ase import io
atoms_orig = io.read("fe_graph.traj")
atoms_graph = io.read("graphene.traj")
atoms_new = atoms_orig.extend(atoms_graph)
atoms_new.write("out.traj")
