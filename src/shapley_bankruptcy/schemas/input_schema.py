from typing import Sequence
from pydantic import BaseModel, Field, field_validator, model_validator
import math

class AlgorithmInput(BaseModel):
    """
    Input model for Shapley value computation in bankruptcy games.

    This model validates the structure and numerical constraints required
    for a valid bankruptcy game:

    - ``E`` (total estate) must be a positive finite float.
    - ``w`` must be a non-empty sequence of positive finite floats.
    - The estate must be strictly smaller than the total claims: ``E < sum(w)``.
    - NaN and Infinity are rejected for both ``E`` and ``w``.
    """
    E: float = Field(..., gt=0, description="Total estate (positive float)")
    w: Sequence[float] = Field(..., description="List of claims (positive floats)")

    @field_validator("w")
    @classmethod
    def validate_claims(cls, w: Sequence[float]):
        if not w:
            raise ValueError("w cannot be empty.")

        for x in w:
            if not isinstance(x, (int, float)):
                raise TypeError("All claims must be numeric (int or float).")
            if math.isnan(x) or math.isinf(x):
                raise ValueError("Claims cannot contain NaN or Infinity.")
            if x <= 0:
                raise ValueError("All claims must be positive floats.")

        return w

    @field_validator("E")
    @classmethod
    def validate_estate(cls, E: float):
        if math.isnan(E) or math.isinf(E):
            raise ValueError("E cannot be NaN or Infinity.")
        return E

    @model_validator(mode="after")
    def validate_relationships(self):
        if self.E >= sum(self.w):
            raise ValueError(
                f"E ({self.E}) must be smaller than the total claims ({sum(self.w)})."
            )
        return self
