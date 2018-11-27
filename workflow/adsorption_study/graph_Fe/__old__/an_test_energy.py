from energetics.dft_energy import Energy, Element_Refs

E_pot = -32.920
E_ZPE = 0.280
Cv_trans = 0.039
Cv_rot = 0.026
Cv_vib = 0.000
Cv_to_Cp = 0.026

S_tot = 0.406


# En = Energy(
#     electronic_e = E_pot,
#     zero_point_e = E_ZPE,
#
#     Cv_trans_term = Cv_trans,
#     Cv_rot_term = Cv_rot,
#     Cv_vib_term = Cv_vib,
#     Cv_to_Cp = Cv_to_Cp,
#
#     entropy_term = S_tot,
#     )

Refs = Element_Refs()
