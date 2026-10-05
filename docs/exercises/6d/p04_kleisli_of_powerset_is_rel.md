# 6D·P04 — The Kleisli category of the power set monad is Rel

**Type:** core · **Technique:** building an isomorphism of categories · **Unlocked by:** `6d_monads` §5
**Source:** adapted from Riehl §5.2

## Statement

Let $\mathbf{Rel}$ be the category whose objects are sets, whose maps $X \to Y$ are relations
$R \subseteq X \times Y$, with composition
$$S \circ R = \{ (x, z) : \text{there is } y \text{ with } (x, y) \in R \text{ and } (y, z) \in S \}$$
for $R \subseteq X \times Y$ and $S \subseteq Y \times Z$, and with the diagonal
$\{(x, x) : x \in X\}$ as identity on $X$. (You may assume $\mathbf{Rel}$ is a category.)

Let $\mathscr{P}$ be the power set monad on $\mathbf{Set}$. Construct an isomorphism of categories
$$\mathbf{Set}_{\mathscr{P}} \;\cong\; \mathbf{Rel}$$
that is the identity on objects, and prove that it is one.

## What you may use

- The definition of the Kleisli category and Theorem 3 of the lecture.
- The definition of the power set monad ($\mathscr{P}(g)$ is direct image, $\mu$ is union).
- The definition of an isomorphism of categories (1E).

## What a complete proof must show

- [ ] For each pair of sets $X, Y$, an explicit function from Kleisli maps $X \rightsquigarrow Y$ to relations, and an explicit inverse, with both composites checked.
- [ ] Identities are sent to identities.
- [ ] The Kleisli composite $g \bullet f = \mu \circ \mathscr{P}(g) \circ f$ is computed on an element $x$, and the result compared with the composite relation.
- [ ] Sets are proved equal by showing they have the same elements.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

An identity-on-objects isomorphism of categories is a family of bijections between hom-sets that
respects identities and composition. So there are three things to do: build the bijections,
check identities, check composition.

</details>

<details>
<summary>Hint 2 — the bijection</summary>

A Kleisli map is a function $f \colon X \to \mathscr{P}(Y)$. Given such an $f$, which pairs $(x, y)$
is it natural to call related? Given a relation, which subset of $Y$ should be attached to $x$?

</details>

<details>
<summary>Hint 3 — composition</summary>

Compute in stages. For $x \in X$: what is $f(x)$? What does the direct image $\mathscr{P}(g)$ do to
it, and what kind of object is the result? What does $\mu$ then do? Finish by answering: for
which $z$ is $z \in (g \bullet f)(x)$?

</details>

<details>
<summary>Hint 4 — identities</summary>

The identity on $X$ in the Kleisli category is not the identity function. What is it, and which
relation does your bijection send it to?

</details>

## Check yourself

- Under your isomorphism, which relations correspond to Kleisli maps of the form $F_{\mathscr{P}}(h) = \eta \circ h$ for a function $h$?
- $\mathbf{Rel}$ is isomorphic to its own opposite (reverse each relation). What does that say about $\mathbf{Set}_{\mathscr{P}}$?
- Did you use that the existential quantifier ranges over $y \in Y$ and not over a subset?

## Write it up

Write your proof in `proofs/6d/p04_kleisli_of_powerset_is_rel.md`, then ask Claude to review it.
