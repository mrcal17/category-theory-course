# 1E·P02 — When are two discrete categories equivalent?

**Type:** warm-up · **Technique:** unpacking the definition, both directions · **Unlocked by:** `1e_equivalence` §2
**Source:** adapted from Leinster §1.3

## Statement

Let $S$ and $T$ be sets, and let $\mathcal{D}_S$ and $\mathcal{D}_T$ be the discrete categories
with object sets $S$ and $T$ (the only arrows are identities). Prove that
$$\mathcal{D}_S \simeq \mathcal{D}_T \quad \text{if and only if} \quad \text{there is a bijection } S \to T.$$

## What you may use

- The definition of an equivalence of categories (1E §2), and that every isomorphism of categories is an equivalence.
- The definition of a discrete category (1A) and of a functor (1C).
- A function is a bijection if and only if it has a two-sided inverse (0B).
- You may use Theorem 2 if you wish, but the exercise can be done from the definition alone, and the non-example "two points are not one point" in §2 is a model.

## What a complete proof must show

- [ ] Both directions, separated and labelled.
- [ ] In the direction "equivalent $\Rightarrow$ bijection": the function $S \to T$ you claim is a bijection, and a proof that it is one.
- [ ] The exact place where discreteness is used: what an arrow $x \to y$ in a discrete category tells you about $x$ and $y$.
- [ ] In the direction "bijection $\Rightarrow$ equivalent": a functor in each direction (including what it does on arrows and why it is a functor), and the two natural isomorphisms.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

An "if and only if", so two proofs. In one direction you are handed an equivalence
$(F, G, \eta, \varepsilon)$ and must extract a bijection from it. In the other you are handed a
bijection and must build an equivalence.

</details>

<details>
<summary>Hint 2 — from an equivalence to a bijection</summary>

A functor between discrete categories is not much more than a function between their object
sets. So the candidates for the bijection and its inverse are already on the table. What would
you need to know about the composites?

</details>

<details>
<summary>Hint 3 — what the components say</summary>

Take an object $s$ of $\mathcal{D}_S$. The component of $\eta$ at $s$ is an arrow of
$\mathcal{D}_S$. Between which two objects? What are the arrows of a discrete category?

</details>

<details>
<summary>Hint 4 — from a bijection to an equivalence</summary>

Given a function $S \to T$, in how many ways can it be extended to a functor
$\mathcal{D}_S \to \mathcal{D}_T$? Do that for the bijection and for its inverse, then look at
the two composite functors.

</details>

## Check yourself

- Did you prove more than you were asked: are equivalent discrete categories in fact *isomorphic*?
- A discrete category is skeletal. How does this exercise fit with the statement of P06?
- Where would your first direction fail for the walking isomorphism $\mathcal{I}$ in place of a discrete category?

## Write it up

Write your proof in `proofs/1e/p02_discrete_categories.md`, then ask Claude to review it.
