dft_params = {
  "kpts": [
    "3",
    "3",
    "1"
  ],
  "parflags": None,
  "xc": "BEEF-vdW",
  "nbands": -20,
  "convergence": {
    "nmix": 10,  # Decreased nmix from 20 to 10, not sure if this helps
    "diag": "david",
    "energy": 2e-04,  #
    "mixing_mode": "plain",  # Changed the mixing_mode to from 'local-TF', this converged better
    "maxsteps": 600,  # Increased maxsteps per SCF cycle
    "mixing": 0.1
  },
  "dw": 4000.0,
  "outdir": "calcdir",
  "pw": 400,
  "noncollinear": False,
  "dipole": {
    "status": False
  },
  "beefensemble": True,
  "printensemble": True,
  "output": {
    "removesave": True
  },
  "sigma": 0.005,
  "spinpol": True,
}
