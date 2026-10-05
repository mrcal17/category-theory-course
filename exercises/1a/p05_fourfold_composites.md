# 1A·P05 — Four-fold composites need no brackets

**Type:** core · **Technique:** chains of equalities justified by one axiom · **Unlocked by:** `1a_categories` §1
**Source:** adapted from a remark in Leinster §1.1

## Statement

Let $\mathcal{A}$ be a category and let

$$A \xrightarrow{f} B \xrightarrow{g} C \xrightarrow{h} D \xrightarrow{k} E$$

be arrows of $\mathcal{A}$. There are five ways to bracket the composite of all four:

$$((k \circ h) \circ g) \circ f, \quad (k \circ (h \circ g)) \circ f, \quad (k \circ h) \circ (g \circ f), \quad k \circ ((h \circ g) \circ f), \quad k \circ (h \circ (g \circ f)).$$

Prove that all five are equal.

## What you may use

- The associativity axiom, exactly as stated in the definition of a category: for composable
  $p, q, r$, $(r \circ q) \circ p = r \circ (q \circ p)$.
- The fact that composition is a function: if $p = p'$ then $r \circ p = r \circ p'$ and
  $p \circ s = p' \circ s$ whenever the composites are defined.
- Nothing else. In particular, not "associativity lets us drop brackets", which is what you
  are proving.

## What a complete proof must show

- [ ] Enough equalities between the five expressions to connect all of them.
- [ ] For each use of the axiom, the three arrows playing the roles of $p, q, r$ are named.
- [ ] Each instance of the axiom is applied to a composable triple (domains and codomains are stated).
- [ ] Where an equality is obtained by composing both sides of an earlier equality with another arrow, that is said.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

This is a direct proof made of single applications of one axiom. You do not need to compare
every pair of expressions. How few equalities are enough to conclude that five things are all
equal?

</details>

<details>
<summary>Hint 2 — the axiom applies to composites too</summary>

The associativity axiom is about *any* three composable arrows. Nothing stops one of the three
from being a composite of two of the original arrows. For a given bracketing, look at its
outermost $\circ$ and at what sits on either side of it: which three arrows could that
expression be one side of the axiom for?

</details>

<details>
<summary>Hint 3 — two kinds of step</summary>

Some pairs of bracketings differ in their outermost structure. Others have the same outermost
structure and differ only *inside* one factor. These need different treatment: one kind is a
single instance of the axiom, the other also needs the fact that composition is a function.
Sort the steps you plan to use into these two kinds before writing them out.

</details>

## Check yourself

- For each use of associativity, can you say which arrows are $p$, $q$, $r$?
- Did you ever write a composite of three or more arrows without brackets? If so, your proof assumes its conclusion.
- How many bracketings are there for five arrows, and what would the strategy be? (You are not asked to carry it out.)

## Write it up

Write your proof in `proofs/1a/p05_fourfold_composites.md`, then ask Claude to review it.
