# 0B·P04 — A left inverse and a right inverse must coincide

**Type:** core · **Technique:** element-free calculation with composites · **Unlocked by:** `0b_proof_toolkit_definitions` §6
**Source:** adapted from Leinster §1.1

## Statement

Let $f \colon A \to B$ be a function. Suppose $g \colon B \to A$ is a left inverse of $f$ and
$h \colon B \to A$ is a right inverse of $f$.

**(a)** Prove that $g = h$.

**(b)** Deduce that $f$ is invertible, and that an invertible function has exactly one two-sided
inverse.

## What you may use

- The definitions of left inverse, right inverse and invertible (0B §6).
- Proposition 2 of 0B: associativity of composition and the identity laws.
- Nothing about elements is needed, and you have no formula for $g$ or $h$.

## What a complete proof must show

- [ ] Part (a) states which two functions are being shown equal and what their common domain and
      codomain are.
- [ ] Every equality is justified by name: associativity, an identity law, the hypothesis on
      $g$, or the hypothesis on $h$.
- [ ] Both hypotheses are used, and the proof says where.
- [ ] Part (b) separates "invertible" (an existence claim) from "exactly one inverse" (a
      uniqueness claim) and says how each follows from (a).

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

You must show two functions are equal, but unfolding at an element $b \in B$ stalls at once:
nothing tells you what $g(b)$ or $h(b)$ is. All you know is how $g$ and $h$ each compose with
$f$. So the proof has to be a calculation with composites, using Proposition 2 of 0B.

</details>

<details>
<summary>Hint 2 — what to calculate</summary>

One hypothesis is about $g$ composed with $f$; the other is about $f$ composed with $h$. Is
there a single composite of functions in which both of those appear, depending on where you put
the brackets?

</details>

<details>
<summary>Hint 3 — finishing</summary>

Simplify your composite twice, once with each bracketing. Each time, one hypothesis and one
identity law apply. What does associativity say about the two answers? For (b): a two-sided
inverse is in particular both a left inverse and a right inverse, so what does (a) say about two
two-sided inverses?

</details>

## Check yourself

- Did you use that $g$ is a *left* inverse and $h$ a *right* inverse, in that order? What goes
  wrong if both are left inverses? (The lecture has an example with two different left inverses.)
- Does any step mention an element of $A$ or $B$?
- Reread your proof with "function" replaced by "element of a monoid" and $\circ$ replaced by the
  monoid operation. Is every step still justified?

## Write it up

Write your proof in `proofs/0b/p04_left_inverse_equals_right_inverse.md`, then ask Claude to review it.
