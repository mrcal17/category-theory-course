# 5B·P02 — The cokernel is a coequalizer

**Type:** warm-up · **Technique:** maps out of a quotient · **Unlocked by:** `5b_colimits` §3
**Source:** adapted from Leinster §5.2

## Statement

Let $\theta \colon G \to H$ be a homomorphism of abelian groups (written additively), and let
$0 \colon G \to H$ be the homomorphism sending every element to $0$. Let
$N = \operatorname{im}(\theta) = \{\theta(g) : g \in G\}$, a subgroup of $H$, and let
$q \colon H \to H/N$ be the quotient homomorphism, $q(h) = h + N$.

Prove that $q$ is a coequalizer of $\theta$ and $0$ in the category $\mathbf{Ab}$.

## What you may use

- The definition of a coequalizer (5B §3), read in the category $\mathbf{Ab}$: all maps are
  homomorphisms.
- The universal property of a quotient group from your algebra course: if
  $N$ is a subgroup of an abelian group $H$ and $f \colon H \to A$ is a homomorphism with
  $f(n) = 0$ for all $n \in N$, then there is a unique homomorphism $\bar{f} \colon H/N \to A$
  with $\bar{f} \circ q = f$.
- That the image of a homomorphism is a subgroup.

## What a complete proof must show

- [ ] $q \circ \theta = q \circ 0$, with a reason.
- [ ] An arbitrary homomorphism $f \colon H \to A$ with $f \theta = f 0$ is fixed, and the
      hypothesis of the quotient-group property is verified for it.
- [ ] Existence of $\bar{f}$ and uniqueness of $\bar{f}$ are each stated and justified (it is
      fine for both to come from the same quoted fact, but say so).
- [ ] The mediating map is a homomorphism, not only a function.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

This is a universal-property proof in which the heavy lifting is done by a fact you may quote.
Your job is the translation: put the definition of coequalizer and the quoted property of
$H/N$ side by side and match the hypotheses.

</details>

<details>
<summary>Hint 2 — what does the condition on f say?</summary>

Write out what $f \circ \theta = f \circ 0$ means at an element $g \in G$. What does it tell you
about the value of $f$ on a typical element of $N$?

</details>

<details>
<summary>Hint 3 — do not forget the first checklist item</summary>

Before the universal property, a coequalizer must satisfy $q \theta = q 0$. What is
$q(\theta(g))$ as a coset, and why is that the zero element of $H/N$?

</details>

## Check yourself

- Did you check $q \theta = q 0$, or only the universal property?
- Compare with the coequalizer in $\mathbf{Set}$ of the underlying functions of $\theta$ and
  $0$. Is it the same set as $H/N$? (Think about $\theta \colon \mathbb{Z} \to \mathbb{Z}$, $\theta(g) = 2g$, and count
  the classes in each case.)
- What is the dual statement about kernels, and where was it mentioned in 5A?

## Write it up

Write your proof in `proofs/5b/p02_cokernel_coequalizer.md`, then ask Claude to review it.
