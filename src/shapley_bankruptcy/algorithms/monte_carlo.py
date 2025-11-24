from shapley_bankruptcy.algorithms.base_algorithm import BaseAlgorithm
from typing import Sequence
import random


class MonteCarloAlgorithm(BaseAlgorithm):
    """
    Monte Carlo approximation of the Shapley value for bankruptcy games.

    This algorithm estimates the Shapley value by sampling M random permutations
    of players and computing their marginal contributions in each ordering.
    """

    def __init__(self, M: int = 10000, seed: int | None = None, round_digits: int = 5):
        """
        Parameters
        ----------
        M : int, optional
            Number of Monte Carlo samples (permutations).
        seed : int or None, optional
            Random seed for reproducibility. Seed is set once at initialization.
        round_digits : int, optional
            Decimal rounding precision for output.
        """
        super().__init__(round_digits)
        self.M = M
        self.seed = seed

        if seed is not None:
            random.seed(seed)

    def compute_raw(self, E: float, w: Sequence[float]) -> list[float]:
        """
        Compute the unrounded Shapley value using Monte Carlo sampling.

        Parameters
        ----------
        E : float
            Total estate.
        w : Sequence[float]
            Claims vector.

        Returns
        -------
        list[float]
            Monte Carlo estimate of the Shapley value.
        """
        n = len(w)
        w = [min(wi, E) for wi in w]     # cap each claim at E (coalition cannot exceed estate)
        phi = [0.0] * n
        players = list(range(n))

        for _ in range(self.M):
            perm = random.sample(players, n)
            sum_future = sum(w)  # claims of players not yet added

            for i in perm:
                sum_future -= w[i]
                v_prev = max(0.0, E - (sum_future + w[i]))  # value before adding i
                v_curr = max(0.0, E - sum_future)           # value after adding i
                phi[i] += (v_curr - v_prev)

        return [v / self.M for v in phi]
