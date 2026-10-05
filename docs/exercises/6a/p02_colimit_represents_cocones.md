# 6A·P02 — A colimit represents the cocone functor

**Type:** warm-up · **Technique:** dualizing a proof · **Unlocked by:** `6a_limits_representables_adjoints` §3
**Source:** adapted from Leinster §6.1

## Statement

Let $\mathcal{A}$ be a locally small category, $\mathbf{I}$ a small category and
$D \colon \mathbf{I} \to \mathcal{A}$ a diagram. For an object $A$ write
$\mathrm{Cocone}(D, A)$ for the set of cocones on $D$ with vertex $A$: families
$(f_I \colon D(I) \to A)_{I}$ with $f_J \circ Du = f_I$ for every $u \colon I \to J$.

1. Say what a map $h \colon A \to A'$ of $\mathcal{A}$ does to cocones, and show that this makes
   $\mathrm{Cocone}(D, -)$ a covariant functor $\mathcal{A} \to \mathbf{Set}$.
2. Let $(q_I \colon D(I) \to C)_I$ be a cocone on $D$. Prove that it is a colimit cocone if and only
   if, for every object $A$, the function
   $$\mathcal{A}(C, A) \to \mathrm{Cocone}(D, A), \qquad g \mapsto (g \circ q_I)_I$$
   is a bijection, and that these functions are then the components of a natural isomorphism
   $H^C \cong \mathrm{Cocone}(D, -)$.

## What you may use

- The definition of a colimit (5B).
- Lemma 2 and Theorem 1 of the lecture, as models or as results applied to another category.
- The principle of duality (1B), provided you say exactly which statement is being applied in which category.

## What a complete proof must show

- [ ] Part 1 checks that the new family is a cocone, and both functor laws.
- [ ] Part 2 identifies which half of "exists a unique" gives surjectivity and which gives injectivity.
- [ ] Naturality in $A$ is verified by taking an element around both sides of the square.
- [ ] If duality is used, the proof states what a cone in $\mathcal{A}^{\mathrm{op}}$ on $D^{\mathrm{op}}$ is in terms of $\mathcal{A}$.

## Hints — one at a time

<details>
<summary>Hint 1 — two possible routes</summary>

You can repeat the lecture's proof of Theorem 1(a) with every arrow reversed, or you can apply
Theorem 1 itself to the diagram $D^{\mathrm{op}} \colon \mathbf{I}^{\mathrm{op}} \to \mathcal{A}^{\mathrm{op}}$.
Pick one route and stay on it; mixing them is where errors come from.

</details>

<details>
<summary>Hint 2 — if you repeat the proof</summary>

The lecture composed a cone with a map *in front*. Where must a map $h \colon A \to A'$ go relative
to a cocone with vertex $A$? Which axiom then gives the functor laws?

</details>

<details>
<summary>Hint 3 — if you dualize</summary>

Write down what $\mathcal{A}^{\mathrm{op}}(A, C)$ is as a set of maps of $\mathcal{A}$, and what
"compose with $q_I$ in $\mathcal{A}^{\mathrm{op}}$" means in $\mathcal{A}$. A contravariant functor on
$\mathcal{A}^{\mathrm{op}}$ is what kind of functor on $\mathcal{A}$?

</details>

## Check yourself

- Is your functor covariant? Test it on the case where $\mathbf{I}$ is discrete with two objects.
- Did you prove the "if" direction of part 2, or only "only if"?
- Which Yoneda-type statement would recover the colimit cocone from a natural isomorphism $H^C \cong \mathrm{Cocone}(D, -)$?

## Write it up

Write your proof in `proofs/6a/p02_colimit_represents_cocones.md`, then ask Claude to review it.
