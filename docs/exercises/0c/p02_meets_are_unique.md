# 0C·P02 — Greatest lower bounds are unique

**Type:** warm-up · **Technique:** uniqueness from antisymmetry · **Unlocked by:** `0c_proof_toolkit_uniqueness` §3
**Source:** adapted from Leinster §5.1 (meets in a poset)

## Statement

Let $P$ be a poset and let $a, b \in P$. An element $x \in P$ is a *lower bound* of $a$ and $b$
if $x \le a$ and $x \le b$. An element $m \in P$ is a *greatest lower bound* (or *meet*) of $a$
and $b$ if

1. $m$ is a lower bound of $a$ and $b$, and
2. for every lower bound $x$ of $a$ and $b$, we have $x \le m$.

Prove that if $m$ and $m'$ are both greatest lower bounds of $a$ and $b$, then $m = m'$.

## What you may use

- The definition of a poset: reflexivity, transitivity, antisymmetry (0C §3).
- The two definitions in the statement.
- Proposition 4 of 0C as a model, but not as a result: this is a different statement.

## What a complete proof must show

- [ ] The Goal and Given are written out: what is assumed about $m$, and what about $m'$ (two
      conditions each).
- [ ] Each use of condition 2 says which candidate's condition it is and which element it is
      being applied to, and checks that this element is a lower bound.
- [ ] The poset axiom that produces the final equality is named.
- [ ] The proof does not claim that a greatest lower bound exists.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

This is a pure uniqueness statement of the "two candidates" kind, with the same outline as
Proposition 4. There is no existence part.

</details>

<details>
<summary>Hint 2 — using the definition</summary>

Each candidate satisfies two conditions. Condition 2 is a "for every lower bound $x$" statement,
so you may apply it to any lower bound you can get your hands on. Which lower bounds of $a$ and
$b$ do the hypotheses give you?

</details>

<details>
<summary>Hint 3 — finishing</summary>

You should arrive at two inequalities between the candidates. Which axiom of a poset converts
two inequalities into an equality?

</details>

## Check yourself

- Did you use condition 1 for both candidates and condition 2 for both candidates? Where?
- In the Compute It poset $\{2, 3, 12, 18\}$ under divisibility, $12$ and $18$ have lower bounds
  but no greatest lower bound. Is that consistent with what you proved?
- If $P$ were only a preorder, which line of your proof would fail, and what would the earlier
  lines still tell you about $m$ and $m'$?

## Write it up

Write your proof in `proofs/0c/p02_meets_are_unique.md`, then ask Claude to review it.
