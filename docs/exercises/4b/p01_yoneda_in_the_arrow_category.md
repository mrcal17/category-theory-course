# 4B·P01 — Yoneda by hand in the arrow category

**Type:** warm-up · **Technique:** unpacking naturality in a small example · **Unlocked by:** `4b_yoneda_lemma` §1
**Source:** adapted from Leinster §4.2

## Statement

Let $\mathbf{2}$ be the category with two objects $0$ and $1$ and exactly one non-identity arrow
$u \colon 0 \to 1$. A presheaf $X$ on $\mathbf{2}$ consists of two sets $X(0)$, $X(1)$ and one
function $X(u) \colon X(1) \to X(0)$ (together with the two identity functions).

Working **directly from the definition of a natural transformation**, and without quoting the
Yoneda lemma:

1. Describe the presheaves $H_0$ and $H_1$ completely: both sets, and the function assigned to $u$.
2. Prove that $\alpha \mapsto \alpha_0(1_0)$ is a bijection from the set of natural transformations
   $H_0 \Rightarrow X$ to $X(0)$.
3. Prove that $\alpha \mapsto \alpha_1(1_1)$ is a bijection from the set of natural transformations
   $H_1 \Rightarrow X$ to $X(1)$. For a given $x \in X(1)$, say explicitly what *both* components of
   the corresponding natural transformation are.

## What you may use

- The definition of $H_A$ on objects and arrows (4A §4).
- The definition of a natural transformation $H_A \Rightarrow X$ as restated in 4B §1.
- Basic facts about functions, including: there is exactly one function out of the empty set into
  any set.

## What a complete proof must show

- [ ] Part 1 lists every arrow in each hom-set of $\mathbf{2}$ that is used, including the empty ones.
- [ ] For each of parts 2 and 3, every naturality equation is written out (there are only a few
      arrows) and it is said which are automatic and which impose a condition.
- [ ] Bijectivity is proved, not asserted: either injective and surjective, or an explicit inverse
      with both composites checked.
- [ ] The Yoneda lemma is not cited at any point.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Everything here is finite and small, so the proof is an exhaustive unpacking. A natural
transformation out of $H_A$ has two components; write down the domain of each one first. One of
the four domains is empty, and that changes what there is to choose.

</details>

<details>
<summary>Hint 2 — how many equations?</summary>

The category has three arrows, so each natural transformation has three naturality squares. Two
of them are for identity arrows. What does a naturality square at an identity arrow say, for any
natural transformation whatsoever?

</details>

<details>
<summary>Hint 3 — part 3</summary>

In part 3 the remaining square, the one at $u$, has a one-element set in its top-left corner.
Chase that one element both ways round. What does the square tell you about the component at $0$
once the component at $1$ is known?

</details>

## Check yourself

- In part 2, what is the component at $1$? Did you say why it is unique?
- After finishing, compare your answer to part 3 with the formula $\tilde{x}_B(p) = X(p)(x)$ from
  the lecture. Do they agree?
- How many natural transformations $H_0 \Rightarrow H_1$ and $H_1 \Rightarrow H_0$ does your result predict?

## Write it up

Write your proof in `proofs/4b/p01_yoneda_in_the_arrow_category.md`, then ask Claude to review it.
