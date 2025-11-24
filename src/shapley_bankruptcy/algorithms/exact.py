from shapley_bankruptcy.algorithms.base_algorithm import BaseAlgorithm

import math
from itertools import combinations
from typing import Sequence


class ExactAlgorithm(BaseAlgorithm):
    """
    Exact Shapley value computation for bankruptcy games.

    This algorithm evaluates the Shapley value using the *definition* directly:
    for each player ``i`` and each coalition ``S ⊆ N \\ {i}``,
    compute the marginal contribution

        v(S U {i}) - v(S)

    weighted by the Shapley probability

        |S|! (n - |S| - 1)! / n!

    where ``v`` is the characteristic function of the bankruptcy game.
    This method is exact but exponential in runtime (O(n · 2ⁿ)).
    """

    def bankruptcy_v(self, E: float, w: Sequence[float], S: set[int]) -> float:
        """
        Bankruptcy characteristic function v(S).

        v(S) = max(0, E - sum of claims outside S)

        Parameters
        ----------
        E : float
            Total estate.
        w : Sequence[float]
            Claims vector.
        S : set[int]
            Coalition represented by a set of player indices.

        Returns
        -------
        float
            Value of the coalition S under the bankruptcy game.
        """
        n = len(w)
        complement_sum = sum(w[j] for j in range(n) if j not in S)
        return max(0.0, E - complement_sum)

    def compute_raw(self, E: float, w: Sequence[float]) -> list[float]:
        """
        Compute the unrounded Shapley value vector using the exact definition.

        Parameters
        ----------
        E : float
            Total estate.
        w : Sequence[float]
            Claims vector.

        Returns
        -------
        list[float]
            Unrounded Shapley value vector of length ``len(w)``.

        Notes
        -----
        - Complexity is exponential (O(n · 2ⁿ)).
        - Intended as a reference implementation for correctness checking.
        """
        n = len(w)
        factorial = math.factorial
        fact_n = factorial(n)

        shapley = [0.0] * n

        for i in range(n):
            others = [j for j in range(n) if j != i]

            # Iterate over all subsets of N\{i}
            for r in range(len(others) + 1):
                for S in combinations(others, r):
                    S = set(S)

                    # Weight: |S|!(n-|S|-1)! / n!
                    weight = factorial(len(S)) * factorial(n - len(S) - 1) / fact_n

                    # Marginal contribution
                    v1 = self.bankruptcy_v(E, w, S | {i})
                    v0 = self.bankruptcy_v(E, w, S)
                    shapley[i] += weight * (v1 - v0)

        return shapley
