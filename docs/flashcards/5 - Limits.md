#flashcards/part5

## 5A: Limits

Definition: a product of objects $X$ and $Y$ in a category $\mathcal{A}$.
?
An object $P$ with maps $p_1 \colon P \to X$, $p_2 \colon P \to Y$ such that for every object $A$ and every pair $f_1 \colon A \to X$, $f_2 \colon A \to Y$ there exists a unique $\bar{f} \colon A \to P$ with $p_1 \bar{f} = f_1$ and $p_2 \bar{f} = f_2$.

Definition: an equalizer of $s, t \colon X \to Y$.
?
A map $i \colon E \to X$ with $s i = t i$ (a fork) such that for every fork $f \colon A \to X$ (meaning $s f = t f$) there exists a unique $\bar{f} \colon A \to E$ with $i \bar{f} = f$.

Definition: a pullback of $s \colon X \to Z$ and $t \colon Y \to Z$.
?
An object $P$ with maps $p_1 \colon P \to X$, $p_2 \colon P \to Y$ such that $s p_1 = t p_2$, and such that for every $A$, $f_1 \colon A \to X$, $f_2 \colon A \to Y$ with $s f_1 = t f_2$ there exists a unique $\bar{f} \colon A \to P$ with $p_1 \bar{f} = f_1$ and $p_2 \bar{f} = f_2$.

Definition: a cone on a diagram $D \colon \mathbf{I} \to \mathcal{A}$.
?
An object $A$ (the vertex) with maps $f_I \colon A \to D(I)$, one for each object $I$ of $\mathbf{I}$, such that $D(u) \circ f_I = f_J$ for every arrow $u \colon I \to J$ of $\mathbf{I}$.

Definition: a limit of a diagram $D \colon \mathbf{I} \to \mathcal{A}$.
?
A cone $(p_I \colon L \to D(I))_{I}$ such that for every cone $(f_I \colon A \to D(I))_{I}$ there exists a unique map $\bar{f} \colon A \to L$ with $p_I \bar{f} = f_I$ for all $I$.

What are the two halves of every universal-property proof?
?
Existence of the mediating map (write it down and verify its equations) and uniqueness (take any map satisfying the same equations and show it equals the first). They are proved separately.

Which shape categories give products, equalizers, pullbacks and terminal objects as limits?
?
Two objects with only identities; two objects with two parallel arrows; three objects with two arrows into one of them; the empty category.

State the explicit formula for the limit of $D \colon \mathbf{I} \to \mathbf{Set}$.
?
$\lim D = \{(x_I)_{I} \in \prod_I D(I) : (Du)(x_I) = x_J \text{ for every arrow } u \colon I \to J\}$, with projections sending a tuple to its $I$-th entry.

Statement: in what sense is a limit unique?
?
If $(L, p_I)$ and $(L', p'_I)$ are limit cones on the same diagram, there is a unique map $j \colon L \to L'$ with $p'_I j = p_I$ for all $I$, and $j$ is an isomorphism.

What technique proves that two maps $h, h' \colon A \to L$ into a limit are equal?
?
Show $p_I h = p_I h'$ for every projection $p_I$. Then both are mediating maps for the same cone, so the uniqueness clause of the limit gives $h = h'$.

Statement: which two kinds of limit suffice to build all small limits?
?
Small products and equalizers. The limit of $D$ is the equalizer of two maps $\prod_{I} D(I) \rightrightarrows \prod_{u} D(\operatorname{cod} u)$, one recording $x_{\operatorname{cod} u}$ and the other $(Du)(x_{\operatorname{dom} u})$.

What is a product in a poset regarded as a category? What is the product of the empty family in any category?
?
A meet (greatest lower bound). A terminal object.

Statement: how do pullbacks interact with monics?
?
The pullback of a monic along any map is monic. And $f \colon X \to Y$ is monic if and only if the square with $1_X, 1_X$ on two sides and $f, f$ on the other two is a pullback.

What technique shows a commuting square is *not* a pullback, or a cone is *not* a limit?
?
Exhibit one test cone for which a mediating map does not exist, or for which two different mediating maps exist. One failure of either half is enough.

## 5B: Colimits

Definition: a cocone on a diagram $D \colon \mathbf{I} \to \mathcal{A}$.
?
An object $A$ with maps $f_I \colon D(I) \to A$, one for each object $I$ of $\mathbf{I}$, such that $f_J \circ D(u) = f_I$ for every arrow $u \colon I \to J$ of $\mathbf{I}$.

Definition: a colimit of a diagram $D \colon \mathbf{I} \to \mathcal{A}$.
?
A cocone $(q_I \colon D(I) \to C)_{I}$ such that for every cocone $(f_I \colon D(I) \to A)_{I}$ there exists a unique map $\bar{f} \colon C \to A$ with $\bar{f} q_I = f_I$ for all $I$.

How are colimits related to limits?
?
A colimit of $D \colon \mathbf{I} \to \mathcal{A}$ is exactly a limit of $D^{\mathrm{op}} \colon \mathbf{I}^{\mathrm{op}} \to \mathcal{A}^{\mathrm{op}}$. So every theorem about limits gives a theorem about colimits by duality.

Definition: a sum (coproduct) of $X$ and $Y$.
?
An object $S$ with maps $i_1 \colon X \to S$, $i_2 \colon Y \to S$ such that for every $A$ and every pair $f_1 \colon X \to A$, $f_2 \colon Y \to A$ there exists a unique $\bar{f} \colon S \to A$ with $\bar{f} i_1 = f_1$ and $\bar{f} i_2 = f_2$.

Definition: a coequalizer of $s, t \colon X \to Y$.
?
A map $q \colon Y \to C$ with $q s = q t$ such that for every $f \colon Y \to A$ with $f s = f t$ there exists a unique $\bar{f} \colon C \to A$ with $\bar{f} q = f$.

Definition: a pushout of $s \colon Z \to X$ and $t \colon Z \to Y$.
?
An object $Q$ with maps $j_1 \colon X \to Q$, $j_2 \colon Y \to Q$ such that $j_1 s = j_2 t$, and such that for every $A$, $f_1 \colon X \to A$, $f_2 \colon Y \to A$ with $f_1 s = f_2 t$ there exists a unique $\bar{f} \colon Q \to A$ with $\bar{f} j_1 = f_1$ and $\bar{f} j_2 = f_2$.

Definition: the equivalence relation generated by a relation $R$ on a set $S$.
?
The smallest equivalence relation on $S$ containing $R$. Concretely, $a \sim b$ if and only if there is a zigzag $a = c_0, c_1, \dots, c_n = b$ (with $n \ge 0$) such that for each $k$ either $(c_k, c_{k+1}) \in R$ or $(c_{k+1}, c_k) \in R$.

State the explicit formula for the colimit of $D \colon \mathbf{I} \to \mathbf{Set}$.
?
$\operatorname{colim} D = \big(\sum_{I} D(I)\big)/{\sim}$, where $\sim$ is the equivalence relation on the disjoint union generated by $(I, x) \sim (J, (Du)(x))$ for all arrows $u \colon I \to J$ and all $x \in D(I)$. The coprojection $q_I$ sends $x$ to the class of $(I, x)$.

Statement: the lemma on maps out of a quotient.
?
If $\sim$ is generated by $R$ on $S$ and $g \colon S \to B$ satisfies $g(a) = g(b)$ for all $(a, b) \in R$, then there is a unique $\bar{g} \colon S/{\sim} \to B$ with $\bar{g} \circ \pi = g$.

What must always be checked when defining a function out of a quotient set by a formula on representatives?
?
That it is well defined: equivalent representatives give the same value. When the relation is generated by $R$, it is enough to check this on the pairs in $R$.

What technique proves that two maps $h, h' \colon C \to A$ out of a colimit are equal?
?
Show $h q_I = h' q_I$ for every coprojection $q_I$; then both are mediating maps for the same cocone, and the uniqueness clause gives $h = h'$.

What are sums in $\mathbf{Set}$, $\mathbf{Top}$, $\mathbf{Ab}$, $\mathbf{Grp}$ and a poset?
?
Disjoint union; disjoint union with the disjoint union topology; direct sum (same object as the product for two groups); free product; join (least upper bound).

Statement: how do pushouts interact with epics?
?
The pushout of an epic along any map is epic. And $f \colon X \to Y$ is epic if and only if the square with $f, f$ on two sides and $1_Y, 1_Y$ on the other two is a pushout.

How do you dualize a proof correctly?
?
Reverse every arrow: swap domain and codomain, reverse the order of every composite, and exchange each notion for its dual (limit/colimit, monic/epic, terminal/initial, "into"/"out of"). Or apply the original theorem in $\mathcal{A}^{\mathrm{op}}$ and translate the conclusion back.

## 5C: Functors & Limits

What does a functor $F \colon \mathcal{A} \to \mathcal{B}$ always do to a cone on $D \colon \mathbf{I} \to \mathcal{A}$, and why?
?
It sends a cone $(f_I \colon A \to D(I))$ to a cone $(F f_I \colon F A \to F D(I))$ on $F \circ D$, because functors preserve composites and so preserve the cone equations $D(u) f_I = f_J$. It need not send limit cones to limit cones.

Definition: $F \colon \mathcal{A} \to \mathcal{B}$ preserves limits of shape $\mathbf{I}$.
?
For every diagram $D \colon \mathbf{I} \to \mathcal{A}$ and every cone $(p_I)$ on $D$: if $(p_I)$ is a limit cone on $D$, then $(F p_I)$ is a limit cone on $F \circ D$.

Definition: $F \colon \mathcal{A} \to \mathcal{B}$ reflects limits of shape $\mathbf{I}$.
?
For every diagram $D \colon \mathbf{I} \to \mathcal{A}$ and every cone $(p_I)$ on $D$: if $(F p_I)$ is a limit cone on $F \circ D$, then $(p_I)$ is a limit cone on $D$.

Definition: $F \colon \mathcal{A} \to \mathcal{B}$ creates limits of shape $\mathbf{I}$.
?
For every diagram $D \colon \mathbf{I} \to \mathcal{A}$ and every limit cone $(q_I \colon B \to F D(I))$ on $F \circ D$: there is a unique cone $(p_I \colon A \to D(I))$ on $D$ with $F(A) = B$ and $F(p_I) = q_I$ for all $I$, and this cone is a limit cone on $D$.

Definition: the comparison map for a functor $F$ and a diagram $D$ with limit $(L, p_I)$, when $F \circ D$ has limit $(M, m_I)$.
?
The unique map $c \colon F L \to M$ with $m_I \circ c = F p_I$ for all $I$. For a product it is $F(X \times Y) \to F X \times F Y$. $F$ preserves the limit exactly when $c$ is an isomorphism.

What must a counterexample to "$F$ preserves limits of shape $\mathbf{I}$" exhibit?
?
A diagram $D$ that has a limit cone in $\mathcal{A}$ whose image under $F$ is not a limit cone: a test cone in $\mathcal{B}$ with no mediating map, or with two. An abstract failure of $F(\lim D) \cong \lim F D$ by counting works only when the sizes really differ; equal sizes prove nothing.

Statement: which functors always reflect limits? What technique proves it?
?
Full and faithful functors. Push a test cone to $\mathcal{B}$, get the mediating map there, use fullness to pull the map back and faithfulness to pull back the equations and the uniqueness.

How does the forgetful functor $U \colon \mathbf{Grp} \to \mathbf{Set}$ behave with limits and colimits?
?
It creates limits (so $\mathbf{Grp}$ has all limits, computed on underlying sets, and $U$ preserves them). It does not preserve sums or the initial object.

How does the forgetful functor $U \colon \mathbf{Top} \to \mathbf{Set}$ behave with limits and colimits?
?
It preserves limits and colimits, but does not reflect or create them: a set can carry several topologies making the legs of a cone continuous, and only one of them gives the limit.

What technique shows that $U \colon \mathbf{Grp} \to \mathbf{Set}$ creates a limit?
?
The projections of a limit in $\mathbf{Set}$ are jointly injective, so an equation in the limit set can be checked after applying each projection. This forces the group operations (uniqueness of the lift), verifies the group axioms (existence of the lift), and shows the mediating function is a homomorphism.

Statement: the lemma relating creation to existence and preservation.
?
If $\mathcal{B}$ has limits of shape $\mathbf{I}$ and $F \colon \mathcal{A} \to \mathcal{B}$ creates them, then $\mathcal{A}$ has limits of shape $\mathbf{I}$ and $F$ preserves them.

Statement: limits in functor categories are computed pointwise (proof in 6B).
?
For small $\mathcal{A}$, $\mathbf{I}$ and locally small $\mathcal{S}$: if each diagram $D(-)(A) \colon \mathbf{I} \to \mathcal{S}$ has a limit, then $D \colon \mathbf{I} \to [\mathcal{A}, \mathcal{S}]$ has a limit cone whose image under every evaluation functor $\mathrm{ev}_A$ is a limit cone, and any cone with that property is a limit cone. E.g. $(X \times Y)(A) = X(A) \times Y(A)$.

Statement: limits commute with limits.
?
For $D \colon \mathbf{I} \times \mathbf{J} \to \mathcal{A}$, the iterated limit $\lim_{\mathbf{I}} \lim_{\mathbf{J}} D(I, J)$ is a limit of $D$ over $\mathbf{I} \times \mathbf{J}$; hence $\lim_{\mathbf{I}} \lim_{\mathbf{J}} D \cong \lim_{\mathbf{J}} \lim_{\mathbf{I}} D$ when both exist. Limits do not commute with colimits in general: in $\mathbf{Set}$ the comparison map $(A \times C) + (B \times D) \to (A + B) \times (C + D)$ is usually not a bijection (for one-element sets the sizes are $2$ and $4$).

Are "preserves limits" and "reflects limits" related by implication?
?
No. The inclusion of a subposet reflects meets but need not preserve them; $U \colon \mathbf{Top} \to \mathbf{Set}$ preserves limits but does not reflect them.
