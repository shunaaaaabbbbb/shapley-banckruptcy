from pydantic import BaseModel, Field, field_validator

class AlgorithmInput(BaseModel):
    E: int | float = Field(..., ge=0, description="Total estate (non-negative integer or float)")
    w: list[int | float] = Field(..., description="List of claims (non-negative integers or floats)")

    @field_validator("w")
    @classmethod
    def validate_claims(cls, w):
        if not w:
            raise ValueError("w cannot be empty.")
        if any(x < 0 for x in w):
            raise ValueError("All claims must be non-negative integers or floats.")
        return w

    @field_validator("E")
    @classmethod
    def validate_total(cls, E, info):
        w = info.data.get("w")
        if w and E >= sum(w):
            raise ValueError(f"E ({E}) must be smaller than the total claims ({sum(w)}).")
        return E
