from abc import ABC, abstractmethod
import time

from src.schemas.input_schema import AlgorithmInput
from src.schemas.output_schema import AlgorithmResult

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

    def compute(self, E: int | float, w: list[int | float]) -> AlgorithmResult:
        input = self._validate_input(E, w)

        start = time.perf_counter()
        raw = self.compute_raw(input.E, input.w) 
        elapsed = time.perf_counter() - start

        return AlgorithmResult(value=self._round_output(raw), elapsed_time=round(elapsed, self.round_digits))

    @abstractmethod
    def compute_raw(self, E: int, w: list[int]) -> list[float]:
        """
        アルゴリズムの核となる部分。
        - シャープレイ値 φ を丸めなしで返す
        """
        raise NotImplementedError

    def _round_output(self, phi):
        """
        結果を round_digits 桁に丸めて返す
        """
        return [round(float(x), self.round_digits) for x in phi]

    def _validate_input(self, E: int | float, w: list[int | float]) -> AlgorithmInput:
        try:
            input = AlgorithmInput(E=E, w=w)
        except ValueError as e:
            raise ValueError(f"Invalid input: {e}") from e
        return input