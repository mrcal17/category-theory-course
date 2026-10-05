# 2A·P04 — Adjunctions compose

**Type:** core · **Technique:** naturality of a bijection · **Unlocked by:** `2a_adjunctions` §1
**Source:** adapted from Leinster §2.1

## Statement

Let $F \colon \mathcal{A} \to \mathcal{B}$ and $G \colon \mathcal{B} \to \mathcal{A}$ be
functors with $F \dashv G$, and let $F' \colon \mathcal{B} \to \mathcal{C}$ and
$G' \colon \mathcal{C} \to \mathcal{B}$ be functors with $F' \dashv G'$. Prove that

$$F' \circ F \;\dashv\; G \circ G' .$$

## What you may use

- The definition of an adjunction, for each of the two given adjunctions.
- That a composite of bijections is a bijection, and that composites of functors are functors.

## What a complete proof must show

- [ ] For every object $A$ of $\mathcal{A}$ and $C$ of $\mathcal{C}$, a map $\mathcal{C}(F'F(A), C) \to \mathcal{A}(A, GG'(C))$ is defined, and it is explained why it is a bijection.
- [ ] (N1) is verified for the new bijection: for $h \colon F'F(A) \to C$ and $r \colon C \to C'$.
- [ ] (N2) is verified for the new bijection: for $p \colon A' \to A$ and $k \colon A \to GG'(C)$.
- [ ] Each step of the two verifications cites which naturality equation of which given adjunction is used.
- [ ] The notation distinguishes the three transposition operations (two given, one new).

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Run the checklist of 2A §1 for the pair $(F'F, GG')$. You are not asked to invent a bijection
from nothing: you have two, and there is an intermediate hom-set that both of them touch.

</details>

<details>
<summary>Hint 2 — the intermediate hom-set</summary>

An arrow $F'(F(A)) \to C$ has the form $F'(\text{object of } \mathcal{B}) \to C$. Which of the
given adjunctions applies to it, and in which hom-set does the result live? Is that hom-set of
a form the other adjunction can act on?

</details>

<details>
<summary>Hint 3 — notation that keeps you safe</summary>

Using one bar for everything will cause mistakes. Choose two different decorations for the two
given transpositions. In (N1) and (N2) for the new transposition you will then deal with the
two decorations one at a time.

</details>

<details>
<summary>Hint 4 — the naturality checks</summary>

For (N1) with $r \colon C \to C'$: one of the given transpositions is natural in $C$, and
turns post-composition with $r$ into post-composition with some other arrow. In which category
does that other arrow live, and which naturality equation of the *other* adjunction is designed
to handle post-composition by an arrow of that category? For (N2), ask the corresponding
question about pre-composition with $p$.

</details>

## Check yourself

- In your (N1) check, which arrow plays the role of "$q$" for the adjunction $F \dashv G$?
- In your (N2) check, which arrow plays the role of "$p$" for the adjunction $F' \dashv G'$?
- The right adjoint of $F'F$ came out as $GG'$, with the order reversed. Where in your proof was that order forced?
- Apply the result to $\mathbf{Set} \rightleftarrows \mathbf{Grp} \rightleftarrows \mathbf{Ab}$ (free group, then abelianization). What does it say?

## Write it up

Write your proof in `proofs/2a/p04_adjunctions_compose.md`, then ask Claude to review it.
