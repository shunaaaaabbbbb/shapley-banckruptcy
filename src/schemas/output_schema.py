from pydantic import BaseModel, Field

class AlgorithmResult(BaseModel):
    value: list[float] = Field(..., description="List of Shapley values")
    elapsed_time: float = Field(..., description="Elapsed time in seconds")
