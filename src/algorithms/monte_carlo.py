from src.algorithms.base_algorithm import BaseAlgorithm
import random

class MonteCarloAlgorithm(BaseAlgorithm):
    def __init__(self, M=10000, seed=None, round_digits=5):
        super().__init__(round_digits)
        self.M = M
        self.seed = seed

    def compute_raw(self, E: int, w: list[int]):
        """
        Correct and efficient Monte Carlo estimation of Shapley value for bankruptcy games.
        """
        if self.seed is not None:
            random.seed(self.seed)
        n = len(w)
        w = [min(wi, E) for wi in w]
        phi = [0.0] * n
        N = list(range(n))

        for _ in range(self.M):
            perm = random.sample(N, n)
            sum_future = sum(w)  # sum of players not yet added
            for i in perm:
                sum_future -= w[i]
                v_prev = max(0, E - (sum_future + w[i]))  # before adding i
                v_curr = max(0, E - sum_future)           # after adding i
                phi[i] += (v_curr - v_prev)

        return [v / self.M for v in phi]
