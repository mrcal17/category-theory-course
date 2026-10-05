# 4B·P03 — The covariant Yoneda lemma

**Type:** core · **Technique:** follow the identity; dualizing a proof · **Unlocked by:** `4b_yoneda_lemma` §5, §8
**Source:** adapted from Leinster §4.2 and Riehl §2.2

## Statement

Let $\mathcal{A}$ be a locally small category, $A$ an object of $\mathcal{A}$, and
$X \colon \mathcal{A} \to \mathbf{Set}$ a (covariant) functor. Recall that
$H^A = \mathcal{A}(A, -) \colon \mathcal{A} \to \mathbf{Set}$.

Prove that the function

$$[\mathcal{A}, \mathbf{Set}](H^A, X) \to X(A), \qquad \alpha \mapsto \alpha_A(1_A),$$

is a bijection.

Give a **direct** proof, modelled on Stages 1–4 of the lecture. (Naturality in $A$ and $X$ is not
required.)

## What you may use

- The definition of $H^A$ on objects and arrows (4A §1) and of a natural transformation (1D).
- The functor axioms for $X$ and the axioms of a category.
- The proof in 4B §5 as a model. You may not quote Theorem 4.1 for this exercise, even applied to
  $\mathcal{A}^{\mathrm{op}}$.

## What a complete proof must show

- [ ] The naturality equation for a transformation $H^A \Rightarrow X$ is written out with its
      quantifiers, with the correct variance.
- [ ] A candidate inverse is defined: for each $x \in X(A)$, a family of functions, with the domain
      and codomain of each stated.
- [ ] That family is proved to be a natural transformation, with the functor axiom used named.
- [ ] Both composites are shown to be identities; for the harder one, the proof says at which
      arrow naturality is applied and at which element it is evaluated.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Mutually inverse functions: define a map back, check it lands where it should, check the two
composites. That is four things, matching Stages 1 to 4 of the lecture. Set up the page with those
four headings before writing any mathematics.

</details>

<details>
<summary>Hint 2 — the inverse</summary>

You are given $x \in X(A)$ and an arrow $p \colon A \to B$, and you need an element of $X(B)$.
The functor $X$ is covariant now. What is the only thing you can build from $X$, $p$ and $x$ that
has the right type?

</details>

<details>
<summary>Hint 3 — which functor axiom goes where</summary>

In the lecture, one functor axiom of $X$ proved that $\tilde{x}$ is natural and the other proved
$\hat{\tilde{x}} = x$. The same division of labour holds here, but the composition axiom now reads
in the covariant order. Write it down for $X$ before you use it.

</details>

<details>
<summary>Hint 4 — the hard composite</summary>

You want to show that a transformation $\alpha$ is recovered from the single element
$\alpha_A(1_A)$. Take an arbitrary $p \colon A \to B$. There is exactly one naturality square of
$\alpha$ that has $1_A$ available in its top-left corner and $p$ as the arrow it is "at". Draw it
and chase.

</details>

## Check yourself

- Compare your naturality equation with the one in 4B §1. Which symbols moved?
- Did you use an identity axiom of $\mathcal{A}$? On which side of $p$ did the identity sit, and
  how does that differ from Lemma 5.3?
- Can you now explain in one sentence how the statement follows from Theorem 4.1 applied to
  $\mathcal{A}^{\mathrm{op}}$?

## Write it up

Write your proof in `proofs/4b/p03_covariant_yoneda.md`, then ask Claude to review it.
