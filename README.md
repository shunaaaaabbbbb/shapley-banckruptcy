![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)
[![arXiv](https://img.shields.io/badge/arXiv-2511.22208-b31b1b?logo=arxiv)](https://arxiv.org/abs/2511.22208)
![NumPy](https://img.shields.io/badge/NumPy-Used-blue?logo=numpy)
![Algorithms](https://img.shields.io/badge/Algorithms-Game%20Theory-yellow)

# Shapley-Bankruptcy

Implementation of algorithms for computing the Shapley value in bankruptcy games. This repository contains implementations of algorithms proposed in the paper "On Computing the Shapley Value in Bankruptcy Games".

ArXiv: https://arxiv.org/abs/2511.22208

## Overview

A bankruptcy game is a cooperative game where an estate of value $E$ must be divided among creditors with claims $w = (w_1, w_2, ..., w_n)$. This implementation provides multiple efficient algorithms for computing the Shapley value in such games.

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
git clone https://github.com/shunaaaaabbbbb/shapley-banckruptcy.git
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

#### 2. `DynamicProgrammingAlgorithm`
A fast algorithm using dynamic programming.

```python
from shapley_bankruptcy.algorithms import DynamicProgrammingAlgorithm

algorithm = DynamicProgrammingAlgorithm()
result = algorithm.compute(E, w)
shapley_values = result.value
```

#### 3. `RecursiveAlgorithm`
A fast algorithm using recursive formulas.

```python
from shapley_bankruptcy.algorithms import RecursiveAlgorithm

algorithm = RecursiveAlgorithm()
result = algorithm.compute(E, w)
shapley_values = result.value
```

#### 4. `RecursiveDualAlgorithm`
A fast algorithm using dual recursive formulas.

```python
from shapley_bankruptcy.algorithms import RecursiveDualAlgorithm

algorithm = RecursiveDualAlgorithm()
result = algorithm.compute(E, w)
shapley_values = result.value
```

#### 5. `MonteCarloAlgorithm`
An approximation algorithm using the Monte Carlo method.

```python
from shapley_bankruptcy.algorithms import MonteCarloAlgorithm

# Specify the number of samples (default: 10000)
algorithm = MonteCarloAlgorithm(M=50000, seed=42)
result = algorithm.compute(E, w)
shapley_values = result.value
```

### Output Rounding

All algorithms can round results to a specified number of decimal places (default: 5 digits).

```python
algorithm = DynamicProgrammingAlgorithm(round_digits=3)
result = algorithm.compute(E, w)
shapley_values = result.value  # Results rounded to 3 decimal places
```

## Algorithm Details

For detailed descriptions and theoretical background of each algorithm, please refer to the paper [On Computing the Shapley Value in Bankruptcy Games](https://arxiv.org/abs/2511.22208).

### Characteristic Function of Bankruptcy Games

The characteristic function $v(S)$ of a bankruptcy game is defined as:

```math
v(S) = \max(0, E - \sum_{i\in N\setminus S} w_i)
```

where $E$ is the total estate value and $w_i$ is the claim of player $i$.

### Shapley Value

The Shapley value $\phi_i$ for player $i$ is defined as:

```math
\phi_i = \sum_{S\subseteq N\setminus \{i\}} \frac{|S|!(n-|S|-1)!}{n!}(v(S\cup \{i\}) - v(S))
```

## License

See the `LICENSE` file for license information.

## Author

Shunta Yamazaki (shuntaweb@gmail.com)

## References

This is an implementation of algorithms proposed in the paper [On Computing the Shapley Value in Bankruptcy Games](https://arxiv.org/abs/2511.22208).
