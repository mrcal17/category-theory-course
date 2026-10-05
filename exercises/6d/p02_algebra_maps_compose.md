# 6D·P02 — Algebras and their maps form a category

**Type:** warm-up · **Technique:** pasting commuting squares · **Unlocked by:** `6d_monads` §3
**Source:** adapted from Riehl §5.2

## Statement

Let $(T, \eta, \mu)$ be a monad on a category $\mathcal{A}$. Recall that a map of $T$-algebras
$(A, a) \to (B, b)$ is a map $f \colon A \to B$ with $f \circ a = b \circ T(f)$.

Prove that:

1. for every algebra $(A, a)$, the identity $1_A$ is a map of algebras $(A, a) \to (A, a)$;
2. if $f \colon (A, a) \to (B, b)$ and $g \colon (B, b) \to (C, c)$ are maps of algebras, so is $g \circ f$;
3. hence $\mathcal{A}^T$ is a category and $U^T \colon \mathcal{A}^T \to \mathcal{A}$ is a faithful functor;
4. if $f \colon (A, a) \to (B, b)$ is a map of algebras and $f$ is an isomorphism in $\mathcal{A}$,
   then $f^{-1}$ is a map of algebras $(B, b) \to (A, a)$.

## What you may use

- The definition of a $T$-algebra and of a map of algebras.
- That $T$ is a functor; that functors preserve isomorphisms (1C).

## What a complete proof must show

- [ ] Each of parts 1, 2 and 4 stated as "this square commutes", with the square identified.
- [ ] Each use of functoriality of $T$ pointed out.
- [ ] For part 3, why associativity and the identity laws hold in $\mathcal{A}^T$, and why $U^T$ is faithful.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

The condition for an algebra map is a commuting square with $T(f)$ on top and $f$ on the bottom.
Draw the squares for $f$ and for $g$ next to each other. What do you need in order to read the
outer rectangle as the square for $g \circ f$?

</details>

<details>
<summary>Hint 2 — the top edge</summary>

The top edge of the pasted rectangle is a composite of two maps. The square for $g \circ f$ has a
single map on top. Which property of $T$ identifies them? The same question, with identities,
handles part 1.

</details>

<details>
<summary>Hint 3 — part 4</summary>

You want an equation with $f^{-1}$ in it and you have one with $f$ in it. What can you compose
with on each side? You will need to know what the inverse of $T(f)$ is.

</details>

## Check yourself

- Did you use the algebra axioms (unit, associativity) for $a$, $b$ or $c$ anywhere? Should you have?
- Did you use the monad axioms anywhere?
- Part 4 says $U^T$ reflects isomorphisms. Does the forgetful functor from topological spaces to sets do that?

## Write it up

Write your proof in `proofs/6d/p02_algebra_maps_compose.md`, then ask Claude to review it.
