from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.linalg import expm

from pyrat.geometry import Geometry, Interval
from pyrat.misc import Reachable, Simulation
from .continuous_system import ContSys, Option


class LinSys:
    @dataclass
    class Option(Option):
        algo: str = "euclidean"
        origin_contained: bool = False
        taylor_terms = 0
        factors: np.ndarray = None
        is_rv: bool = False

        def validate(self) -> bool:
            raise NotImplementedError

    class Sys(ContSys):
        def __init__(
            self,
            xa,
            ub: np.ndarray = None,
            c: float = None,
            xc: np.ndarray = None,
            ud: np.ndarray = None,
            k: float = None,
        ):
            self._xa = xa
            self._ub = ub
            self._c = c
            self._xc = xc
            self._ud = ud
            self._k = k
            self._taylor = {}

        # =============================================== operator
        def __str__(self):
            raise NotImplementedError

        # =============================================== property
        @property
        def dim(self) -> int:
            return self._xa.shape[1]

        # =============================================== private method
        def _exponential(self, op: LinSys.Option):
            xa_abs = abs(self._xa)
            xa_power = [self._xa]
            xa_power_abs = [xa_abs]
            m = np.eye(self.dim, dtype=float)
            # compute powers for each term and sum of these
            for i in range(op.taylor_terms):
                # compute powers
                xa_power.append(xa_power[i] @ self._xa)
                xa_power_abs.append(xa_power_abs[i] @ xa_abs)
                m += xa_power_abs[i] * op.factors[i]
            # determine error due the finite taylor series, see Prop.(2) in [1]
            w = expm(xa_abs * op.t_step) - m
            # compute absolute value of w for numerical stability
            w = abs(w)
            e = Interval(np.stack([-w, w]))
            # write to object structure
            self._taylor["powers"] = xa_power
            self._taylor["err"] = e

        def _computer_time_interval_err(self, op: LinSys.Option):
            xa_power = self._taylor["powers"]
            rby_fac = op.factors
            dim = self.dim
            # initialize asum
            asum_pos = np.zeros((dim, dim), dtype=float)
            asum_neg = np.zeros((dim, dim), dtype=float)

            for i in range(1, op.taylor_terms):
                # compute factor
                exp1, exp2 = -(i + 1) / i, -1 / i
                factor = ((i + 1) ** exp1 - (i + 1) ** exp2) * rby_fac[i]
                # init apos, aneg
                apos = np.zeros((dim, dim), dtype=float)
                aneg = np.zeros((dim, dim), dtype=float)
                # obtain positive and negative parts
                pos_ind = xa_power[i] > 0
                neg_ind = xa_power[i] < 0
                apos[pos_ind] = xa_power[i][pos_ind]
                aneg[neg_ind] = xa_power[i][neg_ind]
                # compute powers; factor is always negative
                asum_pos += factor * aneg
                asum_neg += factor * apos
            # instantiate interval matrix
            asum = Interval(np.stack([asum_neg, asum_pos]))
            # write to object structure
            self._taylor["F"] = asum + self._taylor["err"]

        def _input_solution(self, op: LinSys.Option):
            """
            compute the bloating due to the input
            :param op: options for the linear reachable computation
            :return:
            """
            v = op.u if self._ub is None else self._ub @ op.u
            # compute vTrans
            op.is_rv = True
            if np.all(v.center == 0) and v.z.shape[1] == 1:
                op.is_rv = False
            v_trans = op.u_trans if self._ub is None else self._ub @ op.u

            input_solv = None
            if op.is_rv:
                # init v_sum
                v_sum = op.t_step * v
                a_sum = op.t_step * np.eye(self.dim)
                # compute higher order terms
                for i in range(op.taylor_terms):
                    v_sum += self._taylor["powers"][i] @ (op.factors[i + 1] * v)
                    a_sum += self._taylor["powers"][i] * op.factors[i + 1]

                # compute overall solution
                input_solv = v_sum + self._taylor["err"] * op.t_step * v
            else:
                # TODO
                raise NotImplementedError

            # TODO

            raise NotImplementedError

        def _reach_init_euclidean(self, r: Geometry, op: LinSys.Option):
            # compute exponential matrix
            self._exponential(op)
            # compute time interval error
            self._computer_time_interval_err(op)
            # compute reachable set due to input
            self._input_solution(op)
            # TODO
            raise NotImplementedError

        # =============================================== public method
        def reach_init(self, r_init: Geometry, op: LinSys.Option):
            if op.algo == "euclidean":
                return self._reach_init_euclidean(r_init, op)
            else:
                raise NotImplementedError

        def reach(self, op: LinSys.Option) -> Reachable.Result:
            assert op.validate()

            raise NotImplementedError

        def simulate(self, op) -> Simulation.Result:
            raise NotImplementedError
