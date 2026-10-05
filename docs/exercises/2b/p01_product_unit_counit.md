# 2B·P01 — The unit and counit of the product adjunction

**Type:** warm-up · **Technique:** unpacking a definition in an example · **Unlocked by:** `2b_units_counits` §1, §3
**Source:** adapted from Leinster §2.2

## Statement

Recall from 2A §6.1 the adjunction $\Delta \dashv \Pi$ between $\mathbf{Set}$ and
$\mathbf{Set} \times \mathbf{Set}$, where $\Delta(A) = (A, A)$ and $\Pi(X, Y) = X \times Y$. Its
transposes are

$$\overline{(g_1, g_2)}(a) = (g_1(a), g_2(a)) \quad \text{for } (g_1, g_2) \colon \Delta(A) \to (X, Y),
\qquad \bar{f} = (\pi_1 \circ f, \pi_2 \circ f) \quad \text{for } f \colon A \to X \times Y.$$

1. Using only the definitions $\eta_A = \overline{1_{\Delta(A)}}$ and
   $\varepsilon_{(X,Y)} = \overline{1_{\Pi(X,Y)}}$, find the unit $\eta_A$ for every set $A$ and
   the counit $\varepsilon_{(X, Y)}$ for every pair of sets $(X, Y)$. State the domain and
   codomain of each, and the category it lives in.
2. Verify both triangle identities for this adjunction by direct calculation with elements,
   **without** quoting Lemma 3.

## What you may use

- The description of the adjunction and its transposes given above.
- The definition of the product category $\mathbf{Set} \times \mathbf{Set}$ from 1B: an arrow
  $(X, Y) \to (X', Y')$ is a pair of functions, composition and identities are componentwise.
- How $\Delta$ and $\Pi$ act on arrows: $\Delta(p) = (p, p)$ and
  $\Pi(q_1, q_2) = q_1 \times q_2$.

## What a complete proof must show

- [ ] The identity arrow on $\Delta(A)$ in $\mathbf{Set} \times \mathbf{Set}$ is written down explicitly before it is transposed.
- [ ] $\eta_A$ and $\varepsilon_{(X,Y)}$ are given by explicit formulas, each with domain, codomain and category.
- [ ] Each triangle identity is first written out for this adjunction with all subscripts, including which object the counit or unit is taken at.
- [ ] Each triangle identity is verified by computing the composite on a general element (for the identity that lives in $\mathbf{Set} \times \mathbf{Set}$: in each of the two components).

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Part 1 is substitution into a definition; part 2 is two calculations. Nothing needs to be
invented. The difficulty is keeping track of which category each arrow lives in: one of the
two categories has *pairs* of sets as objects and *pairs* of functions as arrows.

</details>

<details>
<summary>Hint 2 — part 1</summary>

For the unit: what is the identity arrow on the object $(A, A)$ of
$\mathbf{Set} \times \mathbf{Set}$? It is a pair. Feed that pair into the first transpose
formula. For the counit: the identity on $X \times Y$ is a single function; feed it into the
second formula.

</details>

<details>
<summary>Hint 3 — part 2</summary>

Write out the first triangle identity with $F = \Delta$ and $G = \Pi$. You will need
$\Delta(\eta_A)$, which is $\Delta$ applied to a function, and the counit at the object
$\Delta(A)$, so at a pair whose two entries happen to be equal. For the second identity you
need the unit at the set $\Pi(X, Y)$ and $\Pi$ applied to the counit, which is a pair of
functions.

</details>

## Check yourself

- Is your $\eta_A$ a single function or a pair? Is your $\varepsilon_{(X,Y)}$ a single function or a pair? Check against the categories they should live in.
- In the second triangle identity, what is the set $\Pi \Delta \Pi (X, Y)$? Write a typical element of it.
- Use Lemma 2(a) with your $\eta$ to recompute $\overline{(g_1, g_2)}$. Do you get the formula you started from?
- Is $\eta_A$ ever a bijection? For which sets $A$?

## Write it up

Write your proof in `proofs/2b/p01_product_unit_counit.md`, then ask Claude to review it.
