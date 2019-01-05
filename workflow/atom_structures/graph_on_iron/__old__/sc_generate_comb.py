#| - Import Modules
from ase import io
from ase import Atoms
from ase import build
from ase.build import *
from ase.visualize import view
#__|

#ag: 4.202
#au: 4.209
#cu: 3.688
#pt: 4.027

#| - Metal Surface
metal='Fe'
a=3.688

#Integer
slab=fcc111(metal, size=(2,2,4), a=a)

#Root
#slab=fcc111_root(metal, root=3, size=(1,1,1), a=a)

metal_lattice=slab.get_cell()
#__|

#| - MOxHy
############## MOxHy ##########################3

oxide=io.read('gnr1.traj')

#Integer
#b=2
#ad=make_supercell(oxide, [(b,0,0),(0,b,0),(0,0,1)])
#Root

ad=root_surface(oxide, root=3)


# ad.rotate(-120,'z')
#New Lattice

ad_lattice=ad.get_cell()
c=metal_lattice[0][0]/ad_lattice[0][0]
ad.set_cell((c*ad_lattice[0],c*ad_lattice[1],ad_lattice[2]), scale_atoms=True)
#__|

########## Add #########3
add_adsorbate(slab, ad, 2)
slab.center(vacuum=7, axis=2)

io.write('slab.traj', slab)
