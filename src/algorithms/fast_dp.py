from src.algorithms.base_algorithm import BaseAlgorithm
import math


class FastDPAlgorithm(BaseAlgorithm):

    def compute_dp_last_layer(self, order, w_list, E, n):
        """
        pivot を除いた n-1 人の DP を計算し、
        必要な C[n-1][w][t] のみ返す（rolling array で高速化）
        """

        # DP 配列（直前ステップと現在ステップの2層だけ）
        prev = [[0] * (n) for _ in range(E + 1)]
        curr = [[0] * (n) for _ in range(E + 1)]

        prev[0][0] = 1  # 空集合

        # i を順番に追加していく
        # ただし pivot(=order[n-1]) は DPに含めないので n-1 まで
        for i in range(1, n):
            player = order[i - 1]
            wi = w_list[player]

            # dp 更新
            # t: subset size
            for t in range(i + 1):
                # w: claim sum
                for w in range(E + 1):
                    val = prev[w][t]
                    if t > 0 and w >= wi:
                        val += prev[w - wi][t - 1]
                    curr[w][t] = val

            # swap
            prev, curr = curr, prev

        return prev  # これが C[n-1] に相当


    def compute_marginal(self, C_last, pivot, w, E, n, weights):
        """
        pivot の marginal contribution を計算。
        C_last は C[n-1][*][*]
        """

        wi = w[pivot]
        phi = 0.0

        # t: subset size
        for t in range(n - 1):   # pivot 前の人数は最大 n-1
            weight = weights[t]
            row_t = C_last  # alias

            # w: claim sum
            for s in range(E + 1):
                cnt = row_t[s][t]
                if cnt == 0:
                    continue

                phi += weight * min(E - s, wi) * cnt

        return phi


    def compute_raw(self, E, w):
        """
        Shapley value of bankruptcy game via DP (高速版)
        """

        n = len(w)
        phi = [0.0] * n
        base = list(range(n))

        # factorial と重みを前計算
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = fact[i - 1] * i

        # Shapley weight:
        #   t!(n-t-1)! / n!
        weights = [
            fact[t] * fact[n - t - 1] / fact[n]
            for t in range(n)
        ]

        # 各 pivot に対して DP を構築
        for k in range(n):

            # 循環シフト
            order = base[-k:] + base[:-k]
            pivot = order[-1]

            # pivot を除いた DP の最終層 C[n-1]
            C_last = self.compute_dp_last_layer(order, w, E, n)

            # marginal
            phi[pivot] += self.compute_marginal(C_last, pivot, w, E, n, weights)

        return phi
