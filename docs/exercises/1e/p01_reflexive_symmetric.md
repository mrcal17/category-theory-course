# 1E·P01 — Equivalence is reflexive and symmetric

**Type:** warm-up · **Technique:** unpacking the definition · **Unlocked by:** `1e_equivalence` §2
**Source:** adapted from Leinster §1.3

## Statement

Prove, directly from the definition of an equivalence of categories:

1. (**Reflexive.**) For every category $\mathcal{A}$, $\mathcal{A} \simeq \mathcal{A}$.
2. (**Symmetric.**) If $\mathcal{A} \simeq \mathcal{B}$ then $\mathcal{B} \simeq \mathcal{A}$.

In each case say exactly what the four pieces of data (two functors, two natural isomorphisms)
are, and between which functors each natural isomorphism goes.

## What you may use

- The definition of an equivalence $(F, G, \eta, \varepsilon)$ (1E §2).
- The definition of a natural isomorphism as an isomorphism in a functor category, and identity natural transformations (1D §5, §6).
- In any category, the inverse of an isomorphism is an isomorphism (1B).
- Do **not** use Theorem 2 (full, faithful, essentially surjective); this exercise is about the definition.

## What a complete proof must show

- [ ] For part 1: the two functors and the two natural transformations, with the domain and codomain of each transformation written out, and the reason they are natural isomorphisms.
- [ ] For part 2: starting from data $(F, G, \eta, \varepsilon)$ for $\mathcal{A} \simeq \mathcal{B}$, the new data for $\mathcal{B} \simeq \mathcal{A}$, with each new natural isomorphism going in the direction the definition demands.
- [ ] A justification that each new transformation is natural, not only that its components are invertible.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Both parts are "there exists" statements: you prove them by writing down the data and checking
the checklist under the definition in §2. No idea is needed beyond careful bookkeeping of which
functor goes which way.

</details>

<details>
<summary>Hint 2 — part 2, the bookkeeping</summary>

Write the definition out a second time with the roles of $\mathcal{A}$ and $\mathcal{B}$
exchanged, using fresh letters for the four pieces of data. Which functor must go from
$\mathcal{B}$ to $\mathcal{A}$? What must be the domain and codomain of each of the two new
natural isomorphisms? Compare with what $\eta$ and $\varepsilon$ give you.

</details>

<details>
<summary>Hint 3 — directions</summary>

You will find that the transformations you have point the wrong way for the roles you need them
in. What does the definition of "isomorphism in the functor category" hand you for free?

</details>

## Check yourself

- For part 2, did you say why the inverse of a natural isomorphism is again a natural transformation, or did you only invert each component?
- Did you check the direction of each of your four natural transformations against the definition?
- What third property would make $\simeq$ an equivalence relation, and which exercise is it?

## Write it up

Write your proof in `proofs/1e/p01_reflexive_symmetric.md`, then ask Claude to review it.
