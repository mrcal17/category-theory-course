# 2A·P06 — Orbits and fixed points as adjoints

**Type:** stretch · **Technique:** constructing a bijection and proving it natural · **Unlocked by:** `2a_adjunctions` §3
**Source:** adapted from Leinster §2.1

## Statement

Let $G$ be a group. A *$G$-set* is a set $X$ with a left action of $G$, written
$(g, x) \mapsto g \cdot x$, and a map of $G$-sets (an *equivariant* map) is a function
$\phi \colon X \to Y$ with $\phi(g \cdot x) = g \cdot \phi(x)$ for all $g \in G$, $x \in X$.
These form a category $G\text{-}\mathbf{Set}$.

Let $T \colon \mathbf{Set} \to G\text{-}\mathbf{Set}$ send a set $S$ to $S$ with the trivial
action ($g \cdot s = s$ for all $g$, $s$) and a function to itself. For a $G$-set $X$ let

- $X/G$ be the set of orbits of $X$, with $[x]$ denoting the orbit of $x$;
- $X^{G} = \{x \in X : g \cdot x = x \text{ for all } g \in G\}$ be the set of fixed points.

1. Make $X \mapsto X/G$ and $X \mapsto X^{G}$ into functors $G\text{-}\mathbf{Set} \to \mathbf{Set}$.
2. Prove that $(-)/G \;\dashv\; T \;\dashv\; (-)^{G}$.

## What you may use

- The definitions of group action, orbit, and equivariant map; that the orbits partition $X$.
- The definition of an adjunction from 2A §1.
- The principle from Part 0 that a function defined on equivalence classes by choosing a
  representative must be shown to be well defined.

## What a complete proof must show

- [ ] Each of the two functors is defined on arrows, and it is checked that the definition makes sense (well defined on orbits; lands in the fixed points).
- [ ] For $(-)/G \dashv T$: a bijection between $\mathbf{Set}(X/G, S)$ and $G\text{-}\mathbf{Set}(X, T(S))$ for every $G$-set $X$ and set $S$, with both directions defined, each shown to produce an arrow of the right category, and both round trips checked.
- [ ] For $T \dashv (-)^{G}$: the same, for $G\text{-}\mathbf{Set}(T(S), X)$ and $\mathbf{Set}(S, X^{G})$.
- [ ] (N1) and (N2) for each of the two adjunctions.
- [ ] Every place where a representative of an orbit is chosen is followed by an argument that the choice does not matter.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Two adjunctions, so two runs of the five-item checklist, after first building the functors.
Start with the question that organises everything: what does it mean, in terms of elements,
for a function *into* $T(S)$ to be equivariant? And for a function *out of* $T(S)$?

</details>

<details>
<summary>Hint 2 — maps into a trivial action</summary>

An equivariant map $\phi \colon X \to T(S)$ satisfies a condition relating $\phi(g \cdot x)$ and
$\phi(x)$. Rewrite the condition using what the action on $T(S)$ is. On which subsets of $X$
does that restrict the behaviour of $\phi$?

</details>

<details>
<summary>Hint 3 — maps out of a trivial action</summary>

An equivariant map $\psi \colon T(S) \to X$ satisfies a condition relating $\psi(s)$ and
$g \cdot \psi(s)$. What does that say about where the values of $\psi$ live?

</details>

<details>
<summary>Hint 4 — where the care is needed</summary>

In the first adjunction, one direction of the bijection involves no choices at all, and the
other defines a function on orbits. For the second of these, state exactly which property of
$\phi$ makes the definition independent of choices. The same issue arises when you define the
functor $(-)/G$ on arrows.

</details>

## Check yourself

- Is $x \mapsto [x]$ an equivariant map $X \to T(X/G)$? If you used this, did you prove it?
- For the functor $(-)^{G}$ on an equivariant map $\phi \colon X \to Y$: why does $\phi$ send fixed points to fixed points?
- Take $G = \mathbb{Z}/2$ acting on $X = \{a, b, c\}$ by swapping $a$ and $b$. Count both sides of each bijection for $S = \{0, 1\}$. Do the numbers agree?
- Which of the two adjunctions has $T$ as the left adjoint? Check it against the slot $T$ occupies in your hom-sets.

## Write it up

Write your proof in `proofs/2a/p06_orbits_fixed_points.md`, then ask Claude to review it.
