# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""Experimental crystollography data.


Raul Materials: Co, Ni, Mo


Kevin Materials: Ru, Rh, W


Author: Raul A. Flores
"""

most_stable_crystal_structure_dict = {
    # FCC
    "Ni": "fcc",
    "Rh": "fcc",

    # HCP
    "Co": "hcp",
    "Ru": "hcp",

    # BCC
    "Mo": "bcc",
    "W": "bcc",
    }

# All lattice constants are in A
exp_latt_const_dict = {

    #| - Nickel
    "Ni": {
        # Most stable <--------------------------------------------------------
        "fcc": {
            "a": 3.524,
            },

        # Article title:
        # Structure transition and magnetism of bcc-Ni nanowires
        "bcc": {
            "a": 2.88,
            },

        "hcp": {
            "a": None,
            "c": None,
            },
        },
    #__|

    #| - Cobalt
    "Co": {
        "fcc": {
            "a": None,
            },

        "bcc": {
            "a": None,
            },

        # Most stable <--------------------------------------------------------
        "hcp": {
            "a": 2.5071,
            "c": 4.0695,
            },
        },
    #__|

    #| - Ruthenium
    "Ru": {
        "fcc": {
            "a": None,
            },

        "bcc": {
            "a": None,
            },

        # Most stable <--------------------------------------------------------
        "hcp": {
            "a": 2.7059,
            "c": 4.2815,
            },
        },
    #__|

    #| - Rhodium
    "Rh": {
        "fcc": {
            "a": 3.8034,
            },

        "bcc": {
            "a": None,
            },

        # Most stable <--------------------------------------------------------
        "hcp": {
            "a": None,
            "c": None,
            },
        },
    #__|

    #| - Molybdenum
    "Mo": {
        "fcc": {
            "a": None,
            },

        # Most stable <--------------------------------------------------------
        "bcc": {
            "a": 3.147,
            },

        "hcp": {
            "a": None,
            "c": None,
            },
        },
    #__|

    #| - Tungsten
    "W": {

        # FACE CENTERED CUBIC TUNGSTEN FILMS OBTAINED BY
        "fcc": {
            "a": 4.15,
            },

        # Most stable <--------------------------------------------------------
        "bcc": {
            "a": 3.1652,
            },

        "hcp": {
            "a": None,
            "c": None,
            },
        },
    #__|

    }
