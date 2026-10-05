# 1D·P01 — Over a discrete category, every family is natural

**Type:** warm-up · **Technique:** unpacking the definition · **Unlocked by:** `1d_natural_transformations` §1
**Source:** adapted from Leinster §1.3

## Statement

Let $\mathcal{A}$ be a **discrete** category: its only arrows are the identities $1_A$. Let
$\mathcal{B}$ be any category and let $F, G \colon \mathcal{A} \to \mathcal{B}$ be functors.
Suppose that for each object $A$ of $\mathcal{A}$ you are given an arrow
$\alpha_A \colon F(A) \to G(A)$ of $\mathcal{B}$, with no further condition.
Prove that the family $(\alpha_A)_{A \in \mathcal{A}}$ is a natural transformation $F \Rightarrow G$.

## What you may use

- The definition of a natural transformation (1D §1).
- The definition of a functor, in particular what a functor does to identity arrows (1C).
- The identity axioms of the category $\mathcal{B}$.

## What a complete proof must show

- [ ] It says which equation has to be verified, and for which arrows of $\mathcal{A}$.
- [ ] It uses the hypothesis that $\mathcal{A}$ is discrete, and says where.
- [ ] Each equality is justified by a functor axiom or a category axiom, by name.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

This is a direct verification of a "for every arrow $f$ of $\mathcal{A}$" statement. Start by
writing "Let $f \colon A \to A'$ be an arrow of $\mathcal{A}$" and ask what the hypothesis on
$\mathcal{A}$ tells you about $f$, $A$ and $A'$.

</details>

<details>
<summary>Hint 2 — what the square looks like</summary>

Draw the naturality square for the only kind of arrow there is. Two of its four sides are now
arrows you know by name. Which axiom of a functor tells you what they are?

</details>

<details>
<summary>Hint 3 — finishing</summary>

Once the horizontal sides are identified, each route round the square is a composite of
$\alpha_A$ with something very simple. Which axiom of $\mathcal{B}$ simplifies each one?

</details>

## Check yourself

- Did you use that $F$ and $G$ preserve identities, or did you only assert that the square "has nothing in it"?
- Where exactly would your argument break if $\mathcal{A}$ had one non-identity arrow?
- Can you now describe the functor category $[\mathcal{A}, \mathcal{B}]$ for the discrete category with two objects?

## Write it up

Write your proof in `proofs/1d/p01_discrete_families_natural.md`, then ask Claude to review it.
