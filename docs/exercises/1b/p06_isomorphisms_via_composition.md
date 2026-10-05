# 1B·P06 — Isomorphisms are detected by composition

**Type:** stretch · **Technique:** choosing where to evaluate a "for all" hypothesis · **Unlocked by:** `1b_isomorphisms_duality` §1, §2
**Source:** adapted from Riehl §1.2

## Statement

Let $f \colon A \to B$ be an arrow in a category $\mathcal{A}$ whose hom-sets are sets. For each
object $C$, composition with $f$ defines a function

$$f_* \colon \mathcal{A}(C, A) \to \mathcal{A}(C, B), \qquad x \mapsto f \circ x .$$

Prove that the following are equivalent:

1. $f$ is an isomorphism;
2. for **every** object $C$, the function $f_* \colon \mathcal{A}(C, A) \to \mathcal{A}(C, B)$ is a bijection.

## What you may use

- The definitions of category and isomorphism; Proposition 1.1.
- From 0B: a function is a bijection exactly when it is injective and surjective, and exactly
  when it has a two-sided inverse function.
- Nothing about elements of $A$ or $B$. The only "elements" available are elements of
  hom-sets, that is, arrows.

## What a complete proof must show

- [ ] (1 implies 2) For an arbitrary object $C$, the function $f_*$ is shown to be a bijection, either by exhibiting an inverse function and checking both composites, or by proving injectivity and surjectivity separately.
- [ ] (2 implies 1) An arrow $g \colon B \to A$ is produced from hypothesis 2, saying which object $C$ and which half of "bijection" produced it.
- [ ] (2 implies 1) **Both** $f \circ g = 1_B$ and $g \circ f = 1_A$ are proved, saying which object $C$ and which half of "bijection" each uses.
- [ ] The hypothesis in 2 is never used for an unspecified $C$: each use names its $C$.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

An equivalence, so two implications. In one of them you are given an inverse arrow and must
build an inverse *function* between hom-sets. In the other you are given a family of
bijections, one for each object $C$, and must build a single arrow. As in Proposition 2.1, a
hypothesis that holds "for every $C$" is used by choosing $C$.

</details>

<details>
<summary>Hint 2 — from 1 to 2</summary>

If composing with $f$ is the function, what is the natural guess for a function going the
other way, from $\mathcal{A}(C, B)$ to $\mathcal{A}(C, A)$? Check that your guess has the right
domain and codomain before checking anything else.

</details>

<details>
<summary>Hint 3 — from 2 to 1, producing $g$</summary>

You want an arrow $B \to A$. In which hom-set does such an arrow live, and therefore which
choice of $C$ makes $f_*$ a function *out of* that hom-set? For that $C$, which arrows in the
codomain of $f_*$ do you know exist, without assuming anything further about $\mathcal{A}$?

</details>

<details>
<summary>Hint 4 — from 2 to 1, the second equation</summary>

One of the two equations will come straight from how you produced $g$. The other asks you to
prove that two arrows in the same hom-set are equal. Which half of "bijection" is the tool for
proving two things equal, and for which $C$ do both of your arrows lie in the domain of $f_*$?

</details>

## Check yourself

- In (2 implies 1), did you use surjectivity once and injectivity once, each for a named $C$? Are the two choices of $C$ the same?
- Did you use the full strength of hypothesis 2 (all objects $C$), or only two particular objects? What weaker hypothesis would have been enough?
- State the dual result, about the functions $x \mapsto x \circ f$. You do not need to prove it; say in one sentence why it holds.
- Compare with the definition of monic: what does "$f_*$ is injective for every $C$" say on its own?

## Write it up

Write your proof in `proofs/1b/p06_isomorphisms_via_composition.md`, then ask Claude to review it.
