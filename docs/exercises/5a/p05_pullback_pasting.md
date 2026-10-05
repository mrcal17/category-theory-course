# 5A·P05 — The pullback pasting lemma

**Type:** core · **Technique:** existence and uniqueness, twice · **Unlocked by:** `5a_limits` §3, §5
**Source:** adapted from Leinster §5.1; see also Riehl §3.1

## Statement

In a category $\mathcal{A}$, consider a diagram made of two squares side by side:

```
A ---a---> B ---b---> C
|          |          |
u          v          w
v          v          v
D ---d---> E ---e---> F
```

Suppose both squares commute ($v a = d u$ and $w b = e v$) and suppose the **right-hand square**
is a pullback (that is, $(B, v, b)$ is a pullback of $(e, w)$).

Prove that the **left-hand square** is a pullback if and only if the **outer rectangle** is a
pullback. Here the outer rectangle is the square with top edge $b a \colon A \to C$, left edge
$u$, right edge $w$ and bottom edge $e d \colon D \to F$.

## What you may use

- The definition of a pullback (5A §3).
- The axioms of a category.
- The fact, from Proof 4 of the lecture read for a pullback, that two maps into a pullback
  object are equal as soon as they have the same composite with both projections. (If you use
  it, say for which pullback.)

## What a complete proof must show

- [ ] The outer rectangle commutes (needed before it can be a pullback at all).
- [ ] Direction 1 (left square a pullback $\Rightarrow$ rectangle a pullback): for arbitrary test
      data for the rectangle, existence of the mediating map into $A$, and separately its
      uniqueness.
- [ ] Direction 2 (rectangle a pullback $\Rightarrow$ left square a pullback): likewise,
      existence and uniqueness, separately.
- [ ] Each time a pullback property is used, it is stated *which* square's property it is and
      that the test data satisfy that square's commuting condition.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

There are four small tasks: two directions, each with an existence half and a uniqueness half.
Write the four headings first. For each one, write down the test data you are *given* and the
map you must *produce or compare*. Keep a list of which squares you currently know to be
pullbacks; you may use the universal property of those and of no others.

</details>

<details>
<summary>Hint 2 — direction 1</summary>

Test data for the rectangle are a map into $D$ and a map into $C$. The left square, however,
wants a map into $D$ and a map into $B$. You do not have a map into $B$ yet. Which pullback
could manufacture one for you, and what test data would you feed it?

</details>

<details>
<summary>Hint 3 — direction 2</summary>

Now the test data are a map into $D$ and a map into $B$, and the pullback you may use is the
rectangle, which wants a map into $D$ and a map into $C$. Getting test data for the rectangle
is not hard. The difficulty comes afterwards: the rectangle's mediating map $g$ satisfies an
equation involving $b a g$, but you need one involving $a g$. How do you prove two maps into
$B$ are equal?

</details>

<details>
<summary>Hint 4 — uniqueness, both times</summary>

In each uniqueness half, start from "let $g'$ be another map satisfying the two equations".
Show that $g'$ also satisfies the equations that characterise the mediating map of the square
whose universal property you used for existence. Then that square's uniqueness clause finishes
the job.

</details>

## Check yourself

- Where did you use that the right-hand square is a pullback in direction 1? In direction 2?
- Did you verify the commuting condition every time before invoking a universal property?
- The lemma is false if "right-hand" and "left-hand" are exchanged in the hypothesis. You are
  not asked for a counterexample, but which step of your proof would break?

## Write it up

Write your proof in `proofs/5a/p05_pullback_pasting.md`, then ask Claude to review it.
