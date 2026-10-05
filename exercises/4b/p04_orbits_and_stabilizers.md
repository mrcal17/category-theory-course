# 4B·P04 — Orbits and stabilizers

**Type:** core · **Technique:** reading the lemma in a group · **Unlocked by:** `4b_yoneda_lemma` §2
**Source:** adapted from Leinster §4.2 and Riehl §2.2

## Statement

Let $G$ be a group and $S$ a right $G$-set (a presheaf on $G$ regarded as a one-object category).
For $x \in S$, let $\tilde{x} \colon G \to S$ be the equivariant map of Proposition 2.1 of 4B, the
one with $\tilde{x}(1) = x$. Define

- the **orbit** of $x$: $\; x \cdot G = \{\, x \cdot g : g \in G \,\}$;
- the **stabilizer** of $x$: $\; G_x = \{\, g \in G : x \cdot g = x \,\}$.

Prove:

1. The image of $\tilde{x}$ is the orbit $x \cdot G$.
2. $\tilde{x}$ is injective if and only if $G_x = \{1\}$.
3. For $x, y \in S$: the maps $\tilde{x}$ and $\tilde{y}$ have the same image if and only if
   $y \in x \cdot G$.
4. Every equivariant map $\varphi \colon G \to S$ has image a single orbit. Deduce that if $S$ has
   at least two different orbits, no equivariant map $G \to S$ is surjective.

## What you may use

- Proposition 2.1 of 4B (Yoneda for a monoid), including the formula for $\tilde{x}$.
- The axioms of a right action and the group axioms.
- That the orbits of a group action partition $S$, if you want it for part 3; say so if you use it.

## What a complete proof must show

- [ ] Part 1 proves an equality of sets by two inclusions, or by a chain of equalities each justified.
- [ ] Part 2 proves both directions, and says where inverses in $G$ are used.
- [ ] Part 3 proves both directions.
- [ ] Part 4 says explicitly which result converts "every equivariant map" into "every $\tilde{x}$".

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Parts 1 to 3 are direct proofs about one explicit function, $\tilde{x}$; start each by writing
down what $\tilde{x}$ does to an element $p \in G$. Part 4 is where the Yoneda lemma is used: it
lets you replace an unknown equivariant map by one of a very particular form.

</details>

<details>
<summary>Hint 2 — part 2</summary>

Injectivity is about two elements $p, q \in G$ with the same image. From $\tilde{x}(p) = \tilde{x}(q)$
you want to learn something about a *single* element of $G$ that fixes $x$. Which element can you
build from $p$ and $q$, and which action axiom lets you move it across?

</details>

<details>
<summary>Hint 3 — part 4</summary>

Proposition 2.1 says something about *every* equivariant map $G \to S$. What does it say such a
map is equal to? Then part 1 applies.

</details>

## Check yourself

- Where did you use that $G$ is a group and not merely a monoid? Which parts would survive for a monoid?
- In the $\mathbb{Z}/3$ scenario of the lecture's widget, what are the orbits of the four-element
  set, and which of the four equivariant maps are injective?
- Is $G_x$ a subgroup of $G$? You do not need it, but you should know.

## Write it up

Write your proof in `proofs/4b/p04_orbits_and_stabilizers.md`, then ask Claude to review it.
