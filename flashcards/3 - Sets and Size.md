#flashcards/part3

## 3A: Sets & Size

How many functions are there $\emptyset \to A$, and $A \to \emptyset$ for non-empty $A$? What technique proves the first?
?
Exactly one function $\emptyset \to A$ (the empty function); none $A \to \emptyset$ when $A \neq \emptyset$. Technique: existence and uniqueness, both vacuous, because "for all $a \in \emptyset$" statements are true.

Describe the product $A \times B$ by the functions into it.
?
For every set $X$ and functions $f \colon X \to A$, $g \colon X \to B$ there is exactly one $h \colon X \to A \times B$ with $p_1 \circ h = f$ and $p_2 \circ h = g$, namely $h(x) = (f(x), g(x))$. So $\mathbf{Set}(X, A \times B) \cong \mathbf{Set}(X, A) \times \mathbf{Set}(X, B)$.

Definition: the sum $A + B$ of two sets. Why is it not the union?
?
$A + B = (A \times \{1\}) \cup (B \times \{2\})$ with inclusions $i_1(a) = (a, 1)$, $i_2(b) = (b, 2)$. The tags make the two copies disjoint; $A \cup B$ identifies common elements (e.g. $\{0\} \cup \{0\}$ has one element, $\{0\} + \{0\}$ has two).

Definition: the function set $B^A$. How many elements does it have for finite sets?
?
$B^A = \mathbf{Set}(A, B)$, the set of all functions from $A$ to $B$ (the exponent is the domain). $|B^A| = |B|^{|A|}$, including $|B^\emptyset| = 1$.

State the currying bijection and the technique that proves it.
?
$\mathbf{Set}(A \times B, C) \cong \mathbf{Set}(A, C^B)$, $f \mapsto \bar f$ with $\bar f(a)(b) = f(a, b)$. Technique: explicit inverse $g \mapsto \hat g$, $\hat g(a, b) = g(a)(b)$, and check both composites on elements.

Definition: characteristic function of a subset $S \subseteq A$. What bijection does it give?
?
$\chi_S \colon A \to 2$, $\chi_S(a) = \mathrm{true}$ iff $a \in S$. It gives a bijection $\mathcal{P}(A) \cong 2^A$, $S \mapsto \chi_S$.

Definition: equalizer of $f, g \colon A \to B$ in $\mathbf{Set}$, and its universal property.
?
$\mathrm{Eq}(f, g) = \{a \in A : f(a) = g(a)\}$ with inclusion $i$. For every $h \colon X \to A$ with $f \circ h = g \circ h$ there is exactly one $\bar h \colon X \to \mathrm{Eq}(f, g)$ with $i \circ \bar h = h$.

State the property of the quotient map $p \colon A \to A/{\sim}$ concerning functions out of the quotient.
?
For every $f \colon A \to B$ such that $a \sim a'$ implies $f(a) = f(a')$, there is exactly one $\bar f \colon A/{\sim} \to B$ with $\bar f \circ p = f$. The key step in any proof of this kind is well-definedness.

State Cantor's theorem and name the technique.
?
For every set $A$, no function $f \colon A \to \mathcal{P}(A)$ is surjective; hence $|A| < |\mathcal{P}(A)|$. Technique: the diagonal argument, with $D = \{a \in A : a \notin f(a)\}$, which differs from every $f(a)$ at $a$.

In what precise sense is there "no set of all sets"?
?
For every set $I$ and family of sets $(A_i)_{i \in I}$ there is a set $B$ not in bijection with any $A_i$ (take $B = \mathcal{P}(\sum_i A_i)$ and use Cantor's theorem). So no set-indexed family contains every set up to bijection.

Definitions: small, locally small, large, essentially small category
?
Small: the class of all arrows is a set. Locally small: each hom-class $\mathcal{A}(A, B)$ is a set. Large: not small. Essentially small: equivalent to some small category.

Classify: a group as a one-object category; $\mathbf{Set}$; $\mathbf{FinSet}$.
?
A group: small. $\mathbf{Set}$: locally small, not small and not even essentially small. $\mathbf{FinSet}$: not small, but essentially small (equivalent to its skeleton on the sets $\{1, \dots, n\}$).

Why is $\mathbf{Set}$ not essentially small?
?
If $\mathbf{Set}$ were equivalent to a small $\mathcal{B}$ via $F, G$, then every set $X$ would be in bijection with $G(F(X))$, a member of the set-indexed family $(G(b))_{b \in \mathrm{ob}\,\mathcal{B}}$. That contradicts the fact that no set-indexed family contains every set up to bijection.

What does $\mathbf{Cat}$ denote, and why that convention?
?
The category of **small** categories and functors. Restricting to small categories avoids a "category of all categories" that would have to contain itself.
