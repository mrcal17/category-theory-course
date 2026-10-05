# 1C·P06 — Full and faithful functors reflect isomorphisms

**Type:** stretch · **Technique:** using fullness to produce an arrow, faithfulness to prove an equation · **Unlocked by:** `1c_functors` §7
**Source:** adapted from Riehl §1.5 and Leinster §1.2–1.3

## Statement

Let $F \colon \mathcal{A} \to \mathcal{B}$ be a functor that is both full and faithful.

(a) Let $f \colon A \to A'$ be an arrow of $\mathcal{A}$ such that $F(f)$ is an isomorphism in
$\mathcal{B}$. Prove that $f$ is an isomorphism in $\mathcal{A}$.

(b) Let $A, A'$ be objects of $\mathcal{A}$ with $F(A) \cong F(A')$ in $\mathcal{B}$. Prove that
$A \cong A'$ in $\mathcal{A}$.

(c) Show by an example that (b) can fail for a functor that is faithful but not full.

## What you may use

- The definitions of functor, full, faithful and isomorphism.
- Proposition 1.1 of 1B (inverses are unique).
- For (c): any categories and functors from the lectures of 1A–1C.
- You may **not** use exercise P03 in the direction "if $f$ is an isomorphism then $F(f)$ is"
  unless you have proved it; it is not needed here.

## What a complete proof must show

- [ ] In (a): an arrow $g \colon A' \to A$ **of $\mathcal{A}$** is produced, saying which property of $F$ produces it and from which arrow of $\mathcal{B}$.
- [ ] In (a): **both** $g \circ f = 1_A$ and $f \circ g = 1_{A'}$ are proved as equations in $\mathcal{A}$, saying which property of $F$ is used to obtain each from an equation in $\mathcal{B}$, and in which hom-set of $\mathcal{A}$ the two arrows being compared lie.
- [ ] In (b): the isomorphism in $\mathcal{B}$ is first turned into an arrow of $\mathcal{A}$, and then (a) is applied; it is not assumed that the given isomorphism is of the form $F(f)$ without justification.
- [ ] In (c): a specific faithful functor, two specific objects, a proof that their images are isomorphic and a proof that they are not.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Part (a) asks for an isomorphism in $\mathcal{A}$, so you must exhibit an inverse *in
$\mathcal{A}$* and verify two equations *in $\mathcal{A}$*. All your information is in
$\mathcal{B}$. The definitions of full and faithful are precisely the two ways of moving
information from $\mathcal{B}$ back to $\mathcal{A}$: one moves arrows, the other moves
equations.

</details>

<details>
<summary>Hint 2 — producing the candidate</summary>

$F(f)$ has an inverse in $\mathcal{B}$. Between which two objects does that inverse run? Are
those objects of the form required by the definition of full?

</details>

<details>
<summary>Hint 3 — verifying the candidate</summary>

To show two arrows of $\mathcal{A}$ in the same hom-set are equal, faithfulness says it is
enough to compare their images. For each of the two equations you need, work out the image
under $F$ of each side separately, using the functor axioms.

</details>

<details>
<summary>Hint 4 — parts (b) and (c)</summary>

For (b): an isomorphism $F(A) \to F(A')$ is in particular an arrow between two objects in the
image of $F$. For (c): look among the forgetful functors of §7 for two non-isomorphic
structures on underlying sets that are in bijection.

</details>

## Check yourself

- In (a), did you use fullness exactly once and faithfulness exactly twice? If your count differs, check what each use achieved.
- Did you verify that the arrows you compared using faithfulness have the same domain and codomain in $\mathcal{A}$?
- In (c), did you prove that the two objects are not isomorphic in $\mathcal{A}$?
- A full subcategory's inclusion is full and faithful. What do (a) and (b) say about isomorphisms in $\mathbf{Ab}$ versus isomorphisms in $\mathbf{Grp}$?

## Write it up

Write your proof in `proofs/1c/p06_full_faithful_reflect_isomorphisms.md`, then ask Claude to review it.
