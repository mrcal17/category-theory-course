# 4C·P04 — Universal elements are unique up to unique isomorphism

**Type:** core · **Technique:** uniqueness up to unique isomorphism · **Unlocked by:** `4c_yoneda_consequences` §1, §5
**Source:** adapted from Leinster §4.3 and Riehl §2.3

## Statement

Let $X$ be a presheaf on a locally small category $\mathcal{A}$, and let $(A, u)$ and $(A', u')$ be
universal elements of $X$. Prove that there is a unique arrow $j \colon A \to A'$ of $\mathcal{A}$
such that

$$X(j)(u') = u,$$

and that this $j$ is an isomorphism.

Give a proof **directly from the definition of a universal element**. Do not use Corollary 5.1 or
the Yoneda lemma: the point of the exercise is that the definition alone is enough.

## What you may use

- The definition of a universal element (4C §1).
- The functor axioms for the presheaf $X$, in their contravariant form.
- The definition of an isomorphism in a category.

## What a complete proof must show

- [ ] Existence and uniqueness of $j$, with the universal element and the element of $X$ to which
      the definition is being applied both named.
- [ ] A candidate inverse $j' \colon A' \to A$, obtained with a stated justification.
- [ ] Proofs that $j' \circ j = 1_A$ and $j \circ j' = 1_{A'}$. Each must be an actual argument;
      "similarly" is acceptable for the second only if the first is complete.
- [ ] Every use of functoriality of $X$ is written in the correct (contravariant) order.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

This is the "unique up to unique isomorphism" pattern from 0C, which you also met for initial
objects in 2C. The pattern has three moves: use the universal property of one object to get a map;
use the universal property of the other to get a map back; use a *uniqueness* clause to show the
round trips are identities.

</details>

<details>
<summary>Hint 2 — where does $j$ come from?</summary>

The definition of a universal element produces arrows *into* the universal object, one for each
element of $X$ at any object. You want an arrow into $A'$ out of $A$. So: which of the two pairs is
playing the role of "the universal element", and which element of which set $X(B)$ are you feeding
it?

</details>

<details>
<summary>Hint 3 — why is the round trip an identity?</summary>

Both $j' \circ j$ and $1_A$ are arrows $A \to A$, and you want them to be equal. Which clause of
the definition of a universal element ever concludes that two arrows are equal? Decide which
universal element, and which element of which set, that clause should be applied to.

</details>

## Check yourself

- In your computation of $X(j' \circ j)(u)$, in which order did $X(j)$ and $X(j')$ appear?
- Did you prove that $j$ is the unique *arrow* with $X(j)(u') = u$, or only the unique *isomorphism*?
  The statement asks for the former.
- For $U \colon \mathbf{Grp} \to \mathbf{Set}$ (covariant) and the universal elements $(\mathbb{Z}, 1)$
  and $(\mathbb{Z}, -1)$, what is $j$?

## Write it up

Write your proof in `proofs/4c/p04_universal_elements_unique.md`, then ask Claude to review it.
