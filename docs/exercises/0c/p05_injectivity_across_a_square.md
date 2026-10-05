# 0C·P05 — Carrying injectivity across a commutative square

**Type:** core · **Technique:** diagram chase (element chase) · **Unlocked by:** `0c_proof_toolkit_uniqueness` §5, §6
**Source:** adapted from Riehl §1.6

## Statement

Let $f \colon A \to B$, $f' \colon A' \to B'$, $a \colon A \to A'$ and $b \colon B \to B'$ be
functions forming a commutative square:

$$b \circ f = f' \circ a.$$

Suppose that $a$ is surjective and that $f$ and $b$ are injective. Prove that $f'$ is injective.

## What you may use

- The definitions of injective, surjective and composite (0B §3, §4).
- The hypothesis that the square commutes, used as an equation of functions that may be
  evaluated at any element of $A$.
- Nothing about inverses: $a$ is not assumed to be invertible.

## What a complete proof must show

- [ ] The square is drawn, and the Goal is the definition of injectivity for $f'$, with the set
      its elements come from named.
- [ ] Wherever a "there exists" hypothesis is used, the chosen elements get fresh, distinct
      letters, and nothing is assumed about them beyond what the hypothesis gives.
- [ ] The step that switches from one path of the square to the other cites commutativity.
- [ ] Each of the three hypotheses (on $a$, on $f$, on $b$) is used, and the proof says where.
- [ ] The last line is the equality of the two elements introduced in the first line.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

An element chase. The first and last lines are dictated by the definition of "$f'$ is
injective", so write them first. Mark on your drawing of the square which corner your two
elements live in, and which corner the equation you are given lives in.

</details>

<details>
<summary>Hint 2 — getting onto the top row</summary>

The injectivity hypotheses are about $f$ and $b$, which act on elements of $A$ and $B$. Your
elements are not in either of those sets. One hypothesis lets you trade an element for one that
lies further back along an arrow. What precisely does it give you, and what does it *not* tell
you about the elements you get?

</details>

<details>
<summary>Hint 3 — around the square</summary>

Rewrite the equation you were given in terms of your new elements. It now describes one path
around the square. What does commutativity let you replace it with? You then have an equation to
which an injectivity hypothesis applies; after using it, look at what you have and see whether
the other one applies.

</details>

<details>
<summary>Hint 4 — landing</summary>

The chase ends with an equation between elements of $A$, but the goal is an equation between
elements of $A'$. How were your elements of $A$ related to the ones you started with? Applying a
function to equal inputs gives equal outputs.

</details>

## Check yourself

- Mark on the square the route your elements took. Did they ever travel against an arrow without
  a hypothesis that permits it?
- Find the one place where surjectivity of $a$ is used. Then look for a commutative square in
  which $f$ and $b$ are injective, $a$ is not surjective, and $f'$ is not injective (the empty
  set is allowed).
- Did you use injectivity of $b$ before injectivity of $f$, or after? Could it be the other way
  round?

## Write it up

Write your proof in `proofs/0c/p05_injectivity_across_a_square.md`, then ask Claude to review it.
