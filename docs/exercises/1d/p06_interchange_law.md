# 1D·P06 — The interchange law

**Type:** stretch · **Technique:** pasting squares, naming every use of naturality · **Unlocked by:** `1d_natural_transformations` §5, §7
**Source:** adapted from Leinster §1.3 and Riehl §1.7

## Statement

Let $\mathcal{A}$, $\mathcal{B}$, $\mathcal{C}$ be categories. Let
$F, F', F'' \colon \mathcal{A} \to \mathcal{B}$ and $G, G', G'' \colon \mathcal{B} \to \mathcal{C}$
be functors, and let
$$\alpha \colon F \Rightarrow F', \quad \alpha' \colon F' \Rightarrow F'', \qquad
\beta \colon G \Rightarrow G', \quad \beta' \colon G' \Rightarrow G''$$
be natural transformations. Writing $\circ$ for vertical and $*$ for horizontal composition,
prove the **interchange law**
$$(\beta' \circ \beta) * (\alpha' \circ \alpha) \;=\; (\beta' * \alpha') \circ (\beta * \alpha)$$
as natural transformations $GF \Rightarrow G''F''$.

## What you may use

- The definitions of vertical composition, whiskering and horizontal composition (1D §5, §7).
- Propositions 4, 6 and 7 of the lecture. In particular either of the two formulas for the components of a horizontal composite may be used.
- Functoriality of $G$, $G'$, $G''$ and associativity in $\mathcal{C}$.

## What a complete proof must show

- [ ] A statement of what it means for two natural transformations to be equal, so that the goal becomes an equation between arrows of $\mathcal{C}$ for each object $A$ of $\mathcal{A}$.
- [ ] The component at $A$ of each side, expanded using the definitions, with the domain and codomain of every arrow visible.
- [ ] Every use of naturality labelled with the transformation **and the arrow** at which it is used.
- [ ] Every use of functoriality labelled with the functor.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Both sides are natural transformations between the same two functors, so they are equal as soon
as their components agree at each object $A$. Expand both components fully before trying to
prove anything; each becomes a composite of four arrows in $\mathcal{C}$.

</details>

<details>
<summary>Hint 2 — draw it</summary>

Arrange the nine objects obtained by applying one of $G, G', G''$ to one of
$F(A), F'(A), F''(A)$ in a $3 \times 3$ grid, with the images of the $\alpha$'s running in one
direction and the components of the $\beta$'s in the other. Each side of the interchange law is
a path from one corner of the grid to the opposite corner. Mark the two paths.

</details>

<details>
<summary>Hint 3 — where the two paths differ</summary>

The definition of horizontal composite offers two formulas for each $*$. Choose them so that the
two paths share as many edges as possible. How do the two paths then differ?

</details>

<details>
<summary>Hint 4 — why a small square commutes</summary>

A square whose sides are components of one natural transformation and images of one arrow under
two functors is a naturality square. Of which transformation, and at which arrow of which
category? Proposition 7 of the lecture is the model.

</details>

## Check yourself

- Is every arrow in your expanded composites an arrow of $\mathcal{C}$, with matching domains and codomains?
- How many times did you use naturality? Could a different choice of formulas for $*$ have changed that number?
- The law has the same form as "$(a \cdot b)(c \cdot d) = (ac) \cdot (bd)$". In which familiar algebraic setting have you seen two operations related like this?

## Write it up

Write your proof in `proofs/1d/p06_interchange_law.md`, then ask Claude to review it.
