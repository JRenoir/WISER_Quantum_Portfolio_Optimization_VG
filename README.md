# Quantum for Portfolio Optimization

A WISER 2025 Quantum Projects: https://www.thewiser.org/quantum-projects

Project Name: Portfolio Optimization

## Team

Team Name: TAMU for Portfolio Optimization

| Member's Name             | WISER Enrollment ID |
| ------------------------- | ------------------- |
| Qingtian Miao<sup>*</sup> | gst-4UiYo4Uymy3kg8z |
| Wenzhuo Zhang             | gst-AmK6smzoJwnxJH0 |
| Yuhan Wu                  | gst-ah8E30GshygYrpw |

<small>* Group leader.</small>

## Summary

### I. Review the mathematical formulation

We consider a binary quadratic optimization problem with linear constraints.

**Decision variables**: For each bond $c\in C$, $y_c$ is a binary decision variable ($y_c\in\{0,1\}$, where $y_c=1$ means bond c is selected to be in the portfolio, and $y_c=0$ means it is not included). In this simplified model, we fix derived quantity $x_c$ to a predetermined amount whenever $y_c=1$.

**Linear constraints**:

1. We limit how many bonds can be selected, to at most $N$, that is, $\sum_{c \in C} y_c \leq N$.

2. We invest an appropriate amount of money, $1-\frac{\max R C}{M V^b} \leq \sum_{c \in C} \frac{p_c}{100} \frac{\delta_c}{M V^b} x_c \leq 1-\frac{\min R C}{M V^b}$, where $M V^b$ is the total market value of the budget, minRC and maxRC specify the allowed range for residual cash, $p_c$ is market price and $\delta_c$ is minimum increment for bond $c$.
3. Characteristic constraints on selections (binary version): $K_{\ell, j}^{\mathrm{low}}\le\sum_{c \in K_{\ell}} \beta_{c, j} y_c \leq K_{\ell, j}^{\mathrm{up}}$, $\forall j \in J,\ \ell \in L$, where $j$ represents a characteristic, $\ell$ represents a risk bucket, and $\beta_{c,j}$ is the contribution factor of bond $c$ to characteristic $j$. The $K_{\ell,j}^{\rm low}$ and $K_{\ell,j}^{\rm up}$ constraints are making sure the portfolio’s total amount of characteristic $j$ in bucket $\ell$ falls between the guardrails.

**Quadratic objective**:

We want to mimic the index’s characteristics as closely as possible, so our objective will penalize any differences between the portfolio and the index in those characteristics. The given objective is quadratic, $\min\sum_{\ell \in L} \sum_{j \in J} \rho_j\left(\sum_{c \in K_{\ell}} \beta_{c, j} x_c-K_{\ell, j}^{\mathrm{target}}\right)^2$, where $\rho_j$ is a weight for characteristic $j$, and $K_{\ell,j}^{\rm target}$ is the target value of characteristic $j$ in bucket $\ell$, as measured in the index.

### II. Convert the binary optimization problem to quadratic unconstrained binary optimization (QUBO)

Since each $y_c$ is binary ($0$ or $1$), note that $y_c^2=y_c$. The cross terms $y_cy_{c'}$ are the true quadratic interactions. We can write our quadratic objective using an upper triangular matrix $Q\in \mathbb{R}^{n\times n}$, where $n$ is the number of bonds in the set we considered,

$$\min_x x^TQx+c,$$

where $c$ is a constant. It can be mapped to an Ising spin-glass Hamiltonian, making it amenable to implementation on a quantum computer. The linear constraints can be encoded in $A\in\mathbb{R}^{m\times n}$, where $m$ is the number of constraints, such that constraints write as $Ax-b\ge0$. 

Following the approach used by the project initiators, we incorporate the problem’s constraints directly into the objective function by adding a quadratic penalty term,

$$\min_x x^TQx+c+\lambda\sum_{i=1}^m[\max(0,b_i-(Ax)_i)]^2,$$

where the penalty coefficient $\lambda$ is set as

$$\lambda=1.1(\sum_{i,j}Q_{ij}^+-\sum_{i,j}Q_{ij}^-),$$

where $Q_{ij}^+$ denotes the positive entries of the matrix $Q$, and $Q_{ij}^-$ denotes the negative entries in $Q$ matrix. This ensures penalties dominate objective when constraints are violated.

### III. Write a quantum optimization program

We map $n$ binary variables to $n$ qubits. Following the project initiators’ approach, we employ the Variational Quantum Eigensolver (VQE) to solve the unconstrained formulation. Inspired by both the TwoLocal ansatz and the BFCD ansatz (https://arxiv.org/pdf/2405.13898), we design **a custom ansatz** (named `'TwoLocalxx'`) **in which the entanglement block consists of RXX gates arranged according to a bilinear entanglement map**. This structure aims to balance expressibility and circuit depth while leveraging efficient two-qubit interactions. 

We added a new branch in `/src/step_1.py` to handle the case `ansatz == 'TwoLocalxx'`.

**Ansatz Details**:

- **Architecture**: RY rotation gates + RXX entangling gates
- **Parameter**: `θ[0], θ[1], ..., θ[2n-1]` (parameterized rotation angles)
- **Ansatz params**: `{'reps': 1, 'entanglement': 'bilinear'}`
- **Final Measurements**: All qubits measured to classical bits

For the case of $8$ qubits, the ansatz is depicted schematically in the circuit below.

<p align="center">
<img width="600" height="867" alt="Image" src="https://github.com/user-attachments/assets/eb4d45e5-f414-43f4-b11f-9994b5763bf7" />
</p>

In general, for $n$ qubits, the circuit contains $2n-1$ gates and $2n-1$ tunable parameters to be optimized to minimize objective function by the optimizer. Both the depth and the number of parameters are smaller than those of the standard TwoLocal ansatz and the BFCD ansatz provided in the project initiators’ repository. **As shown in the Summary V, this design proves more efficient for tackling the 31-bonds problem**.

### IV. Solve the 31-bond optimization problem

The quantum solution can be viewed in [solve_31_bond_problem.ipynb](solve_31_bond_problem.ipynb).  
In this notebook, the solution is validated using a classical optimization routine for comparison with the quantum approach.

**Details**:

We adopt the optimization pipeline developed by the project initiators:

Step 1: Problem mapping and circuit pattern construction; Step 2: Circuit optimization and transpilation; Step 3: Backend execution and optimization

We also adopt the gradient-free NFT optimizer (https://arxiv.org/pdf/1903.12166) and CVaR aggregation rule ($\alpha$ is fixed at $0.1$) developed by the project initiators. **We are also implementing a new quantum natural gradient optimizer, which will be tested in the next stage**; see **Appendix II** for details.

**Parameters Used**:

- LP file: `data/1/31bonds/docplex-bin-avgonly-nocplexvars.lp` (An original optimization **31-bond problem** with binary variables `iTrade_*`, quadratic objective function, and linear inequality constraints; We uses CPLEX for parsing the LP file)
- Ansatz: `'TwoLocalxx'`
- Ansatz params: `{'reps': 1, 'entanglement': 'bilinear'}`
- Theta initial: `'piby3'` (Parameter initialization)
- Backend: `'AerSimulator'`
- Simulator Type: Matrix Product State (MPS) method
- Noise Model: Noiseless (ideal simulation)

### V. Comparison with the Benchmark Solution

Our ansatz outperforms the standard TwoLocal ansatz and the BFCD ansatz in most experiments, achieving optimal solution with fewer iterations (see the convergence figure below, for details, see the Project Presentation deck).

To further enhance performance for large-scale problems, we designed an entanglement map based on a Small-World graph. This approach aims to improve connectivity efficiency and is described in detail in Appendix I.

## Project Presentation deck

[📄 Project Presentation Deck](Project_Presentation_deck.pptx)

## Appendix

### I. Entanglement Map Based on a Small-World Graph

We design an entanglement map inspired by the small-world network model of Watts–Strogatz, aiming to reduce the average path length between qubits. The core idea is to modify the standard ring connectivity by introducing a probability of connecting two distant qubits. Using a connected Watts–Strogatz graph with $n$ nodes, each connected to $k$ nearest neighbors and a rewiring probability $p$, we generate an edge set representing qubit connections. The resulting edges are then decomposed into matching layers, where each layer contains edges that do not share nodes. This allows the entanglement operations within a layer to be executed in parallel in the quantum circuit.

For small $p$, the connectivity pattern is only slightly modified from the bilinear pattern, but it introduces a few long-range “shortcuts” that reduce the average path length. This approach is currently a prototype and remains to be fully tested, but we anticipate it could be beneficial for large-scale instances where the problem coupling matrix is not geometrically local—e.g., the interaction between qubits $1$ and $n$ can be comparable to that of neighboring pairs. In such cases, a pure ring forces multi-hop mediation and may slow information propagation; our small-world edges add sparse shortcuts that better align the circuit connectivity with the problem couplings while keeping two-qubit depth low via layered matchings. 

For the small-world entanglement approach, we added two functions — `find_small_world_edges` and `_layerize_edges` — in `/src/step_1.py`.

- `find_small_world_edges` generates a connected Watts–Strogatz graph for a given number of qubits, degree $k$, and rewiring probability $p$, returning the edge list.
- `_layerize_edges` decomposes the edge set into matching layers, where no two edges in the same layer share a node, enabling parallel execution of entangling gates in the quantum circuit.

To use this method, set `"entanglement": "smallworld"` in the input parameters.

For the case of $8$ qubits, the ansatz based on the small-world graph ($p=0.1$, $k=2$) is depicted schematically in the circuit below.

<p align="center">
<img width="600" height="858" alt="Image" src="https://github.com/user-attachments/assets/6186afe7-e24a-4293-92e1-8a352c8fe5b3" />
</p>
**Ansatz Details**:

- Ansatz: `'TwoLocalxx'`
- Ansatz params: `{'reps': 1, 'entanglement': 'smallworld'}`

For this certain circuit, it builds upon the bilinear pattern with an extra layer. In general, for $n$ qubits, the circuit ($k=2$) contains $2n$ gates and $2n$ tunable parameters to be optimized by the optimizer.

### II. Quantum Natural SPSA Optimizer

We are currently implementing a new quantum natural gradient optimizer inspired by [PennyLane’s QN-SPSA demo](https://pennylane.ai/qml/demos/qnspsa). QN-SPSA is a built-in method in `qiskit.algorithms.optimizers`. QN refers to metric calculation to smooth the landscape of search and SPSA uses two estimations to approximate the gradient and tensor metric in searching. It covers more parameters in each iteration and stochastic estimation avoids complicated differential operations.

The original project initiators used the NFT optimizer as the primary variational parameter update method. NFT, being a classical approach, does not take into account the geometric properties of quantum state space. In contrast, a quantum natural gradient method introduces the structure of the non-Euclidean parameter space. Prior benchmarking indicates that QN-SPSA can achieve faster convergence and higher final accuracy than conventional optimizers, making it a strong candidate for variational quantum algorithms.

We have added a new branch to the QN-SPSA implementation in `/src/sbo/src/optimizer/optimization_wrapper.py`. The new file `/src/sbo/src/optimizer/QNSPSA_extra.py` defines a helper function for feeding parameters into the QNSPSA optimizer, including the maximum number of iterations and the learning rate. These values can be adjusted for fine-tuning. To use this method, set `optimizer='QNSPSA'` (instead of `optimizer='nft'`) when specifying the optimizer in the input.































