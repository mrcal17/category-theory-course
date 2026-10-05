# 0C·P06 — Products of sets are unique up to unique isomorphism

**Type:** stretch · **Technique:** unique up to unique isomorphism · **Unlocked by:** `0c_proof_toolkit_uniqueness` §7 (and `0a_orientation` §3)
**Source:** adapted from Leinster §5.1

## Statement

Let $A$ and $B$ be sets. In this brief, a *product of $A$ and $B$* is a triple $(P, p_1, p_2)$
consisting of a set $P$ and functions $p_1 \colon P \to A$ and $p_2 \colon P \to B$ with the
following universal property:

> for every set $X$ and all functions $f \colon X \to A$ and $g \colon X \to B$, there exists a
> unique function $h \colon X \to P$ such that $p_1 \circ h = f$ and $p_2 \circ h = g$.

(Module 0A showed that the set of ordered pairs $A \times B$ with its two projections is a
product in this sense.)

Let $(P, p_1, p_2)$ and $(Q, q_1, q_2)$ both be products of $A$ and $B$. Prove:

**(1)** there is exactly one function $u \colon P \to Q$ such that $q_1 \circ u = p_1$ and
$q_2 \circ u = p_2$;

**(2)** this $u$ is an isomorphism of sets.

## What you may use

- The universal property above, for $(P, p_1, p_2)$ and for $(Q, q_1, q_2)$.
- Proposition 2 of 0B: associativity of composition and the identity laws.
- The definition of isomorphism of sets (0C §7), and the *method* of Theorem 7.
- You may **not** assume that $P$ or $Q$ is a set of ordered pairs, and you may not use their
  elements: all you know about them is the universal property.

## What a complete proof must show

- [ ] Every use of a universal property names the product whose property it is, the set $X$, and
      the two functions playing the roles of $f$ and $g$.
- [ ] Claim (1) is addressed in full: existence and uniqueness.
- [ ] A candidate inverse for $u$ is produced, and both composites are proved to be identity
      functions.
- [ ] Every equation between composites is justified: associativity, an identity law, a defining
      equation of $u$ or of its candidate inverse, or the uniqueness clause of a universal
      property.
- [ ] No element of $P$ or $Q$ appears anywhere.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Theorem 7 is the template: obtain a map each way from the two universal properties, then show
the two composites are identities using uniqueness clauses. Claim (1) is a single application of
one universal property. Whose property, and with which $X$, $f$ and $g$?

</details>

<details>
<summary>Hint 2 — the map back</summary>

For claim (2) you need a function $Q \to P$. The situation is symmetric in the two products.
Write down the two equations your new function satisfies; you will need them.

</details>

<details>
<summary>Hint 3 — what replaces "only one map from T to T"?</summary>

In Theorem 7, the key step was that a terminal set has only one function to itself. A product
$P$ has many functions $P \to P$, so that step cannot be copied as it stands. But the
uniqueness clause of $P$ does say that there is only one function $P \to P$ *satisfying certain
equations*. Which choice of $X$, $f$ and $g$ makes that clause talk about functions $P \to P$,
and what are the equations then?

</details>

<details>
<summary>Hint 4 — two functions, the same equations</summary>

You want two particular functions $P \to P$ to be equal. Check that each of them satisfies the
equations you found in Hint 3. For one of them this needs the defining equations of both of
your maps and one law from Proposition 2 of 0B; for the other it needs a different law from the
same proposition. Then do it all again on the other side.

</details>

## Check yourself

- How many times did you invoke a universal property? For each invocation, can you point to the
  sentence that names $X$, $f$ and $g$?
- When $A = B = \{0, 1\}$ there are $24$ bijections from $A \times A$ to itself. Your proof says
  that only one of them is compatible with the projections. Which one, and can you see directly
  why the others fail?
- Compare your proof line by line with Theorem 7. What plays the role of "the only function
  $T \to T$ is $1_T$"?

## Write it up

Write your proof in `proofs/0c/p06_products_unique_up_to_unique_iso.md`, then ask Claude to review it.
