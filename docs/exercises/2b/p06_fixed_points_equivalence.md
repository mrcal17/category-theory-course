# 2B·P06 — An adjunction restricts to an equivalence

**Type:** stretch · **Technique:** triangle identities and isomorphisms · **Unlocked by:** `2b_units_counits` §5
**Source:** adapted from Leinster §2.2

## Statement

Let $F \colon \mathcal{A} \to \mathcal{B}$ and $G \colon \mathcal{B} \to \mathcal{A}$ be
functors with $F \dashv G$, unit $\eta$ and counit $\varepsilon$. Let

- $\mathcal{A}_0$ be the full subcategory of $\mathcal{A}$ whose objects are those $A$ for which $\eta_A$ is an isomorphism;
- $\mathcal{B}_0$ be the full subcategory of $\mathcal{B}$ whose objects are those $B$ for which $\varepsilon_B$ is an isomorphism.

Prove:

1. if $A$ is an object of $\mathcal{A}_0$ then $F(A)$ is an object of $\mathcal{B}_0$, and if $B$ is an object of $\mathcal{B}_0$ then $G(B)$ is an object of $\mathcal{A}_0$;
2. the functors $F$ and $G$ therefore restrict to functors $F_0 \colon \mathcal{A}_0 \to \mathcal{B}_0$ and $G_0 \colon \mathcal{B}_0 \to \mathcal{A}_0$, and these form an equivalence of categories $\mathcal{A}_0 \simeq \mathcal{B}_0$.

## What you may use

- The triangle identities and the naturality of $\eta$ and $\varepsilon$.
- From 1B: the definition of isomorphism, uniqueness of inverses, and what a full subcategory is.
- From 1C: functors preserve isomorphisms.
- From 1D and 1E: a natural transformation is a natural isomorphism exactly when every
  component is an isomorphism; the definition of an equivalence of categories as a pair of
  functors with natural isomorphisms $1 \cong G_0 F_0$ and $F_0 G_0 \cong 1$.

## What a complete proof must show

- [ ] Part 1 names, for each half, the triangle identity used and the arrow that is known to be an isomorphism.
- [ ] Part 1 contains an explicit argument that an arrow which composes with an isomorphism to give an identity is itself an isomorphism (and says what its inverse is).
- [ ] In part 2 it is explained why the restrictions are well-defined functors (objects go to objects of the subcategory; what happens to arrows, and why fullness matters).
- [ ] The two natural isomorphisms required by the definition of equivalence are exhibited, and it is checked that they are natural transformations between the *restricted* functors.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Part 1 is where the work is; part 2 is assembling definitions. For part 1 you know one arrow
is an isomorphism and want to show a different arrow is. Which equations from the lecture
contain both a component of $\eta$ and a component of $\varepsilon$?

</details>

<details>
<summary>Hint 2 — the first half of part 1</summary>

Suppose $\eta_A$ is an isomorphism. You want to know about the counit at the object $F(A)$.
One of the triangle identities mentions exactly that component. What else appears in it, and
what do you know about that other arrow?

</details>

<details>
<summary>Hint 3 — a small lemma to isolate</summary>

State and prove separately: in any category, if $v \circ u$ is an identity and $u$ is an
isomorphism, then $v$ is an isomorphism. What must the inverse of $v$ be? You will use this
lemma twice, once in each half of part 1.

</details>

<details>
<summary>Hint 4 — part 2</summary>

You need natural isomorphisms $1_{\mathcal{A}_0} \Rightarrow G_0 F_0$ and
$F_0 G_0 \Rightarrow 1_{\mathcal{B}_0}$. You already have natural transformations with those
shapes on the big categories. What are their components at objects of the subcategories, and
why do their naturality squares survive the restriction?

</details>

## Check yourself

- In part 1, did you show $\varepsilon_{F(A)}$ has a *two-sided* inverse, or only a one-sided one?
- For a Galois connection $f \dashv g$: what are $\mathcal{A}_0$ and $\mathcal{B}_0$ in the language of 2B §6, and what does the equivalence become between posets?
- For $D \dashv U$ between $\mathbf{Set}$ and $\mathbf{Top}$: which spaces are in $\mathcal{B}_0$? Is the result plausible?
- Can $\mathcal{A}_0$ be empty? Does your proof still make sense then?

## Write it up

Write your proof in `proofs/2b/p06_fixed_points_equivalence.md`, then ask Claude to review it.
