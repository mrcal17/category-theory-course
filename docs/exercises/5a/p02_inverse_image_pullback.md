# 5A·P02 — The inverse image is a pullback

**Type:** warm-up · **Technique:** universal-property proof in Set · **Unlocked by:** `5a_limits` §3
**Source:** adapted from Leinster §5.1

## Statement

Let $s \colon X \to Z$ be a function between sets, let $U \subseteq Z$ be a subset, and let
$t \colon U \to Z$ be the inclusion. Put

$$s^{-1}(U) = \{x \in X : s(x) \in U\},$$

let $p_1 \colon s^{-1}(U) \to X$ be the inclusion, and let $p_2 \colon s^{-1}(U) \to U$ be the
function $p_2(x) = s(x)$.

Prove, directly from the definition of pullback, that

```
s^{-1}(U) --p2--> U
    |             |
    p1            t
    v             v
    X  ----s----> Z
```

is a pullback square in $\mathbf{Set}$.

## What you may use

- The definition of a pullback (5A §3).
- Basic facts about functions from 0B: two functions are equal when they agree on every element;
  inclusions are injective.
- Do **not** quote the general formula for limits in $\mathbf{Set}$ from 5A §6. The point is to
  run the argument by hand once.

## What a complete proof must show

- [ ] $p_2$ is a well-defined function into $U$.
- [ ] The square commutes.
- [ ] For arbitrary test data $(A, f_1, f_2)$ with $s f_1 = t f_2$: a mediating function is
      defined, shown to land in $s^{-1}(U)$, and shown to satisfy both equations.
- [ ] Uniqueness of the mediating function, as a separate step.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Follow the four-item checklist under "Reading the definition" in 5A §3, in that order. Model
your write-up on Proof 2 of the lecture (equalizers in $\mathbf{Set}$): there too the object
was a subset of $X$ and one of the maps was an inclusion.

</details>

<details>
<summary>Hint 2 — where the mediating map must go</summary>

The equation $p_1 \bar{f} = f_1$ already tells you what $\bar{f}(a)$ has to be, because $p_1$
is an inclusion. So the real question in the existence half is not "what is $\bar{f}$?" but
"why is that value allowed?".

</details>

<details>
<summary>Hint 3 — using the hypothesis</summary>

You are given $s \circ f_1 = t \circ f_2$. Evaluate both sides at an element $a \in A$ and
remember that $t$ is an inclusion. What does the resulting equation say about $s(f_1(a))$?
You will need this twice: once to see that $\bar f$ is well defined, and once for the second
of the two equations.

</details>

## Check yourself

- Where exactly did you use the hypothesis $s f_1 = t f_2$? If nowhere, the proof has a gap.
- Which property of $p_1$ did the uniqueness half use?
- Taking $U = \{z\}$ a one-element subset, what familiar set is the pullback?

## Write it up

Write your proof in `proofs/5a/p02_inverse_image_pullback.md`, then ask Claude to review it.
