# Quantum for Portfolio Optimization

A WISER 2025 Quantum Projects: https://www.thewiser.org/quantum-projects

Project Name: Portfolio Optimization

## Team

Team Name: TAMU for Portfolio Optimization

| Member's Name | WISER Enrollment ID |
| ------------- | ------------------- |
| Qingtian Miao | gst-4UiYo4Uymy3kg8z |
| Yuhan Wu      | gst-ah8E30GshygYrpw |
| Wenzhuo Zhang | gst-AmK6smzoJwnxJH0 |

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

Since each $y_c$ is binary (0 or 1), note that $y_c^2=y_c$. The cross terms $y_cy_{c'}$ are the true quadratic interactions. We can write our quadratic objective using an upper triangular matrix $Q\in \mathbb{R}^{n\times n}$, where $n$ is the number of bonds in the set we considered,

$$\min_x x^TQx+c,$$

where $c$ is a constant. It can be mapped to an Ising spin-glass Hamiltonian, making it amenable to implementation on a quantum computer. The linear constraints can be encoded in $A\in\mathbb{R}^{m\times n}$, where $m$ is the number of constraints, such that constraints write as $Ax-b\ge0$. Following the approach used by the Vanguard team, we incorporate the problem’s constraints directly into the objective function by adding a quadratic penalty term,

$$\min_x x^TQx+c+\lambda\sum_{i=1}^m[\max(0,b_i-(Ax)_i)]^2,$$

where the penalty coefficient $\lambda$ is set as

$$\lambda=1.1(\sum_{i,j}Q_{ij}^+-\sum_{i,j}Q_{ij}^-),$$

where $Q_{ij}^+$ denotes the positive entries of the matrix $Q$, and $Q_{ij}^-$ denotes the negative entries in $Q$ matrix.

### III. Write a quantum optimization program

Following the Vanguard team’s approach, we employ the Variational Quantum Eigensolver (VQE) to solve the unconstrained formulation. Inspired by both the TwoLocal ansatz and the BFCD ansatz (https://arxiv.org/pdf/2405.13898), we design a custom ansatz in which the entanglement block consists of $R_{xx}(\theta)$ gates arranged according to a bilinear entanglement map. This structure aims to balance expressibility and circuit depth while leveraging efficient two-qubit interactions. For the case of $8$ qubits, the ansatz is depicted schematically in the circuit below.

<img width="600" height="867" alt="Image" src="https://github.com/user-attachments/assets/eb4d45e5-f414-43f4-b11f-9994b5763bf7" />

In general, for $n$ qubits, the circuit contains $2n-1$ gates and $2n-1$ tunable parameters to be optimized by the classical optimizer. Both the depth and the number of parameters are smaller than those of the standard TwoLocal ansatz and the BFCD ansatz provided in the Vanguard team’s repository. As shown in the subsection IV, this design proves more efficient for tackling the 31-bonds problem.

### IV. Solve the optimization problem













