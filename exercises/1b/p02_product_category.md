# 1B·P02 — The product of two categories is a category

**Type:** warm-up · **Technique:** verifying axioms componentwise · **Unlocked by:** `1b_isomorphisms_duality` §5
**Source:** adapted from Leinster §1.1

## Statement

Let $\mathcal{A}$ and $\mathcal{B}$ be categories. Recall that $\mathcal{A} \times \mathcal{B}$
has as objects the pairs $(A, B)$, as arrows $(A, B) \to (A', B')$ the pairs $(f, g)$ with
$f \colon A \to A'$ in $\mathcal{A}$ and $g \colon B \to B'$ in $\mathcal{B}$, composition
$(f', g') \circ (f, g) = (f' \circ f, g' \circ g)$, and identities $(1_A, 1_B)$.

Prove that $\mathcal{A} \times \mathcal{B}$ is a category.

## What you may use

- The definition of a category and the checklist of `1a_categories` §1.
- That $\mathcal{A}$ and $\mathcal{B}$ are categories.
- Two ordered pairs are equal exactly when their first components are equal and their second
  components are equal.

## What a complete proof must show

- [ ] The composite $(f', g') \circ (f, g)$ is defined exactly when it should be, and is an arrow between the correct pair of objects.
- [ ] $(1_A, 1_B)$ is an arrow $(A, B) \to (A, B)$.
- [ ] Associativity, for an arbitrary composable triple of arrows of $\mathcal{A} \times \mathcal{B}$, with each step justified.
- [ ] **Both** identity laws.
- [ ] Each use of an axiom says whether it is the axiom of $\mathcal{A}$ or of $\mathcal{B}$.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

A direct verification following the four-item checklist. Every arrow in sight is a pair, and
every equation you must prove is an equation between pairs. How is an equation between pairs
proved?

</details>

<details>
<summary>Hint 2 — setting up associativity</summary>

Start by naming a composable triple in $\mathcal{A} \times \mathcal{B}$: three pairs, with
their domains and codomains. What does "composable" in $\mathcal{A} \times \mathcal{B}$ tell
you about the first components on their own, and about the second components on their own?

</details>

<details>
<summary>Hint 3 — keeping it honest</summary>

When you compute each bracketing, apply the definition of composition in
$\mathcal{A} \times \mathcal{B}$ one step at a time, so that each line contains only one change.
The moment at which the axioms of $\mathcal{A}$ and $\mathcal{B}$ enter should be a single
visible step.

</details>

## Check yourself

- Did you say why the composite $f' \circ f$ exists in $\mathcal{A}$ whenever the pairs are composable?
- Did you check both identity laws?
- Would the same proof work for a product of three categories? What, if anything, would change?

## Write it up

Write your proof in `proofs/1b/p02_product_category.md`, then ask Claude to review it.
