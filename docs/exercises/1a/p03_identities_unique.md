# 1A·P03 — Identities are unique

**Type:** core · **Technique:** uniqueness argument · **Unlocked by:** `1a_categories` §1
**Source:** adapted from Leinster §1.1

## Statement

Let $\mathcal{A}$ be a category and $A$ an object of $\mathcal{A}$. Suppose $e \colon A \to A$
is an arrow such that $f \circ e = f$ for every arrow $f$ with domain $A$, and $e \circ g = g$
for every arrow $g$ with codomain $A$. Prove that $e = 1_A$.

## What you may use

- The definition of a category (objects, arrows, composition, the associativity and identity axioms).
- Nothing about what the arrows of $\mathcal{A}$ "are" — they need not be functions.

## What a complete proof must show

- [ ] It says explicitly which two arrows are being shown equal.
- [ ] Every equality in the argument is justified by a named axiom or by the hypothesis on $e$.
- [ ] It never applies an arrow to an "element" — there are none.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

This is a uniqueness statement about something defined by how it composes with other arrows.
The standard move for those appeared in 0C: when two things both claim the same defining
property, look for a single expression that each of them simplifies in a different way.

</details>

<details>
<summary>Hint 2 — which expression?</summary>

You have two arrows $A \to A$ on the table. What is the only non-trivial thing a category lets
you do with two arrows whose domain and codomain match up?

</details>

<details>
<summary>Hint 3 — using both hypotheses</summary>

The hypothesis on $e$ quantifies over *every* arrow out of $A$ and every arrow into $A$. Which
specific arrow is worth plugging in? And what does the identity axiom say about that same
expression?

</details>

## Check yourself

- Did you use the hypothesis on $e$ exactly once, or did you need both halves of it?
- Would your proof still work in a category whose arrows are not functions (say, a poset)?
- Compare with the proof that a group has only one identity element. What is the same?

## Write it up

Write your proof in `proofs/1a/p03_identities_unique.md`, then ask Claude to review it.
