#!/usr/bin/env python

"""TEMP.

Author: Raul A. Flores
"""

#| - IMPORT MODULES



#__|


def point_plot_settings(
    i_ind,
    index,
    row,
    hover_text_row="notes",
    border_color_list=None,
    system_color_map=None,
    ):
    """

    N_graph_Fe
    Fe_slab
    graph_Fe
    graphene
    """
    #| - point_plot_settings

    ads_site_i = row.name[0]
    system_i = row.name[1]
    spinpol_i = row.name[2]

    # print(ads_site_i)
    # print(system_i)
    # print(spinpol_i)
    # print("______")
    # system_color_map[""]

    if system_i == "N_graph_Fe":
        color_i = system_color_map["N_graph_Fe"]
    elif system_i == "Fe_slab":
        color_i = system_color_map["Fe_slab"]
    elif system_i == "graph_Fe":
        color_i = system_color_map["graph_Fe"]
    elif system_i == "graphene":
        color_i = system_color_map["graphene"]
    else:
        print("Color couldn't be found")

    system = row.name[1]
    if system == "N_graph_Fe":
        marker_line = border_color_list[0]
    if system == "graph_Fe":
        marker_line = border_color_list[1]
    if system == "graphene":
        marker_line = border_color_list[2]
    if system == "Fe_slab":
        marker_line = border_color_list[3]

    hover_text = row[hover_text_row]

    if i_ind == 0:
        show_leg = True
    else:
        show_leg = False

    if row["ooh-notes"] == "Desorbed":
        marker_sym = "x"
    elif row["oh-notes"] == "Desorbed":
        marker_sym = "x"
    elif row["o-notes"] == "Desorbed":
        marker_sym = "x"

    elif row["ooh-notes"] == "Dissociated":
        marker_sym = "diamond"
    elif row["oh-notes"] == "Dissociated":
        marker_sym = "diamond"
    elif row["o-notes"] == "Dissociated":
        marker_sym = "diamond"

    else:
        marker_sym = "circle"

    out_dict = {
        "marker_symbol": marker_sym,
        "show_legend": show_leg,
        "hover_text": hover_text,
        "marker_line": marker_line,
        "sys_color": color_i,
        # "marker_sym":,
        }

    return(out_dict)
    #__|
