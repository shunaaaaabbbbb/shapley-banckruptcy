from abc import ABC, abstractmethod
import time

class BaseAlgorithm(ABC):
    """
    破産ゲームのシャープレイ値計算アルゴリズムの共通基底クラス
    """

    def __init__(self, round_digits: int = 5):
        """
        Parameters
        ----------
        round_digits : int
            出力を丸める小数点桁数
        """
        self.round_digits = round_digits

    def compute(self, E, w):
        self._validate_input(E, w)

        start = time.perf_counter()
        raw = self.compute_raw(E, w)
        elapsed = time.perf_counter() - start

        self._last_value = self._round_output(raw)
        self._last_time = round(elapsed, self.round_digits)

    def return_value(self):
        if self._last_value is None:
            raise RuntimeError("Call compute(E, w) first.")
        return self._last_value

    def return_time(self):
        if self._last_time is None:
            raise RuntimeError("Call compute(E, w) first.")
        return self._last_time

    # =========================
    #  アルゴリズムごとに実装
    # =========================
    @abstractmethod
    def compute_raw(self, E: int, w: list[int]) -> list[float]:
        """
        アルゴリズムの核となる部分。
        - シャープレイ値 φ を丸めなしで返す
        """
        raise NotImplementedError

    def _validate_input(self, E: int, w: list[int]):
        # if not isinstance(E, int) or E < 0:
            # raise ValueError("E must be a non-negative integer.")

        # if not isinstance(w, list):
            # raise ValueError("w must be a list of integers.")

        # if any((not isinstance(x, int) or x < 0) for x in w):
            # raise ValueError("All claims w[i] must be non-negative integers.")
        pass
    def _round_output(self, phi):
        """
        結果を round_digits 桁に丸めて返す
        """
        return [round(float(x), self.round_digits) for x in phi]
