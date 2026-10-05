# 5C·P04 — The comparison map

**Type:** core · **Technique:** uniqueness of limits, in both directions · **Unlocked by:** `5c_functors_and_limits` §1, §2; `5a_limits` §5
**Source:** adapted from Leinster §5.3

## Statement

Let $F \colon \mathcal{A} \to \mathcal{B}$ be a functor and let $X, Y$ be objects of $\mathcal{A}$.
Suppose

- $(P, p_1, p_2)$ is a product of $X$ and $Y$ in $\mathcal{A}$, and
- $(M, m_1, m_2)$ is a product of $F X$ and $F Y$ in $\mathcal{B}$.

Let $c \colon F P \to M$ be the comparison map: the unique map with $m_1 \circ c = F p_1$ and
$m_2 \circ c = F p_2$.

Prove that the following are equivalent:

1. $(F P, F p_1, F p_2)$ is a product of $F X$ and $F Y$ in $\mathcal{B}$;
2. $c$ is an isomorphism.

## What you may use

- The definition of a product (5A §1).
- From 5A §5: Proof 5 (two limit cones on the same diagram are related by a unique map
  compatible with the projections, and that map is an isomorphism) and Proof 6 (composing a
  limit cone with an isomorphism gives a limit cone).
- Proof 1 of 5C (the image of a cone is a cone), which is what guarantees that $c$ exists.

## What a complete proof must show

- [ ] Two directions, each under its own heading.
- [ ] In (1) $\Rightarrow$ (2): it is explained why the isomorphism supplied by the uniqueness
      theorem is the map $c$ itself, and not merely *some* isomorphism $F P \to M$.
- [ ] In (2) $\Rightarrow$ (1): the cone $(F P, F p_1, F p_2)$ is expressed in terms of the cone
      $(M, m_1, m_2)$ and $c$, with the equations justifying this stated.
- [ ] Each quoted result from 5A is named, and it is said which cones play which roles.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

An "if and only if" in which both directions are short, because 5A §5 has already done the
work. Your task is to match the present situation to the hypotheses of the two quoted results:
which cone is "the limit cone", which is "the other cone", which map is "the isomorphism".

</details>

<details>
<summary>Hint 2 — for (1) implies (2)</summary>

Under assumption (1) there are two product cones on the same pair of objects of $\mathcal{B}$.
The uniqueness theorem produces a map between their vertices characterised by two equations.
Compare those two equations with the two equations that define $c$.

</details>

<details>
<summary>Hint 3 — for (2) implies (1)</summary>

The defining equations of $c$ can be read from right to left: they express each $F p_i$ as a
composite. Which result of 5A §5 is about cones of exactly that form?

</details>

## Check yourself

- In (1) $\Rightarrow$ (2), did you use the word "unique" to identify the isomorphism with $c$?
- Find the place in the lecture's Compute It, Exercise 1 where $F P$ and $M$ have the same
  number of elements. Why does that not contradict your theorem?
- Nothing in your proof should be special to products. Restate the result for a general diagram
  $D \colon \mathbf{I} \to \mathcal{A}$.

## Write it up

Write your proof in `proofs/5c/p04_comparison_map.md`, then ask Claude to review it.
