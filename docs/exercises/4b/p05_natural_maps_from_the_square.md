# 4B·P05 — Natural maps $B \times B \to B$

**Type:** core · **Technique:** follow the generic element · **Unlocked by:** `4b_yoneda_lemma` §5, §8
**Source:** adapted from Riehl §2.2

## Statement

Let $Q \colon \mathbf{Set} \to \mathbf{Set}$ be the functor with $Q(B) = B \times B$ and
$Q(g)(b, b') = (g(b), g(b'))$ for a function $g \colon B \to C$. For each set $B$ let
$\pi^1_B, \pi^2_B \colon B \times B \to B$ be the two projections, $\pi^1_B(b, b') = b$ and
$\pi^2_B(b, b') = b'$.

Prove that there are **exactly two** natural transformations $Q \Rightarrow 1_{\mathbf{Set}}$,
namely $\pi^1$ and $\pi^2$.

## What you may use

- The definition of a natural transformation (1D).
- The proof of Lemma 5.3 in 4B as a model for the main step.
- If you have completed them: 4A·P05 part 3 and 4B·P03. They give a second, shorter route. Either
  route is acceptable, but do not mix them half-way.

## What a complete proof must show

- [ ] $\pi^1$ and $\pi^2$ are natural transformations (the naturality equation is stated and verified).
- [ ] $\pi^1 \ne \pi^2$: a specific set and a specific pair on which they differ.
- [ ] For an **arbitrary** natural transformation $\alpha \colon Q \Rightarrow 1_{\mathbf{Set}}$, a
      proof that $\alpha = \pi^1$ or $\alpha = \pi^2$: every component, on every pair.
- [ ] The step that uses naturality names the function at which the naturality square is taken and
      the element at which it is evaluated.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

"Exactly two" is three claims: these two things qualify, they are different, and nothing else
qualifies. The third claim is the substantial one, and it has the same shape as Lemma 5.3: show
that a natural transformation is determined by its value on one well-chosen element of one
well-chosen set.

</details>

<details>
<summary>Hint 2 — what plays the role of the identity?</summary>

In Lemma 5.3 every arrow $f \colon B \to A$ was the image of $1_A$ under $H_A(f)$. Here you need a
set $E$ and a pair $e \in Q(E)$ such that every pair $(b, b')$ in every set $B$ is the image of $e$
under $Q(g)$ for a suitable function $g \colon E \to B$. How many elements does $E$ need, and what
is $e$?

</details>

<details>
<summary>Hint 3 — using it</summary>

Once you have $E$ and $e$: the value $\alpha_E(e)$ is an element of $E$, so there are only a few
possibilities. Fix one. Now take any set $B$ and any pair $(b, b')$, write down the function $g$
from Hint 2, and apply naturality of $\alpha$ at $g$ to the element $e$.

</details>

## Check yourself

- Does your argument handle pairs with $b = b'$? Sets $B$ with one element? The empty set?
- Did you prove that a *single* choice (first or second) works for all sets $B$ at once, and not a
  choice that might vary with $B$?
- By the same method, how many natural transformations are there from $B \mapsto B \times B \times B$
  to the identity functor?

## Write it up

Write your proof in `proofs/4b/p05_natural_maps_from_the_square.md`, then ask Claude to review it.
