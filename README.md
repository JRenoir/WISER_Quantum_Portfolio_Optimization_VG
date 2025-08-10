# Quantum for Portfolio Optimization

A WISER 2025 Quantum Projects: https://www.thewiser.org/quantum-projects

Project Name: Portfolio Optimization

## Team

Team Name: TAMU for Portfolio Optimization

| Member's Name (in alphabetical order) | WISER Enrollment ID |
| ------------------------------------- | ------------------- |
| Qingtian Miao<sup>*</sup>             | gst-4UiYo4Uymy3kg8z |
| Yuhan Wu                              | gst-ah8E30GshygYrpw |
| Wenzhuo Zhang                         | gst-AmK6smzoJwnxJH0 |

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

We map $n$ binary variables to $n$ qubits. Following the project initiators’ approach, we employ the Variational Quantum Eigensolver (VQE) to solve the unconstrained formulation. Inspired by both the TwoLocal ansatz and the BFCD ansatz (https://arxiv.org/pdf/2405.13898), we design a custom ansatz (named `'TwoLocalxx'`) in which the entanglement block consists of RXX gates arranged according to a bilinear entanglement map. This structure aims to balance expressibility and circuit depth while leveraging efficient two-qubit interactions. 

**Ansatz Details**:

- **Architecture**: RY rotation gates + RXX entangling gates
- **Parameter**: `θ[0], θ[1], ..., θ[2n-1]` (parameterized rotation angles)
- **Final Measurements**: All qubits measured to classical bits

For the case of $8$ qubits for $8$-bond problem, the ansatz is depicted schematically in the circuit below.

<p align="center">
<img width="600" height="867" alt="Image" src="https://github.com/user-attachments/assets/eb4d45e5-f414-43f4-b11f-9994b5763bf7" />
</p>

In general, for $n$ qubits, the circuit contains $2n-1$ gates and $2n-1$ tunable parameters to be optimized by the classical optimizer. Both the depth and the number of parameters are smaller than those of the standard TwoLocal ansatz and the BFCD ansatz provided in the project initiators’ repository. As shown in the subsection IV, this design proves more efficient for tackling the $31$-bonds problem.

VQE will modify these angles to minimize objective function. 

### IV. Solve the optimization problem

We adopt the optimization pipeline developed by the project initiators:

Step 1: Problem mapping and circuit pattern construction; Step 2: Circuit optimization and transpilation; Step 3: Backend execution and optimization; Step 4: Post-processing and local search

**Parameters Used**:

- LP file: `data/1/31bonds/docplex-bin-avgonly-nocplexvars.lp` (An original optimization $31$-bond problem with binary variables `iTrade_*`, quadratic objective function, and linear inequality constraints)
- Ansatz: `'TwoLocalxx'`
- Ansatz params: `{'reps': 1, 'entanglement': 'bilinear'}`
- Theta initial: `'piby3'` (Parameter initialization)
- Backend: `'AerSimulator'`
- Simulator Type: Matrix Product State (MPS) method
- Noise Model: Noiseless (ideal simulation)

## Appendix

### I. Entanglement Map Based on a Small-World Graph

**Ansatz params**: `'entanglement': 'smallworld'`

We design an entanglement map inspired by the small-world network model of Watts–Strogatz, aiming to reduce the average path length between qubits. The core idea is to modify the standard ring connectivity by introducing a probability of connecting two distant qubits. Using a connected Watts–Strogatz graph with $n$ nodes, each connected to $k$ nearest neighbors and a rewiring probability $p$, we generate an edge set representing qubit connections. The resulting edges are then decomposed into matching layers, where each layer contains edges that do not share nodes. This allows the entanglement operations within a layer to be executed in parallel in the quantum circuit.

For small $p$, the connectivity pattern is only slightly modified from the bilinear pattern, but it introduces a few long-range “shortcuts” that reduce the average path length. This approach is currently a prototype and remains to be fully tested, but we anticipate it could be beneficial for large-scale instances where the problem coupling matrix is not geometrically local—e.g., the interaction between qubits $1$ and $n$ can be comparable to that of neighboring pairs. In such cases, a pure ring forces multi-hop mediation and may slow information propagation; our small-world edges add sparse shortcuts that better align the circuit connectivity with the problem couplings while keeping two-qubit depth low via layered matchings. 

<p align="center">
<img width="600" height="858" alt="Image" src="https://github.com/user-attachments/assets/6186afe7-e24a-4293-92e1-8a352c8fe5b3" />
</p>































