# 1B·P01 — Isomorphisms in a preorder and in a poset

**Type:** warm-up · **Technique:** unpacking a definition · **Unlocked by:** `1b_isomorphisms_duality` §1
**Source:** adapted from Leinster §1.1 and Riehl §1.1

## Statement

Let $(P, \le)$ be a preordered set, regarded as a category as in `1a_categories` §5: there is
exactly one arrow $x \to y$ when $x \le y$, and none otherwise.

(a) Prove that two objects $x, y$ of $P$ are isomorphic if and only if $x \le y$ and $y \le x$.

(b) Deduce that if $\le$ is antisymmetric (so $P$ is a poset), then every isomorphism in $P$
is an identity arrow.

(c) Deduce that the category $P$ is a groupoid if and only if the relation $\le$ is symmetric.

## What you may use

- The definition of isomorphism and of groupoid (`1b_isomorphisms_duality` §1, §6).
- The category of a preorder and Proposition 5.1 of 1A, including the fact that each hom-set
  of $P$ has at most one element.
- The definitions of preorder, antisymmetric and symmetric.

## What a complete proof must show

- [ ] In (a), both directions of "if and only if", each labelled.
- [ ] In the direction that produces an isomorphism: an arrow and a candidate inverse are named, and **both** equations in the definition of isomorphism are justified.
- [ ] In (b), it is explained why the isomorphism is an identity arrow, not merely why its domain and codomain coincide.
- [ ] In (c), both directions.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Part (a) is an "if and only if" whose two sides live in different languages: one talks about
arrows and composites, the other about the relation $\le$. Translate each side into the other
using the definition of the category of a preorder. What does the *existence* of an arrow
$x \to y$ say about $\le$?

</details>

<details>
<summary>Hint 2 — the equations</summary>

In one direction you must check two equations between arrows. Look at which hom-set each
equation lives in. What did 1A say about equations between arrows in the category of a
preorder?

</details>

<details>
<summary>Hint 3 — parts (b) and (c)</summary>

Both are corollaries of (a): do not start again from the definitions. For (b), what does (a)
give you, and what does antisymmetry then say? Then ask how many arrows there are from an
object to itself. For (c), write "groupoid" as a statement about every arrow and feed each
arrow to (a).

</details>

## Check yourself

- Did you verify both $g \circ f = 1_x$ and $f \circ g = 1_y$, or only one?
- In (b), did you distinguish "the objects are equal" from "the arrow is the identity"?
- A symmetric preorder is an equivalence relation. What do the isomorphism classes of objects of $P$ look like in that case?

## Write it up

Write your proof in `proofs/1b/p01_isomorphisms_in_a_preorder.md`, then ask Claude to review it.
