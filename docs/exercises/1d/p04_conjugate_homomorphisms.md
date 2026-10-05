# 1D·P04 — Natural transformations between group homomorphisms

**Type:** core · **Technique:** translating a definition into algebra · **Unlocked by:** `1d_natural_transformations` §3, §6
**Source:** adapted from Riehl §1.4 and Leinster §1.3

## Statement

Let $G$ and $H$ be groups, each regarded as a category with one object (the arrows are the group
elements and composition is multiplication). Let $\varphi, \psi \colon G \to H$ be group
homomorphisms, regarded as functors.

1. Prove that a natural transformation $\varphi \Rightarrow \psi$ is the same thing as an element
   $h \in H$ such that
   $$\psi(g)\, h = h\, \varphi(g) \qquad \text{for all } g \in G.$$
2. Deduce that every natural transformation $\varphi \Rightarrow \psi$ is a natural isomorphism.
3. Deduce that the natural transformations $1_G \Rightarrow 1_G$ from the identity functor of $G$
   to itself are exactly the elements of the centre $Z(G) = \{ z \in G : zg = gz \text{ for all } g \in G \}$.

## What you may use

- The definition of a natural transformation and of a natural isomorphism (1D §1, §6).
- Lemma 5 of the lecture (a natural transformation is a natural isomorphism if and only if each component is an isomorphism); it is the subject of P03 and may be quoted here.
- A group as a one-object category, and homomorphisms as functors (1A, 1C).
- The group axioms.

## What a complete proof must show

- [ ] For part 1: what the family of components consists of when the domain category has one object, and which arrows the naturality condition quantifies over.
- [ ] The naturality equation written in the category $H$ and then rewritten as an equation in the group $H$, with the order of multiplication justified.
- [ ] Both directions of "is the same thing as": a natural transformation gives such an $h$, and such an $h$ gives a natural transformation.
- [ ] For part 2: the reason every arrow of $H$ is an isomorphism.
- [ ] For part 3: which homomorphisms play the roles of $\varphi$ and $\psi$.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Nothing here needs a new idea; it needs the checklist under the definition in §1, applied with
care. Section 3 of the lecture does exactly this for functors from a group to
$\mathbf{Set}$. Imitate that passage with $H$ in place of $\mathbf{Set}$.

</details>

<details>
<summary>Hint 2 — how many components?</summary>

How many objects does $G$ have? So how many components does a natural transformation
$\varphi \Rightarrow \psi$ have, and in which category, between which objects, does each
component live? What kind of thing is an arrow of that category?

</details>

<details>
<summary>Hint 3 — the square</summary>

Draw the naturality square at an arrow $g$ of $G$. All four corners are the same object. Read
off the two composites, remembering that $b \circ a$ in the one-object category is the product
$ba$ in the group.

</details>

<details>
<summary>Hint 4 — parts 2 and 3</summary>

For part 2, ask what the isomorphisms are in a group regarded as a category. For part 3,
specialise part 1; no new argument should be needed.

</details>

## Check yourself

- Did you keep the order of multiplication straight? Check your equation on a non-abelian example such as $S_3$ (Compute It, Exercise 2 gives you a count to compare with).
- Rearrange your condition so that $\psi(g)$ stands alone on one side. What is the usual name for two homomorphisms related in this way?
- Does part 2 remain true if $G$ and $H$ are only monoids? Which step fails?

## Write it up

Write your proof in `proofs/1d/p04_conjugate_homomorphisms.md`, then ask Claude to review it.
