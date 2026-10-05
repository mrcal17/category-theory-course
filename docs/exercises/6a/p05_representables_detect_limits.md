# 6A·P05 — Representables jointly detect limits

**Type:** core · **Technique:** testing a universal property against all representables · **Unlocked by:** `6a_limits_representables_adjoints` §7
**Source:** adapted from Riehl §3.4

## Statement

Let $\mathcal{A}$ be a locally small category, $D \colon \mathbf{I} \to \mathcal{A}$ a diagram, and
$(p_I \colon L \to D(I))_{I}$ a cone on $D$.

Suppose that for **every** object $A$ of $\mathcal{A}$, the cone
$$\big( p_I \circ - \colon \mathcal{A}(A, L) \to \mathcal{A}(A, D(I)) \big)_{I}$$
is a limit cone in $\mathbf{Set}$ on the diagram $\mathcal{A}(A, D(-))$.

Prove that $(p_I)_I$ is a limit cone on $D$ in $\mathcal{A}$.

(Together with Theorem 3 this says: a cone is a limit cone if and only if every representable
$\mathcal{A}(A, -)$ sends it to a limit cone.)

## What you may use

- The definition of a limit cone, in $\mathcal{A}$ and in $\mathbf{Set}$ (5A).
- Lemma 2 and Theorem 1 of the lecture.
- Basic facts about functions out of a one-element set (0B, 3A).

## What a complete proof must show

- [ ] For an arbitrary object $A$ and cone $(f_I)$ on $D$ with vertex $A$, a specific cone in $\mathbf{Set}$ is written down and shown to be a cone.
- [ ] The mediating function supplied by the hypothesis is converted into a map $A \to L$, and the required equations are verified.
- [ ] Uniqueness of the map $A \to L$ is derived from uniqueness of the mediating function, not asserted.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

The hypothesis is a universal property in $\mathbf{Set}$, one for each $A$. A universal property
only does something when you feed it a cone. So the first job is to turn a cone on $D$ in
$\mathcal{A}$ into a cone in $\mathbf{Set}$.

</details>

<details>
<summary>Hint 2 — choosing the vertex</summary>

A cone in $\mathbf{Set}$ has a vertex set $S$ and functions $S \to \mathcal{A}(A, D(I))$. For which
set $S$ is a function $S \to \mathcal{A}(A, D(I))$ the same thing as a single map $A \to D(I)$?

</details>

<details>
<summary>Hint 3 — coming back</summary>

With that $S$, what is a function $S \to \mathcal{A}(A, L)$? Translate "there is a unique function
$S \to \mathcal{A}(A, L)$ commuting with the projections" into a sentence about maps of $\mathcal{A}$.

</details>

## Check yourself

- Did your proof use the hypothesis at every object $A$, or only at some? Which?
- Did you need the full strength of "limit cone in $\mathbf{Set}$", or only its consequence for one particular vertex set?
- Could you instead have used the explicit description of limits in $\mathbf{Set}$ from 5A? What would that proof look like?

## Write it up

Write your proof in `proofs/6a/p05_representables_detect_limits.md`, then ask Claude to review it.
