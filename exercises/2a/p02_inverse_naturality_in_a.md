# 2A·P02 — The second inverse naturality equation

**Type:** warm-up · **Technique:** working with transposes · **Unlocked by:** `2a_adjunctions` §1
**Source:** adapted from Leinster §2.1

## Statement

Let $F \colon \mathcal{A} \to \mathcal{B}$ and $G \colon \mathcal{B} \to \mathcal{A}$ be
functors with $F \dashv G$. Prove equation (N2'): for all arrows $g \colon F(A) \to B$ in
$\mathcal{B}$ and $p \colon A' \to A$ in $\mathcal{A}$,

$$\overline{g \circ F(p)} \;=\; \bar{g} \circ p .$$

## What you may use

- The definition of an adjunction: the bijections $g \mapsto \bar{g}$ and $f \mapsto \bar{f}$
  are mutually inverse, and equations (N1) and (N2) hold.
- Lemma 1 of the lecture as a *model*. You may not quote (N2') itself.

## What a complete proof must show

- [ ] It says in which category, and between which objects, each side of the equation lives.
- [ ] Every use of a bar is on an arrow of the correct form ($F(\text{something}) \to \text{something}$, or $\text{something} \to G(\text{something})$).
- [ ] It says explicitly which of (N1), (N2) is applied, and to which two arrows.
- [ ] It says explicitly where "the two bars are mutually inverse" is used.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

This is the mirror image of Lemma 1. There, an equation about $f \mapsto \bar{f}$ was deduced
from the equation about $g \mapsto \bar{g}$. Here it is the other way round. Which of (N1) and
(N2) involves an arrow $p \colon A' \to A$?

</details>

<details>
<summary>Hint 2 — what to feed in</summary>

The naturality equation you chose is a statement about an arbitrary arrow of the form
$A \to G(B)$. You have been given an arrow $g \colon F(A) \to B$ instead. Does $g$ hand you
an arrow of the required form?

</details>

<details>
<summary>Hint 3 — finishing</summary>

After applying the naturality equation you will have an equation between two arrows of
$\mathcal{B}$, but the statement wants an equation between two arrows of $\mathcal{A}$. What
operation moves an equation from one side to the other, and why is it legitimate to apply it
to both sides?

</details>

## Check yourself

- Write the domain and codomain of $g \circ F(p)$ and of $\bar{g} \circ p$. Do they match what the bar should produce?
- Did you use that $F$ is a functor? (You should not need to.)
- Put (N1), (N2), (N1'), (N2') in a two-by-two table: which variable, which direction of the bar. Could you reproduce all four from memory?

## Write it up

Write your proof in `proofs/2a/p02_inverse_naturality_in_a.md`, then ask Claude to review it.
