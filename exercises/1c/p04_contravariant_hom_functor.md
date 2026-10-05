# 1C·P04 — The contravariant hom-functor

**Type:** core · **Technique:** verifying functoriality · **Unlocked by:** `1c_functors` §5, §6
**Source:** adapted from Riehl §1.3 (Leinster treats hom-functors in §4.1)

## Statement

Let $\mathcal{A}$ be a category whose hom-sets are sets, and fix an object $A$. Define $H_A$ by

- $H_A(B) = \mathcal{A}(B, A)$ for each object $B$;
- for each arrow $g \colon B \to B'$ of $\mathcal{A}$, the function
  $H_A(g) \colon \mathcal{A}(B', A) \to \mathcal{A}(B, A)$, $q \mapsto q \circ g$.

Prove that $H_A$ is a functor $\mathcal{A}^{\mathrm{op}} \to \mathbf{Set}$; that is, a
contravariant functor from $\mathcal{A}$ to $\mathbf{Set}$.

## What you may use

- The definition of a functor, and the unpacked description of a contravariant functor
  (items 1–4 in `1c_functors` §5).
- The axioms of the category $\mathcal{A}$.
- Two functions are equal when they have the same domain and codomain and agree at every element.
- Proposition 6.1 is a model for the layout. You may **not** simply say "by duality from
  Proposition 6.1" unless you write out the dualization in full, in the style of Corollary 4.3
  of 1B: which category Proposition 6.1 is applied to, and why the resulting functor is $H_A$.

## What a complete proof must show

- [ ] For $g \colon B \to B'$, the composite $q \circ g$ is defined and lies in the stated codomain of $H_A(g)$.
- [ ] The composition condition is stated in its contravariant form for arrows $B \xrightarrow{g} B' \xrightarrow{g'} B''$, with the domain and codomain of each side identified, and then proved by evaluating at an arbitrary element.
- [ ] The identity condition is proved.
- [ ] Each step names the axiom of $\mathcal{A}$ it uses.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

This is a functoriality check, with the same three items as Proposition 6.1. The equations to
be proved are equations between *functions*, and the elements those functions act on are
arrows of $\mathcal{A}$. Decide first what an arbitrary element of the relevant domain looks
like.

</details>

<details>
<summary>Hint 2 — getting the statement right</summary>

Before proving the composition condition, write it down. $H_A(g' \circ g)$ is a function from
which set to which set? Of the two candidate right-hand sides, $H_A(g') \circ H_A(g)$ and
$H_A(g) \circ H_A(g')$, only one is a composable pair of functions. Which?

</details>

<details>
<summary>Hint 3 — which axioms</summary>

In Proposition 6.1 the composition condition turned out to be one axiom of $\mathcal{A}$ and
the identity condition another. The same will happen here, but it is not the same identity
law. Evaluate, then look at what you need.

</details>

## Check yourself

- Did you check that each composite you wrote is defined, by naming domains and codomains?
- Which identity law of $\mathcal{A}$ did you use? Which one did Proposition 6.1 use?
- What is $H_A$ when $\mathcal{A}$ is a poset? When $\mathcal{A}$ is a monoid regarded as a one-object category?
- How does the dual space functor of §5 relate to $H_k$ on $\mathbf{Vect}_k$?

## Write it up

Write your proof in `proofs/1c/p04_contravariant_hom_functor.md`, then ask Claude to review it.
