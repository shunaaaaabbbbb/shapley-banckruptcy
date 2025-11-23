from functools import lru_cache
from shapley_bankruptcy.algorithms.base_algorithm import BaseAlgorithm


class FastDualRecursiveAlgorithm(BaseAlgorithm):

    def precompute(self, E, w):
        """事前に全 2^n の coalition sum と v*(S) を precompute"""
        self.E = E
        self.w = w
        self.n = n = len(w)

        size = 1 << n

        # coalition S の sum_w[S]
        self.sum_w = [0] * size

        for S in range(1, size):
            # 最下位ビット(LSB)のプレイヤー i を取り出す
            lsb = S & -S
            i = (lsb.bit_length() - 1)
            S_without_i = S & (S - 1)
            self.sum_w[S] = self.sum_w[S_without_i] + w[i]

        # dual characteristic: v*(S) = min(E, sum_w[S])
        self.v_star = [min(E, self.sum_w[S]) for S in range(size)]

    @lru_cache(maxsize=None)
    def recursive_dual(self, S_mask: int):
        """
        Dual recursive rule (高速化版)
        戻り値: 長さ n の配列（存在しないプレイヤーは 0）
        """
        n = self.n
        w = self.w
        E = self.E

        # coalition が 1 人だけ
        if S_mask & (S_mask - 1) == 0:
            i = (S_mask.bit_length() - 1)
            phi = [0.0] * n
            phi[i] = min(E, w[i])
            return tuple(phi)

        # If v*(S) = self.sum_w[S], return w_i for all players
        elif self.v_star[S_mask] == self.sum_w[S_mask]:
            phi = [w_i for w_i in w]
            return tuple(phi)

        # If v*(S) > 0, compute the allocation
        else:
            v_S = self.v_star[S_mask]
    
            # coalition S のメンバー（bit enumeration）
            members = []
            s = S_mask
            while s:
                lsb = s & -s
                i = (lsb.bit_length() - 1)
                members.append(i)
                s &= s - 1
    
            k = len(members)
            phi = [0.0] * n
    
            # ⬇ 事前に S\{j} の recursive_dual を全部取っておく
            sub_phi_list = {}
            for j in members:
                S_minus_j = S_mask & ~(1 << j)
                sub_phi_list[j] = self.recursive_dual(S_minus_j)
    
            # 各 i について計算
            for i in members:
                S_minus_i = S_mask & ~(1 << i)
                v_S_minus_i = self.v_star[S_minus_i]
    
                # sum_j≠i φ_i(S\{j})
                acc = 0.0
                for j in members:
                    if j != i:
                        acc += sub_phi_list[j][i]
    
                phi[i] = (v_S - v_S_minus_i + acc) / k
    
            return tuple(phi)

    def compute_raw(self, E, w):
        """最終的な φ を計算"""
        self.precompute(E, w)
        full = (1 << len(w)) - 1
        result = self.recursive_dual(full)
        return list(result)
