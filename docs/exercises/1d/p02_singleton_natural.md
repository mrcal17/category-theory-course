# 1D·P02 — The singleton map into the power set is natural

**Type:** warm-up · **Technique:** checking a naturality square on elements · **Unlocked by:** `1d_natural_transformations` §1, §4
**Source:** adapted from Riehl §1.4

## Statement

Let $\mathcal{P} \colon \mathbf{Set} \to \mathbf{Set}$ be the (covariant) power set functor:
$\mathcal{P}(X)$ is the set of all subsets of $X$, and for a function $f \colon X \to Y$ the
function $\mathcal{P}(f) \colon \mathcal{P}(X) \to \mathcal{P}(Y)$ sends a subset $S \subseteq X$
to its image $f(S) = \{ f(s) : s \in S \} \subseteq Y$.

For each set $X$ define $\eta_X \colon X \to \mathcal{P}(X)$ by $\eta_X(x) = \{x\}$.
Prove that $\eta = (\eta_X)_{X \in \mathbf{Set}}$ is a natural transformation
$1_{\mathbf{Set}} \Rightarrow \mathcal{P}$.

## What you may use

- The definition of a natural transformation (1D §1).
- That $\mathcal{P}$, as described, is a functor (you need not re-prove functoriality).
- Two functions with the same domain and codomain are equal when they agree on every element (0B).
- Two sets are equal when they have the same elements.

## What a complete proof must show

- [ ] It identifies the two functors and checks that each $\eta_X$ has the correct domain and codomain.
- [ ] It writes the naturality equation for an arbitrary function $f \colon X \to Y$, with both sides as functions $X \to \mathcal{P}(Y)$.
- [ ] It evaluates both sides at an arbitrary $x \in X$ and shows that the two resulting subsets of $Y$ are equal.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Follow the three-step checklist under the definition in §1. The only step with content is the
square, and it is an equation between functions, so it is proved one element at a time.

</details>

<details>
<summary>Hint 2 — set up the square</summary>

Draw the naturality square for $f \colon X \to Y$. Since the first functor is the identity
functor, the top edge is just $f$. Label all four edges before computing anything.

</details>

<details>
<summary>Hint 3 — the computation</summary>

Start with $x$ in the top-left corner and carry it round each route. On one route you apply
$\mathcal{P}(f)$ to a set you can list completely. What is the image of a one-element set?

</details>

## Check yourself

- Did you prove an equality of *subsets of $Y$*, or only write the same symbol on both sides?
- The family $\eta_X$ is "given by the same formula for every $X$". Which sentence of your proof is where that pays off?
- Would the family $x \mapsto X \setminus \{x\}$ (the complement of the singleton) also be natural? Test it on a function between small sets before answering.

## Write it up

Write your proof in `proofs/1d/p02_singleton_natural.md`, then ask Claude to review it.
