from functools import lru_cache
from shapley_bankruptcy.algorithms.base_algorithm import BaseAlgorithm


class FastRecursiveAlgorithm(BaseAlgorithm):

    def precompute(self, E, w):
        """全 2^n の coalition sum と v(S) を precompute"""
        self.E = E
        self.w = w
        self.w0 = sum(w) - E
        self.n = n = len(w)

        size = 1 << n

        # coalition S の合計値 sum_w[S]
        self.sum_w = [0] * size

        for S in range(1, size):
            lsb = S & -S
            i = (lsb.bit_length() - 1)
            S2 = S & (S - 1)
            self.sum_w[S] = self.sum_w[S2] + w[i]

        # characteristic function v(S) = max(0, sum_w[S] - w0)
        w0 = self.w0
        self.v = [max(0, self.sum_w[S] - w0) for S in range(size)]

    @lru_cache(maxsize=None)
    def recursive_completion(self, S_mask: int):
        """高速化 recursive rule: 長さ n の tuple を返す"""
        n = self.n
        w = self.w
        w0 = self.w0

        # Base case: 1 player
        if S_mask & (S_mask - 1) == 0:
            i = (S_mask.bit_length() - 1)
            phi = [0.0] * n
            phi[i] = max(0, w[i] - w0)
            return tuple(phi)

        # If v(S) = 0, return 0 for all players
        elif self.v[S_mask] == 0:
            phi = [0.0] * n
            return tuple(phi)

        # If v(S) > 0, compute the allocation
        else:
            v_S = self.v[S_mask]
    
            # coalition members
            members = []
            s = S_mask
            while s:
                lsb = s & -s
                i = (lsb.bit_length() - 1)
                members.append(i)
                s &= s - 1
    
            k = len(members)
            phi = [0.0] * n
    
            # 事前に S\{j} の φ を全部計算してキャッシュ
            subs = {}
            for j in members:
                subs[j] = self.recursive_completion(S_mask & ~(1 << j))
    
            # 各 i の計算
            for i in members:
                acc = 0.0
                for j in members:
                    if i != j:
                        acc += subs[j][i]
                phi[i] = (min(w[i], v_S) + acc) / k

        return tuple(phi)

    def compute_raw(self, E, w):
        self.precompute(E, w)
        full = (1 << len(w)) - 1
        result = self.recursive_completion(full)
        return list(result)
