# 0B·P05 — Invertible means bijective

**Type:** core · **Technique:** if-and-only-if; constructing a function and checking it is well defined · **Unlocked by:** `0b_proof_toolkit_definitions` §6, §7
**Source:** adapted from Hammack Ch 12 and Leinster §3.1

## Statement

Let $f \colon A \to B$ be a function. Prove that $f$ is invertible if and only if $f$ is
bijective.

(Recall: $f$ is *invertible* if there exists a function $k \colon B \to A$ with
$k \circ f = 1_A$ and $f \circ k = 1_B$.)

## What you may use

- The definitions of function, injective, surjective, bijective, invertible (0B §1, §4, §6).
- Proposition 4(a) of 0B, and anything you have already proved in P01 to P04.
- You may **not** assume $A$ is non-empty; the statement is for all sets $A$ and $B$.

## What a complete proof must show

- [ ] The two directions are proved separately and labelled, each with its own Goal and Given.
- [ ] ($\Rightarrow$) Both injectivity and surjectivity are established, and the proof says which
      of the two equations satisfied by $k$ is used for each.
- [ ] ($\Leftarrow$) A rule $k$ is defined on all of $B$, and the three items of the function
      checklist (0B §1) are verified for it.
- [ ] ($\Leftarrow$) The proof says exactly where surjectivity of $f$ is used and where
      injectivity of $f$ is used.
- [ ] ($\Leftarrow$) Both equations $k \circ f = 1_A$ and $f \circ k = 1_B$ are verified as
      equalities of functions.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

An "if and only if": two proofs. In ($\Rightarrow$) you are *given* a function $k$ and two
equations, and must verify two definitions. In ($\Leftarrow$) you are given two properties of
$f$ and must *build* a function; that is an existence proof, so the heart of it is a
construction followed by checks.

</details>

<details>
<summary>Hint 2 — the forward direction</summary>

Half of ($\Rightarrow$) is already a result in the lecture. For the other half you start with an
element of $B$ and need an element of $A$. You have exactly one function that goes from $B$ to
$A$.

</details>

<details>
<summary>Hint 3 — the construction</summary>

In ($\Leftarrow$), fix $b \in B$. What do you want $k(b)$ to be, in words? Now run the function
checklist on that description: which hypothesis on $f$ guarantees that there is at least one
candidate value, and which guarantees that there is at most one? Compare with the construction
in Proposition 4(b): what is different about the two cases there, and why does one of them
disappear here?

</details>

<details>
<summary>Hint 4 — the two equations</summary>

One of the two equations follows directly from the sentence that defines $k(b)$. For the other,
you need to identify the value of $k$ at an element of the form $f(a)$. Your definition
characterises that value by a property. Which element of $A$ visibly has that property?

</details>

## Check yourself

- Does your construction quietly choose an arbitrary element of $A$ anywhere? If $A = \emptyset$
  and $f$ is bijective, what must $B$ be, and does your proof still make sense?
- Did you check that $k$ is a function *before* computing with it?
- Find, in your ($\Leftarrow$) proof, the one sentence that uses injectivity and the one that
  uses surjectivity.

## Write it up

Write your proof in `proofs/0b/p05_invertible_iff_bijective.md`, then ask Claude to review it.
