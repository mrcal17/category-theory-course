# 1E·P05 — Equivalences preserve monomorphisms

**Type:** core · **Technique:** apply a full and faithful functor and come back · **Unlocked by:** `1e_equivalence` §3, §4
**Source:** adapted from Riehl §1.5

## Statement

Let $F \colon \mathcal{A} \to \mathcal{B}$ be an equivalence of categories and let
$f \colon A \to A'$ be a monomorphism in $\mathcal{A}$. Prove that $F(f) \colon F(A) \to F(A')$
is a monomorphism in $\mathcal{B}$.

Recall (1B): an arrow $m \colon X \to Y$ is a **monomorphism** if for every object $W$ and every
pair of arrows $u, v \colon W \to X$, $\;m \circ u = m \circ v$ implies $u = v$.

## What you may use

- The definition of a monomorphism (1B) and of an isomorphism (1B).
- Theorem 2, "only if" direction (1E §4): an equivalence is full, faithful and essentially surjective on objects.
- Functoriality of $F$.

## What a complete proof must show

- [ ] The goal written out with its quantifiers: an arbitrary object $W$ **of $\mathcal{B}$** and arbitrary arrows $u, v \colon W \to F(A)$.
- [ ] A treatment of the fact that $W$ need not be of the form $F(\text{something})$.
- [ ] Each use of fullness naming the arrow of $\mathcal{B}$ being lifted and the two objects of $\mathcal{A}$ it is lifted between.
- [ ] Each use of faithfulness preceded by the observation that the two arrows are parallel.
- [ ] The place where the hypothesis "$f$ is monic" is used.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

A direct proof from the definition of monomorphism in $\mathcal{B}$. You are given an equation
in $\mathcal{B}$; your only hypothesis about cancellation lives in $\mathcal{A}$. So the equation
has to be transported to $\mathcal{A}$, used there, and the conclusion transported back. Lemma 1
in §3 is the model for "transport with a full and faithful functor".

</details>

<details>
<summary>Hint 2 — the obstacle</summary>

Fullness only lets you lift arrows *between objects in the image of $F$*. The arrows $u$ and $v$
start at $W$, which is an arbitrary object of $\mathcal{B}$. Which of the three properties of
$F$ talks about arbitrary objects of $\mathcal{B}$?

</details>

<details>
<summary>Hint 3 — repairing the domain</summary>

You can replace $u$ and $v$ by two arrows whose domain *is* in the image of $F$, at the cost of
composing with something. What property must that something have so that, at the end, you can
get back from the modified arrows to $u$ and $v$ themselves?

</details>

## Check yourself

- Did you use all three of full, faithful and essentially surjective? Which would you not need if $W$ were assumed to be of the form $F(A'')$?
- Is the statement true for a functor that is merely faithful? (Try to see where your proof would break; you are not asked for a counterexample.)
- State the dual result about epimorphisms. Could you obtain it without writing a new proof?

## Write it up

Write your proof in `proofs/1e/p05_equivalences_preserve_monics.md`, then ask Claude to review it.
