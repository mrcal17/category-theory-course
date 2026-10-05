# 6A·P03 — A right adjoint to the diagonal gives limits

**Type:** core · **Technique:** re-expressing a universal property · **Unlocked by:** `6a_limits_representables_adjoints` §6
**Source:** adapted from Leinster §6.1 and Riehl §4.5

## Statement

Let $\mathbf{I}$ be a small category and $\mathcal{A}$ a locally small category. Suppose the
diagonal functor $\Delta \colon \mathcal{A} \to [\mathbf{I}, \mathcal{A}]$ has a right adjoint
$R \colon [\mathbf{I}, \mathcal{A}] \to \mathcal{A}$, with counit
$\varepsilon \colon \Delta R \Rightarrow 1$.

Prove that for every diagram $D \colon \mathbf{I} \to \mathcal{A}$, the components
$(\varepsilon_{D, I} \colon R(D) \to D(I))_{I}$ of the natural transformation
$\varepsilon_D \colon \Delta R(D) \Rightarrow D$ form a limit cone on $D$.

Deduce: $\mathcal{A}$ has limits of shape $\mathbf{I}$ if and only if $\Delta$ has a right adjoint.

## What you may use

- Lemma 1 (cones are natural transformations out of a constant functor) and Theorem 2 of the lecture.
- From 2B: for an adjunction $F \dashv G$ with counit $\varepsilon$, the function
  $g \mapsto \varepsilon_B \circ F(g)$ from $\mathcal{A}(A, G(B))$ to $\mathcal{B}(F(A), B)$ is the
  transposition bijection.

## What a complete proof must show

- [ ] Why the family $(\varepsilon_{D,I})_I$ is a cone at all.
- [ ] For an arbitrary object $A$ and an arbitrary cone on $D$ with vertex $A$: existence of a mediating map, and its uniqueness, each traced to a named property of the adjunction.
- [ ] What $\Delta(g)$ is in components, used explicitly.
- [ ] For the final "if and only if", which direction is this exercise and which is a theorem of the lecture.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

You are given one universal property (an adjunction) and asked for another (a limit). Write the
goal in the language of natural transformations $\Delta A \Rightarrow D$ before doing anything
else; Lemma 1 lets you.

</details>

<details>
<summary>Hint 2 — what the adjunction offers</summary>

The 2B formula for transposition involves $F(g)$ and the counit. Here $F = \Delta$. Write out what
the transpose of a map $g \colon A \to R(D)$ is, one component at a time.

</details>

<details>
<summary>Hint 3 — from bijection to universal property</summary>

"This function is a bijection" is two statements. Which of them is "there exists a mediating
map" and which is "it is unique"? Compare with how the lecture read Theorem 1 in the opposite
direction.

</details>

## Check yourself

- Did you use the naturality of the adjunction bijection anywhere, or only that it is a bijection?
- Your proof should not have chosen any limits. Did it?
- What does the statement say when $\mathbf{I}$ is empty?

## Write it up

Write your proof in `proofs/6a/p03_right_adjoint_to_diagonal_gives_limits.md`, then ask Claude to review it.
