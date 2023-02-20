import matplotlib.pyplot as plt
import numpy as np
import sympy

from pyrat.algorithm import ASB2008CDC
from pyrat.dynamic_system import NonLinSys
from pyrat.geometry import Zonotope, Interval, Geometry
from pyrat.geometry.operation import boundary
from pyrat.model import *
from pyrat.util.visualization import plot, plot_cmp

# init dynamic system
system = NonLinSys(Model(jet_engine, [2, 1]))

# settings for the computation
options = ASB2008CDC.Options()
options.t_end = 5
options.step = 0.005
options.tensor_order = 2
options.taylor_terms = 4

options.u = Zonotope([0], np.diag([0]))
options.u_trans = options.u.c

# settings for the using geometry
Zonotope.REDUCE_METHOD = Zonotope.REDUCE_METHOD.GIRARD
Zonotope.ORDER = 50

z = Zonotope([1, 1], np.diag([0.2, 0.2]))

# reachable sets computation without boundary analysis
options.r0 = [z]
ti_whole, tp_whole, _, _ = ASB2008CDC.reach(system, options)

# reachable sets computation with boundary analysis
options.r0 = boundary(z, 1, Geometry.TYPE.ZONOTOPE)
ti_bound, tp_bound, _, _ = ASB2008CDC.reach(system, options)

# visualize the results
plot_cmp([tp_whole, tp_bound], [0, 1], cs=['#FF5722', '#303F9F'])
