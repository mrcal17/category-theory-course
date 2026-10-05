#flashcards/part4

## 4A: Representable Functors

Definition: the covariant hom-functor $H^A$ on a locally small category $\mathcal{A}$
?
$H^A = \mathcal{A}(A, -) \colon \mathcal{A} \to \mathbf{Set}$. On objects: $H^A(B) = \mathcal{A}(A, B)$. On an arrow $g \colon B \to C$: $H^A(g)(p) = g \circ p$ (compose with $g$ afterwards).

Definition: the contravariant hom-functor $H_A$
?
$H_A = \mathcal{A}(-, A) \colon \mathcal{A}^{\mathrm{op}} \to \mathbf{Set}$. On objects: $H_A(B) = \mathcal{A}(B, A)$. On an arrow $g \colon C \to B$: $H_A(g) \colon \mathcal{A}(B, A) \to \mathcal{A}(C, A)$, $p \mapsto p \circ g$ (compose with $g$ beforehand).

Definition: presheaf on a category $\mathcal{A}$
?
A functor $X \colon \mathcal{A}^{\mathrm{op}} \to \mathbf{Set}$: a set $X(A)$ for each object, a function $X(f) \colon X(B) \to X(A)$ for each arrow $f \colon A \to B$, with $X(1_A) = 1_{X(A)}$ and $X(g \circ f) = X(f) \circ X(g)$.

Definition: representable functor, and representation
?
$X \colon \mathcal{A} \to \mathbf{Set}$ is representable if $X \cong H^A$ for some object $A$; a presheaf $X$ is representable if $X \cong H_A$ for some $A$. A representation is a choice of $A$ together with a natural isomorphism $H^A \Rightarrow X$ (or $H_A \Rightarrow X$).

What four things must you supply and check to prove $X \colon \mathcal{A} \to \mathbf{Set}$ is represented by $A$?
?
(1) The object $A$. (2) A function $\alpha_B \colon \mathcal{A}(A, B) \to X(B)$ for every $B$. (3) Each $\alpha_B$ is a bijection. (4) Naturality: $X(g)(\alpha_B(p)) = \alpha_C(g \circ p)$ for every $g \colon B \to C$ and every $p$.

Which objects represent the forgetful functors $\mathbf{Grp} \to \mathbf{Set}$, $\mathbf{Top} \to \mathbf{Set}$ and the identity functor on $\mathbf{Set}$?
?
$\mathbb{Z}$ (via $\varphi \mapsto \varphi(1)$), the one-point space, and the one-element set $1$ (via $p \mapsto p(\star)$). In each case: the free object on one generator.

What represents the contravariant power-set functor $\mathscr{P} \colon \mathbf{Set}^{\mathrm{op}} \to \mathbf{Set}$, and by which bijection?
?
The two-element set $2 = \{0, 1\}$: $\mathbf{Set}(B, 2) \to \mathscr{P}(B)$, $\chi \mapsto \chi^{-1}\{1\}$. Naturality is the identity $g^{-1}(\chi^{-1}\{1\}) = (\chi \circ g)^{-1}\{1\}$.

For an arrow $f$, what are $H^f$ and $H_f$, and which way do they go?
?
For $f \colon A' \to A$: $H^f \colon H^A \Rightarrow H^{A'}$, $(H^f)_B(p) = p \circ f$ (direction reversed). For $f \colon A \to B$: $H_f \colon H_A \Rightarrow H_B$, $(H_f)_C(p) = f \circ p$ (direction kept).

Definition: the Yoneda embedding
?
The functor $H_\bullet \colon \mathcal{A} \to [\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$, $A \mapsto H_A$, $f \mapsto H_f$. It is covariant. (The companion $H^\bullet \colon \mathcal{A}^{\mathrm{op}} \to [\mathcal{A}, \mathbf{Set}]$ is contravariant.)

What technique proves that $H^f$ is a natural transformation?
?
Compute both routes round the naturality square on an arbitrary $p$: one gives $g \circ (p \circ f)$, the other $(g \circ p) \circ f$. They agree by associativity. Composing before and composing after do not interfere.

State the two results linking adjunctions to representables.
?
(1) If $F \dashv G$ with $F \colon \mathcal{A} \to \mathcal{B}$, then for each $A$ the functor $\mathcal{A}(A, G(-)) \colon \mathcal{B} \to \mathbf{Set}$ is represented by $F(A)$. (2) Any functor $G \colon \mathcal{A} \to \mathbf{Set}$ with a left adjoint $F$ is representable: $G \cong H^{F(1)}$.

How do you prove a functor is NOT representable?
?
Find a property that every $H^A$ (or $H_A$) has and show the functor lacks it. Example: $H_A(A)$ always contains $1_A$, so the presheaf that is empty everywhere is not representable. One failed attempt at a bijection proves nothing.

How is the tensor product $U \otimes V$ defined by what it represents?
?
It is a representing object for $\mathrm{Bilin}(U, V; -) \colon \mathbf{Vect}_k \to \mathbf{Set}$: linear maps $U \otimes V \to W$ correspond, naturally in $W$, to bilinear maps $U \times V \to W$.

What is a presheaf on the category with two parallel arrows $s, t \colon V \to E$, and what are its two representables?
?
A directed graph: vertices $X(V)$, edges $X(E)$, source and target $X(s), X(t) \colon X(E) \to X(V)$. $H_V$ is one vertex with no edges; $H_E$ is one edge between two vertices.

## 4B: The Yoneda Lemma

State the Yoneda lemma (Leinster's variance).
?
For a locally small category $\mathcal{A}$: $[\mathcal{A}^{\mathrm{op}}, \mathbf{Set}](H_A, X) \cong X(A)$, naturally in $A \in \mathcal{A}$ and $X \in [\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$. Natural transformations from $H_A$ to a presheaf $X$ correspond to elements of $X(A)$.

What is a natural transformation $\alpha \colon H_A \Rightarrow X$, concretely?
?
A function $\alpha_B \colon \mathcal{A}(B, A) \to X(B)$ for each object $B$, such that $X(g)(\alpha_B(p)) = \alpha_C(p \circ g)$ for every $g \colon C \to B$ and every $p \colon B \to A$.

In the Yoneda lemma, what are the two maps $\alpha \mapsto \hat{\alpha}$ and $x \mapsto \tilde{x}$?
?
$\hat{\alpha} = \alpha_A(1_A) \in X(A)$. For $x \in X(A)$: $\tilde{x}_B(p) = X(p)(x)$ for $p \colon B \to A$. They are mutually inverse.

What does "follow the identity" mean?
?
To understand a natural transformation $\alpha$ out of $H_A$, take the naturality square at an arrow $f \colon B \to A$ and evaluate it at $1_A$. It gives $\alpha_B(f) = X(f)(\alpha_A(1_A))$: every value of $\alpha$ is computed from its value at the identity.

Name the six stages of the proof of the Yoneda lemma.
?
(1) Define $\hat{\alpha} = \alpha_A(1_A)$. (2) Define $\tilde{x}$ and prove it is natural. (3) $\hat{\tilde{x}} = x$. (4) $\tilde{\hat{\alpha}} = \alpha$. (5) Naturality in $X$. (6) Naturality in $A$.

Which fact about $X$ proves that $\tilde{x}$ is natural, and which proves $\hat{\tilde{x}} = x$?
?
Naturality of $\tilde{x}$ is the composition axiom $X(p \circ g) = X(g) \circ X(p)$. The equation $\hat{\tilde{x}} = x$ is the identity axiom $X(1_A) = 1_{X(A)}$.

Which step of the proof shows that $\alpha$ is determined by $\alpha_A(1_A)$, and what does it use?
?
Stage 4, $\tilde{\hat{\alpha}} = \alpha$. It uses naturality of $\alpha$ at $f \colon B \to A$ evaluated at $1_A$, then the identity axiom $1_A \circ f = f$.

What do "naturality in $X$" and "naturality in $A$" say, as equations?
?
In $X$: for $\theta \colon X \Rightarrow X'$, $\widehat{\theta \circ \alpha} = \theta_A(\hat{\alpha})$. In $A$: for $f \colon B \to A$, $\widehat{\alpha \circ H_f} = X(f)(\hat{\alpha})$.

What is a presheaf on a monoid $M$ (as a one-object category), and what is the representable one?
?
A right $M$-set: a set $S$ with $x \cdot 1 = x$ and $x \cdot (mn) = (x \cdot m) \cdot n$. The representable $H_\star$ is $M$ acting on itself by right multiplication. Natural transformations are equivariant maps.

What does the Yoneda lemma say for a monoid $M$ and a right $M$-set $S$?
?
Equivariant maps $\varphi \colon M \to S$ correspond to elements of $S$ via $\varphi \mapsto \varphi(1)$; the inverse sends $x$ to $p \mapsto x \cdot p$.

State Cayley's theorem and say how it comes from the Yoneda lemma.
?
Every monoid $M$ embeds in $\mathbf{Set}(M, M)$ via $x \mapsto \lambda_x$ (left multiplication); every group $G$ is isomorphic to a subgroup of $\mathrm{Sym}(G)$. Take $S = M$ in the monoid case of the lemma: the equivariant maps $M \to M$ for right multiplication are exactly the left multiplications.

What does the Yoneda lemma say in a poset $P$?
?
A natural transformation $H_a \Rightarrow X$ is a family $(x_b)_{b \le a}$ with $x_b \in X(b)$ compatible with restriction, and it is determined by $x_a$. With $X = H_b$: there is a natural transformation $H_a \Rightarrow H_b$ iff $a \le b$, and then exactly one.

State the covariant form of the Yoneda lemma.
?
For $X \colon \mathcal{A} \to \mathbf{Set}$: $[\mathcal{A}, \mathbf{Set}](H^A, X) \cong X(A)$, naturally in $A$ and $X$, via $\alpha \mapsto \alpha_A(1_A)$.

What does the Yoneda lemma NOT say?
?
It does not say $X \cong H_A$ or that $X$ is representable, and it says nothing about natural transformations *into* $H_A$ or out of a non-representable presheaf. It describes the set of maps from a representable to an arbitrary presheaf.

## 4C: Consequences of Yoneda

Definition: universal element of a presheaf $X$ on $\mathcal{A}$
?
A pair $(A, u)$ with $u \in X(A)$ such that for every object $B$ and every $x \in X(B)$ there is a unique arrow $\bar{x} \colon B \to A$ with $X(\bar{x})(u) = x$.

How are representations of a presheaf $X$ related to universal elements?
?
Under the Yoneda bijection $\alpha \mapsto \alpha_A(1_A)$, natural isomorphisms $H_A \Rightarrow X$ correspond exactly to elements $u \in X(A)$ with $(A, u)$ universal. So a representation of $X$ is the same thing as a universal element.

What technique proves "representation = universal element"?
?
Unpack in a chain of equivalences: $\tilde{u}$ is a natural isomorphism iff each $\tilde{u}_B \colon \mathcal{A}(B, A) \to X(B)$, $f \mapsto X(f)(u)$, is a bijection iff each $x \in X(B)$ is $X(f)(u)$ for exactly one $f$.

Give universal elements for $\mathscr{P} \colon \mathbf{Set}^{\mathrm{op}} \to \mathbf{Set}$ and for $U \colon \mathbf{Grp} \to \mathbf{Set}$.
?
$(2, \{1\})$: every subset $S \subseteq B$ is $\chi^{-1}\{1\}$ for a unique $\chi \colon B \to 2$. $(\mathbb{Z}, 1)$: every $x \in G$ is $\varphi(1)$ for a unique homomorphism $\varphi \colon \mathbb{Z} \to G$.

For an adjunction $F \dashv G$, what is the universal element of $\mathcal{A}(A, G(-))$?
?
$(F(A), \eta_A)$, the unit: every $f \colon A \to G(B)$ equals $G(q) \circ \eta_A$ for a unique $q \colon F(A) \to B$.

State the theorem about the Yoneda embedding.
?
For every locally small $\mathcal{A}$, $H_\bullet \colon \mathcal{A} \to [\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$ is full and faithful: $f \mapsto H_f$ is a bijection $\mathcal{A}(A, B) \to [\mathcal{A}^{\mathrm{op}}, \mathbf{Set}](H_A, H_B)$.

How is "the Yoneda embedding is full and faithful" proved?
?
Apply the Yoneda lemma with $X = H_B$: $x \mapsto \tilde{x}$ is a bijection $H_B(A) = \mathcal{A}(A, B) \to \mathrm{Nat}(H_A, H_B)$. Then compute $\tilde{f}_C(p) = H_B(p)(f) = f \circ p = (H_f)_C(p)$, so the bijection is $f \mapsto H_f$.

Given a natural transformation $\alpha \colon H_A \Rightarrow H_B$, which arrow $f$ has $H_f = \alpha$?
?
$f = \alpha_A(1_A)$. Follow the identity.

What do full and faithful functors do to isomorphisms?
?
If $J$ is full and faithful: $f$ is an isomorphism iff $J(f)$ is; and $A \cong A'$ iff $J(A) \cong J(A')$. Fullness pulls the inverse back, faithfulness pulls back the equations saying it is an inverse.

State the corollary relating $H_A \cong H_B$ and $A \cong B$.
?
$H_A \cong H_B \iff A \cong B \iff H^A \cong H^B$. Proof: the Yoneda embedding is full and faithful, and full and faithful functors reflect isomorphisms; for $H^A$, apply this to $\mathcal{A}^{\mathrm{op}}$.

Definition: generalized element; and the criterion for $A \cong B$ in these terms
?
A generalized element of $A$ of shape $C$ is an arrow $C \to A$. $A \cong B$ iff $\mathcal{A}(C, A) \cong \mathcal{A}(C, B)$ naturally in $C$: same generalized elements of every shape, compatibly with change of shape. One shape is not enough, and naturality cannot be dropped.

What does the Yoneda embedding of a poset $P$ look like?
?
$a \mapsto {\downarrow}a = \{b : b \le a\}$, into the poset of down-sets ordered by inclusion. Full and faithful becomes: $a \le b \iff {\downarrow}a \subseteq {\downarrow}b$. The representable down-sets are the principal ones.

In what sense is a representing object unique?
?
If $A$ and $A'$ both represent $X$ then $A \cong A'$ (since $H_A \cong X \cong H_{A'}$). More precisely, two universal elements $(A, u)$, $(A', u')$ are related by a unique arrow $j \colon A \to A'$ with $X(j)(u') = u$, and $j$ is an isomorphism.

What is a "Yoneda-style" proof that $A \cong B$?
?
Produce a chain of bijections $\mathcal{A}(C, A) \cong \cdots \cong \mathcal{A}(C, B)$, each natural in $C$ (or the same with $\mathcal{A}(A, C)$ and $\mathcal{A}(B, C)$), and cite $H_A \cong H_B \Rightarrow A \cong B$. No arrow $A \to B$ is written down. Example: two left adjoints of $G$ agree on objects, because $F(A)$ and $F'(A)$ both represent $\mathcal{A}(A, G(-))$.
