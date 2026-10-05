# 4C·P06 — Composing with a full and faithful functor

**Type:** stretch · **Technique:** building a natural transformation componentwise · **Unlocked by:** `4c_yoneda_consequences` §2, §3
**Source:** adapted from Leinster §4.3

## Statement

Let $J \colon \mathcal{A} \to \mathcal{B}$ be a full and faithful functor and let $\mathcal{C}$ be any
category. For functors $G, G' \colon \mathcal{C} \to \mathcal{A}$ and a natural transformation
$\alpha \colon G \Rightarrow G'$, let $J\alpha$ be the family with components

$$(J\alpha)_C = J(\alpha_C) \colon J(G(C)) \to J(G'(C)) \qquad (C \in \mathcal{C}).$$

1. Prove that $J\alpha$ is a natural transformation $J \circ G \Rightarrow J \circ G'$.
2. Prove that the assignment $\alpha \mapsto J\alpha$ is **injective**: if $J\alpha = J\alpha'$ for
   $\alpha, \alpha' \colon G \Rightarrow G'$, then $\alpha = \alpha'$.
3. Prove that it is **surjective**: every natural transformation
   $\beta \colon J \circ G \Rightarrow J \circ G'$ is equal to $J\alpha$ for some natural transformation
   $\alpha \colon G \Rightarrow G'$.
4. Deduce that if $J \circ G \cong J \circ G'$ then $G \cong G'$.

(Parts 2 and 3 say that the functor $J \circ - \colon [\mathcal{C}, \mathcal{A}] \to [\mathcal{C}, \mathcal{B}]$
is full and faithful. You may take it as given that it is a functor, that is, that
$J(\alpha' \circ \alpha) = J\alpha' \circ J\alpha$ and $J 1_G = 1_{J \circ G}$.)

## What you may use

- The definitions of full and faithful, and of a natural transformation.
- Lemma 3.1 of 4C (proved in 1E): full and faithful functors reflect isomorphisms.
- From 1D: a natural transformation is a natural isomorphism exactly when each component is an
  isomorphism.

## What a complete proof must show

- [ ] Part 1 states and verifies the naturality equation, naming the property of $J$ used.
- [ ] Part 2 reduces equality of natural transformations to equality of components, and says why
      the components being compared are parallel arrows.
- [ ] Part 3 defines $\alpha_C$ for each object $C$ with a justification that it exists, and then
      **proves that the family $\alpha$ is natural**. This is the step most often omitted.
- [ ] Part 4 is a short deduction from parts 2 and 3 together with a quoted result; it does not
      rebuild an inverse by hand unless you choose to.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Parts 1 and 2 are direct. Part 3 is a construction followed by a verification: fullness of $J$
gives you each component separately, but a family of arrows is not a natural transformation until
its naturality squares are shown to commute. Plan for that verification before you start.

</details>

<details>
<summary>Hint 2 — part 3, the components</summary>

For a fixed object $C$, the component $\beta_C$ is an arrow of $\mathcal{B}$ between two objects of
the form $J(\text{something})$. Which property of $J$ gives you an arrow of $\mathcal{A}$ from it?
Is that arrow unique, and does it matter?

</details>

<details>
<summary>Hint 3 — part 3, naturality</summary>

The naturality square you need lives in $\mathcal{A}$. You know that a certain square in
$\mathcal{B}$ commutes, because $\beta$ is natural. How are the two squares related? An equation
between two parallel arrows of $\mathcal{A}$ can be proved by proving the corresponding equation in
$\mathcal{B}$, provided $J$ has a certain property. Which one, and what must you say about the two
arrows before you use it?

</details>

<details>
<summary>Hint 4 — part 4</summary>

A natural isomorphism $J \circ G \cong J \circ G'$ is an isomorphism in the category
$[\mathcal{C}, \mathcal{B}]$. Parts 2 and 3 say that a certain functor into that category is full
and faithful. The lecture has a lemma about exactly this situation.

</details>

## Check yourself

- In part 3, did you use fullness and faithfulness in different places? Where was each needed?
- Did you prove naturality of $\alpha$, or assume it because $\beta$ is natural?
- Take $J = H_\bullet$, the Yoneda embedding. What does part 4 say? This is how the Yoneda lemma is
  used to prove that two *functors* are isomorphic, and it will be used in Part 6.

## Write it up

Write your proof in `proofs/4c/p06_postcomposition_full_faithful.md`, then ask Claude to review it.
