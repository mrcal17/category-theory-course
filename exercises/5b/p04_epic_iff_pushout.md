# 5B·P04 — Epic if and only if a square is a pushout

**Type:** core · **Technique:** translating between two definitions · **Unlocked by:** `5b_colimits` §4, §6
**Source:** adapted from Leinster §5.2

## Statement

Let $f \colon X \to Y$ be a map in a category $\mathcal{A}$. Prove that $f$ is epic if and only
if the square

```
X ---f---> Y
|          |
f          1_Y
v          v
Y --1_Y--> Y
```

is a pushout square. In the notation of 5B §4: the two maps being pushed out are $s = f$ and
$t = f$ (both $X \to Y$), the candidate pushout object is $Q = Y$, and the candidate
coprojections are $j_1 = j_2 = 1_Y$.

Write a **direct** proof in $\mathcal{A}$. Do not deduce the result from 5A·P04 by duality (you
may, afterwards, compare the two).

## What you may use

- The definition of a pushout (5B §4) and of epic (1B).
- The axioms of a category.
- Nothing about elements, and not Proof 6 of the lecture (it concerns a different square).

## What a complete proof must show

- [ ] Two directions, each under its own heading.
- [ ] In "epic $\Rightarrow$ pushout": the square commutes; for arbitrary test data
      $(A, f_1, f_2)$ with $f_1 f = f_2 f$, existence of a mediating map and its uniqueness are
      each proved.
- [ ] In "pushout $\Rightarrow$ epic": arbitrary $h, k \colon Y \to A$ with $h f = k f$ are
      fixed, and the pushout property is applied to explicitly named test data.
- [ ] Composites are written in the correct order throughout (maps go *out of* $Y$ here).

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Substitute $j_1 = j_2 = 1_Y$ into the definition of pushout and simplify the identities away.
Write the definition of epic next to it. Compare the two statements before proving anything.

</details>

<details>
<summary>Hint 2 — epic implies pushout</summary>

Test data are $f_1, f_2 \colon Y \to A$ with $f_1 f = f_2 f$. What does the hypothesis on $f$
say about $f_1$ and $f_2$? After that, how much freedom do the equations
$\bar{f} \circ 1_Y = f_1$ and $\bar{f} \circ 1_Y = f_2$ leave?

</details>

<details>
<summary>Hint 3 — pushout implies epic</summary>

You are given $h, k$ with $h f = k f$. Test data for the pushout are an object and two maps
out of $Y$ satisfying one equation. What do you already have that fits? The universal property
then hands you a single map satisfying two equations. Read the two equations slowly.

</details>

## Check yourself

- Which half of the universal property (existence or uniqueness) did "pushout $\Rightarrow$
  epic" use?
- Lay your proof beside your proof of 5A·P04. Is each line the mirror image of a line there?
- In $\mathbf{Set}$, the pushout of $f$ along itself glues two copies of $Y$ along the image of
  $f$. What does your theorem say when $f$ is surjective?

## Write it up

Write your proof in `proofs/5b/p04_epic_iff_pushout.md`, then ask Claude to review it.
