# 1B·P05 — The isomorphisms of a category form a groupoid

**Type:** core · **Technique:** producing inverses; verifying axioms · **Unlocked by:** `1b_isomorphisms_duality` §1, §6
**Source:** adapted from Riehl §1.1 and Leinster §1.1

## Statement

Let $\mathcal{A}$ be a category.

(a) Prove that if $f \colon A \to B$ and $g \colon B \to C$ are isomorphisms, then
$g \circ f \colon A \to C$ is an isomorphism.

(b) Prove that if $f \colon A \to B$ is an isomorphism, then $f^{-1} \colon B \to A$ is an
isomorphism.

(c) Conclude that the objects of $\mathcal{A}$ together with the isomorphisms of $\mathcal{A}$,
with the composition and identities of $\mathcal{A}$, form a category, and that this category is
a groupoid.

(d) Conclude that $\cong$ is an equivalence relation on the objects of $\mathcal{A}$.

## What you may use

- The definitions of category, isomorphism and groupoid.
- Proposition 1.1 (inverses are unique), so that $f^{-1}$ is meaningful.
- The observation in §1 of the lecture that every identity arrow is an isomorphism.
- Associativity and the identity laws.

## What a complete proof must show

- [ ] In each of (a) and (b): a specific candidate inverse is named, its domain and codomain are checked, and **both** equations of the definition are verified with every step justified.
- [ ] In (a): the composites that appear are defined (domains and codomains match).
- [ ] In (c): each of the four "verify" items for a category is addressed, saying which follow from (a), (b) or the lecture and which are inherited from $\mathcal{A}$; then "every arrow is an isomorphism *in the new category*" is justified, not just "in $\mathcal{A}$".
- [ ] In (d): reflexivity, symmetry and transitivity of $\cong$ are each tied to a specific earlier fact.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Parts (a) and (b) are existence proofs: to show an arrow is an isomorphism you must *exhibit*
an inverse and verify two equations. So the first question in each part is "what could the
inverse possibly be?", answered by looking at which arrows you have available and which
direction they point.

</details>

<details>
<summary>Hint 2 — part (a)</summary>

You need an arrow from $C$ to $A$. Draw $A$, $B$, $C$ with all the arrows the hypotheses give
you, in both directions. How many ways are there to travel from $C$ to $A$ along them?

</details>

<details>
<summary>Hint 3 — verifying the candidate in (a)</summary>

Each of the two equations starts as a composite of four arrows. Associativity lets you choose
which adjacent pair to combine first. Which pair is worth combining?

</details>

<details>
<summary>Hint 4 — part (c), the subtle point</summary>

For the new category to be a groupoid, each of its arrows needs an inverse *that is itself an
arrow of the new category*. Which earlier part guarantees that?

</details>

## Check yourself

- In (a), did you verify both $(\ldots) \circ (g \circ f) = 1_A$ and $(g \circ f) \circ (\ldots) = 1_C$?
- In (b), what is $(f^{-1})^{-1}$, and where does your proof show it?
- In (c), which checklist item used (a), and which used the fact about identities?
- Apply (c) to a one-object category. What familiar statement about monoids do you get?

## Write it up

Write your proof in `proofs/1b/p05_isomorphisms_form_a_groupoid.md`, then ask Claude to review it.
