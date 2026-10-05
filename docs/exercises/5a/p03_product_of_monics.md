# 5A·P03 — A product of monics is monic

**Type:** core · **Technique:** comparing maps into a product through its projections · **Unlocked by:** `5a_limits` §1, §5
**Source:** adapted from Leinster §5.1

## Statement

Let $\mathcal{A}$ be a category and let $f \colon X \to X'$ and $g \colon Y \to Y'$ be maps in
$\mathcal{A}$. Suppose $(P, p_1, p_2)$ is a product of $X$ and $Y$, and $(P', p'_1, p'_2)$ is a
product of $X'$ and $Y'$.

1. Show that there is exactly one map $f \times g \colon P \to P'$ such that
   $$p'_1 \circ (f \times g) = f \circ p_1 \qquad\text{and}\qquad p'_2 \circ (f \times g) = g \circ p_2 .$$
2. Prove: if $f$ and $g$ are both monic, then $f \times g$ is monic.

## What you may use

- The definition of a binary product (5A §1) and of monic (1B).
- The Lemma of 5A §5 (Proof 4), read for a product: two maps into a product are equal as soon
  as they have the same composite with both projections. Say for which product you use it.
- The axioms of a category. Nothing about elements: $\mathcal{A}$ is an arbitrary category.

## What a complete proof must show

- [ ] Part 1 names the test data fed to a universal property, and says which product's
      universal property it is.
- [ ] Part 2 is written with its quantifiers: an arbitrary object $A$ and arbitrary maps
      $h, k$ with stated domain and codomain, and a stated hypothesis on them.
- [ ] Monicity of $f$ and monicity of $g$ are each used, and it is said where.
- [ ] The final step from "equal composites" to "$h = k$" is justified by a named result.
- [ ] No step applies a map to an element.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Part 1 is one application of a universal property; decide which of the two products is "the
product" and what the test data are. Part 2 is a direct proof from the definition of monic: fix
two maps with the same composite with $f \times g$ and show they are equal. They are maps into a
product, and the lecture gives you a standard way to compare such maps.

</details>

<details>
<summary>Hint 2 — what you know and what you want</summary>

Your hypothesis is an equation between two maps into $P'$. Your goal is an equation between two
maps into $P$. Each of the two objects comes with projections. What do you get when you compose
the hypothesis with a projection of $P'$, and which defining equation of $f \times g$ lets you
rewrite the result?

</details>

<details>
<summary>Hint 3 — where the monics enter</summary>

After Hint 2 you hold an equation in which $f$ (or $g$) is the last map applied on both sides.
What does the definition of monic let you do with such an equation? Do this once for each
factor, and then ask what the Lemma needs.

</details>

## Check yourself

- Did you use the Lemma for $P$ or for $P'$? Why that one?
- In $\mathbf{Set}$ your theorem says that $(x, y) \mapsto (f(x), g(y))$ is injective when $f$ and
  $g$ are. Does your proof look like the element-wise proof of that fact?
- Is the converse true? Think about $\mathbf{Set}$ with $Y = \varnothing$.

## Write it up

Write your proof in `proofs/5a/p03_product_of_monics.md`, then ask Claude to review it.
