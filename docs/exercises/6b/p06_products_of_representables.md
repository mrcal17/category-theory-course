# 6B·P06 — When is a product of representables representable?

**Type:** stretch · **Technique:** Yoneda-style proof · **Unlocked by:** `6b_presheaf_limits` §3
**Source:** adapted from Leinster §6.2

## Statement

Let $\mathcal{A}$ be a small category and $A, B$ objects. Write $H_A \times H_B$ for the pointwise
product in $[\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$, with projections
$\mathrm{pr}_1 \colon H_A \times H_B \Rightarrow H_A$ and $\mathrm{pr}_2 \colon H_A \times H_B \Rightarrow H_B$.

1. Suppose $A$ and $B$ have a product $(A \times B, \pi_1, \pi_2)$ in $\mathcal{A}$. Prove that
   $(H_{A \times B}, H_{\pi_1}, H_{\pi_2})$ is a product of $H_A$ and $H_B$.
2. Conversely, suppose $C$ is an object of $\mathcal{A}$ and
   $\varphi \colon H_C \Rightarrow H_A \times H_B$ is a natural isomorphism. Prove that there are
   unique maps $p_1 \colon C \to A$ and $p_2 \colon C \to B$ with $H_{p_i} = \mathrm{pr}_i \circ \varphi$,
   and that $(C, p_1, p_2)$ is a product of $A$ and $B$ in $\mathcal{A}$.

So: $H_A \times H_B$ is representable if and only if $A$ and $B$ have a product.

## What you may use

- Theorems 1 and 2 of the lecture.
- From 4C: the Yoneda embedding is full and faithful.
- From 6A: Theorem 1 (a cone is a limit cone exactly when "compose with the projections" is a bijection for each test object).

## What a complete proof must show

- [ ] In part 1, exactly which theorem is applied and to which limit cone.
- [ ] In part 2, where $p_1, p_2$ come from and why they are unique.
- [ ] In part 2, for an arbitrary object $D$, the function $\mathcal{A}(D, C) \to \mathcal{A}(D, A) \times \mathcal{A}(D, B)$ induced by $\varphi$ is computed in terms of $p_1, p_2$, and its bijectivity is used.
- [ ] The conclusion of part 2 is stated as a universal property and matched against that bijection.

## Hints — one at a time

<details>
<summary>Hint 1 — part 1 is short</summary>

A product is a limit. One theorem of the lecture is about what the Yoneda embedding does to
limits. Say precisely what it gives, including the projections.

</details>

<details>
<summary>Hint 2 — where the maps come from</summary>

$\mathrm{pr}_1 \circ \varphi$ is a natural transformation $H_C \Rightarrow H_A$. Which property of
the Yoneda embedding turns such a thing into a map of $\mathcal{A}$, and which property makes that
map unique?

</details>

<details>
<summary>Hint 3 — evaluate at a test object</summary>

Fix $D$. The component $\varphi_D$ is a bijection from $\mathcal{A}(D, C)$ to a set you can
describe. Using $H_{p_i} = \mathrm{pr}_i \circ \varphi$, what are the two coordinates of
$\varphi_D(g)$ for $g \colon D \to C$?

</details>

<details>
<summary>Hint 4 — recognise the universal property</summary>

You now know that a specific function is a bijection for every $D$. Write the universal property
of a product of $A$ and $B$ as an "exists a unique" statement and compare.

</details>

## Check yourself

- In part 2, did you need $\varphi$ to be natural, or only each $\varphi_D$ to be a bijection? Where exactly?
- Does your argument generalise from binary products to limits of any shape? What would the statement be?
- In a poset, what does the result say about down-sets?

## Write it up

Write your proof in `proofs/6b/p06_products_of_representables.md`, then ask Claude to review it.
