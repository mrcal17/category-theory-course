# 2C·P02 — The identity is initial in the coslice

**Type:** warm-up · **Technique:** dualizing a lecture proof · **Unlocked by:** `2c_universal_arrows` §2
**Source:** adapted from Leinster §2.3

## Statement

Let $A$ be an object of a category $\mathcal{A}$. Recall that an object of the coslice category
$A/\mathcal{A}$ is a pair $(X, h)$ with $h \colon A \to X$, and an arrow
$(X, h) \to (X', h')$ is an arrow $f \colon X \to X'$ of $\mathcal{A}$ with $f \circ h = h'$.

1. Prove that $(A, 1_A)$ is an initial object of $A/\mathcal{A}$.
2. Give an example of a category $\mathcal{A}$ and an object $A$ for which $(A, 1_A)$ is *not*
   terminal in $A/\mathcal{A}$, and prove that it is not.

## What you may use

- The definition of the coslice category and of initial and terminal objects.
- The identity axiom in $\mathcal{A}$.
- Proposition 1 of the lecture as a *model*. You may not deduce part 1 from Proposition 1 by
  saying "by duality" unless you also prove the relationship between the coslice of
  $\mathcal{A}$ and a slice of $\mathcal{A}^{\mathrm{op}}$ that such an argument needs.

## What a complete proof must show

- [ ] Part 1 says what an arrow $(A, 1_A) \to (X, h)$ is, as an arrow of $\mathcal{A}$ satisfying an equation.
- [ ] Part 1 has an existence step and a uniqueness step, for an arbitrary object $(X, h)$.
- [ ] Part 2 names a specific category, object $A$, and object $(X, h)$ of the coslice, and shows that the number of arrows $(X, h) \to (A, 1_A)$ is not one.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Part 1 is Proposition 1 with the arrows reversed. Start, as that proof did, by writing down
the equation that an arrow of $\mathcal{A}$ must satisfy to be an arrow out of $(A, 1_A)$ in
the coslice.

</details>

<details>
<summary>Hint 2 — part 1</summary>

Your equation has an identity in it. Simplify it with an axiom. How many solutions does the
simplified equation have?

</details>

<details>
<summary>Hint 3 — part 2</summary>

For $(A, 1_A)$ to be terminal, every $h \colon A \to X$ would need exactly one arrow
$f \colon X \to A$ with a certain property. Write that property down. In $\mathbf{Set}$, look
for an $h$ for which no such $f$ can exist, or for which there are two. The non-example after
Proposition 1 may suggest where to look.

</details>

## Check yourself

- In part 1, did you check that your candidate arrow has the right domain and codomain in $\mathcal{A}$?
- In part 2, did you prove failure of existence or failure of uniqueness? Could you find an example of the other kind too?
- In a poset $P$, what do parts 1 and 2 say about the up-set of an element $a$?
- For $\mathcal{A} = \mathbf{Set}$ and $A = \{\ast\}$, part 1 identifies the initial pointed set. Which is it?

## Write it up

Write your proof in `proofs/2c/p02_coslice_initial_object.md`, then ask Claude to review it.
