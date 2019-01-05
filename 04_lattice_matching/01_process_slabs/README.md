# 01 | Process Slabs
___

Processing output from 00_run_all_jobs (workflow which constructed all
possible heterointerfaces between support metal and graphene)

The resulting output is stored in a `job_dataframe.pickle` file which is
stored in:
`$PROJ_DATA/01_fe_graph_proj/04_lattice_matching/181218_data`

File is over 1GB in size
(raw data not included in repo)

## an_process_systems.ipynb
The Jupyter notebook, `an_process_systems.ipynb`, processes the data by
performing the following operations:

1. Rotate the unit cell lattice vectors such that:
    * The a-vector is pointed along the x-axis
    * The b-vector is points toward the 1st quadrant (upper right corner of +)
        * Multiply b-vector by -1
    * This is a purely aesthetic manipulation
2. Wraps atoms to be within the unit cell
    * Using periodic boundary conditions
3. Mirror system along xy-plane if the graphene layer is below the support
4. Set support slab thickness by removing atoms below a certain cutoff
5. Constrain lower `frac_constr` fraction of support slab atoms
6. Center atoms in cell
7. Add an appropriate amount of vacuum


Additionally, to filter the thousands of systems produced from
`00_run_all_jobs` the following filters/criteria were imposed:

1. Remove duplicate systems
    * This is done in a very crude way, essentially if 2 systems have the same
    support atom, facet type, and also have the exact same area they are
    considered to be identical
        * This can certainly be improved although I was having issues with
2. Removing systems that were too long (same as not square enough) by imposing
a cutoff criteria between the ratio of the shortest and longest lattice
vector.
3. Removing systems that were too big, with the number of metal/support atoms
being the main criteria


## methods.py
Methods used within `an_process_systems.ipynb`


## \__test__
Smaller version of `$PROJ_DATA/~/job_dataframe.pickle` used for testing
purposes
