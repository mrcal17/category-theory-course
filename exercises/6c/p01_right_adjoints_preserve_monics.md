# 6C·P01 — Right adjoints preserve monics

**Type:** warm-up · **Technique:** moving an equation across an adjunction · **Unlocked by:** `6c_adjoints_and_limits` §2
**Source:** adapted from Leinster §6.3 and Riehl §4.5

## Statement

Let $F \dashv G$ be an adjunction with $F \colon \mathcal{A} \to \mathcal{B}$ and
$G \colon \mathcal{B} \to \mathcal{A}$. Prove, **directly from the definition of monic and without
using pullbacks**, that if $m \colon B \to B'$ is monic in $\mathcal{B}$ then
$G(m) \colon G(B) \to G(B')$ is monic in $\mathcal{A}$.

(There is also a two-line proof combining Theorem 1 with results from 5A and 5C. Find it
afterwards as a check; the point of this exercise is the transposition argument, which is the
proof of Theorem 1 in miniature.)

## What you may use

- The definition of monic (1B).
- That transposition is a bijection, and its naturality in $B$: equation (N) of the lecture, which is (N1) of 2A.

## What a complete proof must show

- [ ] The goal written with its quantifiers: for every object $A$ and every pair of maps $x, y \colon A \to G(B)$ with ...
- [ ] Every time an equation is moved from $\mathcal{A}$ to $\mathcal{B}$ or back, the fact that justifies the move is named.
- [ ] The hypothesis that $m$ is monic is used in $\mathcal{B}$, where it lives.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Start from the definition: take two parallel maps into $G(B)$ that become equal after composing
with $G(m)$. You want to cancel $G(m)$, but the only thing you are allowed to cancel is $m$, and
$m$ is in the other category.

</details>

<details>
<summary>Hint 2 — crossing over</summary>

Equation (N) relates $G(q) \circ \bar{g}$ to a transpose. Read it with $q = m$. Every map
$x \colon A \to G(B)$ is the transpose of something; of what?

</details>

<details>
<summary>Hint 3 — coming back</summary>

Once the equation lives in $\mathcal{B}$ and $m$ has been cancelled there, you have an equation
between two maps out of $F(A)$. Which property of transposition returns it to an equation between
$x$ and $y$?

</details>

## Check yourself

- Did your proof use both that transposition is injective and that it is natural? Where?
- State the dual result. Which functor does it concern, and which class of maps?
- Does a right adjoint preserve epics? Think about the inclusion of $\mathbb{Z}$ into $\mathbb{Q}$ in the category of rings and the forgetful functor to sets.

## Write it up

Write your proof in `proofs/6c/p01_right_adjoints_preserve_monics.md`, then ask Claude to review it.
