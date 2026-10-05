# 5B·P06 — Pushouts of injections in Set

**Type:** stretch · **Technique:** choosing a test cocone · **Unlocked by:** `5b_colimits` §4, §5
**Source:** adapted from Leinster §5.2

## Statement

In $\mathbf{Set}$, let $s \colon Z \to X$ and $t \colon Z \to Y$ be functions, and let

```
Z ---t---> Y
|          |
s          j2
v          v
X ---j1--> Q
```

be a pushout square. Prove: if $s$ is injective, then $j_2$ is injective.

(Proof 6 of the lecture shows that pushouts carry epics to epics in every category. This
exercise is the corresponding statement for injections, and it is special to $\mathbf{Set}$:
your proof will have to use sets and elements somewhere.)

## What you may use

- The definition of a pushout (5B §4) and its universal property, for the given $Q$.
- Basic facts about injective functions from 0B, including: if a composite $g \circ j$ is
  injective, then $j$ is injective.
- Elementary set constructions (subsets, complements, disjoint unions).
- You may use the explicit formula for the pushout from 5B §4–§5 if you wish, but you are
  strongly advised not to: reasoning about zigzags is much harder than the route the hints
  suggest.

## What a complete proof must show

- [ ] A set $B$ and functions $g_1 \colon X \to B$, $g_2 \colon Y \to B$ are defined explicitly.
- [ ] $g_1$ is shown to be a well-defined function, and it is said where injectivity of $s$ is
      used.
- [ ] $g_1 \circ s = g_2 \circ t$ is verified.
- [ ] The universal property of the pushout is applied to this test data, and injectivity of
      $j_2$ is deduced from the resulting equations.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

There are two ways to show $j_2$ is injective. One is to describe $Q$ as a quotient and study
when two elements of $Y$ are joined by a zigzag. The other uses only the universal property:
a pushout maps to *every* commuting square. If you could find one commuting square in which
the map out of $Y$ is injective, what would the universal property tell you about $j_2$?

</details>

<details>
<summary>Hint 2 — what to look for</summary>

So you need a set $B$ and functions $g_1 \colon X \to B$, $g_2 \colon Y \to B$ with
$g_1 s = g_2 t$ and $g_2$ injective. The simplest way to make $g_2$ injective is to let $B$
contain $Y$. The equation $g_1 s = g_2 t$ then dictates the value of $g_1$ on some elements of
$X$. Which ones, and what value?

</details>

<details>
<summary>Hint 3 — is it a function?</summary>

Your answer to Hint 2 defines $g_1(x)$ for those $x$ of the form $s(z)$, in terms of $z$. For
that to be a definition, the value must not depend on which $z$ you picked. Why does it not?
This is where the hypothesis on $s$ enters.

</details>

<details>
<summary>Hint 4 — the leftovers</summary>

Elements of $X$ that are not of the form $s(z)$ are not constrained by the equation at all.
You still have to send them somewhere, so $B$ may need to be a little bigger than $Y$. Any
choice that makes $g_1$ a function will do; pick one and say what $B$ is.

</details>

## Check yourself

- Did you verify that $g_1$ is well defined before using it?
- Your proof should work for *any* pushout $Q$, not only the one given by the formula. Does it?
- Find a small example (two- or three-element sets) where $s$ is not injective and $j_2$ is not
  injective, to see that the hypothesis is needed.

## Write it up

Write your proof in `proofs/5b/p06_pushout_of_injection.md`, then ask Claude to review it.
