# 4A·P03 — Elements of order dividing $n$

**Type:** core · **Technique:** exhibiting a representation · **Unlocked by:** `4a_representables` §2
**Source:** adapted from Leinster §4.1

## Statement

Fix an integer $n \ge 1$. For a group $G$ (written multiplicatively, with identity $1$) put

$$T_n(G) = \{\, x \in G : x^n = 1 \,\}.$$

1. Show that for every group homomorphism $\theta \colon G \to G'$, the function $\theta$ sends
   $T_n(G)$ into $T_n(G')$, and that this makes $T_n$ a functor $\mathbf{Grp} \to \mathbf{Set}$.
2. Prove that $T_n$ is representable, with representing object the cyclic group $\mathbb{Z}/n\mathbb{Z}$:
   $$T_n \cong \mathbf{Grp}(\mathbb{Z}/n\mathbb{Z}, -).$$

## What you may use

- The definition of a representable functor and of a representation from 4A §2.
- Standard facts about homomorphisms: they preserve products, identities and powers.
- The universal property of the quotient group: if $\psi \colon \mathbb{Z} \to G$ is a homomorphism
  with $n \in \ker \psi$, there is exactly one homomorphism
  $\bar{\psi} \colon \mathbb{Z}/n\mathbb{Z} \to G$ with $\bar{\psi}([k]) = \psi(k)$ for all $k$.
- From 4A §2: homomorphisms $\mathbb{Z} \to G$ correspond to elements of $G$ via $\varphi \mapsto \varphi(1)$.

## What a complete proof must show

- [ ] Part 1 checks that $\theta(x)$ really lies in $T_n(G')$, and both functor axioms.
- [ ] For each group $G$, a function between $\mathbf{Grp}(\mathbb{Z}/n\mathbb{Z}, G)$ and $T_n(G)$ is
      named explicitly, and it is checked that its values lie in the stated codomain.
- [ ] That function is shown to be a bijection: injective and surjective, or by giving an inverse
      and checking both composites.
- [ ] Naturality is stated with its quantifiers and verified for an arbitrary homomorphism
      $\theta \colon G \to G'$.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Follow the four-item checklist under "Reading the definition" in 4A §2: an object (given to you),
a function for every $G$, bijectivity, naturality. Do them in that order and do not merge them.

</details>

<details>
<summary>Hint 2 — which function?</summary>

In the lecture, $\mathbf{Grp}(\mathbb{Z}, G) \to U(G)$ was "evaluate at the generator". The group
$\mathbb{Z}/n\mathbb{Z}$ also has a preferred generator. Where does a homomorphism send it, and why
is the result an element of $T_n(G)$ and not merely of $G$?

</details>

<details>
<summary>Hint 3 — surjectivity is the real work</summary>

Given $x \in T_n(G)$ you must produce a homomorphism out of $\mathbb{Z}/n\mathbb{Z}$. Start with a
homomorphism out of $\mathbb{Z}$ that you already know exists. What must be true of it before the
quotient property applies, and where does the hypothesis $x^n = 1$ enter?

</details>

<details>
<summary>Hint 4 — naturality</summary>

Write the naturality square for $\theta \colon G \to G'$ and chase one homomorphism
$\varphi \colon \mathbb{Z}/n\mathbb{Z} \to G$ around it. Compare with the one-line naturality
computations in 4A §2.

</details>

## Check yourself

- Where exactly did you use $x^n = 1$? If nowhere, your proof also "shows" that $U$ is represented
  by $\mathbb{Z}/n\mathbb{Z}$, which is false.
- Is $T_n(G)$ a subgroup of $G$? Does your proof need it to be?
- What does the statement say when $n = 1$?

## Write it up

Write your proof in `proofs/4a/p03_torsion_elements_representable.md`, then ask Claude to review it.
