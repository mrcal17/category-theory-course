# 6B·P02 — The elements of a representable form a slice category

**Type:** warm-up · **Technique:** unpacking a definition · **Unlocked by:** `6b_presheaf_limits` §4
**Source:** adapted from Leinster §6.2 and Riehl §2.4

## Statement

Let $\mathcal{A}$ be a locally small category and $B$ an object. Recall from 2C that the slice
category $\mathcal{A}/B$ has as objects the pairs $(A, g)$ with $g \colon A \to B$, and as maps
$(A', g') \to (A, g)$ the maps $f \colon A' \to A$ with $g \circ f = g'$.

Prove that the category of elements $\mathbf{E}(H_B)$ of the representable presheaf
$H_B = \mathcal{A}(-, B)$ is isomorphic, as a category, to $\mathcal{A}/B$.

## What you may use

- The definitions of $H_B$ on objects and on maps (4A), of $\mathbf{E}(X)$, and of the slice category (2C).
- The definition of an isomorphism of categories (1E): a functor with a two-sided inverse functor.

## What a complete proof must show

- [ ] What $H_B(f)$ does to an element, written out.
- [ ] A functor in each direction (or a single functor shown to be bijective on objects and on each hom-set), with functoriality addressed.
- [ ] That the two composites are identity functors, on objects and on maps.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Write the two definitions side by side in a table: objects of each, maps of each, composition of
each. The proof is the observation that the columns match, made precise.

</details>

<details>
<summary>Hint 2 — the one computation</summary>

An object of $\mathbf{E}(H_B)$ is a pair $(A, x)$ with $x \in H_B(A)$. The condition for
$f \colon A' \to A$ to be a map $(A', x') \to (A, x)$ mentions $(H_B f)(x)$. What is that, as a map
of $\mathcal{A}$?

</details>

<details>
<summary>Hint 3 — what is left to say</summary>

Matching objects and maps is not yet an isomorphism of categories. What else must your two
assignments respect, and why do they?

</details>

## Check yourself

- Which object of $\mathcal{A}/B$ is terminal? What element of $H_B$ does it correspond to?
- If you replaced $H_B$ by the covariant $H^B$, which category from 2C would appear instead?
- Is your isomorphism compatible with the projection functors to $\mathcal{A}$ on both sides?

## Write it up

Write your proof in `proofs/6b/p02_elements_of_a_representable.md`, then ask Claude to review it.
