#flashcards/part0

## 0A: Orientation

What does a category consist of, informally?
?
Objects, maps (arrows) between them, a composition rule for maps that meet head to tail, and an identity map on each object; composition is associative and identities do nothing.

What is the "bird's-eye view" that category theory takes?
?
It ignores what objects are made of and studies only the maps between them and how those maps compose, so that patterns shared by algebra, topology and order theory become visible.

What is the general form of a universal property?
?
"For every ... there exists a unique map ... such that ...". It describes an object by the maps into it or out of it.

State the universal property of a one-element set $1$.
?
For every set $X$ there is exactly one function $X \to 1$.

Which sets $T$ have the property "for every set $X$ there is exactly one function $X \to T$", and how does each other kind of set fail?
?
Exactly the one-element sets. The empty set fails existence (no function $\{0\} \to \emptyset$); a set with two or more elements fails uniqueness (several functions $\{0\} \to T$).

State the universal property of the product $A \times B$ with projections $p_1, p_2$.
?
For every set $X$ and all functions $f \colon X \to A$, $g \colon X \to B$, there is exactly one function $h \colon X \to A \times B$ with $p_1 \circ h = f$ and $p_2 \circ h = g$.

In the product of sets, what is the unique $h \colon X \to A \times B$ with $p_1 \circ h = f$ and $p_2 \circ h = g$?
?
$h(x) = (f(x), g(x))$.

What two halves does every proof of a universal property have?
?
Existence (build a map and check it satisfies the equations) and uniqueness (show any map satisfying the equations equals the one built).

How many functions are there from an $n$-element set to an $m$-element set, and what does the case $n = 1$ say?
?
$m^n$. For $n = 1$ there are $m$ of them: a function from a one-element set into $M$ is the same thing as an element of $M$.

What are the five steps of the course's proof anatomy?
?
Goal (the statement with its quantifiers), Given (the definitions and hypotheses available), Plan (the shape of the argument), Proof (each step justified by name), What made it work (the idea to reuse).

Which function acts first in $g \circ f$?
?
$f$. The composite $A \xrightarrow{f} B \xrightarrow{g} C$ is written $g \circ f$ because $(g \circ f)(a) = g(f(a))$.

How does proof review work in this course?
?
You write the proof in `proofs/<module>/pNN_<slug>.md` and ask Claude to review it. The review points at gaps and asks questions; it never supplies a model proof. There are no solutions in the repository.

## 0B: Proof Toolkit I: Definitions & Direct Proof

What three things must be checked to show that a rule is a function $f \colon A \to B$?
?
Every $a \in A$ gets a value; the value is unambiguous (it does not depend on how $a$ is written or on any choice made); the value lies in $B$. The second item is what "well defined" means.

How do you prove a statement of the form "for all $x \in A$, $P(x)$"? How do you disprove it?
?
Prove: write "Let $x \in A$" and prove $P(x)$ using nothing about $x$ except $x \in A$. Disprove: exhibit one specific $x \in A$ for which $P(x)$ fails (a counterexample).

How do you prove a statement of the form "there exists $x \in A$ with $P(x)$"? How do you use one that is given?
?
Prove: name a specific witness, check it is in $A$ and check $P$ for it. Use: "choose $x \in A$ with $P(x)$", with a fresh letter, knowing nothing else about $x$.

What is the difference between $\forall x\, \exists y\, P(x, y)$ and $\exists y\, \forall x\, P(x, y)$?
?
In the first, the witness $y$ may depend on $x$. In the second, one $y$ must work for every $x$. The second implies the first, but not conversely (example: $x + y = 0$ over $\mathbb{Z}$).

When are two functions $f$ and $g$ equal?
?
When they have the same domain, the same codomain, and $f(a) = g(a)$ for every $a$ in the domain. A proof usually starts "Let $a \in A$".

Define the composite $g \circ f$ and say when it is defined.
?
For $f \colon A \to B$ and $g \colon B \to C$ (the codomain of $f$ must equal the domain of $g$), $g \circ f \colon A \to C$ is given by $(g \circ f)(a) = g(f(a))$.

State the associativity and identity laws for composition of functions.
?
For $f \colon A \to B$, $g \colon B \to C$, $h \colon C \to D$: $h \circ (g \circ f) = (h \circ g) \circ f$, and $f \circ 1_A = f = 1_B \circ f$.

Define injective, with quantifiers. What are the first and last lines of a proof that $f$ is injective?
?
For all $a, a' \in A$: if $f(a) = f(a')$ then $a = a'$. First line: "Let $a, a' \in A$ and assume $f(a) = f(a')$." Last line: "$a = a'$."

Define surjective, with quantifiers. How do you show a function is not surjective?
?
For every $b \in B$ there exists $a \in A$ with $f(a) = b$. Not surjective: exhibit one $b \in B$ and prove no $a \in A$ has $f(a) = b$.

Define left inverse, right inverse and invertible for $f \colon A \to B$.
?
$g \colon B \to A$ is a left inverse if $g \circ f = 1_A$; $h \colon B \to A$ is a right inverse if $f \circ h = 1_B$; $f$ is invertible if a single $k \colon B \to A$ satisfies both equations.

How are left inverses related to injectivity?
?
If $f$ has a left inverse then $f$ is injective. Conversely, if $f$ is injective and $A$ is non-empty then $f$ has a left inverse (which need not be unique).

In the construction of a left inverse for an injective $f$, where is injectivity used?
?
To show that the rule "send $b$ in the image of $f$ to the $a$ with $f(a) = b$" is well defined: there is only one such $a$.

What are the converse and the contrapositive of "if $P$ then $Q$", and which is equivalent to the original?
?
Converse: "if $Q$ then $P$" (independent of the original). Contrapositive: "if not $Q$ then not $P$" (logically equivalent to the original).

What technique proves that a composite of two injections is an injection?
?
A direct proof from the definition: start from $(g \circ f)(a) = (g \circ f)(a')$, peel off $g$ using its injectivity, then $f$ using its injectivity.

## 0C: Proof Toolkit II: Uniqueness, Diagrams & Algebra Refresher

What two statements make up "there exists a unique $x \in A$ with $P(x)$"?
?
Existence: some $x \in A$ has $P(x)$. Uniqueness: for all $x, x' \in A$, if $P(x)$ and $P(x')$ then $x = x'$. They are independent and each needs its own proof.

What are the two standard ways to prove uniqueness?
?
Two candidates: take two things with the property and show they are equal, typically via one expression that each simplifies differently. Forced value: show the property forces any candidate to equal one specific formula.

Define a monoid.
?
A set $M$ with a binary operation $\cdot$ and an element $e$ such that $(a \cdot b) \cdot c = a \cdot (b \cdot c)$ and $e \cdot a = a = a \cdot e$ for all $a, b, c \in M$.

What technique proves that a monoid has only one identity element?
?
Two candidates applied to each other: consider $e \cdot e'$ and simplify it once using that $e'$ is an identity and once using that $e$ is an identity.

Define a monoid homomorphism and a group homomorphism. Which condition is automatic for groups but not for monoids?
?
Monoid: $f(a \cdot b) = f(a) \cdot f(b)$ and $f(e) = e$. Group: only $f(a \cdot b) = f(a) \cdot f(b)$. Preserving the identity follows for groups (cancel using an inverse) but not for monoids: $n \mapsto 0$ on $(\mathbb{Z}, \times, 1)$ preserves products and not $1$.

Define preorder and partial order.
?
A preorder is a reflexive, transitive relation. A partial order is a preorder that is also antisymmetric: $x \le y$ and $y \le x$ imply $x = y$.

Define a monotone map between posets.
?
A function $f \colon P \to Q$ such that $x \le y$ implies $f(x) \le f(y)$ for all $x, y \in P$.

Why does a poset have at most one least element?
?
If $m$ and $m'$ are both least, then $m \le m'$ (property of $m$ applied to $m'$) and $m' \le m$ (property of $m'$ applied to $m$), so $m = m'$ by antisymmetry.

What does it mean for a diagram of sets and functions to commute?
?
For every pair of nodes $X$, $Y$, all directed paths from $X$ to $Y$ have the same composite function. A square with top $f$, right $g$, left $h$, bottom $k$ commutes exactly when $g \circ f = k \circ h$.

What is the difference between an equation chase and an element chase?
?
An equation chase rewrites composites using associativity and the given commuting regions, with no elements; it works in any category. An element chase follows a chosen element along the arrows; it needs objects that have elements.

State the pasting result for two commutative squares sharing an edge. Is the converse true?
?
If both squares commute then the outer rectangle commutes. The converse is false: the rectangle can commute while a square does not.

Define a terminal set, and state what "terminal sets are unique up to unique isomorphism" means.
?
$T$ is terminal if for every set $X$ there is exactly one function $X \to T$. If $T$ and $T'$ are terminal there is exactly one function $T \to T'$, and it is invertible.

What is the key move in proving that two terminal sets are isomorphic?
?
Probe each object with itself: $v \circ u$ and $1_T$ are both functions $T \to T$, and the uniqueness clause for $T$ (with $X = T$) forces them to be equal. The same for $u \circ v$ and $1_{T'}$.

Distinguish "unique", "unique up to isomorphism" and "unique up to unique isomorphism".
?
Unique: any two such objects are equal. Up to isomorphism: any two are isomorphic. Up to unique isomorphism: between any two there is exactly one isomorphism respecting the data of the property. Two-element sets are unique up to isomorphism but not up to unique isomorphism.
