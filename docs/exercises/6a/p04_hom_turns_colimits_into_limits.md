# 6A·P04 — Hom out of a colimit is a limit of homs

**Type:** core · **Technique:** pointwise argument in Set · **Unlocked by:** `6a_limits_representables_adjoints` §7
**Source:** adapted from Leinster §6.2 and Riehl §3.4

## Statement

Let $\mathcal{A}$ be a locally small category, $A$ an object, and $D \colon \mathbf{I} \to \mathcal{A}$
a diagram with a colimit cocone $(q_I \colon D(I) \to C)_{I}$.

Define $E \colon \mathbf{I}^{\mathrm{op}} \to \mathbf{Set}$ by $E(I) = \mathcal{A}(D(I), A)$ and, for
$u \colon I \to J$ in $\mathbf{I}$, $E(u) = (- \circ Du) \colon \mathcal{A}(D(J), A) \to \mathcal{A}(D(I), A)$.

Prove that the family
$$\big( - \circ q_I \colon \mathcal{A}(C, A) \to \mathcal{A}(D(I), A) \big)_{I}$$
is a limit cone on $E$ in $\mathbf{Set}$. In symbols:
$\mathcal{A}(\mathrm{colim}\, D, A) \cong \lim \mathcal{A}(D(-), A)$.

## What you may use

- The definition of a colimit (5B) and of a limit cone in $\mathbf{Set}$ (5A).
- Theorem 3 of the lecture, either as a model for a direct proof or applied to another category.
- If you write "by duality", you must name the category and the functor Theorem 3 is applied to.

## What a complete proof must show

- [ ] $E$ is a functor on $\mathbf{I}^{\mathrm{op}}$, with the variance explained.
- [ ] The displayed family is a cone on $E$.
- [ ] For an arbitrary set $S$ and cone on $E$ with vertex $S$: existence and uniqueness of the mediating function.
- [ ] Equality of functions out of $S$ is proved by evaluating at an arbitrary element.

## Hints — one at a time

<details>
<summary>Hint 1 — two possible routes</summary>

Either imitate the proof of Theorem 3 element by element, or apply Theorem 3 in
$\mathcal{A}^{\mathrm{op}}$. Decide before you start which one you are writing.

</details>

<details>
<summary>Hint 2 — the direct route</summary>

Fix one element $s$ of the vertex set $S$ of a cone in $\mathbf{Set}$. The cone gives you one map
of $\mathcal{A}$ for each $I$. What kind of family do those maps form, and which universal
property accepts that kind of family as input?

</details>

<details>
<summary>Hint 3 — the duality route</summary>

Which functor on $\mathcal{A}$ is the representable $\mathcal{A}^{\mathrm{op}}(A, -)$? What is a
limit cone in $\mathcal{A}^{\mathrm{op}}$, described in $\mathcal{A}$, and over which shape category
does its diagram run?

</details>

<details>
<summary>Hint 4 — a variance check</summary>

For $u \colon I \to J$, write down the domain and codomain of $- \circ Du$. Does the cone
condition you are proving point in a direction consistent with $E$ being defined on
$\mathbf{I}^{\mathrm{op}}$?

</details>

## Check yourself

- For $\mathbf{I}$ discrete with two objects, does your statement reduce to "a map out of a sum is a pair of maps"?
- Where did you use that $(q_I)$ is a *colimit* cocone and not just a cocone?
- Does $\mathcal{A}(-, A)$ send limits in $\mathcal{A}$ to anything in particular? Try $\mathbf{Set}(X \times Y, 2)$ with small finite sets.

## Write it up

Write your proof in `proofs/6a/p04_hom_turns_colimits_into_limits.md`, then ask Claude to review it.
