# 5B·P01 — A union is a pushout

**Type:** warm-up · **Technique:** universal-property proof in Set · **Unlocked by:** `5b_colimits` §4
**Source:** adapted from Leinster §5.2

## Statement

Let $A$ and $B$ be subsets of a set $U$. Let $s \colon A \cap B \to A$, $t \colon A \cap B \to B$,
$j_1 \colon A \to A \cup B$ and $j_2 \colon B \to A \cup B$ be the inclusion functions.

Prove, directly from the definition of pushout, that

```
A ∩ B ---t---> B
  |            |
  s            j2
  v            v
  A  ---j1---> A ∪ B
```

is a pushout square in $\mathbf{Set}$.

## What you may use

- The definition of a pushout (5B §4).
- Basic facts about functions and subsets from 0B.
- Do **not** quote the general formula for colimits in $\mathbf{Set}$ (5B §5) or the Lemma on maps
  out of a quotient. No quotient is needed here; the point is to run the argument by hand.

## What a complete proof must show

- [ ] The square commutes.
- [ ] For arbitrary test data (a set $C$ and functions $f_1 \colon A \to C$, $f_2 \colon B \to C$
      with $f_1 s = f_2 t$): a function $\bar{f} \colon A \cup B \to C$ is defined, and it is
      shown to be **well defined**.
- [ ] $\bar{f} j_1 = f_1$ and $\bar{f} j_2 = f_2$.
- [ ] Uniqueness of $\bar{f}$, as a separate step.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Follow the four-step checklist for a pushout. Think back to your proof of 3A·P03 (functions
out of a sum): there, too, a function out of a union of two pieces had to be defined. What is
different here about the two pieces?

</details>

<details>
<summary>Hint 2 — the danger</summary>

A definition by cases is only a definition if the cases never disagree. Which elements of
$A \cup B$ fall under both cases?

</details>

<details>
<summary>Hint 3 — using the hypothesis</summary>

Evaluate the hypothesis $f_1 \circ s = f_2 \circ t$ at an element $x \in A \cap B$, remembering
that $s$ and $t$ are inclusions. What does the resulting equation say, and which checklist item
does it settle?

</details>

## Check yourself

- Where did you use $f_1 s = f_2 t$? If nowhere, your $\bar{f}$ may not be a function.
- Which property of $j_1$ and $j_2$ together did the uniqueness half use?
- If $A \cap B = \varnothing$, which statement from 5B §2 do you recover?

## Write it up

Write your proof in `proofs/5b/p01_union_is_pushout.md`, then ask Claude to review it.
