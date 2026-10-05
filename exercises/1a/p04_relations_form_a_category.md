# 1A·P04 — Sets and relations form a category

**Type:** core · **Technique:** verifying axioms; equality of sets · **Unlocked by:** `1a_categories` §2
**Source:** adapted from Riehl §1.1

## Statement

A **relation** from a set $A$ to a set $B$ is a subset $R \subseteq A \times B$. Given relations
$R \subseteq A \times B$ and $S \subseteq B \times C$, define

$$S \circ R = \{\, (a, c) \in A \times C \;:\; \text{there exists } b \in B \text{ with } (a, b) \in R \text{ and } (b, c) \in S \,\}.$$

For a set $A$, let $\Delta_A = \{ (a, a) : a \in A \} \subseteq A \times A$.

Prove that there is a category $\mathbf{Rel}$ whose objects are sets, whose arrows $A \to B$ are
the relations from $A$ to $B$, with composition $\circ$ as above and identities $\Delta_A$.

(To respect the convention that an arrow has one domain and one codomain, an arrow of
$\mathbf{Rel}$ is officially a triple $(A, B, R)$. You may leave this implicit.)

## What you may use

- The definition of a category and the checklist of `1a_categories` §1.
- Basic set theory: two sets are equal exactly when each is a subset of the other; the meaning
  of "there exists".
- Nothing about functions: a relation need not be a function.

## What a complete proof must show

- [ ] $S \circ R$ is a relation from $A$ to $C$, and $\Delta_A$ is a relation from $A$ to $A$.
- [ ] Associativity: for $R \subseteq A \times B$, $S \subseteq B \times C$, $T \subseteq C \times D$, the sets $(T \circ S) \circ R$ and $T \circ (S \circ R)$ are equal, proved as an equality of sets.
- [ ] Both identity laws, each proved as an equality of sets (two inclusions, or a chain of "if and only if" steps each of which is justified).
- [ ] Every "there exists" that is used is unpacked by naming a witness, and every "there exists" that is claimed is proved by supplying one.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Closure is quick here; the work is in the axioms, and each axiom is an equality between two
subsets of a product. From 0B: how do you prove two sets are equal? Fix an arbitrary pair and
ask what it means for it to belong to each side.

</details>

<details>
<summary>Hint 2 — associativity</summary>

Take a pair $(a, d)$ and unpack "$(a, d) \in (T \circ S) \circ R$" completely, until no
$\circ$ remains. How many intermediate elements appear, and which sets do they live in? Do the
same for the other bracketing and compare the two unpacked statements.

</details>

<details>
<summary>Hint 3 — the identity laws</summary>

Unpack "$(a, b) \in R \circ \Delta_A$". The definition gives you a witness in $A$. What does
membership in $\Delta_A$ tell you about that witness? For the reverse inclusion you must
*produce* a witness yourself: what are the candidates?

</details>

<details>
<summary>Hint 4 — a point of rigour</summary>

In the associativity argument you will meet a statement of the form "there exists $b$ such
that (there exists $c$ such that ...)" and want one with the quantifiers arranged differently.
Say explicitly why that rearrangement is allowed: which parts of the statement mention $b$,
and which mention $c$?

</details>

## Check yourself

- Did you prove both inclusions for each of the three equalities (or justify each "if and only if")?
- Did you check both identity laws, $R \circ \Delta_A = R$ and $\Delta_B \circ R = R$?
- Every function $f \colon A \to B$ has a graph $\{(a, f(a)) : a \in A\}$, which is a relation. Is the composite of two graphs, in the sense above, the graph of the composite function? (Not part of the exercise, but worth convincing yourself.)

## Write it up

Write your proof in `proofs/1a/p04_relations_form_a_category.md`, then ask Claude to review it.
