import matplotlib.pyplot as plt
import numpy as np
import sympy

from pyrat.algorithm import ASB2008CDC
from pyrat.dynamic_system import NonLinSys
from pyrat.geometry import Zonotope, Interval, Geometry
from pyrat.geometry.operation import boundary
from pyrat.model import *
from pyrat.util.visualization import plot, plot_cmp


def test_lotka_volterra_cmp():
    # init dynamic system
    system = NonLinSys(Model(synchronous_machine, [2, 1]))

    # settings for the computation
    options = ASB2008CDC.Options()
    options.t_end = 3
    options.step = 0.01
    options.tensor_order = 3
    options.taylor_terms = 4

    options.u = Zonotope.zero(1, 1)
    options.u_trans = np.zeros(1)

    # settings for the using geometry
    Zonotope.REDUCE_METHOD = Zonotope.REDUCE_METHOD.GIRARD
    Zonotope.ORDER = 50

    z = Zonotope([0, 3], np.diag([0.1, 0.1]))

    # reachable sets computation without boundary analysis
    options.r0 = [z]
    ti_whole, tp_whole, _, _ = ASB2008CDC.reach(system, options)

    # reachable sets computation with boundary analysis
    options.r0 = boundary(z, 1, Geometry.TYPE.ZONOTOPE)
    ti_bound, tp_bound, _, _ = ASB2008CDC.reach(system, options)

    # visualize the results
    plot_cmp([tp_whole, tp_bound], [0, 1], cs=['#FF5722', '#303F9F'])


def test_synchronous_machine_cmp():
    # init dynamic system
    system = NonLinSys(Model(synchronous_machine, [2, 1]))

    # settings for the computation
    options = ASB2008CDC.Options()
    options.t_end = 3
    options.step = 0.01
    options.tensor_order = 3
    options.taylor_terms = 4

    options.u = Zonotope.zero(1, 1)
    options.u_trans = np.zeros(1)

    # settings for the using geometry
    Zonotope.REDUCE_METHOD = Zonotope.REDUCE_METHOD.GIRARD
    Zonotope.ORDER = 50

    z = Zonotope([0, 3], np.diag([0.1, 0.1]))

    # reachable sets computation without boundary analysis
    options.r0 = [z]
    ti_whole, tp_whole, _, _ = ASB2008CDC.reach(system, options)

    # reachable sets computation with boundary analysis
    options.r0 = boundary(z, 1, Geometry.TYPE.ZONOTOPE)
    ti_bound, tp_bound, _, _ = ASB2008CDC.reach(system, options)

    # visualize the results
    plot_cmp([tp_whole, tp_bound], [0, 1], cs=['#FF5722', '#303F9F'])


def test_2d_ode_vector_field():
    x = np.linspace(-10, 10, 200)
    y = np.linspace(-10, 10, 200)
    xx, yy = np.meshgrid(x, y)
    xy = np.vstack([xx.reshape(-1), yy.reshape(-1)]).T
    us = np.zeros((xy.shape[0], 1))
    print(xy.shape)
    print(us.shape)
    model = Model(ode2d, [2, 1])
    model.reverse()

    results = []
    for i in range(xy.shape[0]):
        this_xy = xy[i]
        this_u = us[i]
        this_v = model.evaluate((this_xy, this_u), 'numpy', 0, 0)
        results.append(this_v)
    uv = np.vstack(results)

    plt.streamplot(xx, yy, uv[:, 0].reshape(xx.shape), uv[:, 1].reshape(xx.shape), linewidth=1)
    plt.scatter(-3, 5, c='red')
    plt.scatter(-3, -3, c='red')
    plt.scatter(3, -3, c='red')
    plt.scatter(3, 3, c='red')
    plt.axis('equal')
    plt.show()


def test_ode_2d_cmp():
    # init dynamic system
    system = NonLinSys(Model(ode2d, [2, 1]))

    # settings for the computation
    options = ASB2008CDC.Options()
    options.t_end = 3
    options.step = 0.01
    options.tensor_order = 3
    options.taylor_terms = 4

    options.u = Zonotope.zero(1, 1)
    options.u_trans = np.zeros(1)

    # settings for the using geometry
    Zonotope.REDUCE_METHOD = Zonotope.REDUCE_METHOD.GIRARD
    Zonotope.ORDER = 50

    z = Zonotope([10, -5], np.diag([0.1, 2]))

    # reachable sets computation without boundary analysis
    options.r0 = [z]
    ti_whole, tp_whole, _, _ = ASB2008CDC.reach(system, options)

    # reachable sets computation with boundary analysis
    options.r0 = boundary(z, 1, Geometry.TYPE.ZONOTOPE)
    ti_bound, tp_bound, _, _ = ASB2008CDC.reach(system, options)

    # visualize the results
    plot_cmp([tp_whole, tp_bound], [0, 1], cs=['#FFBE7A', '#8ECFC9'])


def test_2d_ode():
    # init dynamic system
    system = NonLinSys(Model(ode2d, [2, 1]))

    # settings for the computation
    options = ASB2008CDC.Options()
    options.t_end = 1
    options.step = 0.02
    options.tensor_order = 3
    options.taylor_terms = 4
    options.r0 = [Zonotope([0.05, 0.1], np.diag([0.01, 0.01]))]

    options.u = Zonotope.zero(1, 1)
    # options.u = Zonotope([0], [[0.05]])
    options.u_trans = np.zeros(1)

    # settings for the using geometry
    Zonotope.REDUCE_METHOD = Zonotope.REDUCE_METHOD.GIRARD
    Zonotope.ORDER = 50

    # reachable sets computation
    ti, tp, _, _ = ASB2008CDC.reach(system, options)

    # visualize the results
    plot(tp, [0, 1], c='red')
    # plot(tp, [0, 1], xlim=[-5, 2], ylim=[-5, 2])


def test_van_der_pol():
    # init dynamic system
    system = NonLinSys(Model(vanderpol, [2, 1]))

    # settings for the computation
    options = ASB2008CDC.Options()
    options.t_end = 6.74
    options.step = 0.005
    options.tensor_order = 3
    options.taylor_terms = 4
    options.r0 = [Zonotope([1.4, 2.4], np.diag([0.17, 0.06]))]

    options.u = Zonotope.zero(1, 1)
    options.u_trans = np.zeros(1)

    # settings for the using geometry
    Zonotope.REDUCE_METHOD = Zonotope.REDUCE_METHOD.GIRARD
    Zonotope.ORDER = 50

    # reachable sets computation
    ti, tp, _, _ = ASB2008CDC.reach(system, options)

    # visualize the results
    plot(tp, [0, 1], xlim=[-3.5, 3.5], ylim=[-3, 4])


def test_vanderpol_bound_reach():
    # init dynamic system
    system = NonLinSys(Model(vanderpol, [2, 1]))

    # settings for the computation
    options = ASB2008CDC.Options()
    options.t_end = 6.74
    options.step = 0.005
    options.tensor_order = 3
    options.taylor_terms = 4
    z = Zonotope([1.4, 2.4], np.diag([0.17, 0.06]))
    options.r0 = boundary(z, 1, Geometry.TYPE.ZONOTOPE)

    options.u = Zonotope.zero(1, 1)
    options.u_trans = np.zeros(1)

    # settings for the using geometry
    Zonotope.REDUCE_METHOD = Zonotope.REDUCE_METHOD.GIRARD
    Zonotope.ORDER = 50

    # reachable sets computation
    ti, tp, _, _ = ASB2008CDC.reach(system, options)

    # visualize the results
    plot(tp, [0, 1], xlim=[-3.5, 3.5], ylim=[-3, 4])


def test_vanderpol_cmp():
    # init dynamic system
    system = NonLinSys(Model(vanderpol, [2, 1]))

    # settings for the computation
    options = ASB2008CDC.Options()
    options.t_end = 6.74
    options.step = 0.005
    options.tensor_order = 3
    options.taylor_terms = 4

    options.u = Zonotope.zero(1, 1)
    options.u_trans = np.zeros(1)

    # settings for the using geometry
    Zonotope.REDUCE_METHOD = Zonotope.REDUCE_METHOD.GIRARD
    Zonotope.ORDER = 50

    z = Zonotope([1.4, 2.4], np.diag([0.17, 0.06]))

    # reachable sets computation without boundary analysis
    options.r0 = [z]
    ti_whole, tp_whole, _, _ = ASB2008CDC.reach(system, options)

    # reachable sets computation with boundary analysis
    options.r0 = boundary(z, 1, Geometry.TYPE.ZONOTOPE)
    ti_bound, tp_bound, _, _ = ASB2008CDC.reach(system, options)

    # visualize the results
    plot_cmp([tp_whole, tp_bound], [0, 1], cs=['#FF5722', '#303F9F'])


def test_tank6eq():
    # init dynamic system
    system = NonLinSys(Model(tank6eq, [6, 1]))

    # settings for the computation
    options = ASB2008CDC.Options()
    options.t_end = 400
    options.step = 1
    options.tensor_order = 3
    options.taylor_terms = 4
    options.r0 = [Zonotope([2, 4, 4, 2, 10, 4], np.eye(6) * 0.2)]
    options.u = Zonotope([0], [[0.005]])
    options.u = Zonotope.zero(1, 1)
    options.u_trans = np.zeros(1)

    # settings for the using geometry
    Zonotope.REDUCE_METHOD = Zonotope.METHOD.REDUCE.GIRARD
    Zonotope.ORDER = 50

    # reachable sets computation
    ti, tp, _, _ = ASB2008CDC.reach(system, options)

    # visualize the results
    plot(tp, [0, 1])
    plot(tp, [2, 3])
    plot(tp, [4, 5])


def test_tank6eq_bound_reach():
    # init dynamic system
    system = NonLinSys(Model(tank6eq, [6, 1]))

    # settings for the computation
    options = ASB2008CDC.Options()
    options.t_end = 400
    options.step = 1
    options.tensor_order = 3
    options.taylor_terms = 4
    z = Zonotope([2, 4, 4, 2, 10, 4], np.eye(6) * 0.2)
    options.r0 = boundary(z, 1, Geometry.TYPE.ZONOTOPE)
    options.u = Zonotope([0], [[0.005]])
    options.u = Zonotope.zero(1, 1)
    options.u_trans = np.zeros(1)

    # settings for the using geometry
    Zonotope.REDUCE_METHOD = Zonotope.METHOD.REDUCE.GIRARD
    Zonotope.ORDER = 50

    # reachable sets computation
    ti, tp, _, _ = ASB2008CDC.reach(system, options)

    # visualize the results
    plot(tp, [0, 1])
    plot(tp, [2, 3])
    plot(tp, [4, 5])


def test_laub_loomis():
    # init dynamic system
    system = NonLinSys(Model(laubloomis, [7, 1]))

    # settings for the computation
    options = ASB2008CDC.Options()
    options.t_end = 20
    options.step = 0.04
    options.tensor_order = 2
    options.taylor_terms = 4
    options.r0 = [Zonotope([1.2, 1.05, 1.5, 2.4, 1, 0.1, 0.45], np.eye(7) * 0.01)]
    options.u = Zonotope([0], [[0.005]])
    options.u = Zonotope.zero(1, 1)
    options.u_trans = np.zeros(1)

    # settings for using geometry
    Zonotope.REDUCE_METHOD = Zonotope.METHOD.REDUCE.GIRARD
    Zonotope.ORDER = 50

    ti, tp, _, _ = ASB2008CDC.reach(system, options)

    plot(tp, [0, 1])
    plot(tp, [2, 4])
    plot(tp, [5, 6])
    plot(tp, [1, 5])
    plot(tp, [4, 6])
