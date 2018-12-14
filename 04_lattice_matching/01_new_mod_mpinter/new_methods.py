"""Modified MPInterface methods to return all heterostructures found.

Author: Raul A. Flores
"""

# | - Import Modules
import sys

import pickle
import numpy as np
from pymatgen.core.structure import Structure
from pymatgen.core.lattice import Lattice

from mpinterfaces.transformations import (
    # get_aligned_lattices,
    # get_matching_lattices,

    # Structure,
    generate_all_configs,
    get_mismatch,
    get_angle,
    get_area,
    get_r_list,
    reduced_supercell_vectors,
    )

from math import sqrt

# from mpinterfaces.utils import slab_from_file
from mpinterfaces.interface import Interface
#__|

def create_heterostructure(
    bulk_structure=None,
    slab_structure=None,

    strain_sys="overlayer",  # 'support' or 'overlayer'

    surface_cut=[0, 0, 1],
    separation=3,
    nlayers_2d=1,
    nlayers_substrate=4,

    # Lattice matching algorithm parameters
    max_area=40,
    max_mismatch=1,
    max_angle_diff=0.1,
    r1r2_tol=0.01,
    ):
    """

    bulk_structure:
        ase atoms object for the support material
    slab_structure:
        overlayer material

    strain_sys:
    surface_cut:
    separation:
    nlayers_2d:
    nlayers_substrate:
    max_area:
    max_mismatch:
    max_angle_diff:
    r1r2_tol:

    """
    #| - create_heterostructure
    # substrate_bulk = Structure.from_file(bulk_filename)

    substrate_slab = Interface(
        bulk_structure,
        # substrate_bulk,
        hkl=surface_cut,
        min_thick=20,
        min_vac=30,
        primitive=False,
        from_ase=True,
        )

    # mat2d_slab = slab_from_file([0, 0, 1], graphene_filename)
    mat2d_slab = slab_structure

    if strain_sys == "support":
        lower_mat = mat2d_slab
        upper_mat = substrate_slab
    elif strain_sys == "overlayer":
        lower_mat = substrate_slab
        upper_mat = mat2d_slab

    # mat2d_slab_aligned, substrate_slab_aligned = get_aligned_lattices(
    # lower_mat_aligned, upper_mat_aligned = get_aligned_lattices(
    all_aligned_lattices = get_aligned_lattices(
        lower_mat,
        upper_mat,
        max_area=max_area,
        max_mismatch=max_mismatch,
        max_angle_diff=max_angle_diff,
        r1r2_tol=r1r2_tol,
        )
    # return(tmp)
    # return(lower_mat_aligned, upper_mat_aligned)
    hetero_interfaces_list = []
    for aligned_lattices_i in all_aligned_lattices:
        lower_mat_aligned = aligned_lattices_i[0]
        upper_mat_aligned = aligned_lattices_i[1]

        if strain_sys == "support":
            mat2d_slab_aligned = lower_mat_aligned
            substrate_slab_aligned = upper_mat_aligned
        elif strain_sys == "overlayer":
            mat2d_slab_aligned = upper_mat_aligned
            substrate_slab_aligned = lower_mat_aligned


        # # Writing hetero_interfaces to pickle file
        # with open('aligned_latt_materials.pickle', 'wb') as fle:
        #     pickle.dump((substrate_slab_aligned, mat2d_slab_aligned), fle)
        #
        # substrate_slab_aligned.to(filename='00_substrate_opt.POSCAR')
        # mat2d_slab_aligned.to(filename='00_graphene_opt.POSCAR')


        # merge substrate and mat2d in all possible ways
        hetero_interfaces = generate_all_configs(
            mat2d_slab_aligned,
            substrate_slab_aligned,
            nlayers_2d,
            nlayers_substrate,
            separation,
            )

        # # Writing hetero_interfaces to pickle file
        # with open('hetero_interfaces.pickle', 'wb') as fle:
        #     pickle.dump(hetero_interfaces, fle)

        # TEMP | Only appending the first entry because they are all just
        # translations of the 2D material
        hetero_interfaces_list.append(hetero_interfaces[0])

        # return(hetero_interfaces)

    return(hetero_interfaces_list)
    #__|


def get_aligned_lattices(
    slab_sub,
    slab_2d,
    max_area=200,
    max_mismatch=0.05,
    max_angle_diff=1,
    r1r2_tol=0.2,
    ):
    """
    given the 2 slab structures and the alignment paramters, return
    slab structures with lattices that are aligned with respect to each
    other
    """
    #| - get_aligned_lattices

    def process_sys(
        slab_sub,
        slab_2d,
        uv_substrate,
        uv_mat2d,
        ):
        """
        """
        #| - process_sys
        substrate = Structure.from_sites(slab_sub)
        mat2d = Structure.from_sites(slab_2d)
        # map the intial slabs to the newly found matching lattices
        substrate_latt = Lattice(
            np.array(
                [
                    uv_substrate[0][:],
                    uv_substrate[1][:],
                    substrate.lattice.matrix[2, :]
                    ]
                )
            )

        # to avoid numerical issues with find_mapping
        mat2d_fake_c = mat2d.lattice.matrix[2, :] / np.linalg.norm(
            mat2d.lattice.matrix[2, :]) * 5.0
        mat2d_latt = Lattice(
            np.array(
                [
                    uv_mat2d[0][:],
                    uv_mat2d[1][:],
                    mat2d_fake_c
                    ]
                )
            )

        mat2d_latt_fake = Lattice(
            np.array(
                [
                    mat2d.lattice.matrix[0, :],
                    mat2d.lattice.matrix[1, :],
                    mat2d_fake_c
                    ]
                )
            )

        _, __, scell = substrate.lattice.find_mapping(substrate_latt,
                                                      ltol=0.05,
                                                      atol=1)
        scell[2] = np.array([0, 0, 1])
        substrate.make_supercell(scell)
        _, __, scell = mat2d_latt_fake.find_mapping(mat2d_latt,
                                                    ltol=0.05,
                                                    atol=1)
        scell[2] = np.array([0, 0, 1])
        mat2d.make_supercell(scell)
        # modify the substrate lattice so that the 2d material can be
        # grafted on top of it
        lmap = Lattice(
            np.array(
                [
                    substrate.lattice.matrix[0, :],
                    substrate.lattice.matrix[1, :],
                    mat2d.lattice.matrix[2, :]
                    ]
                )
            )

        mat2d.modify_lattice(lmap)

        return(substrate, mat2d)
    #__|


    # get the matching substrate and 2D material lattices
    # uv_substrate, uv_mat2d = get_matching_lattices(
    all_matching_lattices = get_matching_lattices(
        slab_sub,
        slab_2d,
        max_area=max_area,
        max_mismatch=max_mismatch,
        max_angle_diff=max_angle_diff,
        r1r2_tol=r1r2_tol,
        )


    sub_mat2d_list = []
    for sys_i in all_matching_lattices:

        uv_substrate, uv_mat2d = sys_i[0], sys_i[1]

        substrate, mat2d = process_sys(
            slab_sub,
            slab_2d,
            uv_substrate,
            uv_mat2d,
            )

        sub_mat2d_list.append(
            (substrate, mat2d)
            )

    # if not uv_substrate and not uv_mat2d:
    #     print("no matching u and v, trying adjusting the parameters")
    #     sys.exit()


    return(sub_mat2d_list)

    # return(substrate, mat2d)

    #| - __old__
    # substrate = Structure.from_sites(slab_sub)
    # mat2d = Structure.from_sites(slab_2d)
    # # map the intial slabs to the newly found matching lattices
    # substrate_latt = Lattice(
    #     np.array(
    #         [
    #             uv_substrate[0][:],
    #             uv_substrate[1][:],
    #             substrate.lattice.matrix[2, :]
    #             ]
    #         )
    #     )
    #
    # # to avoid numerical issues with find_mapping
    # mat2d_fake_c = mat2d.lattice.matrix[2, :] / np.linalg.norm(
    #     mat2d.lattice.matrix[2, :]) * 5.0
    # mat2d_latt = Lattice(
    #     np.array(
    #         [
    #             uv_mat2d[0][:],
    #             uv_mat2d[1][:],
    #             mat2d_fake_c
    #             ]
    #         )
    #     )
    #
    # mat2d_latt_fake = Lattice(
    #     np.array(
    #         [
    #             mat2d.lattice.matrix[0, :],
    #             mat2d.lattice.matrix[1, :],
    #             mat2d_fake_c
    #             ]
    #         )
    #     )
    #
    # _, __, scell = substrate.lattice.find_mapping(substrate_latt,
    #                                               ltol=0.05,
    #                                               atol=1)
    # scell[2] = np.array([0, 0, 1])
    # substrate.make_supercell(scell)
    # _, __, scell = mat2d_latt_fake.find_mapping(mat2d_latt,
    #                                             ltol=0.05,
    #                                             atol=1)
    # scell[2] = np.array([0, 0, 1])
    # mat2d.make_supercell(scell)
    # # modify the substrate lattice so that the 2d material can be
    # # grafted on top of it
    # lmap = Lattice(
    #     np.array(
    #         [
    #             substrate.lattice.matrix[0, :],
    #             substrate.lattice.matrix[1, :],
    #             mat2d.lattice.matrix[2, :]
    #             ]
    #         )
    #     )
    #
    # mat2d.modify_lattice(lmap)
    #
    # return(substrate, mat2d)
    #__|

    #__|


def get_matching_lattices(
    iface1,
    iface2,
    max_area=100,
    max_mismatch=0.01,
    max_angle_diff=1,
    r1r2_tol=0.02,
    ):
    """
    computes a list of matching reduced lattice vectors that satify
    the max_area, max_mismatch and max_anglele_diff criteria
    """
    #| - get_matching_lattices
    if iface1 is None and iface2 is None:
        # | - iface1 and 2 is None
        # test : the numbers from the paper
        a1 = 5.653
        a2 = 6.481
        # for 100 plane
        ab1 = [[0, a1 / 2, -a1 / 2], [0, a1 / 2, a1 / 2]]
        ab2 = [[0, a2 / 2, -a2 / 2], [0, a2 / 2, a2 / 2]]
        area1 = a1 ** 2 / 2
        area2 = a2 ** 2 / 2
        # for 110 plane
        ab1 = [[a1 / 2, -a1 / 2, 0], [0, 0, a1]]
        ab2 = [[a2 / 2, -a2 / 2, 0], [0, 0, a2]]
        area1 = a1 ** 2 / sqrt(2)
        area2 = a2 ** 2 / sqrt(2)
        # for 111 surface
        # ab1 = [ [a1/2, 0, a1/2], [a1/2, a1/2, 0]]
        # ab2 = [ [a2/2, 0, a2/2], [a2/2, a2/2, 0]]
        # area1 = a1**2 * sqrt(3)/4 #/ 2 /sqrt(2)
        # area2 = a2**2 * sqrt(3)/4 #/ 2 / sqrt(2)
        #__|

    else:
        # | - else
        area1 = iface1.surface_area
        area2 = iface2.surface_area
        # a, b vectors that define the surface
        ab1 = [iface1.lattice.matrix[0, :], iface1.lattice.matrix[1, :]]
        ab2 = [iface2.lattice.matrix[0, :], iface2.lattice.matrix[1, :]]
        # __|

    #| - r_list
    print('initial values:\nuv1:\n{0}\nuv2:\n{1}\n '.format(ab1, ab2))
    r_list = get_r_list(area1, area2, max_area, tol=r1r2_tol)
    if not r_list:
        print(
            'r_list is empty.',
            ' Try increasing the max surface area or/and the other',
            ' tolerance paramaters',
            )
        sys.exit()
    #__|

    # | - Searching For-loop
    found = []
    print('searching ...')
    for r1r2 in r_list:
        uv1_list, tm1_list = reduced_supercell_vectors(ab1, r1r2[0])
        uv2_list, tm2_list = reduced_supercell_vectors(ab2, r1r2[1])
        if not uv1_list and not uv2_list:
            continue
        for i, uv1 in enumerate(uv1_list):
            for j, uv2 in enumerate(uv2_list):
                u_mismatch = get_mismatch(uv1[0], uv2[0])
                v_mismatch = get_mismatch(uv1[1], uv2[1])
                angle1 = get_angle(uv1[0], uv1[1])
                angle2 = get_angle(uv2[0], uv2[1])
                angle_mismatch = abs(angle1 - angle2)
                area1 = get_area(uv1)
                area2 = get_area(uv2)
                if abs(u_mismatch) < max_mismatch and abs(
                        v_mismatch) < max_mismatch:
                    max_angle = max(angle1, angle2)
                    min_angle = min(angle1, angle2)
                    mod_angle = max_angle % min_angle
                    is_angle_factor = False
                    if abs(mod_angle) < 0.001 or abs(
                            mod_angle - min_angle) < 0.001:
                        is_angle_factor = True
                    if angle_mismatch < max_angle_diff or is_angle_factor:
                        if angle_mismatch > max_angle_diff:
                            if angle1 > angle2:
                                uv1[1] = uv1[0] + uv1[1]
                                tm1_list[i][1] = tm1_list[i][0] + tm1_list[i][
                                    1]
                            else:
                                uv2[1] = uv2[0] + uv2[1]
                                tm2_list[j][1] = tm2_list[j][0] + tm2_list[j][
                                    1]

                        found.append(
                            (
                                uv1, uv2, min(area1, area2),
                                u_mismatch,
                                v_mismatch,
                                angle_mismatch,
                                tm1_list[i],
                                tm2_list[j],
                                )
                            )
    #__|

    if found:

        return(found)

        #| - If structure found
        # print('\nMATCH FOUND\n')
        # uv_opt = sorted(found, key=lambda x: x[2])[0]
        # print('optimum values:\nuv1:\n{0}\nuv2:\n{1}\narea:\n{2}\n'.format(
        #     uv_opt[0], uv_opt[1], uv_opt[2]))
        # print('optimum transition matrices:\ntm1:\n{0}\ntm2:\n{1}\n'.format(
        #     uv_opt[6], uv_opt[7]))
        # print('u,v & angle mismatches:\n{0}, {1}, {2}\n'.format(uv_opt[3],
        #                                                         uv_opt[4],
        #                                                         uv_opt[5]))
        # return uv_opt[0], uv_opt[1]
        #__|

    else:
        # | - else
        print('\n NO MATCH FOUND')
        return None, None
        #__|

    #__|
