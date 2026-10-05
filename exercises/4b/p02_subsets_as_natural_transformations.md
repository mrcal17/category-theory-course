# 4B·P02 — Subsets as natural transformations

**Type:** warm-up · **Technique:** verifying an instance of $x \mapsto \tilde{x}$ · **Unlocked by:** `4b_yoneda_lemma` §4, §5
**Source:** adapted from Leinster §4.2

## Statement

Let $\mathscr{P} \colon \mathbf{Set}^{\mathrm{op}} \to \mathbf{Set}$ be the contravariant power-set
functor of 4A: $\mathscr{P}(B)$ is the set of subsets of $B$, and for $g \colon C \to B$ the
function $\mathscr{P}(g)$ sends $T \subseteq B$ to $g^{-1}(T) \subseteq C$.

Fix a set $A$ and a subset $S \subseteq A$. For each set $B$ define

$$\sigma_B \colon \mathbf{Set}(B, A) \to \mathscr{P}(B), \qquad \sigma_B(f) = f^{-1}(S).$$

1. Prove, directly from the definition, that $\sigma = (\sigma_B)_B$ is a natural transformation
   $H_A \Rightarrow \mathscr{P}$.
2. Compute $\hat{\sigma}$, the element of $\mathscr{P}(A)$ that the Yoneda lemma assigns to $\sigma$.
3. Using the Yoneda lemma, prove: for every natural transformation
   $\alpha \colon H_A \Rightarrow \mathscr{P}$ there is exactly one subset $S \subseteq A$ such that
   $\alpha_B(f) = f^{-1}(S)$ for all sets $B$ and all functions $f \colon B \to A$.

## What you may use

- The definition of a natural transformation $H_A \Rightarrow X$ (4B §1).
- For part 3 only: the Yoneda lemma (4B, Theorem 4.1), including the formulas for
  $\hat{\alpha}$ and $\tilde{x}$.
- Elementary facts about preimages. If you use $(f \circ g)^{-1}(S) = g^{-1}(f^{-1}(S))$, prove it.

## What a complete proof must show

- [ ] Part 1 states the naturality equation with quantifiers and proves an equality of two subsets
      by showing they have the same elements.
- [ ] Part 2 gives a specific subset of $A$ with a one-line justification.
- [ ] Part 3 proves both existence and uniqueness of $S$, and says which half of "bijection" gives which.
- [ ] Part 1 does **not** cite the Yoneda lemma; part 3 does not redo part 1.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Part 1 is a direct naturality check: fix $g \colon C \to B$ and $f \colon B \to A$, and compare
two subsets of $C$. Part 2 is a one-step evaluation. Part 3 is an application of a theorem: your
job is to match the theorem's notation to this situation, not to prove anything from scratch.

</details>

<details>
<summary>Hint 2 — part 2</summary>

The hat evaluates one particular component at one particular arrow. Which component, which arrow,
and what is the preimage of a set under that arrow?

</details>

<details>
<summary>Hint 3 — part 3</summary>

The Yoneda lemma says that $x \mapsto \tilde{x}$ is a bijection from $\mathscr{P}(A)$ onto the
natural transformations $H_A \Rightarrow \mathscr{P}$. For $x = S$, write out what $\tilde{S}_B(f)$
is using the definition of $\tilde{\ }$ and the definition of $\mathscr{P}$ on arrows. What have you
just recognised?

</details>

## Check yourself

- In part 1, did you compare elements $c \in C$, or did you manipulate symbols $f^{-1}$, $g^{-1}$
  without saying what they mean?
- What natural transformation corresponds to $S = \varnothing$? To $S = A$?
- How many natural transformations $H_A \Rightarrow \mathscr{P}$ are there when $A$ has three elements?

## Write it up

Write your proof in `proofs/4b/p02_subsets_as_natural_transformations.md`, then ask Claude to review it.
