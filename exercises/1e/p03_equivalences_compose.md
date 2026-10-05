# 1E·P03 — Equivalences compose

**Type:** core · **Technique:** closure of three properties under composition, or whiskering · **Unlocked by:** `1e_equivalence` §4, §5
**Source:** adapted from Leinster §1.3 and Riehl §1.5

## Statement

Let $F \colon \mathcal{A} \to \mathcal{B}$ and $F' \colon \mathcal{B} \to \mathcal{C}$ be
equivalences of categories. Prove that the composite $F' \circ F \colon \mathcal{A} \to \mathcal{C}$
is an equivalence. Conclude that $\simeq$ is transitive: if $\mathcal{A} \simeq \mathcal{B}$ and
$\mathcal{B} \simeq \mathcal{C}$ then $\mathcal{A} \simeq \mathcal{C}$.

## What you may use

- Theorem 2 of the lecture: a functor is an equivalence if and only if it is full, faithful and essentially surjective on objects.
- The definitions of full, faithful and essentially surjective on objects (1E §3), and that functors preserve isomorphisms (1C).
- Alternatively, the definition of equivalence together with whiskering and vertical composition from 1D §5, §7. Either route is acceptable; choose one and stay with it.

## What a complete proof must show

If you use Theorem 2:

- [ ] A separate argument for each of faithful, full, essentially surjective, each beginning from the definition for $F' \circ F$ with its quantifiers.
- [ ] In the "faithful" part: the statement that the two arrows being compared are parallel, each time faithfulness is invoked.
- [ ] In the "essentially surjective" part: an explicit isomorphism in $\mathcal{C}$ from $F'F(A)$ to the given object, built from two isomorphisms, with the reason each one is an isomorphism.

If you work from the definition instead:

- [ ] The candidate inverse functor $\mathcal{C} \to \mathcal{A}$ and both natural isomorphisms, each written as a vertical composite of whiskered transformations, with domains and codomains checked.
- [ ] The reason each whiskered transformation is again a natural *isomorphism*.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Theorem 2 turns "is an equivalence" into three properties, and each property can be handled on
its own. For each, write down what must be shown about $F' \circ F$, then ask which hypothesis
about $F'$ and which about $F$ you will need, and in which order.

</details>

<details>
<summary>Hint 2 — faithful and full</summary>

For faithfulness you start with an equation in $\mathcal{C}$ and want an equation in
$\mathcal{A}$: peel the functors off from the outside. For fullness you start with an arrow of
$\mathcal{C}$ and want an arrow of $\mathcal{A}$: again work from the outside in. Between which
objects does the intermediate arrow live?

</details>

<details>
<summary>Hint 3 — essentially surjective</summary>

Given an object $C$ of $\mathcal{C}$, essential surjectivity of $F'$ gives you an object of
$\mathcal{B}$, and then essential surjectivity of $F$ gives you an object of $\mathcal{A}$. You
now hold two isomorphisms, one in $\mathcal{C}$ and one in $\mathcal{B}$. They cannot be
composed as they stand. What do you do to the one in $\mathcal{B}$?

</details>

## Check yourself

- Did your "essentially surjective" argument use the fact that functors preserve isomorphisms? Where?
- Did you use the axiom of choice? (If you used Theorem 2, in which direction, and how many times?)
- Together with P01, what have you now shown about the relation $\simeq$?

## Write it up

Write your proof in `proofs/1e/p03_equivalences_compose.md`, then ask Claude to review it.
