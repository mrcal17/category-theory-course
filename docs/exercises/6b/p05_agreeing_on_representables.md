# 6B·P05 — Colimit-preserving functors that agree on representables

**Type:** core · **Technique:** using density · **Unlocked by:** `6b_presheaf_limits` §5
**Source:** adapted from Leinster §6.2 and Riehl §3.4

## Statement

**Part 1 (a lemma about colimits).** Let $D, D' \colon \mathbf{J} \to \mathcal{B}$ be diagrams and
$\theta \colon D \Rightarrow D'$ a natural isomorphism. Suppose
$(c_j \colon D(j) \to C)_j$ and $(c'_j \colon D'(j) \to C')_j$ are colimit cocones. Prove that there
is an isomorphism $k \colon C \to C'$ with $k \circ c_j = c'_j \circ \theta_j$ for all $j$.

**Part 2.** Let $\mathcal{A}$ be a small category, $\mathcal{B}$ a category, and
$F, G \colon [\mathcal{A}^{\mathrm{op}}, \mathbf{Set}] \to \mathcal{B}$ two functors that preserve
colimits. Suppose there is a natural isomorphism
$\beta \colon F \circ H_\bullet \Rightarrow G \circ H_\bullet$ between their restrictions to
representables. Prove that $F(X) \cong G(X)$ for every presheaf $X$.

## What you may use

- The density theorem (Theorem 3 of the lecture).
- The definition of "preserves colimits" (5C, dualized): the image of a colimit cocone is a colimit cocone.
- The definition of a colimit (5B). Do not quote "isomorphic diagrams have isomorphic colimits"; that is Part 1.

## What a complete proof must show

- [ ] In Part 1: a cocone is built and checked to be a cocone before the universal property is used; a map in each direction; both composites shown to be identities by a uniqueness argument.
- [ ] In Part 2: the two diagrams in $\mathcal{B}$ whose colimits are $F(X)$ and $G(X)$ are named, with their cocones.
- [ ] A natural isomorphism between those two diagrams is produced from $\beta$, with its naturality justified.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Part 2 is: write $X$ as a colimit, push the colimit through $F$ and through $G$, and compare. The
comparison is Part 1. So start by writing down, for a fixed $X$, the diagram and colimit cocone
that density gives you.

</details>

<details>
<summary>Hint 2 — Part 1</summary>

To get a map out of the colimit $C$ you need a cocone on $D$ with vertex $C'$. You have a cocone
on $D'$ with vertex $C'$, and maps $\theta_j$. Why is the obvious family a cocone? For the inverse,
what do you have because $\theta$ is an *isomorphism*?

</details>

<details>
<summary>Hint 3 — showing the two maps are inverse</summary>

A map out of a colimit is determined by its composites with the cocone maps. What are the
composites of $k' \circ k$ with each $c_j$? What other map $C \to C$ has the same composites?

</details>

<details>
<summary>Hint 4 — the diagrams in Part 2</summary>

Both diagrams are indexed by $\mathbf{E}(X)$ and factor through the projection $P$. How do you get
a natural transformation between $F \circ H_\bullet \circ P$ and $G \circ H_\bullet \circ P$ out of
$\beta$, and why are its components isomorphisms?

</details>

## Check yourself

- Where did you use that $F$ preserves colimits, and where that $G$ does?
- Is the isomorphism $F(X) \cong G(X)$ you built natural in $X$? You were not asked to prove it; what would you need to check?
- What does the result say when $\mathcal{A} = \mathbf{1}$?

## Write it up

Write your proof in `proofs/6b/p05_agreeing_on_representables.md`, then ask Claude to review it.
