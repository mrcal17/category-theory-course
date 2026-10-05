# 5B·P03 — A sum of epics is epic

**Type:** core · **Technique:** dualizing a proof · **Unlocked by:** `5b_colimits` §1, §2
**Source:** adapted from Leinster §5.2

## Statement

Let $\mathcal{A}$ be a category and let $f \colon X \to X'$ and $g \colon Y \to Y'$ be maps in
$\mathcal{A}$. Suppose $(S, i_1, i_2)$ is a sum of $X$ and $Y$, and $(S', i'_1, i'_2)$ is a sum of
$X'$ and $Y'$. Let $f + g \colon S \to S'$ be the unique map with

$$(f + g) \circ i_1 = i'_1 \circ f \qquad\text{and}\qquad (f + g) \circ i_2 = i'_2 \circ g .$$

Prove: if $f$ and $g$ are both epic, then $f + g$ is epic.

Give **two** proofs:

1. a proof by duality, quoting the statement of 5A·P03 (a product of monics is monic);
2. a direct proof in $\mathcal{A}$ that never mentions $\mathcal{A}^{\mathrm{op}}$.

## What you may use

- The definitions of sum (5B §2) and epic (1B).
- The statement of 5A·P03, as a theorem valid in every category (for proof 1 only).
- The dictionary of 5B §1: what products, sums, monics and epics become in the opposite
  category.
- Proof 1 of 5B: two maps out of a colimit are equal as soon as they have the same composite
  with every coprojection (for proof 2).

## What a complete proof must show

- [ ] It says why the map $f + g$ exists and is unique: which universal property, which test data.
- [ ] Proof 1 says precisely which category the quoted theorem is applied in, which objects and
      maps play the roles of the two products and of $f \times g$ there, and why the defining
      equations match.
- [ ] Proof 2 fixes arbitrary $h, k$ with stated domain and codomain, and says where each of the
      two epics is used.
- [ ] Neither proof applies a map to an element.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Proof 1 is a translation: you are showing that the hypotheses of an existing theorem hold in
another category. Proof 2 is a direct proof from the definition of epic, about two maps *out of*
a sum, and the lecture has a tool for comparing such maps.

</details>

<details>
<summary>Hint 2 — for proof 1</summary>

In $\mathcal{A}^{\mathrm{op}}$, what are the domain and codomain of $f$, $g$, the coprojections
and $f + g$? Write the two defining equations of $f + g$ as composites in
$\mathcal{A}^{\mathrm{op}}$. Do you recognise them?

</details>

<details>
<summary>Hint 3 — for proof 2</summary>

Take your own proof of 5A·P03 and rewrite it line by line with every composite reversed. If you
would rather start afresh: your hypothesis is an equation between maps out of $S$, your goal is
an equation between maps out of $S'$. What can you compose the hypothesis with, and on which
side?

</details>

## Check yourself

- In $\mathbf{Set}$ your theorem says that a disjoint union of two surjections is surjective.
  Does that match what you know?
- Put your direct proof next to your proof of 5A·P03. Does each line have a mirror image?
- Which is shorter to write, proof 1 or proof 2? Which convinces you more?

## Write it up

Write your proof in `proofs/5b/p03_sum_of_epics.md`, then ask Claude to review it.
