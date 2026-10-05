# 6B·P01 — The category of elements is a category

**Type:** warm-up · **Technique:** verifying axioms · **Unlocked by:** `6b_presheaf_limits` §4
**Source:** adapted from Leinster §6.2

## Statement

Let $\mathcal{A}$ be a category and $X \colon \mathcal{A}^{\mathrm{op}} \to \mathbf{Set}$ a presheaf.
Recall that $\mathbf{E}(X)$ has as objects the pairs $(A, x)$ with $x \in X(A)$, and as maps
$(A', x') \to (A, x)$ the maps $f \colon A' \to A$ of $\mathcal{A}$ with $(Xf)(x) = x'$.

Prove that:

1. with composition and identities taken from $\mathcal{A}$, $\mathbf{E}(X)$ is a category;
2. $P \colon \mathbf{E}(X) \to \mathcal{A}$, $P(A, x) = A$, $P(f) = f$, is a functor;
3. $P$ is faithful.

## What you may use

- The definition of a category and of a (contravariant) functor (1A, 1C).
- The definition of faithful (1C).

## What a complete proof must show

- [ ] The composite in $\mathcal{A}$ of two maps of $\mathbf{E}(X)$ satisfies the defining condition for a map of $\mathbf{E}(X)$, with the right source and target.
- [ ] Each identity of $\mathcal{A}$ satisfies the condition for the appropriate objects.
- [ ] Why associativity and the identity laws need no new argument.
- [ ] For faithfulness: two maps of $\mathbf{E}(X)$ with the same domain, codomain and image under $P$ are equal.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Most of the category axioms are inherited from $\mathcal{A}$. The work is in two places only: the
condition "$(Xf)(x) = x'$" must survive composition, and must hold for identities. Say this, then
do those two checks.

</details>

<details>
<summary>Hint 2 — composition</summary>

Take $f' \colon (A'', x'') \to (A', x')$ and $f \colon (A', x') \to (A, x)$. Which functor law for
$X$ describes $X(f \circ f')$? Write it down with the contravariance visible before you apply it
to $x$.

</details>

<details>
<summary>Hint 3 — faithfulness</summary>

What, by definition, *is* a map $(A', x') \to (A, x)$ in $\mathbf{E}(X)$? If two of them have the
same image under $P$, what does that say?

</details>

## Check yourself

- Is $P$ full? Find a small example (a graph will do) where it is not.
- Can two different objects of $\mathbf{E}(X)$ have the same image under $P$?
- Did you ever apply $Xf$ to an element of the wrong set? Check the domain of each $Xf$ you wrote.

## Write it up

Write your proof in `proofs/6b/p01_category_of_elements_is_a_category.md`, then ask Claude to review it.
