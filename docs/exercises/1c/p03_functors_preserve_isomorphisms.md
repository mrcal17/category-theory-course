# 1C·P03 — Functors preserve isomorphisms

**Type:** core · **Technique:** applying a functor to an equation; counterexample · **Unlocked by:** `1c_functors` §1, §4
**Source:** adapted from Leinster §1.2

## Statement

Let $F \colon \mathcal{A} \to \mathcal{B}$ be a functor.

(a) Prove that if $f \colon A \to A'$ is an isomorphism in $\mathcal{A}$, then $F(f)$ is an
isomorphism in $\mathcal{B}$, and $F(f)^{-1} = F(f^{-1})$.

(b) Deduce that if $A \cong A'$ in $\mathcal{A}$, then $F(A) \cong F(A')$ in $\mathcal{B}$.

(c) Show that the converse of (a) is false: give categories $\mathcal{A}$, $\mathcal{B}$, a
functor $F \colon \mathcal{A} \to \mathcal{B}$ and an arrow $f$ of $\mathcal{A}$ such that
$F(f)$ is an isomorphism but $f$ is not. Justify every claim about your example.

## What you may use

- The definition of a functor and of an isomorphism.
- Proposition 1.1 of 1B (inverses are unique), to make sense of $F(f)^{-1}$.
- For (c): any category and any functor that the lectures of 1A–1C have shown to be a category
  or a functor.

## What a complete proof must show

- [ ] In (a): a candidate inverse for $F(f)$ is named, with its domain and codomain.
- [ ] In (a): **both** equations of the definition of isomorphism are verified for $F(f)$, with each step attributed to a specific functor axiom or to a hypothesis on $f$.
- [ ] In (a): the formula $F(f)^{-1} = F(f^{-1})$ is justified, not just asserted.
- [ ] In (c): a proof that $f$ is not an isomorphism (no inverse exists), and a proof that $F(f)$ is.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Part (a) is an existence proof: you must exhibit an inverse for $F(f)$. The hypothesis hands
you an arrow of $\mathcal{A}$ and two equations in $\mathcal{A}$. The only tool that moves
things from $\mathcal{A}$ to $\mathcal{B}$ is $F$.

</details>

<details>
<summary>Hint 2 — which axioms, and how many times</summary>

Each of the two equations you start from has a composite on one side and an identity on the
other. A functor has one axiom about composites and one about identities. Plan to use each
axiom once per equation.

</details>

<details>
<summary>Hint 3 — part (c)</summary>

You want a functor that is forced to send a non-isomorphism to an isomorphism. One way to
force this is to choose a target category with very few arrows. What is the smallest category
you know, and which functors go into it?

</details>

## Check yourself

- Did you verify two equations in (a), in two different hom-sets of $\mathcal{B}$?
- Where did you use preservation of identities? If nowhere, something is missing.
- In (c), did you prove that $f$ has *no* inverse, as opposed to pointing at one arrow that is not an inverse?
- The contrapositive of (b) is how invariants are used: if $F(A) \not\cong F(A')$ then $A \not\cong A'$. Can you think of an invariant from algebra or topology that works this way?

## Write it up

Write your proof in `proofs/1c/p03_functors_preserve_isomorphisms.md`, then ask Claude to review it.
