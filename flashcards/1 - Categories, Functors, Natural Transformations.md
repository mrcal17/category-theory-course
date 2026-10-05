#flashcards/part1

## 1A: Categories

What data make up a category $\mathcal{A}$?
?
A collection of objects; for each pair of objects $A, B$ a collection $\mathcal{A}(A, B)$ of arrows from $A$ to $B$; for each triple $A, B, C$ a composition function $\mathcal{A}(B, C) \times \mathcal{A}(A, B) \to \mathcal{A}(A, C)$, $(g, f) \mapsto g \circ f$; and for each object $A$ an identity arrow $1_A \in \mathcal{A}(A, A)$.

State the two axioms of a category, with their quantifiers.
?
Associativity: for all $f \colon A \to B$, $g \colon B \to C$, $h \colon C \to D$, $(h \circ g) \circ f = h \circ (g \circ f)$. Identity laws: for all $f \colon A \to B$, $f \circ 1_A = f = 1_B \circ f$.

When is the composite $g \circ f$ defined?
?
Exactly when the codomain of $f$ equals the domain of $g$: $f \colon A \to B$ and $g \colon B \to C$. Then $g \circ f \colon A \to C$.

To prove "these objects and arrows form a category", what four things must be verified?
?
(1) The composite of two permitted arrows is a permitted arrow between the right objects (closure). (2) Each identity is a permitted arrow. (3) Associativity. (4) Both identity laws.

In a category of sets-with-structure such as $\mathbf{Grp}$, which parts of the verification have real content, and why?
?
Closure: a composite of homomorphisms is a homomorphism, and the identity function is a homomorphism. Associativity and the identity laws are inherited from composition of functions.

What is the hom-set $\mathcal{A}(A, B)$?
?
The collection of all arrows of $\mathcal{A}$ with domain $A$ and codomain $B$. The order matters: $\mathcal{A}(A, B)$ and $\mathcal{A}(B, A)$ are different, and different hom-sets share no arrows.

How is a monoid $(M, \cdot, e)$ a category?
?
One object $\star$; the arrows $\star \to \star$ are the elements of $M$; composition is $g \circ f = g \cdot f$; the identity arrow is $e$. Conversely, in any one-object category the arrows form a monoid under composition.

How is a preorder $(P, \le)$ a category?
?
Objects are the elements of $P$; there is exactly one arrow $x \to y$ if $x \le y$ and none otherwise. Transitivity supplies composites, reflexivity supplies identities.

Why do associativity and the identity laws hold automatically in the category of a preorder?
?
Each axiom is an equation between two arrows in the same hom-set, and every hom-set has at most one element, so any two such arrows are equal. Technique: "the hom-set has at most one element".

What is a discrete category?
?
A category whose only arrows are identities: $\mathcal{A}(A, B)$ is empty for $A \neq B$ and $\mathcal{A}(A, A) = \{1_A\}$. A discrete category amounts to a set (its set of objects).

Why may you not write $f(a)$ in a proof about an arbitrary category?
?
Objects of a general category need not be sets and arrows need not be functions (think of a monoid or a poset as a category). Only composition, associativity and the identity laws are available.

Give a reflexive, symmetric relation on $\mathbb{R}$ whose "arrows" do not form a category, and say what fails.
?
One arrow $x \to y$ when $|x - y| \le 1$. There are arrows $0 \to 1$ and $1 \to 2$ but none $0 \to 2$, so composition cannot be defined (the relation is not transitive).

What technique proves that an arrow with the defining property of an identity must equal the identity?
?
A uniqueness argument: form one expression involving both candidates and simplify it in two ways, once with each candidate's defining property.

In the course's finite-category encoding, what does `compose[(g, f)]` mean and when must the key exist?
?
It is the name of $g \circ f$. The key `(g, f)` must exist exactly when the codomain of `f` equals the domain of `g`.

## 1B: Isomorphisms, Duality & New Categories from Old

Define: $f \colon A \to B$ is an isomorphism.
?
There exists $g \colon B \to A$ with $g \circ f = 1_A$ and $f \circ g = 1_B$. Both equations are required. $g$ is the inverse of $f$, written $f^{-1}$, and $A \cong B$ means some isomorphism $A \to B$ exists.

State "inverses are unique" and name the technique that proves it.
?
If $g$ and $g'$ are both inverses of $f$ then $g = g'$. Technique: the sandwich $g \circ f \circ g'$, bracketed two ways. The argument only needs $g$ to be a left inverse and $g'$ a right inverse.

Why is isomorphism defined by an inverse arrow and not by "bijective"?
?
A general category has no elements, so "bijective" is meaningless there. Even among structured sets it gives the wrong notion: in $\mathbf{Top}$ a continuous bijection such as $[0, 1) \to S^1$ need not have a continuous inverse.

Define monomorphism (monic).
?
$f \colon A \to B$ is monic if for every object $C$ and all $g, h \colon C \to A$, $f \circ g = f \circ h$ implies $g = h$. (Left-cancellable; test arrows go into the domain of $f$.)

Define epimorphism (epic).
?
$f \colon A \to B$ is epic if for every object $C$ and all $g, h \colon B \to C$, $g \circ f = h \circ f$ implies $g = h$. (Right-cancellable; test arrows go out of the codomain of $f$.)

What are the monics and the epics in $\mathbf{Set}$?
?
Monic means injective; epic means surjective. Proof idea for "monic implies injective": test against a one-element set, whose maps into $A$ pick out elements of $A$.

Give an arrow that is monic and epic but not an isomorphism.
?
The inclusion $(\mathbb{N}, +, 0) \to (\mathbb{Z}, +, 0)$ in $\mathbf{Mon}$; or the non-identity arrow of the poset $\{0 \le 1\}$, which has no arrow back.

If $g \circ f$ is monic, which of $f$, $g$ must be monic? If $g \circ f$ is epic?
?
If $g \circ f$ is monic then $f$ (the arrow applied first) is monic. If $g \circ f$ is epic then $g$ (the arrow applied second) is epic. The second statement is the dual of the first.

Define the opposite category $\mathcal{A}^{\mathrm{op}}$.
?
Same objects; $\mathcal{A}^{\mathrm{op}}(A, B) = \mathcal{A}(B, A)$; the composite of $A \xrightarrow{f} B \xrightarrow{g} C$ in $\mathcal{A}^{\mathrm{op}}$ is $f \circ g$ computed in $\mathcal{A}$; same identities.

State the principle of duality and say why it holds.
?
If a statement holds in every category, so does its dual (reverse every arrow and the order of every composite). Reason: the dual statement holds in $\mathcal{A}$ exactly when the original holds in $\mathcal{A}^{\mathrm{op}}$, which is a category.

What are the duals of: monic, domain, left inverse, isomorphism?
?
Epic, codomain, right inverse, isomorphism (self-dual).

Define the product category $\mathcal{A} \times \mathcal{B}$.
?
Objects are pairs $(A, B)$; arrows $(A, B) \to (A', B')$ are pairs $(f, g)$ with $f \colon A \to A'$ and $g \colon B \to B'$; composition is componentwise, $(f', g') \circ (f, g) = (f' \circ f, g' \circ g)$; identities are $(1_A, 1_B)$.

Define groupoid, and say what a one-object groupoid is.
?
A category in which every arrow is an isomorphism. A one-object groupoid is a group.

What are the monic arrows and the isomorphisms in a monoid regarded as a one-object category?
?
An arrow $m$ is monic when it is left-cancellable ($m g = m h \Rightarrow g = h$) and an isomorphism when it is an invertible element. In $(\mathbb{N}, +, 0)$ every arrow is monic and epic but only $0$ is an isomorphism.

## 1C: Functors

Define a functor $F \colon \mathcal{A} \to \mathcal{B}$.
?
A function on objects $A \mapsto F(A)$ and, for each pair $A, A'$, a function $\mathcal{A}(A, A') \to \mathcal{B}(F(A), F(A'))$, $f \mapsto F(f)$, such that $F(f' \circ f) = F(f') \circ F(f)$ for all composable $f, f'$ and $F(1_A) = 1_{F(A)}$ for all $A$.

What three things must be verified to show a construction is a functor?
?
(1) $F(f)$ is an arrow of $\mathcal{B}$ from $F(A)$ to $F(A')$ (including being a homomorphism, continuous, etc.). (2) Composition is preserved. (3) Identities are preserved. The last two are independent.

What is a functor between two monoids regarded as one-object categories? Between two posets?
?
A monoid homomorphism. An order-preserving map.

What does a forgetful functor do? Give two examples.
?
It discards structure and keeps the rest: $\mathbf{Grp} \to \mathbf{Set}$ (underlying set, homomorphism as a function), $\mathbf{Vect}_k \to \mathbf{Ab}$ (forget scalar multiplication).

Describe the free monoid functor $W \colon \mathbf{Set} \to \mathbf{Mon}$.
?
$W(S)$ is the monoid of finite words in $S$ under concatenation, with the empty word as unit. $W(f)$ applies $f$ letter by letter.

Define a contravariant functor from $\mathcal{A}$ to $\mathcal{B}$ and unpack it.
?
A functor $\mathcal{A}^{\mathrm{op}} \to \mathcal{B}$. Unpacked: $f \colon A \to A'$ is sent to $F(f) \colon F(A') \to F(A)$, with $F(f' \circ f) = F(f) \circ F(f')$ and $F(1_A) = 1_{F(A)}$.

Give two contravariant functors.
?
The power-set functor with preimages, $\mathbf{Set}^{\mathrm{op}} \to \mathbf{Set}$, $f \mapsto f^{-1}$; the dual space $\mathbf{Vect}_k^{\mathrm{op}} \to \mathbf{Vect}_k$, $f \mapsto (\theta \mapsto \theta \circ f)$.

Define the hom-functors $H^A$ and $H_A$.
?
$H^A = \mathcal{A}(A, -) \colon \mathcal{A} \to \mathbf{Set}$ sends $B$ to $\mathcal{A}(A, B)$ and $g$ to $p \mapsto g \circ p$. $H_A = \mathcal{A}(-, A) \colon \mathcal{A}^{\mathrm{op}} \to \mathbf{Set}$ sends $B$ to $\mathcal{A}(B, A)$ and $g$ to $q \mapsto q \circ g$.

Which axioms of $\mathcal{A}$ make $H^A$ a functor?
?
Associativity gives preservation of composition; the identity law $1_B \circ p = p$ gives preservation of identities. Technique: evaluate both sides at an arbitrary arrow $p$.

Define faithful and full.
?
$F$ is faithful (full) if for every pair of objects $A, A'$ the function $\mathcal{A}(A, A') \to \mathcal{B}(F(A), F(A'))$ is injective (surjective). These are conditions on each hom-set separately, not on the collection of all arrows.

Define essentially surjective on objects.
?
For every object $B$ of $\mathcal{B}$ there is an object $A$ of $\mathcal{A}$ with $F(A) \cong B$ (isomorphic, not necessarily equal).

Is the forgetful functor $U \colon \mathbf{Grp} \to \mathbf{Set}$ faithful? Full? Essentially surjective?
?
Faithful: yes. Full: no ($n \mapsto n + 1$ on $\mathbb{Z}$ is not a homomorphism). Essentially surjective: no (the empty set is not the underlying set of any group).

What is $\mathbf{Cat}$, and what must be proved for it to make sense?
?
The category of small categories and functors. One must prove that the composite of two functors is a functor (apply the preservation property of the inner functor, then of the outer), and note that composition of functors is associative with identity functors as identities.

Do functors preserve monics? What technique shows the answer?
?
No. A counterexample: a functor $\mathbf{2} \to \mathbf{Set}$ can send the arrow $u$ (monic in $\mathbf{2}$) to any function, including a non-injective one, because functors out of $\mathbf{2}$ correspond to arrows of the target.

## 1D: Natural Transformations

Definition: natural transformation $\alpha \colon F \Rightarrow G$ between functors $F, G \colon \mathcal{A} \to \mathcal{B}$
?
A family of arrows $\alpha_A \colon F(A) \to G(A)$ of $\mathcal{B}$, one for each object $A$ of $\mathcal{A}$, such that for every arrow $f \colon A \to A'$ of $\mathcal{A}$: $G(f) \circ \alpha_A = \alpha_{A'} \circ F(f)$.

What are the three things to check to show a family is a natural transformation $F \Rightarrow G$?
?
(1) $F$ and $G$ have the same domain, the same codomain and the same variance. (2) Each $\alpha_A$ is an arrow of $\mathcal{B}$ from $F(A)$ to $G(A)$ (a homomorphism, linear map, ... as required). (3) The naturality square commutes for **every** arrow $f$ of $\mathcal{A}$.

Describe the naturality square of $\alpha \colon F \Rightarrow G$ at $f \colon A \to A'$.
?
Top edge $F(f) \colon F(A) \to F(A')$, bottom edge $G(f) \colon G(A) \to G(A')$, left edge $\alpha_A$, right edge $\alpha_{A'}$. Commuting means the two routes $F(A) \to G(A')$ are equal.

In what sense is the determinant a natural transformation, and what technique proves it?
?
$\det \colon M_n \Rightarrow U$ between functors $\mathbf{CRing} \to \mathbf{Mon}$: for every ring homomorphism $\varphi \colon R \to S$, $\varphi(\det X) = \det(\varphi \text{ applied to each entry of } X)$. Technique: the determinant is one formula in the ring operations, and $\varphi$ preserves them.

What is a natural transformation between two functors $G \to \mathbf{Set}$, for a group $G$ regarded as a one-object category?
?
A $G$-equivariant map between the two $G$-sets: a function $\alpha$ with $\alpha(g \cdot s) = g \cdot \alpha(s)$ for all $g$ and $s$.

When is there a natural transformation $F \Rightarrow G$ between order-preserving maps $F, G \colon P \to Q$ of posets, and how many are there?
?
Exactly when $F(p) \leq G(p)$ for all $p \in P$, and then exactly one. Naturality is automatic because parallel arrows in a poset are equal.

State the natural transformation $1 \Rightarrow (-)^{**}$ on $\mathbf{Vect}_k$.
?
$\mathrm{ev}_V \colon V \to V^{**}$, $\mathrm{ev}_V(v)(\theta) = \theta(v)$. Naturality at $f \colon V \to W$: $f^{**} \circ \mathrm{ev}_V = \mathrm{ev}_W \circ f$; both sides send $v$ to $\theta \mapsto \theta(f(v))$.

Why can there be no natural transformation between $1_{\mathbf{Vect}_k}$ and the single dual $(-)^*$?
?
The identity functor is covariant and $(-)^*$ is contravariant, so the definition of natural transformation does not apply: the naturality square cannot be drawn.

Definition: vertical composite $\beta \circ \alpha$ of $\alpha \colon F \Rightarrow G$ and $\beta \colon G \Rightarrow H$
?
The natural transformation $F \Rightarrow H$ with components $(\beta \circ \alpha)_A = \beta_A \circ \alpha_A$.

What technique proves that a vertical composite of natural transformations is natural?
?
Pasting: the naturality square of $\alpha$ at $f$ sits on top of the naturality square of $\beta$ at $f$; if both commute, so does the outer rectangle.

Definition: the functor category $[\mathcal{A}, \mathcal{B}]$
?
Objects: functors $\mathcal{A} \to \mathcal{B}$. Arrows: natural transformations. Composition: vertical composition. Identities: $1_F$ with components $1_{F(A)}$.

Definition: natural isomorphism. What does "$F(A) \cong G(A)$ naturally in $A$" mean?
?
A natural isomorphism is an isomorphism in $[\mathcal{A}, \mathcal{B}]$; equivalently, a natural transformation all of whose components are isomorphisms. "$F(A) \cong G(A)$ naturally in $A$" means such a natural isomorphism $F \cong G$ exists, which is stronger than an isomorphism for each $A$ separately.

Definition: the whiskerings $G\alpha$ and $\beta F$, for $\alpha \colon F \Rightarrow F'$ (with $F, F' \colon \mathcal{A} \to \mathcal{B}$) and $\beta \colon G \Rightarrow G'$ (with $G, G' \colon \mathcal{B} \to \mathcal{C}$)
?
$(G\alpha)_A = G(\alpha_A) \colon GF(A) \to GF'(A)$ and $(\beta F)_A = \beta_{F(A)} \colon GF(A) \to G'F(A)$.

Definition: horizontal composite $\beta * \alpha \colon GF \Rightarrow G'F'$. Why are the two formulas for it equal?
?
$(\beta * \alpha)_A = \beta_{F'(A)} \circ G(\alpha_A) = G'(\alpha_A) \circ \beta_{F(A)}$. They agree by naturality of $\beta$ at the arrow $\alpha_A$ of $\mathcal{B}$.

## 1E: Equivalence of Categories

Definition: isomorphism of categories
?
A functor $F \colon \mathcal{A} \to \mathcal{B}$ for which there is a functor $G \colon \mathcal{B} \to \mathcal{A}$ with $G \circ F = 1_{\mathcal{A}}$ and $F \circ G = 1_{\mathcal{B}}$ (equalities of functors).

Definition: equivalence of categories
?
Functors $F \colon \mathcal{A} \to \mathcal{B}$ and $G \colon \mathcal{B} \to \mathcal{A}$ together with natural isomorphisms $\eta \colon 1_{\mathcal{A}} \Rightarrow GF$ and $\varepsilon \colon FG \Rightarrow 1_{\mathcal{B}}$. Written $\mathcal{A} \simeq \mathcal{B}$.

Why is isomorphism of categories too strict a notion of sameness?
?
It demands equalities of objects such as $GF(A) = A$. Example: $\mathbf{FinSet}$ and its full subcategory $\mathcal{N}$ on the sets $[n] = \{1, \dots, n\}$ are not isomorphic (distinct isomorphic objects $\{1\}, \{2\}$ would have to go to distinct isomorphic objects of $\mathcal{N}$, and there are none), yet they are equivalent.

Definitions: faithful, full, essentially surjective on objects, for $F \colon \mathcal{A} \to \mathcal{B}$
?
Faithful: each map $\mathcal{A}(A, A') \to \mathcal{B}(F(A), F(A'))$, $f \mapsto F(f)$, is injective. Full: each such map is surjective. Essentially surjective on objects: for every object $B$ of $\mathcal{B}$ there is an object $A$ of $\mathcal{A}$ with $F(A) \cong B$.

State the theorem characterising equivalences.
?
A functor is an equivalence if and only if it is full, faithful and essentially surjective on objects. ("Only if" needs no choice; "if" uses the axiom of choice.)

In the proof that a full, faithful, essentially surjective functor $F$ is an equivalence, exactly where is a choice made?
?
In the first step: for each object $B$ of $\mathcal{B}$ one chooses an object $G(B)$ of $\mathcal{A}$ together with an isomorphism $\varepsilon_B \colon FG(B) \to B$. Everything after that ($G$ on arrows, $\eta$) is determined uniquely by fullness and faithfulness.

In that proof, how is $G$ defined on an arrow $g \colon B \to B'$?
?
$G(g)$ is the unique arrow $G(B) \to G(B')$ with $F(G(g)) = \varepsilon_{B'}^{-1} \circ g \circ \varepsilon_B$. It exists and is unique because $F$ is full and faithful; the equation is exactly naturality of $\varepsilon$.

What does "a full and faithful functor reflects isomorphisms" say, and what technique proves it?
?
If $F$ is full and faithful and $F(f)$ is an isomorphism then $f$ is; hence $F(A) \cong F(A')$ implies $A \cong A'$. Technique: use fullness to lift the inverse, then faithfulness (on parallel arrows) to lift the two equations.

What must you say before every use of faithfulness?
?
That the two arrows being compared are parallel: same domain and same codomain. Faithfulness says nothing about non-parallel arrows.

Why is every functor in an equivalence faithful?
?
Naturality of $\eta$ at $f$ with $\eta$ invertible gives $f = \eta_{A'}^{-1} \circ GF(f) \circ \eta_A$, so $f$ is determined by $GF(f)$, hence by $F(f)$.

Definitions: skeletal category; skeleton of a category
?
Skeletal: isomorphic objects are equal. A skeleton of $\mathcal{A}$ is a full subcategory $\mathcal{S}$ such that every object of $\mathcal{A}$ is isomorphic to exactly one object of $\mathcal{S}$.

Why is a category equivalent to each of its skeletons?
?
The inclusion of a skeleton is full and faithful (full subcategory) and essentially surjective on objects (every object is isomorphic to one in the skeleton), so it is an equivalence by the characterisation theorem.

Give two examples of an equivalence that is not an isomorphism.
?
(1) $\mathcal{N} \simeq \mathbf{FinSet}$, where $\mathcal{N}$ has the sets $\{1, \dots, n\}$ as objects. (2) $\mathbf{Mat}_k \simeq \mathbf{FDVect}_k$ via $n \mapsto k^n$, $M \mapsto (x \mapsto Mx)$.

What is a duality between categories $\mathcal{A}$ and $\mathcal{B}$? Give an example.
?
An equivalence $\mathcal{A}^{\mathrm{op}} \simeq \mathcal{B}$. Example: $\mathbf{FDVect}_k^{\mathrm{op}} \simeq \mathbf{FDVect}_k$ via the dual space $V \mapsto V^*$, using the natural isomorphism $V \cong V^{**}$.
