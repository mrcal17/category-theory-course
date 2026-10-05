# 6D·P05 — The Kleisli category is the category of free algebras

**Type:** core · **Technique:** building a comparison functor · **Unlocked by:** `6d_monads` §5
**Source:** adapted from Riehl §5.2

## Statement

Let $(T, \eta, \mu)$ be a monad on $\mathcal{A}$. Define
$$J \colon \mathcal{A}_T \to \mathcal{A}^T, \qquad J(A) = (TA, \mu_A), \qquad
J(g \colon A \rightsquigarrow B) = \mu_B \circ T(g).$$

Prove that:

1. $J(g)$ is a map of algebras $(TA, \mu_A) \to (TB, \mu_B)$, and $J$ is a functor;
2. $J \circ F_T = F^T$ and $U^T \circ J = U_T$;
3. $J$ is full and faithful.

Conclude that $\mathcal{A}_T$ is equivalent to the full subcategory of $\mathcal{A}^T$ whose
objects are the free algebras $(TA, \mu_A)$.

## What you may use

- Lemma 1, Theorem 2 and Theorem 3 of the lecture, including the functoriality of $U_T$ proved there.
- The monad axioms and naturality of $\eta$ and $\mu$.
- From 1E: a full, faithful, essentially surjective functor is an equivalence.

## What a complete proof must show

- [ ] The algebra-map square for $\mu_B \circ T(g)$, with each step justified by a named axiom or naturality.
- [ ] For part 3: for each $A, B$, that $g \mapsto \mu_B \circ T(g)$ is a bijection from $\mathcal{A}(A, TB)$ to the set of algebra maps $(TA, \mu_A) \to (TB, \mu_B)$, by exhibiting an inverse and checking both composites.
- [ ] In checking that the inverse really is one, the step that uses "is a map of algebras" is identified.
- [ ] The conclusion about the full subcategory, with what "essentially surjective" refers to.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Parts 1 and 2 are verifications that reuse computations from the proof of Theorem 3. Part 3 is
the real content: a bijection between hom-sets. The reliable way to prove a function is a
bijection is to write down its inverse.

</details>

<details>
<summary>Hint 2 — the algebra-map square</summary>

Write $\mu_B \circ T(g)$ as a composite of two maps, each of which you already know to be a map of
algebras for a reason given in the lecture. Which lemma covers $T(g)$, and what is the
domain algebra of $\mu_B$?

</details>

<details>
<summary>Hint 3 — finding the inverse</summary>

Given an algebra map $k \colon TA \to TB$, you need a map $A \to TB$. There is only one map in
sight from $A$ to $TA$. What do you get by using it?

</details>

<details>
<summary>Hint 4 — why it is an inverse</summary>

One composite is a unit-law computation. For the other you must show that an algebra map out of
a free algebra is determined by its restriction along the unit. Which monad axiom expresses
$1_{TA}$ in terms of $\eta_A$, and what does the algebra-map condition for $k$ let you move past
what?

</details>

## Check yourself

- Compare your bijection with the transposition of the adjunction $F^T \dashv U^T$. Is it the same function?
- In the poset case, Theorem 5(c), what does part 3 say?
- Is $J$ injective on objects? Does it need to be for the conclusion?

## Write it up

Write your proof in `proofs/6d/p05_kleisli_embeds_in_eilenberg_moore.md`, then ask Claude to review it.
