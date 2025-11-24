# Shapley-Bankruptcy

Implementation of algorithms for computing the Shapley value in bankruptcy games. This repository contains implementations of algorithms proposed in the paper "On Computing the Shapley Value in Bankruptcy Games".

## Overview

A bankruptcy game is a cooperative game where an estate of value E must be divided among creditors with claims w = (w₁, w₂, ..., wₙ). This implementation provides multiple efficient algorithms for computing the Shapley value in such games.

## Installation

### Requirements

- Python 3.11 or higher

### Install from PyPI

```bash
pip install shapley-bankruptcy
```

### Install from source

```bash
# Clone the repository
git clone <repository-url>
cd shapley-banckruptcy

# Install dependencies
pip install -e .
```

## Usage

### Basic Example

```python
from shapley_bankruptcy.algorithms import (
    DynamicProgrammingAlgorithm,
    MonteCarloAlgorithm,
    ExactAlgorithm
)

# Problem setup
E = 100  # Total estate value
w = [50, 60, 80]  # Claims of each player

# Select an algorithm and compute
algorithm = DynamicProgrammingAlgorithm()
result = algorithm.compute(E, w)

# Get results
shapley_values = result.value
computation_time = result.elapsed_time

print(f"Shapley values: {shapley_values}")
print(f"Computation time: {computation_time} seconds")
```

### Implemented Algorithms

#### 1. `ExactAlgorithm`
An exact algorithm based on the definition of the Shapley value. It enumerates all subsets to compute the value.

```python
from shapley_bankruptcy.algorithms import ExactAlgorithm

algorithm = ExactAlgorithm()
result = algorithm.compute(E, w)
shapley_values = result.value
```

**Features:**
- Guarantees exact results
- Time complexity: O(2ⁿ × n)
- Suitable for small-scale problems

#### 2. `DynamicProgrammingAlgorithm`
A fast algorithm using dynamic programming.

```python
from shapley_bankruptcy.algorithms import DynamicProgrammingAlgorithm

algorithm = DynamicProgrammingAlgorithm()
result = algorithm.compute(E, w)
shapley_values = result.value
```

**Features:**
- Efficient computation using dynamic programming
- Suitable for medium to large-scale problems

#### 3. `RecursiveAlgorithm`
A fast algorithm using recursive formulas.

```python
from shapley_bankruptcy.algorithms import RecursiveAlgorithm

algorithm = RecursiveAlgorithm()
result = algorithm.compute(E, w)
shapley_values = result.value
```

**Features:**
- Fast computation using recursive formulas with memoization
- Optimized by precomputing characteristic functions

#### 4. `RecursiveDualAlgorithm`
A fast algorithm using dual recursive formulas.

```python
from shapley_bankruptcy.algorithms import RecursiveDualAlgorithm

algorithm = RecursiveDualAlgorithm()
result = algorithm.compute(E, w)
shapley_values = result.value
```

**Features:**
- Recursive computation using dual characteristic functions
- Fast computation with memoization

#### 5. `MonteCarloAlgorithm`
An approximation algorithm using the Monte Carlo method.

```python
from shapley_bankruptcy.algorithms import MonteCarloAlgorithm

# Specify the number of samples (default: 10000)
algorithm = MonteCarloAlgorithm(M=50000, seed=42)
result = algorithm.compute(E, w)
shapley_values = result.value
```

**Features:**
- Fast computation even for large-scale problems
- Adjustable balance between accuracy and speed via the number of samples M
- Reproducible results with seed setting

### Output Rounding

All algorithms can round results to a specified number of decimal places (default: 5 digits).

```python
algorithm = DynamicProgrammingAlgorithm(round_digits=3)
result = algorithm.compute(E, w)
shapley_values = result.value  # Results rounded to 3 decimal places
```

## Algorithm Details

For detailed descriptions and theoretical background of each algorithm, please refer to the paper "On Computing the Shapley Value in Bankruptcy Games".

### Characteristic Function of Bankruptcy Games

The characteristic function v(S) of a bankruptcy game is defined as:

```
v(S) = max(0, E - Σ_{j∉S} wⱼ)
```

where E is the total estate value and wⱼ is the claim of player j.

### Shapley Value

The Shapley value φᵢ for player i is defined as:

```
φᵢ = Σ_{S⊆N\{i}} (|S|!(n-|S|-1)!/n!) × [v(S∪{i}) - v(S)]
```

## Performance

Choose an algorithm based on the problem size and accuracy requirements:

- **Small-scale (n ≤ 10)**: `ExactAlgorithm` is appropriate
- **Medium-scale (10 < n ≤ 20)**: `DynamicProgrammingAlgorithm` or `RecursiveAlgorithm` is recommended
- **Large-scale (n > 20)**: `MonteCarloAlgorithm` is practical

## License

See the `LICENSE` file for license information.

## Author

ShuntaYamazaki (shuntaweb@gmail.com)

## References

This is an implementation of algorithms proposed in the paper "On Computing the Shapley Value in Bankruptcy Games".
