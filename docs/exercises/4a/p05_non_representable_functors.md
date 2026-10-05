# 4A·P05 — A test for non-representability

**Type:** core · **Technique:** proving a negative with an invariant · **Unlocked by:** `4a_representables` §2
**Source:** adapted from Riehl §2.1

## Statement

Recall that a **terminal object** of a category $\mathcal{A}$ is an object $1$ such that for every
object $A$ there is exactly one arrow $A \to 1$.

1. Let $\mathcal{A}$ be a locally small category with a terminal object $1$, and let
   $X \colon \mathcal{A} \to \mathbf{Set}$ be a representable functor. Prove that $X(1)$ has
   exactly one element.
2. Let $S \colon \mathbf{Set} \to \mathbf{Set}$ be the functor with $S(B) = B \times \{0, 1\}$
   (two disjoint copies of $B$) and $S(g)(b, i) = (g(b), i)$. Prove that $S$ is **not** representable.
3. Let $Q \colon \mathbf{Set} \to \mathbf{Set}$ be the functor with $Q(B) = B \times B$ and
   $Q(g)(b, b') = (g(b), g(b'))$. Prove that $Q$ **is** representable.

You may take it as given that $S$ and $Q$ are functors.

## What you may use

- The definition of a representable functor and of a representation (4A §2).
- From 1D: the components of a natural isomorphism are isomorphisms; in $\mathbf{Set}$ these are bijections.
- The definition of a terminal object; that a one-element set is terminal in $\mathbf{Set}$.

## What a complete proof must show

- [ ] Part 1 is proved for an arbitrary representing object $A$, not for a particular one.
- [ ] Part 2 is a proof that *no* object and *no* natural isomorphism can work, not a report that
      one attempted bijection failed.
- [ ] Part 3 names a representing set, a function for each $B$, shows each is a bijection, and
      verifies naturality for an arbitrary function $g \colon B \to C$.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Part 1 produces an *invariant*: a property that every representable functor on $\mathcal{A}$ has.
Part 2 is then a proof by contradiction that uses the invariant. Part 3 is a separate, positive
argument following the checklist in 4A §2.

</details>

<details>
<summary>Hint 2 — part 1</summary>

If $X \cong H^A$, then the set $X(1)$ is in bijection with a certain hom-set. Write that hom-set
down. What does the word "terminal" say about it?

</details>

<details>
<summary>Hint 3 — part 3</summary>

A pair of elements of $B$ is two elements of $B$, each chosen freely. An element of $B$ is the
same as a function from a one-element set (4A, Proposition 2.1). A pair of elements of $B$ is the
same as a function from what?

</details>

## Check yourself

- Does the functor $Q$ pass the test of part 1? It had better.
- Passing the test of part 1 does not prove representability. Can you see why the test is only
  one-directional?
- In part 2, did you use the full strength of "natural isomorphism", or only one component? Say which.

## Write it up

Write your proof in `proofs/4a/p05_non_representable_functors.md`, then ask Claude to review it.
