#flashcards/part6

## 6A: Limits via Representables & Adjoints

Definition: the diagonal functor $\Delta \colon \mathcal{A} \to [\mathbf{I}, \mathcal{A}]$.
?
$\Delta A$ is the constant functor: every object of $\mathbf{I}$ goes to $A$, every map to $1_A$. For $g \colon A' \to A$, $\Delta g$ is the natural transformation all of whose components are $g$.

A cone on $D \colon \mathbf{I} \to \mathcal{A}$ with vertex $A$ is the same thing as what kind of natural transformation?
?
A natural transformation $\Delta A \Rightarrow D$. The naturality square at $u \colon I \to J$ has $1_A$ on one side, so it collapses to the cone triangle $Du \circ f_I = f_J$. Hence $\mathrm{Cone}(A, D) = [\mathbf{I}, \mathcal{A}](\Delta A, D)$.

Definition: the cone functor of a diagram $D$.
?
$\mathrm{Cone}(-, D) \colon \mathcal{A}^{\mathrm{op}} \to \mathbf{Set}$ sends $A$ to the set of cones on $D$ with vertex $A$, and $g \colon A' \to A$ to "compose in front": $(f_I)_I \mapsto (f_I \circ g)_I$. ($\mathcal{A}$ locally small, $\mathbf{I}$ small.)

State: limits as representations.
?
A cone $(p_I \colon L \to D(I))$ is a limit cone if and only if $g \mapsto (p_I \circ g)_I$ is a bijection $\mathcal{A}(A, L) \to \mathrm{Cone}(A, D)$ for every $A$; these bijections are then natural in $A$. Conversely a natural isomorphism $\alpha \colon H_L \cong \mathrm{Cone}(-, D)$ gives the limit cone $\alpha_L(1_L)$.

In the universal property of a limit, which half is surjectivity and which is injectivity of $g \mapsto (p_I g)_I$?
?
"There exists a mediating map" is surjectivity. "It is unique" is injectivity.

What technique recovers the limit cone from a representation $H_L \cong \mathrm{Cone}(-, D)$?
?
Follow the identity (Yoneda): the limit cone is the image of $1_L$, and the natural isomorphism is then forced to be "compose with that cone".

How is $\lim \alpha \colon \lim D \to \lim D'$ defined for a natural transformation $\alpha \colon D \Rightarrow D'$?
?
As the unique map with $p^{D'}_I \circ \lim \alpha = \alpha_I \circ p^D_I$ for all $I$. Before using uniqueness you must check that $(\alpha_I p^D_I)_I$ is a cone on $D'$.

State: limits as an adjoint.
?
If $\mathbf{I}$ is small and $\mathcal{A}$ is locally small with all limits of shape $\mathbf{I}$, then $\lim \colon [\mathbf{I}, \mathcal{A}] \to \mathcal{A}$ is right adjoint to $\Delta$: $[\mathbf{I}, \mathcal{A}](\Delta A, D) \cong \mathcal{A}(A, \lim D)$ naturally in $A$ and $D$. Dually $\mathrm{colim} \dashv \Delta$.

What is the counit of $\Delta \dashv \lim$ at $D$?
?
The limit cone itself, $(p^D_I \colon \lim D \to D(I))_I$, viewed as a natural transformation $\Delta(\lim D) \Rightarrow D$.

How do you remember which side of $\Delta$ the functor $\lim$ is on?
?
Test with products: maps *into* $X \times Y$ are pairs of maps, so $\lim$ sits in the second slot of a hom-set, where right adjoints sit. $\mathrm{colim} \dashv \Delta \dashv \lim$.

State: representables preserve limits.
?
For $\mathcal{A}$ locally small and any object $A$, the functor $\mathcal{A}(A, -) \colon \mathcal{A} \to \mathbf{Set}$ sends every limit cone to a limit cone: $\mathcal{A}(A, \lim D) \cong \lim \mathcal{A}(A, D(-))$, the right-hand limit taken in $\mathbf{Set}$.

What proof technique shows that $\mathcal{A}(A, -)$ preserves limits?
?
Work one element at a time: an element $s$ of the vertex of a cone in $\mathbf{Set}$ gives a cone in $\mathcal{A}$ with vertex $A$; the universal property in $\mathcal{A}$ turns it into one map $A \to L$, which is the value of the mediating function at $s$.

Give an example showing representables need not preserve colimits.
?
$\mathbf{Set}(2, 1 + 1)$ has $4$ elements, but $\mathbf{Set}(2, 1) + \mathbf{Set}(2, 1)$ has $2$.

Why is "a bijection $\mathcal{A}(A, L) \cong \mathrm{Cone}(A, D)$ for each $A$" not enough to make $L$ a limit?
?
A representation needs the bijections to be natural in $A$. Without naturality, Yoneda cannot be applied and no limit cone is determined.

## 6B: Limits & Colimits of Presheaves

Definition: the evaluation functor $\mathrm{ev}_A \colon [\mathcal{A}, \mathcal{S}] \to \mathcal{S}$.
?
It sends a functor $X$ to $X(A)$ and a natural transformation $\alpha$ to its component $\alpha_A$. For a diagram $D \colon \mathbf{I} \to [\mathcal{A}, \mathcal{S}]$, the composite $D_A = \mathrm{ev}_A \circ D$ is the diagram $I \mapsto D(I)(A)$ in $\mathcal{S}$.

State: limits in functor categories are computed pointwise.
?
Let $\mathcal{A}, \mathbf{I}$ be small, $\mathcal{S}$ locally small, $D \colon \mathbf{I} \to [\mathcal{A}, \mathcal{S}]$, and suppose each $D_A$ has a limit. Then (a) there is a cone on $D$ whose components at each $A$ form a limit cone on $D_A$; (b) any cone on $D$ with that property is a limit cone.

In the pointwise-limit theorem, how is the limit functor $L$ defined on a map $f \colon A \to A'$?
?
$L(f)$ is the unique map $L(A) \to L(A')$ with $p_{I,A'} \circ L(f) = D(I)(f) \circ p_{I,A}$ for all $I$. It exists because the right-hand family is a cone on $D_{A'}$, which uses naturality of each $D(u)$.

What is joint monicity of limit projections, and why is it the main tool in functor-category proofs?
?
If $p_I g = p_I g'$ for all $I$ then $g = g'$. It replaces "two functions agree on every element" when the target category has no elements: to prove two maps into a limit equal, compose with every projection.

Corollary of the pointwise theorem when $\mathcal{S}$ has all limits of shape $\mathbf{I}$.
?
$[\mathcal{A}, \mathcal{S}]$ has all limits of shape $\mathbf{I}$ and every $\mathrm{ev}_A$ preserves them. In particular $[\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$ has all small limits and colimits, computed pointwise.

Does the Yoneda embedding preserve limits? Colimits?
?
For small $\mathcal{A}$, $H_\bullet \colon \mathcal{A} \to [\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$ preserves limits (evaluate at each $B$ and use that $\mathcal{A}(B, -)$ preserves limits). It does not preserve colimits: $H_0$ of an initial object $0$ is not the empty presheaf.

Definition: the category of elements $\mathbf{E}(X)$ of a presheaf $X$.
?
Objects are pairs $(A, x)$ with $x \in X(A)$. A map $(A', x') \to (A, x)$ is a map $f \colon A' \to A$ of $\mathcal{A}$ with $(Xf)(x) = x'$. The projection $P \colon \mathbf{E}(X) \to \mathcal{A}$ forgets the element.

In $\mathbf{E}(X)$, which element does $Xf$ get applied to, and why?
?
To $x$, the element over the codomain $A$ of $f \colon A' \to A$. $X$ is contravariant, so $Xf \colon X(A) \to X(A')$; applying it to $x'$ would not make sense.

What is the category of elements of a directed graph (a presheaf on $V \rightrightarrows E$)?
?
The subdivided graph: one object per vertex and per edge, and for each edge one arrow from its source vertex and one from its target vertex into the edge.

State the density theorem.
?
For a small category $\mathcal{A}$ and a presheaf $X$, $X$ is the colimit of $\mathbf{E}(X) \xrightarrow{P} \mathcal{A} \xrightarrow{H_\bullet} [\mathcal{A}^{\mathrm{op}}, \mathbf{Set}]$, with colimit cocone $(\tilde{x} \colon H_A \Rightarrow X)_{(A,x)}$, where $\tilde{x}$ corresponds to $x$ under Yoneda.

What is the key technique in the proof of the density theorem?
?
Translate with Yoneda: a natural transformation out of $H_A$ is an element. A cocone becomes a family of elements $y_{(A,x)} \in Y(A)$, the mediating map is forced to be $\theta_A(x) = y_{(A,x)}$, and the cocone condition is exactly naturality of $\theta$.

What does the density theorem say for $\mathcal{A} = \mathbf{1}$?
?
A presheaf is a set $X$, $\mathbf{E}(X)$ is discrete on the elements of $X$, and the theorem reads $X \cong \coprod_{x \in X} 1$: every set is the disjoint union of its one-element subsets.

Is every presheaf a sum (coproduct) of representables?
?
No. It is a colimit of representables, and the gluing maps matter. A graph consisting of one vertex with one loop is not a sum of copies of $H_V$ and $H_E$.

## 6C: Adjoints & Limits

State: adjoints and limits.
?
If $F \dashv G$ then the right adjoint $G$ preserves limits and the left adjoint $F$ preserves colimits. The categories are locally small (as in 6A); nothing is assumed about which limits exist.

The short proof that right adjoints preserve limits.
?
$\mathcal{A}(A, G(L)) \cong \mathcal{B}(F(A), L) \cong \mathrm{Cone}(F(A), D) \cong \mathrm{Cone}(A, G \circ D)$, naturally in $A$: adjunction, then $L$ represents cones on $D$, then the adjunction on each component of a cone.

What makes that chain of isomorphisms a legitimate proof?
?
(1) Transposing a cone componentwise gives a cone (naturality of transposition). (2) Following $f$ through the chain shows the composite is $f \mapsto (G p_I \circ f)_I$, so the limit cone is exactly $(G p_I)$. (3) The chain never assumes $\lim (G \circ D)$ exists; it produces it.

How do you use "right adjoints preserve limits" to show a functor has no adjoint?
?
Contrapositive. A functor that fails to preserve some limit has no left adjoint; one that fails to preserve some colimit has no right adjoint. Example: $U \colon \mathbf{Grp} \to \mathbf{Set}$ does not preserve the initial object, so it has no right adjoint.

Definition: complete poset; an order-preserving map that preserves meets.
?
Every subset $S$ has a meet $\bigwedge S$, including $S = \emptyset$ (the greatest element) and infinite $S$. $G$ preserves meets if $G(\bigwedge S)$ is a meet of $\{G(s) : s \in S\}$ for every $S$.

State the adjoint functor theorem for posets, with the formula for the adjoint.
?
For a poset $A$, a complete poset $B$ and order-preserving $G \colon B \to A$: $G$ has a left adjoint if and only if $G$ preserves meets. Then $F(a) = \bigwedge \{ b \in B : a \le G(b) \}$.

What is the key step in building the left adjoint of a meet-preserving map?
?
Showing $a \le G(F(a))$: since $G$ preserves meets, $G(F(a))$ is the greatest lower bound of $\{G(b) : a \le G(b)\}$, and $a$ is a lower bound of that set. So the meet of "everything above" is itself above.

Definition: weakly initial set.
?
A *set* $\mathcal{S}$ of objects of a category such that every object receives at least one map from some member of $\mathcal{S}$. For $(A \Rightarrow G)$ this is the solution set condition.

State the General Adjoint Functor Theorem.
?
Let $\mathcal{A}$ be a category, $\mathcal{B}$ complete and locally small, $G \colon \mathcal{B} \to \mathcal{A}$ a functor, and suppose each comma category $(A \Rightarrow G)$ has a weakly initial set. Then $G$ has a left adjoint if and only if $G$ preserves limits.

State the Special Adjoint Functor Theorem.
?
Let $\mathcal{A}$ be locally small, and $\mathcal{B}$ complete, locally small, well-powered and with a coseparating set. Then $G \colon \mathcal{B} \to \mathcal{A}$ has a left adjoint if and only if $G$ preserves limits.

Definitions: well-powered; coseparating set.
?
Well-powered: for each object, the monics into it form a set up to isomorphism. Coseparating set: a set $\mathcal{Q}$ of objects such that for any parallel $f \ne g \colon B \to B'$ there are $Q \in \mathcal{Q}$ and $h \colon B' \to Q$ with $hf \ne hg$.

Why can the size condition in the adjoint functor theorems not be dropped?
?
The opposite of the ordered class of ordinals is complete and locally small, and its functor to $\mathbf{1}$ preserves limits, but a left adjoint would be a greatest ordinal. No set of ordinals is weakly initial there.

Definition: cartesian closed category.
?
A category with finite products in which, for each object $B$, the functor $- \times B$ has a right adjoint $(-)^B$: $\mathcal{A}(A \times B, C) \cong \mathcal{A}(A, C^B)$ naturally in $A$ and $C$.

Why are $\mathbf{Vect}_k$ and $\mathbf{Grp}$ not cartesian closed?
?
In a cartesian closed category $- \times B$ is a left adjoint, so it preserves the initial object: $0 \times B \cong 0$. In $\mathbf{Vect}_k$ and $\mathbf{Grp}$ the initial object is also terminal, so $0 \times B \cong B$, which would force every $B$ to be $0$.

## 6D: Monads

Definition: a monad on a category $\mathcal{A}$.
?
A functor $T \colon \mathcal{A} \to \mathcal{A}$ with natural transformations $\eta \colon 1 \Rightarrow T$ and $\mu \colon TT \Rightarrow T$ such that $\mu_A \circ T(\mu_A) = \mu_A \circ \mu_{TA}$ (associativity) and $\mu_A \circ \eta_{TA} = 1_{TA} = \mu_A \circ T(\eta_A)$ (unit laws).

Describe the free monoid monad and the power set monad on $\mathbf{Set}$.
?
Free monoid: $TX$ = finite words in $X$; $\eta$ = one-letter word; $\mu$ = concatenate a word of words. Power set: $TX = \mathscr{P}(X)$ with direct images; $\eta_X(x) = \{x\}$; $\mu$ = union of a set of subsets.

What monad does an adjunction $F \dashv G$ (unit $\eta$, counit $\varepsilon$) induce, and on which category?
?
On the domain $\mathcal{A}$ of the left adjoint $F \colon \mathcal{A} \to \mathcal{B}$: $T = GF$, unit $\eta$, multiplication $\mu_A = G(\varepsilon_{F(A)})$.

Which facts prove the monad axioms for $(GF, \eta, G\varepsilon F)$?
?
Each unit law is one triangle identity. Associativity is naturality of $\varepsilon$ at the map $\varepsilon_{F(A)}$, followed by applying $G$.

Definition: a $T$-algebra and a map of $T$-algebras.
?
An object $A$ with a map $a \colon TA \to A$ such that $a \circ \eta_A = 1_A$ and $a \circ \mu_A = a \circ T(a)$. A map $(A, a) \to (B, b)$ is $f \colon A \to B$ with $f \circ a = b \circ T(f)$. Together they form the Eilenberg–Moore category $\mathcal{A}^T$.

What is the free $T$-algebra on $A$, and why is it an algebra?
?
$(TA, \mu_A)$. Its unit axiom is the first unit law of the monad and its associativity axiom is the associativity law of the monad.

Describe the Eilenberg–Moore adjunction.
?
$F^T \colon \mathcal{A} \to \mathcal{A}^T$, $A \mapsto (TA, \mu_A)$, is left adjoint to the forgetful $U^T$. The unit is $\eta$ and the counit at $(A, a)$ is $a$ itself. It induces the monad $T$.

Definition: the Kleisli category $\mathcal{A}_T$.
?
Same objects as $\mathcal{A}$; a map $A \rightsquigarrow B$ is a map $A \to TB$ of $\mathcal{A}$; the identity on $A$ is $\eta_A$; the composite of $f \colon A \to TB$ and $g \colon B \to TC$ is $g \bullet f = \mu_C \circ T(g) \circ f$.

Describe the Kleisli adjunction.
?
$F_T(A) = A$, $F_T(f) = \eta_B \circ f$; $U_T(A) = TA$, $U_T(g) = \mu_B \circ T(g)$. $F_T \dashv U_T$, the hom-set bijection is the identity $\mathcal{A}_T(A, B) = \mathcal{A}(A, TB)$, and it induces the monad $T$.

Definition: the comparison functor, and a monadic functor.
?
For $F \dashv G$ with $T = GF$: $K \colon \mathcal{B} \to \mathcal{A}^T$, $K(B) = (G(B), G(\varepsilon_B))$, $K(q) = G(q)$, with $U^T K = G$ and $K F = F^T$. $G$ is monadic if $K$ is an equivalence of categories.

Give a monadic functor and a non-monadic right adjoint.
?
$\mathbf{Mon} \to \mathbf{Set}$ and $\mathbf{Grp} \to \mathbf{Set}$ are monadic. $\mathbf{Top} \to \mathbf{Set}$ is not: its monad is the identity monad, whose algebras are just sets, and the comparison functor is the forgetful functor, which is not full.

What does Beck's monadicity theorem characterise (statement only)?
?
For $G$ with a left adjoint: the comparison functor $K$ is an isomorphism of categories if and only if $G$ (strictly) creates coequalizers of those parallel pairs $f, g$ for which $G(f), G(g)$ has a split coequalizer. The up-to-isomorphism version characterises $K$ being an equivalence.

What is a monad on a poset, and what are its algebras?
?
A closure operator: order-preserving $T$ with $p \le T(p)$ and $T(T(p)) \le T(p)$. The axioms are automatic because every diagram in a poset commutes. Its algebras are the closed elements, $T(p) = p$, and the Eilenberg–Moore adjunction is $T \colon P \to \mathrm{Cl}(T)$ left adjoint to the inclusion.

For a Galois connection $F \dashv G$ between posets, when is the comparison map $K \colon Q \to \mathrm{Cl}(GF)$ an isomorphism?
?
Exactly when $G$ reflects the order ($G(q) \le G(q') \Rightarrow q \le q'$). $K$ is always order-preserving and surjective.
