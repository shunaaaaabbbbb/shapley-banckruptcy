from functools import lru_cache
from typing import Sequence

from shapley_bankruptcy.algorithms.base_algorithm import BaseAlgorithm


class RecursiveDualAlgorithm(BaseAlgorithm):
    """
     Shapley value computation for bankruptcy games
    using the dual recursive formulation.

    This algorithm uses the dual characteristic function:

        v*(S) = min(E, sum(w_i for i in S))

    and applies a recursive decomposition rule over coalitions.
    The recursion is memoized and runs in O(2^n · n), which is
    significantly faster than the exact definition for medium-sized n.
    """

    def precompute(self, E: float, w: Sequence[float]) -> None:
        """
        Precompute:
        - The total claim sum for every coalition S ⊆ N,
        - The dual characteristic value v*(S) = min(E, sum_w[S]).

        Parameters
        ----------
        E : float
            Total estate.
        w : Sequence[float]
            Claims vector.
        """
        self.E = E
        self.w = w
        self.n = n = len(w)

        size = 1 << n

        # sum_w[S] = sum of w[i] for i in S
        self.sum_w = [0.0] * size

        for S in range(1, size):
            # Extract lowest set bit
            lsb = S & -S
            i = lsb.bit_length() - 1
            S_without_i = S & (S - 1)
            self.sum_w[S] = self.sum_w[S_without_i] + w[i]

        # Dual characteristic
        self.v_star = [min(E, self.sum_w[S]) for S in range(size)]

        # Reset recursion cache (important when compute_raw is called multiple times)
        self.recursive_dual.cache_clear()

    @lru_cache(maxsize=None)
    def recursive_dual(self, S_mask: int):
        """
        Compute the dual-recursive contribution vector φ*(S)
        for a coalition encoded by a bitmask S_mask.

        Parameters
        ----------
        S_mask : int
            Coalition represented as a bitmask.

        Returns
        -------
        tuple[float]
            A tuple of length n containing the dual-Shapley contributions for S.
        """
        n = self.n
        w = self.w
        E = self.E

        # Case 1: |S| = 1
        if S_mask & (S_mask - 1) == 0:
            i = S_mask.bit_length() - 1
            phi = [0.0] * n
            phi[i] = min(E, w[i])
            return tuple(phi)

        # Case 2: v*(S) = sum_w[S]  → trivial allocation
        if self.v_star[S_mask] == self.sum_w[S_mask]:
            phi = [w_i for w_i in w]
            return tuple(phi)

        # Case 3: general recursive case
        v_S = self.v_star[S_mask]

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

        # Precompute S\{j} contributions for all j
        sub_phi_list = {}
        for j in members:
            S_minus_j = S_mask & ~(1 << j)
            sub_phi_list[j] = self.recursive_dual(S_minus_j)

        # Compute φ_i(S) per the recursive rule
        for i in members:
            S_minus_i = S_mask & ~(1 << i)
            v_S_minus_i = self.v_star[S_minus_i]

            # sum_{j ≠ i} φ_i(S\{j})
            acc = sum(sub_phi_list[j][i] for j in members if j != i)

            phi[i] = (v_S - v_S_minus_i + acc) / k

        return tuple(phi)

    def compute_raw(self, E: float, w: Sequence[float]) -> list[float]:
        """
        Compute the unrounded Shapley value vector using the
        dual recursive formulation.

        Parameters
        ----------
        E : float
            Estate.
        w : Sequence[float]
            Claims vector.

        Returns
        -------
        list[float]
            Unrounded Shapley value vector.
        """
        self.precompute(E, w)
        full = (1 << len(w)) - 1
        result = self.recursive_dual(full)
        return list(result)
