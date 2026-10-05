# 6D·P03 — The comparison functor is well defined

**Type:** core · **Technique:** checking algebra axioms · **Unlocked by:** `6d_monads` §6
**Source:** adapted from Riehl §5.2–5.3

## Statement

Let $F \dashv G$ be an adjunction, $F \colon \mathcal{A} \to \mathcal{B}$,
$G \colon \mathcal{B} \to \mathcal{A}$, with unit $\eta$ and counit $\varepsilon$, and let
$(T, \eta, \mu)$ be the induced monad on $\mathcal{A}$: $T = GF$, $\mu_A = G(\varepsilon_{F(A)})$.

Prove that:

1. for every object $B$ of $\mathcal{B}$, the pair $\big(G(B),\, G(\varepsilon_B)\big)$ is a $T$-algebra;
2. for every map $q \colon B \to B'$ of $\mathcal{B}$, $G(q)$ is a map of algebras
   $\big(G(B), G(\varepsilon_B)\big) \to \big(G(B'), G(\varepsilon_{B'})\big)$;
3. $K(B) = \big(G(B), G(\varepsilon_B)\big)$, $K(q) = G(q)$ defines a functor
   $K \colon \mathcal{B} \to \mathcal{A}^T$ with $U^T \circ K = G$ and $K \circ F = F^T$.

## What you may use

- The triangle identities and naturality of $\eta$ and $\varepsilon$ (2B).
- The definitions of $T$-algebra, map of algebras, $F^T$ and $U^T$.
- Theorem 1 of the lecture and its proof, as a model.
- Brief P02 (that $\mathcal{A}^T$ is a category).

## What a complete proof must show

- [ ] The unit axiom and the associativity axiom for $a = G(\varepsilon_B)$, each written with $T$ and $\mu$ expanded, and each traced to a triangle identity or to naturality at a named map.
- [ ] The algebra-map square for $G(q)$, traced to naturality at a named map.
- [ ] The two equations of functors in part 3 checked on objects and on maps.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Nothing is constructed here; three definitions have to be matched against what an adjunction
provides. Begin by writing the two algebra axioms for $(G(B), G(\varepsilon_B))$ with every $T$
replaced by $GF$ and every $\mu$ by its definition, so that you can see what is being claimed.

</details>

<details>
<summary>Hint 2 — the unit axiom</summary>

After expanding, the unit axiom is an equation between a composite and an identity map on $G(B)$.
There are two triangle identities. Which one has this shape?

</details>

<details>
<summary>Hint 3 — the associativity axiom</summary>

Compare with part (ii) of the proof of Theorem 1, where naturality of $\varepsilon$ was applied at
one particular map and then $G$ was applied. The same move works here. At which map should
$\varepsilon$ be natural this time?

</details>

<details>
<summary>Hint 4 — parts 2 and 3</summary>

The algebra-map square for $G(q)$ is the image under $G$ of a square in $\mathcal{B}$. Which
square, and why does it commute? For $K \circ F = F^T$, compare the algebra structure of $K(F(A))$
with the definition of $\mu_A$.

</details>

## Check yourself

- Which of the two triangle identities did you *not* use? Where was it used in the lecture?
- For the adjunction between sets and monoids, describe $K(M)$ for a monoid $M$ in words.
- For the adjunction between sets and topological spaces with discrete spaces on the left, what is $K$?

## Write it up

Write your proof in `proofs/6d/p03_comparison_functor.md`, then ask Claude to review it.
