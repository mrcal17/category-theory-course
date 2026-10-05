# 0C·P03 — Group homomorphisms preserve inverses

**Type:** core · **Technique:** direct calculation, then an appeal to uniqueness · **Unlocked by:** `0c_proof_toolkit_uniqueness` §2
**Source:** standard group theory; technique from Hammack Ch 7

## Statement

Let $G$ and $H$ be groups and let $f \colon G \to H$ be a group homomorphism. Prove that for
every $a \in G$,

$$f(a^{-1}) = f(a)^{-1}.$$

## What you may use

- The definitions of group and group homomorphism (0C §2).
- Proposition 2 of 0C: $f(e_G) = e_H$.
- The fact recorded in 0C §2 that each element of a group has exactly one inverse.

## What a complete proof must show

- [ ] It says what the symbol $f(a)^{-1}$ means: which element of which group, characterised by
      which equations.
- [ ] It identifies a candidate element of $H$ and verifies, by calculation, every equation
      needed for the candidate to be an inverse of $f(a)$.
- [ ] Each step of each calculation is justified: the homomorphism property, the definition of
      inverse in $G$, or Proposition 2.
- [ ] Uniqueness of inverses is invoked explicitly to conclude.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

The right-hand side $f(a)^{-1}$ is not given by a formula. It is defined as *the unique element
with a certain property*. To prove that some element equals "the unique thing with property
$P$", it is enough to prove that the element has property $P$. So this is a verification
followed by one sentence that appeals to uniqueness.

</details>

<details>
<summary>Hint 2 — what is property P?</summary>

Write down, for an arbitrary $y \in H$, exactly what must be true for $y$ to be an inverse of
the element $f(a)$. How many equations is that? Which element of $H$ are you claiming satisfies
them?

</details>

<details>
<summary>Hint 3 — the verification</summary>

Each equation has a product of two values of $f$ on one side. The homomorphism property is the
only tool that says anything about such a product. After applying it, what do you find inside
$f$, and which proposition tells you its image?

</details>

## Check yourself

- Did you verify both equations for an inverse, or only one?
- Where exactly did you use that inverses in $H$ are unique? What would your argument prove
  without that fact?
- Compare with Proposition 2. There the identity was pinned down by cancelling; here the inverse
  is pinned down by uniqueness. Which of the two proofs used more of the group axioms of $H$?
- Suppose instead that $f$ is a *monoid* homomorphism between monoids and that $a$ happens to
  have an inverse. Which lines of your proof still stand?

## Write it up

Write your proof in `proofs/0c/p03_homomorphisms_preserve_inverses.md`, then ask Claude to review it.
