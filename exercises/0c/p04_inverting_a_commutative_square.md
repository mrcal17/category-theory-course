# 0C·P04 — Inverting the sides of a commutative square

**Type:** core · **Technique:** diagram chase (equation chase) · **Unlocked by:** `0c_proof_toolkit_uniqueness` §5, §6
**Source:** adapted from Riehl §1.6

## Statement

Let $f \colon A \to B$, $f' \colon A' \to B'$, $a \colon A \to A'$ and $b \colon B \to B'$ be
functions forming a commutative square:

$$b \circ f = f' \circ a.$$

Suppose $a$ and $b$ are invertible, with two-sided inverses $a^{-1} \colon A' \to A$ and
$b^{-1} \colon B' \to B$. Prove that the square obtained by reversing the two vertical arrows
also commutes:

$$f \circ a^{-1} = b^{-1} \circ f'.$$

## What you may use

- The definition of invertible function and two-sided inverse (0B §6): four equations in all,
  two for $a$ and two for $b$.
- Proposition 2 of 0B: associativity of composition and the identity laws.
- The hypothesis that the original square commutes.

## What a complete proof must show

- [ ] Both squares are drawn, and the Goal is stated as an equation between two functions with
      their common domain and codomain named.
- [ ] Every equality in the chase is justified: associativity, an identity law, one of the four
      inverse equations (say which), or the given square.
- [ ] The given square is used, and the proof says at which step.
- [ ] No element of any of the four sets appears.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

An equation chase in the style of Proposition 5: a chain of equalities between composites, each
justified by a law of composition or a given equation. You know nothing about what the four
functions do to elements, so elements cannot help.

</details>

<details>
<summary>Hint 2 — connecting the hypothesis to the goal</summary>

The hypothesis is an equation that mentions $a$ and $b$. The goal mentions $a^{-1}$ and
$b^{-1}$. If two functions are equal, then composing both with the same third function, on the
same side, gives equal functions. Which function, composed on which side of the hypothesis,
would make $b$ disappear from one side?

</details>

<details>
<summary>Hint 3 — and then</summary>

After the first move, one of the arrows of the goal is in place and $a$ is still in the way.
Repeat the idea on the other side. Keep track of which of the four inverse equations each
cancellation uses: you will not need all four.

</details>

## Check yourself

- Which two of the four inverse equations did you use? Would a left inverse of $b$ and a right
  inverse of $a$ have been enough?
- Did any step silently drop or move brackets? Each re-bracketing is a use of associativity.
- Your proof used only associativity, identity laws and given equations. Keep that in mind: it
  means the same proof will hold verbatim in any category (Module 1A).

## Write it up

Write your proof in `proofs/0c/p04_inverting_a_commutative_square.md`, then ask Claude to review it.
