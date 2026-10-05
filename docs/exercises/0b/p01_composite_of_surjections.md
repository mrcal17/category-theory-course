# 0B·P01 — A composite of surjections is a surjection

**Type:** warm-up · **Technique:** unpack the definition (direct proof) · **Unlocked by:** `0b_proof_toolkit_definitions` §4
**Source:** adapted from Hammack Ch 12

## Statement

Let $f \colon A \to B$ and $g \colon B \to C$ be functions. Prove that if $f$ and $g$ are both
surjective, then $g \circ f \colon A \to C$ is surjective.

## What you may use

- The definitions of function, composite and surjective (0B §1, §3, §4).
- Nothing else is needed. In particular you do not need Proposition 3, although it is a good
  model for the layout.

## What a complete proof must show

- [ ] The Goal is written with its quantifiers: which set the "for every" ranges over and which
      set the "there exists" ranges over.
- [ ] The element introduced in the first line is arbitrary: nothing is assumed about it beyond
      the set it belongs to.
- [ ] Each of the two hypotheses is used, and the proof says to which element each is applied.
- [ ] A witness is named and the required equation for it is verified, citing the definition of
      composite.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

The thing to be proved is the definition of "surjective" for the function $g \circ f$. That
definition is a "for every ... there exists ..." statement, so 0B §2 tells you the first sentence
of the proof and tells you what kind of object you must produce by the end. Write those down
before anything else.

</details>

<details>
<summary>Hint 2 — which hypothesis first?</summary>

After the first sentence you are holding one element. Which set does it live in? Each hypothesis
is a "for every" statement about the elements of one particular set. Only one of the two
hypotheses can be applied to what you are holding.

</details>

<details>
<summary>Hint 3 — the second step</summary>

Applying a "there exists" hypothesis hands you a new element (give it a fresh letter). Which set
does *that* one live in, and which hypothesis talks about that set? Compare the order in which
the hypotheses get used with the order in the proof of Proposition 3.

</details>

## Check yourself

- Is your witness an element of $A$? Did you verify an equation, or only assert it?
- Did the witness depend on the element you started with? Should it?
- In Proposition 3 the hypothesis on $g$ was used first. Here, which was used first, and why is
  the order different?

## Write it up

Write your proof in `proofs/0b/p01_composite_of_surjections.md`, then ask Claude to review it.
