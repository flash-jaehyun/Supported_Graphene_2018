# Cleaning script, return dir to original state

echo "Cleaning directory"
rm -r 01_heterostructures_outdir __pycache__

rm -r 00_graphene_opt.POSCAR
rm -r 00_substrate_opt.POSCAR
rm -r 01_heterostructures
rm -r aligned_latt_materials.pickle
# rm -r clean.sh
# rm -r facet.json
rm -r hetero_interfaces.pickle
# rm -r init_graphene.cif
# rm -r init_support.cif
# rm -r model.py
rm -r tmp.POSCAR
