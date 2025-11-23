from shapley_bankruptcy.algorithms.base_algorithm import BaseAlgorithm

import math
from itertools import combinations

class ExactSetAlgorithm(BaseAlgorithm):
    def bankruptcy_v(self, E, w, S):
        """破産ゲームの特性関数 v(S)"""
        n = len(w)
        complement_sum = sum(w[j] for j in range(n) if j not in S)
        return max(0, E - complement_sum)


    def compute_raw(self, E: int, w: list[int]) -> list[float]:
        """
        破産ゲームのシャープレイ値を定義通りに計算する。
        E: 遺産総額
        w: 各プレイヤーの主張
        """
        n = len(w)
        factorial = math.factorial
        shapley = [0.0] * n

        for i in range(n):
            # N\{i}
            others = [j for j in range(n) if j != i]

            # 全ての S ⊆ N\{i}
            for r in range(len(others) + 1):
                for S in combinations(others, r):
                    S = set(S)

                    # 重み： |S|!(n-|S|-1)! / n!
                    weight = factorial(len(S)) * factorial(n - len(S) - 1) / factorial(n)

                    # 限界貢献 v(S ∪ {i}) − v(S)
                    v1 = self.bankruptcy_v(E, w, S | {i})
                    v0 = self.bankruptcy_v(E, w, S)
                    marginal = v1 - v0

                    shapley[i] += weight * marginal

        return shapley
