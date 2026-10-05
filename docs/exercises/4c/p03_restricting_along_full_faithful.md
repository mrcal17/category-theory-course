# 4C·P03 — Restricting a representable along a full and faithful functor

**Type:** core · **Technique:** existence and uniqueness, transported along a functor · **Unlocked by:** `4c_yoneda_consequences` §1, §2
**Source:** adapted from Leinster §4.3

## Statement

Let $J \colon \mathcal{A} \to \mathcal{B}$ be a full and faithful functor between locally small
categories, and let $X \colon \mathcal{B}^{\mathrm{op}} \to \mathbf{Set}$ be a presheaf on
$\mathcal{B}$. Write $X \circ J^{\mathrm{op}}$ for the presheaf on $\mathcal{A}$ that sends an
object $B$ of $\mathcal{A}$ to $X(J(B))$ and an arrow $g$ of $\mathcal{A}$ to $X(J(g))$.

Suppose that $A$ is an object of $\mathcal{A}$ and $u \in X(J(A))$ is such that $(J(A), u)$ is a
universal element of $X$.

1. Prove that $(A, u)$ is a universal element of $X \circ J^{\mathrm{op}}$.
2. Deduce: if a presheaf on $\mathcal{B}$ is represented by an object in the image of $J$, then its
   restriction to $\mathcal{A}$ is representable.
3. Show by an example that the hypothesis "full" cannot be dropped in part 1: give a faithful
   functor $J$, a presheaf $X$ and a universal element $(J(A), u)$ of $X$ for which $(A, u)$ is not
   a universal element of $X \circ J^{\mathrm{op}}$.

You may take it as given that $X \circ J^{\mathrm{op}}$ is a presheaf.

## What you may use

- The definition of a universal element and Theorem 1.1 (4C §1).
- The definitions of full and faithful (restated in 4C §2).
- For part 3, any small categories you like; one-object or two-object categories suffice.

## What a complete proof must show

- [ ] Part 1 fixes an arbitrary object $B$ of $\mathcal{A}$ and an arbitrary element
      $x \in X(J(B))$, and proves existence and uniqueness of the required arrow $B \to A$ of
      $\mathcal{A}$ as two separate steps.
- [ ] Each step says whether it uses universality of $(J(A), u)$, fullness of $J$, or faithfulness
      of $J$.
- [ ] Part 2 is an explicit deduction naming which theorem turns universal elements into
      representations, in each direction.
- [ ] Part 3 specifies the categories, the functor, the presheaf and the element completely, and
      identifies which of existence or uniqueness fails.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Part 1 is an "exists unique" statement in $\mathcal{A}$, and your hypothesis is an "exists unique"
statement in $\mathcal{B}$. The functor $J$ is the bridge between them. Write the two statements
out in full, one above the other, and mark which symbols differ.

</details>

<details>
<summary>Hint 2 — existence</summary>

The hypothesis hands you an arrow of $\mathcal{B}$ between two objects that both happen to be
values of $J$. You need an arrow of $\mathcal{A}$. Which property of $J$ produces arrows of
$\mathcal{A}$ from arrows of $\mathcal{B}$?

</details>

<details>
<summary>Hint 3 — uniqueness</summary>

Suppose two arrows $f, f' \colon B \to A$ of $\mathcal{A}$ both do the job. Apply $J$ to each. What
does the uniqueness half of the hypothesis tell you about $J(f)$ and $J(f')$, and which property
of $J$ finishes the argument? Remember to say that $f$ and $f'$ are parallel.

</details>

<details>
<summary>Hint 4 — part 3</summary>

You want a situation where $\mathcal{B}$ has an arrow between two objects in the image of $J$ that
does not come from $\mathcal{A}$. The smallest way to arrange that is for $\mathcal{A}$ to have
fewer arrows than $\mathcal{B}$ on the same objects. For $X$, a representable presheaf on
$\mathcal{B}$ always has a universal element that you know from the Yoneda lemma.

</details>

## Check yourself

- Did you use fullness and faithfulness in *different* steps? If one of them was never used, look again.
- Take $J$ to be the inclusion of finite-dimensional vector spaces into $\mathbf{Vect}_k$. What
  does part 2 say?
- Does part 1 have a converse: if $(A, u)$ is universal for $X \circ J^{\mathrm{op}}$, must
  $(J(A), u)$ be universal for $X$? (No proof required; think about what $X$ could do on objects
  outside the image of $J$.)

## Write it up

Write your proof in `proofs/4c/p03_restricting_along_full_faithful.md`, then ask Claude to review it.
