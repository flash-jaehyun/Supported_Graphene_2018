#| - IMPORT MODULES
from ase.build import graphene_nanoribbon
from ase.io import read, write

import math
#__|

gr = graphene_nanoribbon(3, 3, type='armchair', saturated=False)



theta_rot = 90
phi_rot = 0
psi_rot = 0

theta_rot	= math.pi/180.*theta_rot
phi_rot		= math.pi/180.*phi_rot
psi_rot		= math.pi/180.*psi_rot

gr.rotate_euler(phi = phi_rot , theta = theta_rot , psi = psi_rot )

write("gnr1.traj",gr)
