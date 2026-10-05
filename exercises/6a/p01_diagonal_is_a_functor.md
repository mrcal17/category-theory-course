# 6A·P01 — The diagonal is a functor

**Type:** warm-up · **Technique:** verifying functoriality · **Unlocked by:** `6a_limits_representables_adjoints` §1
**Source:** adapted from Leinster §6.1

## Statement

Let $\mathbf{I}$ be a small category and $\mathcal{A}$ a category. For each object $A$ of $\mathcal{A}$
let $\Delta A \colon \mathbf{I} \to \mathcal{A}$ be the constant functor at $A$, and for each map
$g \colon A' \to A$ let $\Delta g$ be the family of maps indexed by the objects of $\mathbf{I}$ whose
every member is $g$.

Prove that:

1. $\Delta g$ is a natural transformation $\Delta A' \Rightarrow \Delta A$;
2. $\Delta(1_A) = 1_{\Delta A}$ and $\Delta(g \circ g') = \Delta g \circ \Delta g'$ whenever the
   composite $g \circ g'$ is defined.

Conclude that $\Delta \colon \mathcal{A} \to [\mathbf{I}, \mathcal{A}]$ is a functor.

## What you may use

- The definitions of functor, natural transformation, and the functor category $[\mathbf{I}, \mathcal{A}]$ (1C, 1D).
- That $\Delta A$ is a functor (checked in the lecture).
- The axioms of the category $\mathcal{A}$.

## What a complete proof must show

- [ ] For an arbitrary map $u \colon I \to J$ of $\mathbf{I}$, the naturality square of $\Delta g$ is written out with all four sides named, and the axiom that makes it commute is cited.
- [ ] It says what it means for two natural transformations to be equal before proving two of them equal.
- [ ] It uses the definition of the identity and of composition in $[\mathbf{I}, \mathcal{A}]$, not an appeal to "the same thing".

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

This is a verification: nothing has to be invented. Make the list of obligations first. There is
one naturality condition for each map of $\mathbf{I}$, and two functor laws, each of which is an
equation between natural transformations.

</details>

<details>
<summary>Hint 2 — the naturality square</summary>

Fix $u \colon I \to J$. What do the functors $\Delta A'$ and $\Delta A$ do to $u$? Once the square
is drawn with those two sides filled in, ask which axiom of a category compares its two paths.

</details>

<details>
<summary>Hint 3 — the functor laws</summary>

In 1D, how were the identity natural transformation and the composite of two natural
transformations defined? What is the component at $I$ of each side of the two equations you
have to prove?

</details>

## Check yourself

- Did you use any property of $\mathbf{I}$ other than that it is a category?
- Where, if anywhere, did your proof use that $\mathbf{I}$ is small?
- If $\mathbf{I}$ is the two-object discrete category, what does your proof say about the map $A \mapsto (A, A)$?

## Write it up

Write your proof in `proofs/6a/p01_diagonal_is_a_functor.md`, then ask Claude to review it.
