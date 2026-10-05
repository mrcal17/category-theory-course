# 2A·P03 — Left adjoints preserve initial objects

**Type:** core · **Technique:** existence and uniqueness via a bijection · **Unlocked by:** `2a_adjunctions` §4
**Source:** adapted from Leinster §2.1

## Statement

Let $F \colon \mathcal{A} \to \mathcal{B}$ and $G \colon \mathcal{B} \to \mathcal{A}$ be
functors with $F \dashv G$, and let $I$ be an initial object of $\mathcal{A}$. Prove that
$F(I)$ is an initial object of $\mathcal{B}$.

Then state the dual result about right adjoints and terminal objects. You need not prove it
separately, but say precisely what it asserts and about which functor.

## What you may use

- The definition of an adjunction (bijections, (N1), (N2)).
- The definition of an initial object.
- Nothing about limits or colimits: they have not been defined yet.

## What a complete proof must show

- [ ] The statement to be proved is unpacked: for *every* object $B$ of $\mathcal{B}$, there is exactly one arrow $F(I) \to B$.
- [ ] Existence and uniqueness are both accounted for, with the reason for each.
- [ ] The object of $\mathcal{A}$ to which initiality of $I$ is applied is named.
- [ ] The dual statement is written out with the roles of $F$ and $G$ correct.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

You must count the arrows in a hom-set of $\mathcal{B}$ and show the answer is one. You know
how to count arrows out of $I$ in $\mathcal{A}$. What tool relates a hom-set of $\mathcal{B}$
to a hom-set of $\mathcal{A}$?

</details>

<details>
<summary>Hint 2 — which hom-sets?</summary>

Fix an object $B$ of $\mathcal{B}$. Write down the adjunction's bijection with $A$ replaced by
the particular object you care about. What is on each side?

</details>

<details>
<summary>Hint 3 — from a bijection to "exactly one"</summary>

If two sets are in bijection and you know the size of one of them, what do you know about the
other? Make sure you say which object of $\mathcal{A}$ the initiality of $I$ is being applied
to; it depends on $B$.

</details>

## Check yourself

- Did your proof use naturality? If not, is that a gap, or is it not needed here?
- Test the result on free monoids: what is $F(\emptyset)$, and is it initial in $\mathbf{Mon}$?
- The lecture claims this result shows $U \colon \mathbf{Field} \to \mathbf{Set}$ has no left adjoint. Can you now write that argument in three sentences?
- Does a *right* adjoint preserve initial objects? Test with $U \colon \mathbf{Mon} \to \mathbf{Set}$.

## Write it up

Write your proof in `proofs/2a/p03_left_adjoints_preserve_initial.md`, then ask Claude to review it.
