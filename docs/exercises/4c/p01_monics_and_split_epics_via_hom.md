# 4C·P01 — Monics and split epics through $H_f$

**Type:** warm-up · **Technique:** unpacking definitions; follow the identity · **Unlocked by:** `4c_yoneda_consequences` §2, §3
**Source:** adapted from Riehl §2.2

## Statement

Let $f \colon A \to B$ be an arrow of a locally small category $\mathcal{A}$, and recall the natural
transformation $H_f \colon H_A \Rightarrow H_B$ with components

$$(H_f)_C \colon \mathcal{A}(C, A) \to \mathcal{A}(C, B), \qquad p \mapsto f \circ p .$$

Prove:

1. $f$ is monic if and only if $(H_f)_C$ is injective for every object $C$.
2. $f$ has a right inverse (an arrow $s \colon B \to A$ with $f \circ s = 1_B$) if and only if
   $(H_f)_C$ is surjective for every object $C$.

## What you may use

- The definition of a monic arrow from 1B: $f$ is monic when, for every object $C$ and all
  $p, q \colon C \to A$, $f \circ p = f \circ q$ implies $p = q$.
- The definitions of injective and surjective functions (0B).
- The axioms of a category.

## What a complete proof must show

- [ ] Each of the two statements is proved in both directions, and the directions are labelled.
- [ ] In part 1, the two definitions being compared are written side by side with their quantifiers.
- [ ] In part 2, the direction "surjective for every $C$ implies a right inverse" says *which*
      object $C$ and *which* element of $\mathcal{A}(C, B)$ the hypothesis is applied to.
- [ ] In part 2, the other direction produces, for an arbitrary $q \in \mathcal{A}(C, B)$, an
      explicit preimage and verifies that it is one.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Part 1 is a comparison of two definitions: write out "$(H_f)_C$ is injective for every $C$" in
full, with no abbreviations, and put it next to the definition of monic. Part 2 has one easy
direction (direct) and one direction where you must choose where to use a "for every $C$"
hypothesis.

</details>

<details>
<summary>Hint 2 — part 2, from a right inverse</summary>

Given $s$ with $f \circ s = 1_B$ and an arbitrary $q \colon C \to B$, you need some
$p \colon C \to A$ with $f \circ p = q$. You have exactly two arrows available to build $p$ from.

</details>

<details>
<summary>Hint 3 — part 2, to a right inverse</summary>

The hypothesis holds for every object $C$, so you are free to choose $C$. A right inverse is an
arrow into $A$ whose composite with $f$ is a specific arrow. Of which hom-set $\mathcal{A}(C, B)$
is that specific arrow an element? This is the same move as following the identity in the
Yoneda lemma.

</details>

## Check yourself

- Did part 1 need any idea at all, or was it a restatement? Say so in your proof if it was.
- "Epic" is not the same as "has a right inverse". Which of the two does part 2 characterize, and
  can you name an epic in some category with no right inverse?
- Combine parts 1 and 2 with Corollary 3.3(b) of the lecture. What do you learn about an arrow
  that is monic and has a right inverse?

## Write it up

Write your proof in `proofs/4c/p01_monics_and_split_epics_via_hom.md`, then ask Claude to review it.
