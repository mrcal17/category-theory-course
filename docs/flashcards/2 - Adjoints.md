#flashcards/part2

## 2A: Adjunctions: Definition & Examples

State the definition of an adjunction $F \dashv G$ between $F \colon \mathcal{A} \to \mathcal{B}$ and $G \colon \mathcal{B} \to \mathcal{A}$.
?
For every $A$ in $\mathcal{A}$ and $B$ in $\mathcal{B}$, a bijection $\mathcal{B}(F(A), B) \to \mathcal{A}(A, G(B))$, $g \mapsto \bar{g}$ (inverse $f \mapsto \bar{f}$), satisfying the two naturality equations (N1) and (N2). $F$ is the left adjoint, $G$ the right adjoint.

Write out the naturality equation (N1), naturality in $B$.
?
For all $g \colon F(A) \to B$ and $q \colon B \to B'$ in $\mathcal{B}$: $\overline{q \circ g} = G(q) \circ \bar{g}$.

Write out the naturality equation (N2), naturality in $A$.
?
For all $p \colon A' \to A$ and $f \colon A \to G(B)$ in $\mathcal{A}$: $\overline{f \circ p} = \bar{f} \circ F(p)$.

What are the inverse-direction naturality equations (N1') and (N2')?
?
(N1'): $\overline{G(q) \circ f} = q \circ \bar{f}$ for $f \colon A \to G(B)$, $q \colon B \to B'$. (N2'): $\overline{g \circ F(p)} = \bar{g} \circ p$ for $g \colon F(A) \to B$, $p \colon A' \to A$.

In $F \dashv G$, which functor appears in which slot of which hom-set?
?
$F$ in the left slot of $\mathcal{B}(F(A), B)$; $G$ in the right slot of $\mathcal{A}(A, G(B))$. Arrows *out of* $F(A)$ correspond to arrows *into* $G(B)$.

What five things must be checked to prove $F \dashv G$ from the definition?
?
(1) $\bar{g}$ is defined and is an arrow of $\mathcal{A}$; (2) $\bar{f}$ is defined and is an arrow of $\mathcal{B}$; (3) both round trips $\bar{\bar{g}} = g$, $\bar{\bar{f}} = f$; (4) (N1); (5) (N2).

For the free monoid adjunction $F \dashv U$ between $\mathbf{Set}$ and $\mathbf{Mon}$, what are the two transposes?
?
For a homomorphism $g \colon F(S) \to M$: $\bar{g}(s) = g((s))$, restriction to one-letter words. For a function $f \colon S \to U(M)$: $\bar{f}(s_1 \cdots s_n) = f(s_1) \cdots f(s_n)$, with the empty word going to $1_M$.

What are the left and right adjoints of the forgetful functor $U \colon \mathbf{Top} \to \mathbf{Set}$?
?
$D \dashv U \dashv I$: the discrete-space functor $D$ is left adjoint to $U$, the indiscrete-space functor $I$ is right adjoint to $U$.

Define initial object and terminal object.
?
$I$ is initial in $\mathcal{A}$ if for every object $A$ there is exactly one arrow $I \to A$. $T$ is terminal if for every object $A$ there is exactly one arrow $A \to T$.

In what sense is an initial object unique, and what technique proves it?
?
Between any two initial objects there is exactly one isomorphism. Technique: a uniqueness argument. Initiality gives arrows each way; each composite is an arrow from an initial object to itself, and there is only one of those, the identity.

How are initial and terminal objects adjoints?
?
For the unique functor $! \colon \mathcal{A} \to \mathbf{1}$: a functor $\mathbf{1} \to \mathcal{A}$ is left adjoint to $!$ iff it picks out an initial object, and right adjoint to $!$ iff it picks out a terminal object.

What is a Galois connection between posets $P$ and $Q$?
?
Order-preserving maps $f \colon P \to Q$ and $g \colon Q \to P$ with $f(a) \le b \iff a \le g(b)$ for all $a \in P$, $b \in Q$. It is exactly an adjunction $f \dashv g$ between the posets regarded as categories; naturality is automatic.

If $f \dashv g$ is a Galois connection, what is the formula for $g(b)$ in terms of $f$?
?
$g(b)$ is the greatest element of $\{a \in P : f(a) \le b\}$. So a right adjoint between posets is unique when it exists.

State the adjunctions involving products and function sets in $\mathbf{Set}$.
?
$\Delta \dashv \times$: $\mathbf{Set}(A, X) \times \mathbf{Set}(A, Y) \cong \mathbf{Set}(A, X \times Y)$. And $(- \times B) \dashv (-)^B$: $\mathbf{Set}(A \times B, C) \cong \mathbf{Set}(A, C^B)$, with $\bar{g}(a) = g(a, -)$.

## 2B: Units & Counits

Define the unit of an adjunction $F \dashv G$. Which way does it point?
?
$\eta_A = \overline{1_{F(A)}} \colon A \to GF(A)$, the transpose of the identity on $F(A)$. It is a natural transformation $\eta \colon 1_{\mathcal{A}} \Rightarrow GF$.

Define the counit of an adjunction $F \dashv G$. Which way does it point?
?
$\varepsilon_B = \overline{1_{G(B)}} \colon FG(B) \to B$, the transpose of the identity on $G(B)$. It is a natural transformation $\varepsilon \colon FG \Rightarrow 1_{\mathcal{B}}$.

How is the transpose of $g \colon F(A) \to B$ computed from the unit?
?
$\bar{g} = G(g) \circ \eta_A$, the composite $A \to GF(A) \to G(B)$.

How is the transpose of $f \colon A \to G(B)$ computed from the counit?
?
$\bar{f} = \varepsilon_B \circ F(f)$, the composite $F(A) \to FG(B) \to B$.

State the two triangle identities.
?
$\varepsilon_{F(A)} \circ F(\eta_A) = 1_{F(A)}$ for every $A$ in $\mathcal{A}$, and $G(\varepsilon_B) \circ \eta_{G(B)} = 1_{G(B)}$ for every $B$ in $\mathcal{B}$.

What technique proves $\bar{g} = G(g) \circ \eta_A$?
?
Insert an identity and use naturality: $\bar{g} = \overline{g \circ 1_{F(A)}} = G(g) \circ \overline{1_{F(A)}}$ by (N1). A "follow the identity" argument.

What technique proves that the unit is natural?
?
Show the two sides of the naturality square have the same transpose (both transpose to $F(p)$), then use that transposition is injective.

State the theorem relating the two definitions of adjunction.
?
For functors $F \colon \mathcal{A} \to \mathcal{B}$, $G \colon \mathcal{B} \to \mathcal{A}$ there is a one-to-one correspondence between adjunctions (natural hom-set bijections) with $F$ on the left and pairs of natural transformations $\eta \colon 1 \Rightarrow GF$, $\varepsilon \colon FG \Rightarrow 1$ satisfying the triangle identities.

Given $(\eta, \varepsilon)$ satisfying the triangle identities, what three moves show that $g \mapsto G(g) \circ \eta_A$ and $f \mapsto \varepsilon_B \circ F(f)$ are mutually inverse?
?
Functoriality (split the composite), one naturality square (slide $g$ past $\varepsilon$, or $f$ past $\eta$), one triangle identity (cancel).

To prove $F \dashv G$ by the unit–counit route, what four things must be checked?
?
$\eta$ is natural; $\varepsilon$ is natural; the first triangle identity; the second triangle identity.

What are the unit and counit of the free monoid adjunction?
?
Unit $S \to UF(S)$: $s \mapsto (s)$, a letter as a one-letter word. Counit $FU(M) \to M$: multiply out a word of elements of $M$.

What are the unit and counit of $(- \times B) \dashv (-)^B$ in $\mathbf{Set}$?
?
Unit $A \to (A \times B)^B$: $a \mapsto (b \mapsto (a, b))$. Counit $C^B \times B \to C$: evaluation $(h, b) \mapsto h(b)$.

For order-preserving maps $f \colon P \to Q$, $g \colon Q \to P$, restate $f \dashv g$ using unit and counit.
?
$a \le g(f(a))$ for all $a \in P$ and $f(g(b)) \le b$ for all $b \in Q$. Naturality and the triangle identities are automatic in a poset.

Define a closure operator on a poset $P$, and say how a Galois connection produces one.
?
A map $c \colon P \to P$ that is order-preserving, extensive ($a \le c(a)$) and idempotent ($c(c(a)) = c(a)$). If $f \dashv g$ then $c = g \circ f$ is a closure operator; idempotence comes from $f g f = f$, the poset form of a triangle identity.

## 2C: Adjunctions via Initial Objects

Define the comma category $(P \Rightarrow Q)$ for functors $P \colon \mathcal{A} \to \mathcal{C}$ and $Q \colon \mathcal{B} \to \mathcal{C}$.
?
Objects: triples $(A, h, B)$ with $h \colon P(A) \to Q(B)$ in $\mathcal{C}$. Arrows $(A, h, B) \to (A', h', B')$: pairs $(f \colon A \to A', g \colon B \to B')$ with $Q(g) \circ h = h' \circ P(f)$. Composition and identities are componentwise.

Define the slice category $\mathcal{A}/A$.
?
The comma category $(1_{\mathcal{A}} \Rightarrow A)$. Objects: pairs $(X, h)$ with $h \colon X \to A$. Arrows $(X, h) \to (X', h')$: arrows $f \colon X \to X'$ with $h' \circ f = h$.

Define the coslice category $A/\mathcal{A}$.
?
The comma category $(A \Rightarrow 1_{\mathcal{A}})$. Objects: pairs $(X, h)$ with $h \colon A \to X$. Arrows $(X, h) \to (X', h')$: arrows $f \colon X \to X'$ with $f \circ h = h'$.

Which object of the slice $\mathcal{A}/A$ is terminal, and why?
?
$(A, 1_A)$. An arrow $(X, h) \to (A, 1_A)$ is an $f \colon X \to A$ with $1_A \circ f = h$, that is $f = h$: exactly one solution.

For $G \colon \mathcal{B} \to \mathcal{A}$ and $A$ in $\mathcal{A}$, describe the category $(A \Rightarrow G)$.
?
Objects: pairs $(B, f)$ with $B$ in $\mathcal{B}$ and $f \colon A \to G(B)$ in $\mathcal{A}$. Arrows $(B, f) \to (B', f')$: arrows $q \colon B \to B'$ of $\mathcal{B}$ with $G(q) \circ f = f'$.

What is a universal arrow from $A$ to $G$? Write the property out in full.
?
An initial object $(B_0, u)$ of $(A \Rightarrow G)$: for every $B$ in $\mathcal{B}$ and every $f \colon A \to G(B)$ there is exactly one $q \colon B_0 \to B$ in $\mathcal{B}$ with $G(q) \circ u = f$.

What does the unit of an adjunction $F \dashv G$ have to do with comma categories?
?
For every $A$, $(F(A), \eta_A)$ is an initial object of $(A \Rightarrow G)$: every $f \colon A \to G(B)$ factors as $G(q) \circ \eta_A$ for exactly one $q \colon F(A) \to B$ (namely $q = \bar{f}$).

What technique proves that $(F(A), \eta_A)$ is initial in $(A \Rightarrow G)$?
?
Rewrite the condition $G(q) \circ \eta_A = f$ as $\bar{q} = f$ using $\bar{q} = G(q) \circ \eta_A$ (2B), then use that transposition is a bijection: "bijection" and "exactly one" are the same statement.

State the theorem describing adjunctions via initial objects.
?
For functors $F \colon \mathcal{A} \to \mathcal{B}$, $G \colon \mathcal{B} \to \mathcal{A}$: adjunctions $F \dashv G$ correspond one-to-one to natural transformations $\eta \colon 1_{\mathcal{A}} \Rightarrow GF$ such that each $(F(A), \eta_A)$ is initial in $(A \Rightarrow G)$. The adjunction is sent to its unit.

In that theorem, how is the counit recovered from $\eta$?
?
$\varepsilon_B$ is the unique arrow $(FG(B), \eta_{G(B)}) \to (B, 1_{G(B)})$ in $(G(B) \Rightarrow G)$: the unique $\varepsilon_B \colon FG(B) \to B$ with $G(\varepsilon_B) \circ \eta_{G(B)} = 1_{G(B)}$.

What is an "initial-object argument" for proving two arrows equal?
?
Show that both are arrows of a comma category out of the same initial object and into the same object (same $B$ and same arrow component). Since there is exactly one such arrow, they are equal. Each membership must be verified first.

When does a functor $G \colon \mathcal{B} \to \mathcal{A}$ have a left adjoint?
?
Exactly when, for every object $A$ of $\mathcal{A}$, the comma category $(A \Rightarrow G)$ has an initial object.

Given initial objects $(F(A), \eta_A)$ of each $(A \Rightarrow G)$, how is $F$ defined on an arrow $p \colon A' \to A$?
?
$F(p)$ is the unique arrow $F(A') \to F(A)$ with $G(F(p)) \circ \eta_{A'} = \eta_A \circ p$. Functoriality follows from the uniqueness; the defining equation is naturality of $\eta$.

In what sense are left adjoints unique, and what proves it?
?
If $F \dashv G$ and $F' \dashv G$ then there is a unique natural transformation $\alpha \colon F \Rightarrow F'$ with $G(\alpha_A) \circ \eta_A = \eta'_A$, and it is a natural isomorphism. Proof: both $(F(A), \eta_A)$ and $(F'(A), \eta'_A)$ are initial in $(A \Rightarrow G)$, and initial objects are unique up to unique isomorphism.
