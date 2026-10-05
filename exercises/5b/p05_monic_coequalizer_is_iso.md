# 5B·P05 — A monic coequalizer is an isomorphism

**Type:** core · **Technique:** building an inverse from a universal property · **Unlocked by:** `5b_colimits` §3
**Source:** adapted from Leinster §5.2

## Statement

Let $\mathcal{A}$ be a category, let $s, t \colon X \to Y$ be maps in $\mathcal{A}$, and let
$q \colon Y \to C$ be a coequalizer of $s$ and $t$. Suppose that $q$ is also monic.

Prove that $q$ is an isomorphism.

## What you may use

- The definitions of coequalizer (5B §3), monic and epic (1B), and isomorphism (1B).
- From 5B §3: every coequalizer is epic.
- The axioms of a category. Nothing about elements.

## What a complete proof must show

- [ ] A map $r \colon C \to Y$ is produced, and the universal property used to produce it is
      applied to test data that have been checked to be legitimate.
- [ ] $r \circ q = 1_Y$, with a reason.
- [ ] $q \circ r = 1_C$, with a reason. (This is a separate equation and needs a separate
      argument.)
- [ ] It is clear where the hypothesis "monic" is used and where "coequalizer" is used.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

To prove a map is an isomorphism you must produce an inverse and check two equations. The only
tool you have for producing maps *out of* $C$ is the universal property of the coequalizer, and
it needs a map out of $Y$ that makes $s$ and $t$ agree.

</details>

<details>
<summary>Hint 2 — two hypotheses on one map</summary>

You have two hypotheses on $q$, and the universal property by itself uses only one of them.
Write down the one equation you already know that involves $q$, $s$ and $t$ together. What
does the other hypothesis do to an equation of that form?

</details>

<details>
<summary>Hint 3 — feeding the universal property</summary>

The universal property turns certain maps out of $Y$ into maps out of $C$. After Hint 2, how
restrictive is the condition those maps must satisfy? Write down the equation you want a
candidate inverse to satisfy and compare its shape with the equation in the definition.

</details>

<details>
<summary>Hint 4 — the other composite</summary>

The second equation is an equality between two maps out of $C$. "What you may use" contains a
statement about exactly that kind of equality. What would you need to know first in order to
apply it?

</details>

## Check yourself

- Did you prove both $r q = 1_Y$ and $q r = 1_C$?
- In $\mathbf{Set}$, a coequalizer is a quotient map. What does your theorem say about a
  quotient map that is injective?
- State the dual theorem (about an equalizer that is epic). Which results of 5A would its
  proof quote?

## Write it up

Write your proof in `proofs/5b/p05_monic_coequalizer_is_iso.md`, then ask Claude to review it.
