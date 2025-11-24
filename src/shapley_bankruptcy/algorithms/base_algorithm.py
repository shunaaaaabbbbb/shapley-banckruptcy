from abc import ABC, abstractmethod
import time
from typing import Sequence

from shapley_bankruptcy.schemas.input_schema import AlgorithmInput
from shapley_bankruptcy.schemas.output_schema import AlgorithmResult


class BaseAlgorithm(ABC):
    """
    Abstract base class for Shapley value computation algorithms 
    in bankruptcy games.

    This class defines the public interface, common validation, 
    timing, and rounding utilities used by all algorithm implementations.
    Subclasses must implement the core computation logic in 
    :meth:`compute_raw`.
    """

    def __init__(self, round_digits: int = 5):
        """
        Initialize a Shapley value algorithm.

        Parameters
        ----------
        round_digits : int, optional (default=5)
            Number of decimal digits used to round the computed Shapley values.
        """
        self.round_digits = round_digits

    def compute(self, E: float, w: Sequence[float]) -> AlgorithmResult:
        """
        Compute the Shapley value φ(E, w) for a bankruptcy game.

        This method performs:
        1. Input validation using :class:`AlgorithmInput`
        2. Execution of the algorithm-specific raw computation via :meth:`compute_raw`
        3. Timing of the computation
        4. Rounding of the output

        Parameters
        ----------
        E : float
            Total estate of the bankruptcy game.
        w : Sequence[float]
            A sequence of positive claims.

        Returns
        -------
        AlgorithmResult
            An object containing:
            - `value`: the list of rounded Shapley value components
            - `elapsed_time`: execution time in seconds (rounded)

        Raises
        ------
        ValueError
            If the input fails validation.
        """
        input = self._validate_input(E, w)

        start = time.perf_counter()
        raw = self.compute_raw(input.E, input.w)
        elapsed = time.perf_counter() - start

        return AlgorithmResult(
            value=self._round_output(raw),
            elapsed_time=round(elapsed, self.round_digits)
        )

    @abstractmethod
    def compute_raw(self, E: float, w: Sequence[float]) -> list[float]:
        """
        Core algorithm implementation.

        Subclasses must override this method to compute the 
        **unrounded Shapley value vector** for the given bankruptcy game.

        Parameters
        ----------
        E : float
            Total estate.
        w : Sequence[float]
            Claims vector.

        Returns
        -------
        list[float]
            The unrounded Shapley value vector. 
            The length of the returned list must match ``len(w)``.

        Notes
        -----
        - Do **not** perform input validation here. Validation is handled 
          by :class:`AlgorithmInput` before this method is called.
        - This method should focus solely on the mathematical/algorithmic logic.
        """
        raise NotImplementedError

    def _round_output(self, phi: Sequence[float]) -> list[float]:
        """
        Round a Shapley value vector to ``self.round_digits`` decimal places.

        Parameters
        ----------
        phi : Sequence[float]
            The unrounded Shapley value vector.

        Returns
        -------
        list[float]
            Rounded values as a new list of floats.
        """
        return [round(float(x), self.round_digits) for x in phi]

    def _validate_input(self, E: float, w: Sequence[float]) -> AlgorithmInput:
        """
        Validate inputs using :class:`AlgorithmInput`.

        This method ensures that all numerical and structural conditions on
        ``E`` and ``w`` are satisfied before computation begins.

        Parameters
        ----------
        E : float
            Total estate.
        w : Sequence[float]
            Claims.

        Returns
        -------
        AlgorithmInput
            A validated model containing the sanitized values.

        Raises
        ------
        ValueError
            If validation fails.
        """
        try:
            input = AlgorithmInput(E=E, w=w)
        except ValueError as e:
            raise ValueError(f"Invalid input: {e}") from e
        return input
