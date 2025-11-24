from shapley_bankruptcy.algorithms.base_algorithm import BaseAlgorithm
import math
from typing import Sequence


class DynamicProgrammingAlgorithm(BaseAlgorithm):
    """
    Dynamic-programming-based Shapley value computation for bankruptcy games.

    This algorithm computes the Shapley value using a combinatorial DP formulation
    that counts the number of coalitions of size ``t`` with total claim sum ``s``.
    Compared to the exact combinatorial enumeration, this method runs in:

        O(n * E * n) = O(n^2 * E)

    where ``E`` is the estate and must be **an integer**, as must the claims.
    Therefore, unlike other algorithms in this library, this DP variant strictly
    requires integer-valued ``E`` and ``w``.
    
    Notes
    -----
    - E, w must be integers.
    """

    def _validate_input(self, E: float, w: Sequence[float]):
        """
        Validate inputs using the base validator, then enforce
        integer constraints required by the DP formulation.
        """
        data = super()._validate_input(E, w)

        # E must be an integer
        if not float(data.E).is_integer():
            raise ValueError(
                "DynamicProgrammingAlgorithm requires estate E to be an integer."
            )

        # Each claim must be an integer
        for x in data.w:
            if not float(x).is_integer():
                raise ValueError(
                    "DynamicProgrammingAlgorithm requires all claims w_i to be integers."
                )

        return data

    def compute_dp_last_layer(self, order, w_list, E, n):
        """
        Compute the last DP layer C[n-1][s][t] using a rolling array.

        Parameters
        ----------
        order : list[int]
            Ordering of players; pivot is excluded from the DP.
        w_list : Sequence[int]
            Claims vector (must be integers).
        E : int
            Total estate (must be integer).
        n : int
            Number of players.

        Returns
        -------
        list[list[int]]
            DP counts C[n-1][s][t] for all 0 ≤ s ≤ E and 0 ≤ t < n.
        """
        prev = [[0] * n for _ in range(E + 1)]
        curr = [[0] * n for _ in range(E + 1)]

        prev[0][0] = 1  # empty set

        # Build DP for players except the pivot (order[n-1])
        for i in range(1, n):
            player = order[i - 1]
            wi = w_list[player]

            for t in range(i + 1):
                for s in range(E + 1):
                    val = prev[s][t]
                    if t > 0 and s >= wi:
                        val += prev[s - wi][t - 1]
                    curr[s][t] = val

            prev, curr = curr, prev  # rolling array swap

        return prev

    def compute_marginal(self, C_last, pivot, w, E, n, weights):
        """
        Compute the marginal contribution of the pivot player
        using the precomputed DP layer C_last (i.e., C[n-1]).

        Parameters
        ----------
        C_last : list[list[int]]
            DP counts for all coalition sizes and claim sums.
        pivot : int
            Index of pivot player.
        w : Sequence[int]
            Claims vector.
        E : int
            Estate.
        n : int
            Number of players.
        weights : list[float]
            Precomputed Shapley weights |S|!(n-|S|-1)! / n!.

        Returns
        -------
        float
            Marginal contribution accumulated for the pivot.
        """
        wi = w[pivot]
        phi = 0.0

        for t in range(n - 1):
            weight = weights[t]

            for s in range(E + 1):
                cnt = C_last[s][t]
                if cnt == 0:
                    continue

                phi += weight * min(E - s, wi) * cnt

        return phi

    def compute_raw(self, E: float, w: Sequence[float]) -> list[float]:
        """
        Compute the unrounded Shapley value vector using the DP formulation.

        Parameters
        ----------
        E : float (must represent an integer)
        w : Sequence[float] (each must represent an integer)

        Returns
        -------
        list[float]
            Unrounded Shapley value vector.
        """
        n = len(w)
        E = int(E)  # safe because validation already ensured integer-ness
        w = [int(x) for x in w]

        phi = [0.0] * n
        base = list(range(n))

        # Precompute factorials and weights
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = fact[i - 1] * i

        weights = [
            fact[t] * fact[n - t - 1] / fact[n]
            for t in range(n)
        ]

        # Run DP once per pivot
        for k in range(n):
            order = base[-k:] + base[:-k]
            pivot = order[-1]

            C_last = self.compute_dp_last_layer(order, w, E, n)

            phi[pivot] += self.compute_marginal(C_last, pivot, w, E, n, weights)

        return phi
