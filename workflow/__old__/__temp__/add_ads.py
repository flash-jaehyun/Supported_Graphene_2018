#| - IMPORT MODULES
from ase import io
from ase.build import add_adsorbate

from ase_modules.adsorbates import Adsorbate
#__|

Ads = Adsorbate()

        # OO_bl=1.359,
        # OH_bl=0.993,
        # OO_angle=30.,
        # H_up_down="down",

ads = Ads.get_adsorbate("h2o",
    # OO_angle=30.,
    H_up_down="up",
    )

# ads.rotate(180, "x")

# ads = Ads.get_adsorbate("ooh", OO_bl=1.359)
atoms = io.read("init.traj")
add_adsorbate(atoms, ads, 4, position=[0.355, -0.615])
atoms.write("out.traj")
