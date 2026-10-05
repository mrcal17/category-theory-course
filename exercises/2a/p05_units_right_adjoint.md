# 2A·P05 — The group of units is right adjoint to the inclusion

**Type:** core · **Technique:** verifying an adjunction from the checklist · **Unlocked by:** `2a_adjunctions` §3
**Source:** adapted from Leinster §2.1

## Statement

Let $U \colon \mathbf{Grp} \to \mathbf{Mon}$ be the inclusion functor, which regards a group as
a monoid and a group homomorphism as a monoid homomorphism. For a monoid $M$, let

$$M^{\times} = \{ m \in M : \text{there exists } n \in M \text{ with } mn = 1 = nm \}$$

be its set of invertible elements.

1. Show that $M^{\times}$ is a group under the multiplication of $M$, and that a monoid
   homomorphism $q \colon M \to M'$ restricts to a group homomorphism
   $q^{\times} \colon M^{\times} \to M'^{\times}$, so that $R(M) = M^{\times}$,
   $R(q) = q^{\times}$ defines a functor $R \colon \mathbf{Mon} \to \mathbf{Grp}$.
2. Prove that $U \dashv R$.

## What you may use

- The definitions of monoid, group, and homomorphisms of each (a monoid homomorphism preserves
  products and the identity).
- The definition of an adjunction from 2A §1.
- The fact from 1B that inverses in a monoid are unique when they exist.

## What a complete proof must show

- [ ] $M^{\times}$ is closed under multiplication, contains $1$, and contains the inverse of each of its elements.
- [ ] $q(M^{\times}) \subseteq M'^{\times}$, with the reason; and $R$ preserves identities and composition.
- [ ] For a group $H$ and a monoid $M$, both directions of the correspondence between $\mathbf{Mon}(U(H), M)$ and $\mathbf{Grp}(H, M^{\times})$ are defined, and each is shown to produce an arrow of the claimed category.
- [ ] Both round trips are checked.
- [ ] (N1) is checked for a monoid homomorphism $q \colon M \to M'$, and (N2) for a group homomorphism $p \colon H' \to H$.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Part 1 is a sequence of small closure checks. Part 2 is the five-item checklist of 2A §1,
with $U$ in the role of the *left* adjoint: the hom-set bijection has $U(H)$ in the left slot.
Theorem 2 of the lecture is the model for how to lay it out.

</details>

<details>
<summary>Hint 2 — the one real idea</summary>

Let $g \colon U(H) \to M$ be a monoid homomorphism out of a group. Pick $x \in H$. What can
you say about the element $g(x)$ of $M$, using that $x$ has an inverse in $H$?

</details>

<details>
<summary>Hint 3 — the other direction</summary>

A group homomorphism $f \colon H \to M^{\times}$ and the inclusion of $M^{\times}$ into $M$ are
both available. What must you verify before you may call the resulting function an arrow of
$\mathbf{Mon}$?

</details>

<details>
<summary>Hint 4 — naturality</summary>

Neither transposition changes what happens to an individual element. Use that: to check (N1)
and (N2), evaluate both sides on an element $x$ and compare. Be explicit about what $R(q)$
does to an element.

</details>

## Check yourself

- Did you prove that the inverse of an element of $M^{\times}$ again lies in $M^{\times}$, or only that it lies in $M$?
- In the hom-set bijection, is $U$ in the left slot? If you found yourself writing $\mathbf{Grp}(M^{\times}, H)$, the direction is reversed.
- What is $M^{\times}$ for $M = (\mathbb{Z}, \times)$? For $M = (\mathbb{N}, +)$? Does the bijection give the right count of homomorphisms from $\mathbb{Z}/2$ into each?
- Depending on your definition, a group homomorphism need only preserve products. Did you check the identity where a *monoid* homomorphism was required?

## Write it up

Write your proof in `proofs/2a/p05_units_right_adjoint.md`, then ask Claude to review it.
