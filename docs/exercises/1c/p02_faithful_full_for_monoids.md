# 1C·P02 — Faithful and full for functors between monoids

**Type:** warm-up · **Technique:** unpacking a definition · **Unlocked by:** `1c_functors` §3, §7
**Source:** adapted from Leinster §1.2

## Statement

Let $M$ and $N$ be monoids, regarded as one-object categories, and let $F \colon M \to N$ be a
functor, corresponding to the monoid homomorphism $\varphi \colon M \to N$ as in Proposition 3.1.

(a) Prove that $F$ is faithful if and only if $\varphi$ is injective.

(b) Prove that $F$ is full if and only if $\varphi$ is surjective.

(c) Prove that $F$ is essentially surjective on objects, whatever $\varphi$ is.

(d) Give, with justification, a homomorphism between monoids whose functor is faithful but not
full, and one whose functor is full but not faithful.

## What you may use

- The definitions of faithful, full and essentially surjective on objects (`1c_functors` §7).
- Proposition 3.1 of the lecture and Proposition 4.1 of 1A (the dictionary between monoids and
  one-object categories).
- The definitions of injective and surjective (0B).
- For (c): the observation in `1b_isomorphisms_duality` §1 that every identity arrow is an isomorphism.

## What a complete proof must show

- [ ] In (a) and (b): the definition of faithful / full is written out for these particular categories, naming the hom-sets involved, before any conclusion is drawn.
- [ ] In (a) and (b): both directions of each "if and only if" are addressed (a chain of equivalent statements is acceptable if each link is justified).
- [ ] In (c): for the object of $N$, an object of $M$ and an isomorphism are named.
- [ ] In (d): two explicit homomorphisms, each checked to be a homomorphism, with the relevant injectivity / surjectivity verified or refuted by explicit elements.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Parts (a)–(c) are proofs by unpacking: each definition in §7 begins "for every pair of
objects" or "for every object". How many pairs of objects does $M$ have? How many objects does
$N$ have? Write the definitions out with those quantifiers resolved.

</details>

<details>
<summary>Hint 2 — the hom-set function</summary>

For the one pair of objects there is, identify the function
$\mathcal{A}(A, A') \to \mathcal{B}(F(A), F(A'))$ of the definition as a function you already
have a name for.

</details>

<details>
<summary>Hint 3 — part (d)</summary>

You need small monoids and homomorphisms between them that are injective but not surjective,
and surjective but not injective. Additive monoids of numbers and their quotients or
submonoids are a good place to look. Remember that a monoid homomorphism must preserve the
unit as well as the operation.

</details>

## Check yourself

- Did you say which hom-sets the definition of faithful refers to here, or did you jump straight to "injective"?
- In (d), did you verify that your maps preserve the unit?
- §7 warned that "faithful" is not the same as "injective on arrows". Why is there no difference in this exercise?
- Proposition 2.2 of 1B found a monoid homomorphism that is epic in $\mathbf{Mon}$ without being surjective. So which of "full" and "epic in $\mathbf{Mon}$" is the stronger condition on a homomorphism, in that example?

## Write it up

Write your proof in `proofs/1c/p02_faithful_full_for_monoids.md`, then ask Claude to review it.
