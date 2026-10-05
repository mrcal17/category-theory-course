# 6B·P04 — Representable means the category of elements has a terminal object

**Type:** core · **Technique:** re-expressing a universal property · **Unlocked by:** `6b_presheaf_limits` §4
**Source:** adapted from Leinster §6.2 and Riehl §2.4

## Statement

Let $\mathcal{A}$ be a locally small category and $X \colon \mathcal{A}^{\mathrm{op}} \to \mathbf{Set}$
a presheaf. For $u \in X(A)$ write $\tilde{u} \colon H_A \Rightarrow X$ for the natural
transformation with $\tilde{u}_B(g) = (Xg)(u)$.

1. Prove that an object $(A, u)$ of $\mathbf{E}(X)$ is terminal if and only if $\tilde{u}$ is a
   natural isomorphism.
2. Deduce that $X$ is representable if and only if $\mathbf{E}(X)$ has a terminal object.

## What you may use

- The definition of $\mathbf{E}(X)$ and of a terminal object.
- The Yoneda lemma (4B): every natural transformation $H_A \Rightarrow X$ is $\tilde{u}$ for exactly one $u \in X(A)$.
- That a natural transformation is a natural isomorphism exactly when each component is a bijection (1D).
- From 4C (Theorem 1.1): $\tilde{u}$ is a natural isomorphism if and only if $(A, u)$ is a universal element of $X$. If you quote it, the work of part 1 is to show that "terminal in $\mathbf{E}(X)$" and "universal element" are the same condition; say at the start which route you are taking.

## What a complete proof must show

- [ ] "Terminal" unpacked into a statement with explicit quantifiers over objects $(B, x)$ and maps of $\mathcal{A}$.
- [ ] "Each $\tilde{u}_B$ is a bijection" unpacked the same way.
- [ ] The two unpacked statements compared, in both directions.
- [ ] In part 2, starting from an arbitrary representation $\alpha \colon H_A \cong X$, which element $u$ is used and why $\alpha = \tilde{u}$.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Both conditions in part 1 are "for every ... there is exactly one ..." statements. Write each out
in full, in terms of maps of $\mathcal{A}$ and elements of the sets $X(B)$, and put them next to
each other.

</details>

<details>
<summary>Hint 2 — unpacking terminal</summary>

A map $(B, x) \to (A, u)$ in $\mathbf{E}(X)$ is a map $g \colon B \to A$ with a condition. Write the
condition. Now what does "exactly one such map, for each $(B, x)$" say about the function
$g \mapsto (Xg)(u)$?

</details>

<details>
<summary>Hint 3 — part 2</summary>

A representation is some natural isomorphism $\alpha \colon H_A \Rightarrow X$, not visibly of
the form $\tilde{u}$. Which lemma tells you it is of that form, and what is $u$?

</details>

## Check yourself

- For a graph, which objects of the subdivided picture could be terminal, and for which graphs is one of them terminal?
- Is the terminal object of $\mathbf{E}(X)$ unique? Up to what? What does that say about representations?
- Did you use local smallness anywhere?

## Write it up

Write your proof in `proofs/6b/p04_representable_iff_terminal_element.md`, then ask Claude to review it.
