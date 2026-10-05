# 0B·P02 — Left inverses compose, in the opposite order

**Type:** warm-up · **Technique:** equality of functions from associativity and identity laws · **Unlocked by:** `0b_proof_toolkit_definitions` §3, §6
**Source:** adapted from Leinster §3.1

## Statement

Let $f \colon A \to B$ and $g \colon B \to C$ be functions. Suppose $f' \colon B \to A$ is a left
inverse of $f$ and $g' \colon C \to B$ is a left inverse of $g$. Prove that $f' \circ g'$ is a
left inverse of $g \circ f$.

## What you may use

- The definition of left inverse (0B §6).
- Proposition 2 of 0B: associativity of composition and the identity laws.
- You may argue with elements if you wish, but the statement can be proved without mentioning
  any element, and that is the version worth practising.

## What a complete proof must show

- [ ] It says what the domain and codomain of $f' \circ g'$ are, and that the composites being
      formed are defined.
- [ ] The Goal is written as a single equation between two functions, with the domain and
      codomain of both sides stated.
- [ ] Every equality in the argument is justified by name: associativity, an identity law, or
      one of the two hypotheses.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Unpack "is a left inverse of" for the pair in the conclusion. You get one equation between
functions. Unpack it for each hypothesis too: two more equations. The proof is a calculation
that starts at one side of the goal and reaches the other, and Proposition 2 of 0B supplies the
only rules you need.

</details>

<details>
<summary>Hint 2 — where to look</summary>

One side of the goal is a composite of four functions in a row. Write them out as a chain of
sets and arrows. The hypotheses each speak about a composite of *two* functions. Is either of
those two-function composites sitting somewhere in your chain?

</details>

<details>
<summary>Hint 3 — making it visible</summary>

Brackets decide which pairs are composed first, and one law lets you move brackets. After you
have used a hypothesis, something appears in the chain that another law removes. What remains
then?

</details>

## Check yourself

- Why is it $f' \circ g'$ and not $g' \circ f'$? Is $g' \circ f'$ even defined in general?
- Count your uses of associativity. Did you state each one, or slide past it by dropping
  brackets?
- Does your proof use anything about $A$, $B$, $C$ being sets? Keep the answer in mind for
  Module 1B.

## Write it up

Write your proof in `proofs/0b/p02_left_inverses_compose.md`, then ask Claude to review it.
