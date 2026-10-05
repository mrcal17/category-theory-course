# 2A·P01 — Adjunctions between discrete categories

**Type:** warm-up · **Technique:** unpacking the definition · **Unlocked by:** `2a_adjunctions` §1
**Source:** adapted from Leinster §2.1

## Statement

Recall that a category is *discrete* if its only arrows are identities. Let $\mathcal{A}$ and
$\mathcal{B}$ be discrete categories and let $F \colon \mathcal{A} \to \mathcal{B}$ and
$G \colon \mathcal{B} \to \mathcal{A}$ be functors. Prove that $F \dashv G$ if and only if
$G(F(A)) = A$ for every object $A$ of $\mathcal{A}$ and $F(G(B)) = B$ for every object $B$ of
$\mathcal{B}$.

## What you may use

- The definition of an adjunction from 2A §1: the bijections and the equations (N1) and (N2).
- The definition of a discrete category, and the fact that a functor between discrete
  categories is determined by what it does on objects.

## What a complete proof must show

- [ ] It describes the hom-sets $\mathcal{B}(F(A), B)$ and $\mathcal{A}(A, G(B))$ explicitly: when each is empty and what it contains otherwise.
- [ ] Both directions of the "if and only if" are proved, each labelled.
- [ ] In the direction that constructs an adjunction, the bijection is specified for *every* pair $(A, B)$, including the pairs where the hom-sets are empty.
- [ ] (N1) and (N2) are addressed, with a reason, and not skipped.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

This is an "if and only if" obtained by unpacking a definition. Before proving anything,
translate: in a discrete category, what does it mean for a hom-set to be non-empty? How many
elements can it have?

</details>

<details>
<summary>Hint 2 — what a bijection between tiny sets says</summary>

Two sets that each have at most one element are in bijection under exactly one circumstance.
State the existence of the adjunction's bijections as a condition relating two *equations
between objects*, one in $\mathcal{B}$ and one in $\mathcal{A}$.

</details>

<details>
<summary>Hint 3 — choosing the objects</summary>

Your condition holds for all pairs $(A, B)$. To extract a statement about $G(F(A))$, which $B$
is worth pairing with a given $A$? For the converse, you are given two equations and must
prove an implication in each direction; what can you apply to both sides of an equation
between objects?

</details>

<details>
<summary>Hint 4 — naturality</summary>

Look at the arrows $q$ and $p$ that appear in (N1) and (N2). In a discrete category, what
must they be? Compare with how naturality was handled in Proposition 4 of the lecture.

</details>

## Check yourself

- Did you use that $F$ and $G$ are functors anywhere, or only that they are functions on objects? Is that reasonable here?
- Your result says $F$ and $G$ are mutually inverse bijections on objects. Does an adjunction between non-discrete categories force that? Name a counterexample from the lecture.
- Did you handle a pair $(A, B)$ for which both hom-sets are empty?

## Write it up

Write your proof in `proofs/2a/p01_discrete_adjunctions.md`, then ask Claude to review it.
