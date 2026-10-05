# 1C·P05 — Faithful functors reflect monics and epics

**Type:** core · **Technique:** cancellation; using faithfulness · **Unlocked by:** `1c_functors` §7 and `1b_isomorphisms_duality` §2
**Source:** built from the definitions in Riehl §1.2 (monics, epics) and Leinster §1.2 (faithful functors)

## Statement

Let $F \colon \mathcal{A} \to \mathcal{B}$ be a **faithful** functor and let $f \colon A \to A'$
be an arrow of $\mathcal{A}$.

(a) Prove that if $F(f)$ is monic in $\mathcal{B}$, then $f$ is monic in $\mathcal{A}$.

(b) Prove that if $F(f)$ is epic in $\mathcal{B}$, then $f$ is epic in $\mathcal{A}$.

(c) Use (a), (b) and the forgetful functor $U \colon \mathbf{Grp} \to \mathbf{Set}$ to show that
every injective group homomorphism is monic in $\mathbf{Grp}$ and every surjective group
homomorphism is epic in $\mathbf{Grp}$.

## What you may use

- The definitions of functor, faithful, monic and epic.
- Proposition 7.1 ($U$ is faithful), Proposition 2.1 of 1B (monic in $\mathbf{Set}$ means
  injective) and, for the epic half of (c), the statement of exercise 1B·P03 (epic in
  $\mathbf{Set}$ means surjective).
- You may prove (b) by a direct argument parallel to (a). If you prefer to deduce it from (a)
  by duality, you must say which functor between which opposite categories you are applying
  (a) to, and why that is a faithful functor.

## What a complete proof must show

- [ ] In (a): an arbitrary object $C$ and arbitrary arrows $x, y \colon C \to A$ with $f \circ x = f \circ y$ are introduced, and $x = y$ is derived.
- [ ] The step that moves the equation into $\mathcal{B}$ names the functor axiom used.
- [ ] The step that uses "$F(f)$ is monic" says which test arrows of $\mathcal{B}$ it is applied to.
- [ ] The step that uses faithfulness says why the two arrows concerned lie in the **same** hom-set of $\mathcal{A}$.
- [ ] In (c): each claim is deduced from (a) or (b) and a cited result, with no element-chasing in $\mathbf{Grp}$.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

To prove $f$ is monic you start, as always, from an equation $f \circ x = f \circ y$ in
$\mathcal{A}$ and must reach $x = y$. You know nothing about cancelling $f$ in $\mathcal{A}$;
your cancellation hypothesis lives in $\mathcal{B}$. So the proof has three stages: go to
$\mathcal{B}$, cancel there, come back.

</details>

<details>
<summary>Hint 2 — going and cancelling</summary>

What does a functor do to both sides of an equation between composites? After that, what does
the hypothesis on $F(f)$ let you conclude, and about which two arrows of $\mathcal{B}$?

</details>

<details>
<summary>Hint 3 — coming back</summary>

You will have an equation in $\mathcal{B}$ between the images of two arrows of $\mathcal{A}$.
Which property of $F$ turns such an equation into an equation in $\mathcal{A}$, and what must
be true of the two arrows before that property applies?

</details>

## Check yourself

- Did you check that $x$ and $y$ are parallel (same domain, same codomain) before invoking faithfulness?
- Did you use fullness anywhere? You should not have needed it.
- The lecture (§4) showed that functors need not *preserve* monics. Is the functor used there faithful? Is that a contradiction with this exercise?
- Proposition 2.2 of 1B showed directly that an injective monoid homomorphism is monic. How would this exercise give that in one line?

## Write it up

Write your proof in `proofs/1c/p05_faithful_functors_reflect_monics.md`, then ask Claude to review it.
