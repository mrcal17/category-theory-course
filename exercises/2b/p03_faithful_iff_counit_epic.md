# 2B·P03 — A right adjoint is faithful exactly when the counit is epic

**Type:** core · **Technique:** translating a property through the transpose · **Unlocked by:** `2b_units_counits` §2
**Source:** adapted from Leinster §2.2

## Statement

Let $F \colon \mathcal{A} \to \mathcal{B}$ and $G \colon \mathcal{B} \to \mathcal{A}$ be
functors with $F \dashv G$ and counit $\varepsilon$. Prove that $G$ is faithful if and only if
$\varepsilon_B \colon FG(B) \to B$ is an epimorphism for every object $B$ of $\mathcal{B}$.

## What you may use

- From 1C: $G$ is *faithful* if for all objects $B, B'$ and all arrows $h, h' \colon B \to B'$,
  $G(h) = G(h')$ implies $h = h'$.
- From 1B: an arrow $e \colon X \to B$ is an *epimorphism* if for all objects $B'$ and all arrows
  $h, h' \colon B \to B'$, $h \circ e = h' \circ e$ implies $h = h'$.
- Lemma 2 of the lecture, naturality of $\varepsilon$ (2B §2), and the fact that
  transposition is a bijection.

## What a complete proof must show

- [ ] Both definitions are written out with their quantifiers before any argument begins.
- [ ] A precise relationship is established between the arrow $G(h)$ of $\mathcal{A}$ and the arrow $h \circ \varepsilon_B$ of $\mathcal{B}$, for an arbitrary $h \colon B \to B'$.
- [ ] Both directions of the "if and only if" are proved (or a single chain of equivalences is given, with each "iff" individually justified).
- [ ] It is clear where the bijectivity of transposition is used.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Put the two definitions side by side. Each is of the form "for all $h, h' \colon B \to B'$:
(some equation) implies $h = h'$". So the whole task is to compare the two *hypotheses*: the
equation $G(h) = G(h')$ and the equation $h \circ \varepsilon_B = h' \circ \varepsilon_B$.

</details>

<details>
<summary>Hint 2 — two categories</summary>

One of the two equations lives in $\mathcal{A}$ and the other in $\mathcal{B}$. Which is which?
What is the one device an adjunction gives you for carrying an arrow, and hence an equation
between arrows, from one of these categories to the other?

</details>

<details>
<summary>Hint 3 — where to look in the lecture</summary>

You do not have to compute anything new. One of the proofs in 2B §2 already contains a line
relating an arrow built from $G(q)$ to an arrow built from $q$ and a component of
$\varepsilon$. Find that line and decide what it lets you say here. Then ask which property of
the device from Hint 2 turns a statement about single arrows into the "if and only if" you need.

</details>

## Check yourself

- Did you prove both directions, and did each use the full "for every $B$ and $B'$" quantification?
- Test on the free monoid adjunction: is $U \colon \mathbf{Mon} \to \mathbf{Set}$ faithful, and is "multiply out a word" surjective? Test on $D \dashv U$ for topological spaces too.
- Test on a Galois connection: every functor between posets is faithful. Is every arrow in a poset epic?
- State the dual result about the left adjoint $F$ and the unit $\eta$. Which notion from 1B replaces "epimorphism"?

## Write it up

Write your proof in `proofs/2b/p03_faithful_iff_counit_epic.md`, then ask Claude to review it.
