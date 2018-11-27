"""Processing ORR Adsorption Energetics."""

#| - IMPORT MODULES
import sys
import copy
import os
import time

import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None

# import plotly
# import plotly.graph_objs as go

import plotly
# plotly.__version__
import plotly.plotly as py
from plotly.grid_objs import Grid, Column


# My Modules
from dft_job_automat.job_analysis import DFT_Jobs_Analysis
from  dft_job_automat.job_types_classes.dft_methods import DFT_Methods

# from orr_reaction.orr_methods import ORR_Free_E_Plot, process_orr_adsorbates_fed
from orr_reaction.orr_methods import ORR_Free_E_Plot
#__|

#| - SCRIPT INPUTS
color_list = [
    "rgb(37,69,0)",
    "rgb(0,76,214)",
    "rgb(168,0,15)",
    "rgb(0,85,162)",
    "rgb(255,113,196)",
    ]

interp_points = 100
#__|

#| - FUNCTIONS
def extract_e(atoms_list, index=-1):
    """
    """
    #| - extract_e
    e_list = []
    for image in atoms_list:
        e_i = image.get_potential_energy()
        e_list.append(e_i)

    print(len(e_list))
    print(e_list)

    atoms = atoms_list[index]
    e_out = atoms.get_potential_energy()

    return(e_out)
    #__|

def extract_e_list(atoms_list, interp_points=100):
    """
    """
    #| - extract_e_list
    e_list = []
    for image in atoms_list:
        e_i = image.get_potential_energy()
        e_list.append(e_i)

    x_vals_0 = range(len(e_list))
    x_vals_interp = np.linspace(0, len(e_list) - 1, interp_points)

    e_list_interp = np.interp(x_vals_interp, x_vals_0, e_list)

    return(e_list_interp)
    #__|

def return_ith_e(e_list, ind):
    """
    """
    #| - return_ith_e
    return(e_list[ind])
    #__|

#__|

#| - Reference Energies
bare_slab = -31722.653798

# Using Water for Oxygen Reference
hyd_ref = -32.920360 / 2.
h2o_ref = -476.63
oxy_ref = h2o_ref - 2. * hyd_ref
#__|

#| - Initiate Instance
compenv = os.environ["COMPENV"]
if compenv == "wsl":
    load_dataframe = True
    update_job_state = False
else:
    load_dataframe = False
    update_job_state = True


dft_inst = DFT_Methods(
    methods_to_run=[
        "elec_energy",
        "atom_type_num_dict",
        "atoms_object",
        ],
    )

Jobs = DFT_Jobs_Analysis(
    update_job_state=update_job_state,
    job_type_class=dft_inst,
    load_dataframe=load_dataframe,
    working_dir="1STEP",
    )
#__|

#| - Data Processing
df = Jobs.data_frame

df["e_list"] = df["atoms_object"].apply(extract_e_list, interp_points=interp_points)

#| - Finding Minimum Energy
e_min_list = []
for index, row in df.iterrows():
    min_i = row["e_list"].min()
    e_min_list.append(min_i)

e_min_list = np.array(e_min_list)
e_min = e_min_list.min()
#__|

df["e_list_norm"] = df["e_list"] - e_min

data_master = []
for i_ind in range(100):
    data = np.zeros((10, 10))
    for index, row in df.iterrows():

        elec_e = row["e_list_norm"][i_ind]
        x_int = row["x_coord"]
        y_int = row["y_coord"]
        data[x_int][y_int] = elec_e
    data_master.append(data)


#| - Plotly Animation

#| - Creating Grid
x = range(10)
y = range(10)

my_columns = [Column(x, "x"), Column(y, "y")]

for i_ind, data_i in enumerate(data_master):
    my_columns.append(Column(data_i, "z{}".format(str(i_ind).zfill(2))))

grid = Grid(my_columns)
py.grid_ops.upload(grid, "graphene_trans_fe111r3r3_" + str(time.time()), auto_open=False)
#__|

#| - Make The Figure
data=[dict(
    type='heatmap',
    xsrc=grid.get_column_reference('x'),
    ysrc=grid.get_column_reference('y'),
    zsrc=grid.get_column_reference('z00'),
    zmin=0,
    zmax=1.68,
    zsmooth='best',
    colorscale="Hot",
    colorbar=dict(thickness=20, ticklen=4),
    )]

title='Iron-Supported Graphene Staggered  <br>'+\
'Configuration Energy Heat Map'

#| - Layout

#| - EXAMPLE TEMP
# # make figure
# figure = {
#     'data': [],
#     'layout': {},
#     'frames': []
# }
#
# # fill in most of layout
# figure['layout']['xaxis'] = {'range': [30, 85], 'title': 'Life Expectancy'}
# figure['layout']['yaxis'] = {'title': 'GDP per Capita', 'type': 'log'}
# figure['layout']['hovermode'] = 'closest'
# figure['layout']['sliders'] = {
#     'args': [
#         'transition', {
#             'duration': 400,
#             'easing': 'cubic-in-out'
#         }
#     ],
#     'initialValue': '0',
#     'plotlycommand': 'animate',
#     'values': [str(i) for i in range(100)],
#     'visible': True
# }
# figure['layout']['updatemenus'] = [
#     {
#         #| - Buttons
#         'buttons': [
#             {
#                 'args': [None, {'frame': {'duration': 500, 'redraw': False},
#                          'fromcurrent': True, 'transition': {'duration': 300, 'easing': 'quadratic-in-out'}}],
#                 'label': 'Play',
#                 'method': 'animate'
#             },
#             {
#                 'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate',
#                 'transition': {'duration': 0}}],
#                 'label': 'Pause',
#                 'method': 'animate'
#             }
#         ],
#         #__|
#
#         'direction': 'left',
#         'pad': {'r': 10, 't': 87},
#         'showactive': False,
#         'type': 'buttons',
#         'x': 0.1,
#         'xanchor': 'right',
#         'y': 0,
#         'yanchor': 'top'
#     }
# ]
#
#__|

layout = dict(
    title=title,
    autosize=False,
    height=900,
    width=900,
    hovermode='closest',
    xaxis=dict(range=[0, 9], autorange=False),
    yaxis=dict(range=[0, 9], autorange=False),
    showlegend=False,

    #| - Slider
    sliders={
        'args': [
            'transition', {
                'duration': 400,
                'easing': 'cubic-in-out'
            }
        ],
        'initialValue': '0',
        'plotlycommand': 'animate',
        'values': [str(i) for i in range(100)],
        'visible': True
        },

    #__|

    #| - UpdateMenus
    updatemenus=[dict(
        type='buttons',
        showactive=False,
        y=1,
        x=-0.05,
        xanchor='right',
        yanchor='top',
        pad=dict(t=0, r=10),

        #| - Buttons
        buttons=[

            dict(
                label='Play',
                method='animate',
                args=[
                    None,
                    dict(frame=dict(duration=100, redraw=True),
                    transition=dict(duration=0),
                    fromcurrent=True,
                    mode='immediate'),
                    ]
                ),

            dict(
                label='Pause',
                method='animate',
                args=[
                    [None],

                    {'frame': {'duration': 0, 'redraw': False},
                    'mode': 'immediate',
                    "transition": {'duration': 0}},
                    ],
                ),


            ],
        #__|

        )],
    #__|

    )
#__|

#| - Frames

sliders_dict = {
    'active': 0,
    'yanchor': 'top',
    'xanchor': 'left',
    'currentvalue': {
        'font': {'size': 20},
        'prefix': 'Year:',
        'visible': True,
        'xanchor': 'right'
    },
    'transition': {'duration': 300, 'easing': 'cubic-in-out'},
    'pad': {'b': 10, 't': 50},
    'len': 0.9,
    'x': 0.1,
    'y': 0,
    'steps': []
}

frames=[dict(
    data=[dict(
        zsrc=grid.get_column_reference('z{}'.format(str(i_ind).zfill(2))),
        zmax=1.68
        )],
    traces=[0],
    name='frame{}'.format(i_ind),

    ) for i_ind in range(len(data_master))
    ]


for i_ind in range(len(data_master)):
    slider_step = {'args': [
        [str(i_ind)],
        {'frame': {'duration': 300, 'redraw': False},
        'mode': 'immediate',
        'transition': {'duration': 300}}
        ],
    'label': str(i_ind),
    'method': 'animate'}
    sliders_dict["steps"].append(slider_step)

layout["sliders"] = [sliders_dict]

fig=dict(data=data, layout=layout, frames=frames)
# plotly.plotly.create_animations()
py.create_animations(fig, filename='animheatmap'+str(time.time()))

#__|

#__|

#__|









sys.exit(0)








energy_label = "new_energy"
df["new_energy"] = df["atoms_object"].apply(extract_e, index=0)
min_e = df[energy_label].min()
df["norm_e"] = df[energy_label] - min_e
#__|

#| - Building Energy Matrix
data = np.zeros((10, 10))
for index, row in df.iterrows():
    # elec_e = row["elec_energy"]
    elec_e = row["norm_e"]
    x_int = row["x_coord"]
    y_int = row["y_coord"]
    data[x_int][y_int] = elec_e
#__|

#| - Plotting
trace = go.Heatmap(z=data)
data = [trace]

plotly.offline.plot(
    {
        "data": data,
        # "layout": layout,
        },
    filename="pl_fed_supp_graph.html"
    )
#__|
