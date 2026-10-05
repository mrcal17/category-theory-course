# 1D·P03 — A natural transformation with invertible components is a natural isomorphism

**Type:** core · **Technique:** manipulating a naturality square with inverses · **Unlocked by:** `1d_natural_transformations` §6
**Source:** adapted from Leinster §1.3

## Statement

Let $F, G \colon \mathcal{A} \to \mathcal{B}$ be functors and let $\alpha \colon F \Rightarrow G$
be a natural transformation. Prove that the following are equivalent:

1. $\alpha$ is a natural isomorphism, that is, an isomorphism in the functor category
   $[\mathcal{A}, \mathcal{B}]$;
2. for every object $A$ of $\mathcal{A}$, the component $\alpha_A \colon F(A) \to G(A)$ is an
   isomorphism in $\mathcal{B}$.

(This is Lemma 5 of the lecture, which was stated there without proof.)

## What you may use

- The definitions of natural transformation, vertical composition, identity transformation and natural isomorphism (1D §1, §5, §6).
- The definition of an isomorphism in a category and uniqueness of inverses (1B).
- Associativity and identity axioms in $\mathcal{B}$.

## What a complete proof must show

- [ ] Both directions, separated and labelled.
- [ ] In the direction (2) $\Rightarrow$ (1): a definition of the candidate inverse family, one component for each object of $\mathcal{A}$.
- [ ] A proof that this candidate family is **natural**. This is the heart of the exercise and may not be skipped.
- [ ] A check that the candidate is a two-sided inverse of $\alpha$ for vertical composition, stated as equations between natural transformations.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

An "if and only if": two separate proofs. One direction is a matter of reading the equations
$\beta \circ \alpha = 1_F$ and $\alpha \circ \beta = 1_G$ one component at a time. The other
direction requires you to *construct* a natural transformation $G \Rightarrow F$, and a
construction of a natural transformation always has two parts: the components, then the squares.

</details>

<details>
<summary>Hint 2 — the candidate</summary>

In the direction (2) $\Rightarrow$ (1) there is no freedom in choosing the components of the
inverse. Why not? What does 1B tell you about inverses?

</details>

<details>
<summary>Hint 3 — the naturality square you need</summary>

Write down the naturality square you must prove for the candidate family at an arrow
$f \colon A \to A'$, and next to it the naturality square of $\alpha$ at the same $f$, which you
already have. They involve the same four objects. The second is an equation between arrows
$F(A) \to G(A')$; the first is an equation between arrows $G(A) \to F(A')$.

</details>

<details>
<summary>Hint 4 — getting from one square to the other</summary>

You know an equation and you want another one in which some arrows have been replaced by their
inverses. In a group, how do you get from $ab = cd$ to an equation involving $a^{-1}$ and
$c^{-1}$? Do the analogous thing here, keeping careful track of which side you compose on and of
domains and codomains.

</details>

## Check yourself

- Did you prove naturality of the inverse family, or did you only say that each component is invertible?
- In your manipulation, is every composite you wrote actually defined (do the codomain and domain match)?
- Which facts about $\alpha$ did you use: only that its components are invertible, or also that $\alpha$ is natural? Where?

## Write it up

Write your proof in `proofs/1d/p03_natural_iso_componentwise.md`, then ask Claude to review it.
