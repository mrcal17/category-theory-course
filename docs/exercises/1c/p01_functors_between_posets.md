# 1C·P01 — Functors between posets are order-preserving maps

**Type:** warm-up · **Technique:** unpacking a definition; verifying functoriality · **Unlocked by:** `1c_functors` §3
**Source:** adapted from Leinster §1.2

## Statement

Let $(P, \le)$ and $(Q, \le)$ be posets, regarded as categories as in `1a_categories` §5. A
function $\varphi \colon P \to Q$ is **order-preserving** if $x \le y$ in $P$ implies
$\varphi(x) \le \varphi(y)$ in $Q$.

(a) Prove that if $F \colon P \to Q$ is a functor, then its function on objects is
order-preserving.

(b) Prove that if $\varphi \colon P \to Q$ is an order-preserving function, then there is
exactly one functor $F \colon P \to Q$ with $F(x) = \varphi(x)$ for every object $x$.

## What you may use

- The definition of a functor and the three-item "verify" checklist of `1c_functors` §1.
- The category of a poset: there is exactly one arrow $x \to y$ if $x \le y$ and none
  otherwise, so every hom-set has at most one element.
- You may model the layout on Proposition 3.1 (monoids), but the argument here is different:
  there the object part was forced and the arrow part carried the information; decide for
  yourself what happens here.

## What a complete proof must show

- [ ] (a) Starting from $x \le y$, an arrow of $Q$ from $F(x)$ to $F(y)$ is exhibited, and the conclusion $F(x) \le F(y)$ is drawn from its existence.
- [ ] (b), existence: $F$ is defined on arrows as well as objects; the definition uses the hypothesis that $\varphi$ is order-preserving; preservation of composition and of identities are each verified with a reason.
- [ ] (b), uniqueness: two functors with the same function on objects are shown to agree on every arrow.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Part (a) is a direct proof that unpacks "functor" and "the category of a poset". Part (b) is an
existence-and-uniqueness statement, so it needs two separate arguments (0C). In both parts,
translate between "$x \le y$" and "there is an arrow $x \to y$" at every opportunity.

</details>

<details>
<summary>Hint 2 — part (a)</summary>

A functor does something to every arrow. If $x \le y$, which arrow can you feed to $F$, and
between which objects of $Q$ does the definition of a functor say the result lies?

</details>

<details>
<summary>Hint 3 — part (b)</summary>

For an arrow $x \to y$ of $P$, how many arrows of $Q$ are there that $F$ could send it to, and
what guarantees there is at least one? Then recall how Proposition 5.1 of 1A proved the
axioms of a category for a preorder: what was the one fact about hom-sets that made every
equation hold?

</details>

## Check yourself

- In (b), where exactly did you use that $\varphi$ is order-preserving? If nowhere, the definition of $F$ on arrows is incomplete.
- Did you verify both functor axioms, even if each took one line?
- Did you use antisymmetry anywhere? Would the statement still be true for preorders?
- What is a *contravariant* functor from $P$ to $Q$ in these terms?

## Write it up

Write your proof in `proofs/1c/p01_functors_between_posets.md`, then ask Claude to review it.
