# 2C·P06 — An adjunction is an isomorphism of comma categories

**Type:** stretch · **Technique:** building mutually inverse functors · **Unlocked by:** `2c_universal_arrows` §1, §5
**Source:** adapted from Riehl §4.1 and Leinster §2.3

## Statement

Let $F \colon \mathcal{A} \to \mathcal{B}$ and $G \colon \mathcal{B} \to \mathcal{A}$ be
functors with $F \dashv G$. Consider the two comma categories

- $(F \Rightarrow 1_{\mathcal{B}})$: objects $(A, g, B)$ with $g \colon F(A) \to B$ in $\mathcal{B}$; an arrow $(A, g, B) \to (A', g', B')$ is a pair $(p, q)$, $p \colon A \to A'$, $q \colon B \to B'$, with $q \circ g = g' \circ F(p)$;
- $(1_{\mathcal{A}} \Rightarrow G)$: objects $(A, f, B)$ with $f \colon A \to G(B)$ in $\mathcal{A}$; an arrow $(A, f, B) \to (A', f', B')$ is a pair $(p, q)$ with $G(q) \circ f = f' \circ p$.

Each has a *projection functor* to the product category $\mathcal{A} \times \mathcal{B}$,
sending $(A, h, B)$ to $(A, B)$ and $(p, q)$ to $(p, q)$.

Prove that there is an isomorphism of categories

$$\Phi \colon (F \Rightarrow 1_{\mathcal{B}}) \longrightarrow (1_{\mathcal{A}} \Rightarrow G)$$

that commutes with the two projection functors (that is, projecting after $\Phi$ equals
projecting directly).

## What you may use

- The definition of an adjunction with (N1), (N2), and the inverse-direction equations (N1')
  (Lemma 1 of 2A) and (N2') (brief 2A·P02).
- The definition of a comma category, of the product category (1B), and of an isomorphism of
  categories (1E): a functor with a two-sided inverse functor.
- That $(P \Rightarrow Q)$ is a category (brief P01).

## What a complete proof must show

- [ ] $\Phi$ is defined on objects and on arrows.
- [ ] **Well-definedness on arrows:** if $(p, q)$ satisfies the square condition in $(F \Rightarrow 1_{\mathcal{B}})$, then its image satisfies the square condition in $(1_{\mathcal{A}} \Rightarrow G)$. The naturality equations used are named.
- [ ] $\Phi$ preserves identities and composition.
- [ ] A functor $\Psi$ in the opposite direction is defined, with the same well-definedness check, and $\Psi \Phi$ and $\Phi \Psi$ are shown to be identity functors on objects *and* on arrows.
- [ ] Compatibility with the projection functors is verified.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

You must build a functor, build its inverse, and check a compatibility. The compatibility
requirement tells you most of what $\Phi$ has to be: it may not change the components $A$ and
$B$ of an object, nor the pair $(p, q)$. So what is the only thing left for $\Phi$ to change,
and what tool turns an arrow $F(A) \to B$ into an arrow $A \to G(B)$?

</details>

<details>
<summary>Hint 2 — the real content</summary>

With $\Phi$ defined that way, functoriality is nearly automatic. The step with content is
well-definedness on arrows: you are given that two arrows $F(A) \to B'$ are equal, and must
deduce that two arrows $A \to G(B')$ are equal. What operation, applied to both sides of the
given equation, produces arrows of the right kind?

</details>

<details>
<summary>Hint 3 — which naturality equations</summary>

After applying that operation, each side is the transpose of a composite. One composite has
an arrow of $\mathcal{B}$ applied *after* $g$; the other has $F$ of an arrow applied *before*
$g'$. Of the four naturality equations, one handles each shape.

</details>

<details>
<summary>Hint 4 — the inverse</summary>

$\Psi$ is defined the same way in the other direction, and its well-definedness uses the
remaining two of the four equations. For $\Psi\Phi = 1$ and $\Phi\Psi = 1$, what single fact
about the two bars do you need?

</details>

## Check yourself

- Did you check well-definedness for $\Psi$ as well as for $\Phi$, or only assert it "similarly"? If "similarly", can you name the two equations it uses?
- Is $\Phi$ an *isomorphism* of categories or merely an equivalence? Which did you prove?
- Under $\Phi$, what does the object $(A, 1_{F(A)}, F(A))$ go to? What does $(G(B), \varepsilon_B, B)$ go to?
- Suppose conversely you were *given* such an isomorphism $\Phi$ commuting with the projections. Can you see how to read off a hom-set bijection from it? What would (N1) and (N2) correspond to? (You are not asked to prove this.)

## Write it up

Write your proof in `proofs/2c/p06_comma_categories_isomorphic.md`, then ask Claude to review it.
