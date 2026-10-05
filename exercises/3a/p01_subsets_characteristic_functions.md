# 3A·P01 — Subsets are functions into the two-element set

**Type:** warm-up · **Technique:** explicit bijection · **Unlocked by:** `3a_sets_and_size` §4
**Source:** adapted from Leinster §3.1

## Statement

Let $A$ be a set and $2 = \{\mathrm{true}, \mathrm{false}\}$. For a subset $S \subseteq A$ let
$\chi_S \colon A \to 2$ be its characteristic function ($\chi_S(a) = \mathrm{true}$ exactly when
$a \in S$). Prove that
$$\Theta \colon \mathcal{P}(A) \to 2^A, \qquad \Theta(S) = \chi_S,$$
is a bijection.

## What you may use

- The definitions of $\mathcal{P}(A)$, of $2^A$ and of $\chi_S$ (3A §3, §4).
- A function is a bijection if and only if it has a two-sided inverse (0B).
- Two subsets of $A$ are equal when they have the same elements; two functions $A \to 2$ are equal when they agree at every element of $A$.

## What a complete proof must show

- [ ] A function $\Psi \colon 2^A \to \mathcal{P}(A)$ in the opposite direction, with its definition written out.
- [ ] $\Psi \circ \Theta = 1_{\mathcal{P}(A)}$, proved as an equality of **subsets** for an arbitrary $S$.
- [ ] $\Theta \circ \Psi = 1_{2^A}$, proved as an equality of **functions** for an arbitrary $\chi \colon A \to 2$, checked at an arbitrary $a \in A$.
- [ ] No counting: the proof must work when $A$ is infinite.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

The model is Proposition 2 of the lecture (currying): to show a function is a bijection, write
down a candidate inverse and verify the two composites. Each verification is an equality of two
things of a specific kind, and each kind has its own criterion for equality.

</details>

<details>
<summary>Hint 2 — the inverse</summary>

Given a function $\chi \colon A \to 2$, which subset of $A$ is it "trying to describe"? The
reading list under the definition in §4 contains the answer; your job is to prove it works.

</details>

<details>
<summary>Hint 3 — the second composite</summary>

When you check that two functions $A \to 2$ agree at $a$, you will have two cases, according
to the value of one of them at $a$. The set $2$ has exactly two elements; where do you use that?

</details>

## Check yourself

- Did you check both composites? One of them alone proves only injectivity or only surjectivity; which?
- Where did you use that $2$ has *exactly* two elements? Would the statement be true with a three-element set in place of $2$?
- Does your proof handle $A = \emptyset$ without a special case?

## Write it up

Write your proof in `proofs/3a/p01_subsets_characteristic_functions.md`, then ask Claude to review it.
