import numpy as np
from pybdr.geometry import Zonotope, Geometry, Interval
from pybdr.geometry.operation import cvt2
from pybdr.dynamic_system import LinearSystemSimple
from pybdr.algorithm import ReachLinearZonoAlgo3
from pybdr.util.visualization import plot


def test_reach_linear_zono_algo3_case_00():
    xa = [[-1, -4], [4, -1]]
    ub = np.array([[1], [1]])

    lin_sys = LinearSystemSimple(xa, ub)
    opts = ReachLinearZonoAlgo3.Settings()
    opts.t_end = 5
    opts.step = 0.04
    opts.eta = 4
    opts.x0 = cvt2(Interval([0.9, 0.9], [1.1, 1.1]), Geometry.TYPE.ZONOTOPE)
    opts.u = cvt2(ub @ Interval(0.1, 0.3), Geometry.TYPE.ZONOTOPE)  # u must contain origin

    _, ri, _, _ = ReachLinearZonoAlgo3.reach(lin_sys, opts)

    plot(ri, [0, 1])


def test_reach_linear_zono_algo3_case_01():
    xa = np.array([[-1, -4, 0, 0, 0], [4, - 1, 0, 0, 0], [0, 0, -3, 1, 0], [0, 0, -1, -3, 0], [0, 0, 0, 0, -2]])
    ub = np.eye(5)

    lin_sys = LinearSystemSimple(xa, ub)
    opts = ReachLinearZonoAlgo3.Settings()
    opts.t_end = 5
    opts.step = 0.04
    opts.eta = 4
    opts.x0 = cvt2(Interval(0.9 * np.ones(5), 1.1 * np.ones(5)), Geometry.TYPE.ZONOTOPE)
    u = Interval([0.9, -0.25, -0.1, 0.25, -0.75], [1.1, 0.25, 0.1, 0.75, -0.25])
    opts.u = cvt2(ub @ u, Geometry.TYPE.ZONOTOPE)  # this case is special because u does not contain origin

    _, ri, _, _ = ReachLinearZonoAlgo3.reach(lin_sys, opts)

    plot(ri, [0, 1])
    plot(ri, [1, 2])
    plot(ri, [2, 3])
    plot(ri, [3, 4])
