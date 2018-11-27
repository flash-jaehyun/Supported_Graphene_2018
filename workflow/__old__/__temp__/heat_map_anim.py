"""Online example for heat map animation."""

#| - IMPORT MODULES
import plotly
plotly.__version__

import plotly.plotly as py
from plotly.grid_objs import Grid, Column

import time
import numpy as np
from scipy.stats import multivariate_normal as Nd
#__|

#| - FUNCTIONS
# returns V=(X,Y)~N(m, Sigma)
def bivariate_N(m=[0., 0.], stdev=[1.0, 1.0], rho=0):
    cov = rho*stdev[0] * stdev[1] # covariance(X,Y)
    Sigma = np.array([[stdev[0]**2, cov], [cov, stdev[1]**2]]) # covariance  matrix
    return Nd(mean=m, cov=Sigma) # joint distribution of (X,Y), of mean  vector, m, and cov matrix, Sigma

# returns the pdf of the bivariate normal distribution
def pdf_bivariate_N(m, stdev, V):
    X = np.linspace(m[0] - 3*stdev[0], m[0] + 3*stdev[0], 100)
    Y = np.linspace(m[1] - 3*stdev[1], m[1] + 3*stdev[1], 100)
    x, y = np.meshgrid(X, Y)
    pos = np.empty(x.shape + (2, ))
    pos[:, :, 0] = x; pos[:, :, 1] = y
    z = V.pdf(pos)
    return X, Y, z

#__|

#| - Colorscale
colorscale = [
    [0.0, 'rgb(25, 23, 10)'],
    [0.05, 'rgb(69, 48, 44)'],
    [0.1, 'rgb(114, 52, 47)'],
    [0.15, 'rgb(155, 58, 49)'],
    [0.2, 'rgb(194, 70, 51)'],
    [0.25, 'rgb(227, 91, 53)'],
    [0.3, 'rgb(250, 120, 56)'],
    [0.35, 'rgb(255, 152, 60)'],
    [0.4, 'rgb(255, 188, 65)'],
    [0.45, 'rgb(236, 220, 72)'],
    [0.5, 'rgb(202, 243, 80)'],
    [0.55, 'rgb(164, 252, 93)'],
    [0.6, 'rgb(123, 245, 119)'],
    [0.65, 'rgb(93, 225, 162)'],
    [0.7, 'rgb(84, 196, 212)'],
    [0.75, 'rgb(99, 168, 238)'],
    [0.8, 'rgb(139, 146, 233)'],
    [0.85, 'rgb(190, 139, 216)'],
    [0.9, 'rgb(231, 152, 213)'],
    [0.95, 'rgb(241, 180, 226)'],
    [1.0, 'rgb(206, 221, 250)'],
    ]

#__|

#| - Make the Grid
correls=[-0.95, -0.85, -0.75, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.75, 0.85, 0.95]

m=[0., 0.]
stdev=[1., 1.]
V=bivariate_N()
x, y = pdf_bivariate_N(m, stdev,  V)[:2]

my_columns=[Column(x, 'x'), Column(y, 'y')]
zvmax=[]
for k, rho in enumerate(correls):
    V = bivariate_N(rho = rho)
    z = pdf_bivariate_N(m, stdev, V)[2]
    zvmax.append(np.max(z))
    my_columns.append(Column(z, 'z{}'.format(k + 1)))
grid = Grid(my_columns)

py.grid_ops.upload(grid, 'norm-bivariate1'+str(time.time()), auto_open=False)
#__|

#| - Make The Figure
data=[dict(
    type='heatmap',
    xsrc=grid.get_column_reference('x'),
    ysrc=grid.get_column_reference('y'),
    zsrc=grid.get_column_reference('z1'),
    zmin=0,
    zmax=zvmax[6],
    zsmooth='best',
    colorscale=colorscale,
    colorbar=dict(thickness=20, ticklen=4),
    )]

title='Contour plot for bivariate normal distribution'+\
'<br> N(m=[0,0], sigma=[1,1], rho in (-1, 1))'

#| - Layout
layout = dict(
    title=title,
    autosize=False,
    height=600,
    width=600,
    hovermode='closest',
    xaxis=dict(range=[-3, 3], autorange=False),
    yaxis=dict(range=[-3, 3], autorange=False),
    showlegend=False,
    updatemenus=[dict(
        type='buttons',
        showactive=False,
        y=1,
        x=-0.05,
        xanchor='right',
        yanchor='top',
        pad=dict(t=0, r=10),
        buttons=[dict(
            label='Play',
            method='animate',
            args=[
                None,
                dict(frame=dict(duration=100, redraw=True),
                transition=dict(duration=0),
                fromcurrent=True,
                mode='immediate'),
                ]
            )
            ]
        )]
    )
#__|

frames=[dict(
    data=[dict(zsrc=grid.get_column_reference('z{}'.format(k + 1)),
    zmax=zvmax[k])],
    traces=[0],
    name='frame{}'.format(k),

    ) for k in range(len(correls))
    ]


fig=dict(data=data, layout=layout, frames=frames)

# plotly.plotly.create_animations()
py.create_animations(fig, filename='animheatmap'+str(time.time()))

#__|
