# 2B·P05 — Unit and counit of a composite adjunction

**Type:** core · **Technique:** triangle identities · **Unlocked by:** `2b_units_counits` §5
**Source:** adapted from Leinster §2.2 and Riehl §4.4

## Statement

Let $F \colon \mathcal{A} \to \mathcal{B}$, $G \colon \mathcal{B} \to \mathcal{A}$ with
$F \dashv G$, unit $\eta$ and counit $\varepsilon$; and let
$F' \colon \mathcal{B} \to \mathcal{C}$, $G' \colon \mathcal{C} \to \mathcal{B}$ with
$F' \dashv G'$, unit $\eta'$ and counit $\varepsilon'$. For each object $A$ of $\mathcal{A}$ and
$C$ of $\mathcal{C}$ define

$$\eta''_A = G(\eta'_{F(A)}) \circ \eta_A, \qquad
\varepsilon''_C = \varepsilon'_C \circ F'(\varepsilon_{G'(C)}).$$

1. Check that $\eta''_A$ is an arrow $A \to GG'F'F(A)$ and $\varepsilon''_C$ is an arrow
   $F'FGG'(C) \to C$.
2. Prove that $\eta''$ is a natural transformation $1_{\mathcal{A}} \Rightarrow GG'F'F$.
3. Prove both triangle identities for the pair $(\eta'', \varepsilon'')$ and the functors
   $F'F$ and $GG'$.

You may take for granted that $\varepsilon''$ is natural (the argument mirrors part 2). By
Theorem 4 your work shows $F'F \dashv GG'$ with unit $\eta''$ and counit $\varepsilon''$, giving
a second proof of 2A·P04.

## What you may use

- Naturality of $\eta$, $\varepsilon$, $\eta'$, $\varepsilon'$ and the triangle identities of the
  two given adjunctions.
- Functoriality of $F$, $G$, $F'$, $G'$.
- Not 2A·P04, and not the hom-set bijections: this is to be done entirely with units and
  counits.

## What a complete proof must show

- [ ] Domains and codomains in part 1 are computed step by step.
- [ ] In part 2, the naturality square for $\eta''$ at an arrow $p \colon A' \to A$ is written down, and each step cites the naturality of a named transformation at a named arrow.
- [ ] In part 3, each triangle identity is stated for the composite functors with all subscripts in place, then proved.
- [ ] Every equality in part 3 is justified by exactly one of: functoriality (named functor), naturality (named transformation, named arrow), a triangle identity (named adjunction, which of the two).

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Part 3 is a calculation with long composites. The model is the round-trip computation in
Theorem 4: split with functoriality, slide with one naturality square, cancel with one
triangle identity. Here you will cancel twice, once for each given adjunction, and the order
in which the cancellations become available matters.

</details>

<details>
<summary>Hint 2 — set it up before calculating</summary>

Write the first triangle identity for $(F'F, GG', \eta'', \varepsilon'')$ with the definitions
substituted. You should see a composite of four arrows. Use functoriality of $F'$ to gather
the three of them that are "$F'$ of something" into $F'$ of a single composite in
$\mathcal{B}$.

</details>

<details>
<summary>Hint 3 — the composite inside</summary>

Inside that $F'(\ldots)$ you have a composite of three arrows of $\mathcal{B}$, in which a
component of $\varepsilon$ is applied immediately after $FG$ of some arrow. That pair is one
side of a naturality square for $\varepsilon$. At which arrow? After sliding, look at the two
arrows that have become neighbours.

</details>

<details>
<summary>Hint 4 — the second identity and part 2</summary>

The second triangle identity runs the same way with the roles of the two adjunctions
exchanged: gather under $G$, slide using naturality of $\eta'$, cancel the inner pair, then
the outer. For part 2, the square for $\eta''$ is two squares side by side: one is a naturality
square of $\eta$, the other is $G$ applied to a naturality square of $\eta'$. At which arrow of
$\mathcal{B}$?

</details>

## Check yourself

- In part 3, did the adjunction $F \dashv G$ get cancelled first or last in the first identity? And in the second?
- Did you ever apply a triangle identity "inside" a functor? If so, did you say which functor preserved the resulting identity arrow?
- Sanity check with posets: if $a \le g(f(a))$ and $b \le g'(f'(b))$, what inequality is $\eta''_a$?
- For the free abelian group on a set, built as abelianization after free group: describe $\eta''_S$ in words.

## Write it up

Write your proof in `proofs/2b/p05_composite_unit_counit.md`, then ask Claude to review it.
