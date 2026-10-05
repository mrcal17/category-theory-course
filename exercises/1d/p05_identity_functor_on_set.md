# 1D·P05 — The identity functor on Set has only one natural endomorphism

**Type:** core · **Technique:** naturality at a well-chosen arrow · **Unlocked by:** `1d_natural_transformations` §1
**Source:** adapted from Riehl §1.4

## Statement

Let $\alpha \colon 1_{\mathbf{Set}} \Rightarrow 1_{\mathbf{Set}}$ be a natural transformation from
the identity functor on $\mathbf{Set}$ to itself. Prove that $\alpha$ is the identity
transformation: $\alpha_X = 1_X$ for every set $X$.

## What you may use

- The definition of a natural transformation (1D §1).
- Two functions $X \to X$ are equal when they agree at every element of $X$ (0B).
- Elementary facts about functions between sets, including what the functions out of, and into, a one-element set are.

## What a complete proof must show

- [ ] It fixes an arbitrary set $X$ and an arbitrary element $x \in X$, and states that the goal is $\alpha_X(x) = x$.
- [ ] It names the specific arrow of $\mathbf{Set}$ at which naturality of $\alpha$ is used.
- [ ] It handles the case in which $X$ is empty (one sentence, but it must be there).
- [ ] It does not assume anything about $\alpha_X$ beyond naturality.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

You are given a natural transformation about which you know nothing except that *every*
naturality square commutes. The whole proof is a choice of which square to look at. The
non-example in §1 of the lecture, where a family failed to be natural, was refuted by a single
square; study which arrow was used there.

</details>

<details>
<summary>Hint 2 — what you want an arrow to do</summary>

You want to pin down the value of $\alpha_X$ at one particular element $x$. Naturality relates
$\alpha_X$ to $\alpha_W$ for another set $W$ through a function $W \to X$. What property should
that function have so that the square talks about $x$ specifically?

</details>

<details>
<summary>Hint 3 — choosing $W$</summary>

Is there a set $W$ for which you already know, without any argument about naturality, exactly
what $\alpha_W$ must be, simply because there are so few functions $W \to W$?

</details>

## Check yourself

- Your proof should work for every natural transformation $\alpha$, without knowing a formula for it. Does it?
- Did you treat $X = \emptyset$?
- Try the same strategy on the functor $L$ of finite sequences from §4: can you pin down every natural transformation $L \Rightarrow L$ this way? What goes differently? (You are not asked to prove anything here.)

## Write it up

Write your proof in `proofs/1d/p05_identity_functor_on_set.md`, then ask Claude to review it.
