from functools import lru_cache
from typing import Sequence

from shapley_bankruptcy.algorithms.base_algorithm import BaseAlgorithm


class RecursiveAlgorithm(BaseAlgorithm):
    """
     Shapley value computation for bankruptcy games
    using the primal recursive formulation.

    The characteristic function of the bankruptcy game is:

        v(S) = max(0, sum(w_i for i in S) - w0)

    where ``w0 = sum(w) - E``.  
    This formulation allows an efficient recursive computation of the Shapley
    value using a memoized decomposition over coalitions.
    """

    def precompute(self, E: float, w: Sequence[float]) -> None:
        """
        Precompute:
        - The total claim sum for every coalition S ⊆ N,
        - The characteristic value v(S) = max(0, sum_w[S] - w0).

        Parameters
        ----------
        E : float
            Total estate.
        w : Sequence[float]
            Claims vector.
        """
        self.E = E
        self.w = w
        self.w0 = sum(w) - E
        self.n = n = len(w)

        size = 1 << n

        # sum_w[S] = sum of claims in S
        self.sum_w = [0.0] * size

        for S in range(1, size):
            lsb = S & -S
            i = lsb.bit_length() - 1
            S2 = S & (S - 1)
            self.sum_w[S] = self.sum_w[S2] + w[i]

        w0 = self.w0
        self.v = [max(0.0, self.sum_w[S] - w0) for S in range(size)]

        # Reset recursion cache (important when compute_raw is called multiple times)
        self.recursive_completion.cache_clear()

    @lru_cache(maxsize=None)
    def recursive_completion(self, S_mask: int):
        """
        Compute the primal recursive contribution vector φ(S) for a coalition S.

        Parameters
        ----------
        S_mask : int
            Coalition represented as a bitmask.

        Returns
        -------
        tuple[float]
            Length-n tuple representing φ(S) for all players.
        """
        n = self.n
        w = self.w
        w0 = self.w0

        # Case 1: |S| = 1
        if S_mask & (S_mask - 1) == 0:
            i = S_mask.bit_length() - 1
            phi = [0.0] * n
            phi[i] = max(0.0, w[i] - w0)
            return tuple(phi)

        # Case 2: v(S) = 0
        if self.v[S_mask] == 0:
            return tuple(0.0 for _ in range(n))

        # Case 3: general recursive case
        v_S = self.v[S_mask]

        # Extract members of S
        members = []
        s = S_mask
        while s:
            lsb = s & -s
            i = lsb.bit_length() - 1
            members.append(i)
            s &= s - 1

        k = len(members)
        phi = [0.0] * n

        # Precompute φ(S \ {j}) for all j in S
        subs = {
            j: self.recursive_completion(S_mask & ~(1 << j))
            for j in members
        }

        # Compute φ_i(S)
        for i in members:
            acc = sum(subs[j][i] for j in members if j != i)
            phi[i] = (min(w[i], v_S) + acc) / k

        return tuple(phi)

    def compute_raw(self, E: float, w: Sequence[float]) -> list[float]:
        """
        Compute the unrounded Shapley value vector using the
        primal recursive formulation.

        Parameters
        ----------
        E : float
            Total estate.
        w : Sequence[float]
            Claims vector.

        Returns
        -------
        list[float]
            Unrounded Shapley value vector.
        """
        self.precompute(E, w)
        full = (1 << len(w)) - 1
        result = self.recursive_completion(full)
        return list(result)
