# 1B·P04 — A one-sided inverse and a cancellation property give an isomorphism

**Type:** core · **Technique:** cancellation; dualizing a proof · **Unlocked by:** `1b_isomorphisms_duality` §2, §3, §4
**Source:** adapted from Riehl §1.2

## Statement

Let $f \colon A \to B$ and $g \colon B \to A$ be arrows in a category $\mathcal{A}$.

(a) Prove that if $g \circ f = 1_A$ and $f$ is epic, then $f \circ g = 1_B$. (So $f$ is an
isomorphism with inverse $g$.)

(b) Deduce **by duality** that if $f \circ g = 1_B$ and $f$ is monic, then $g \circ f = 1_A$.
Write the dualization out in full, in the style of Corollary 4.3: say which statement is being
applied in $\mathcal{A}^{\mathrm{op}}$, to which arrows, and how the conclusion translates back.

(c) Conclude that the following are equivalent for an arrow $f$: (i) $f$ is an isomorphism;
(ii) $f$ is epic and has a left inverse; (iii) $f$ is monic and has a right inverse.

## What you may use

- The definitions of monic, epic, isomorphism and opposite category.
- Associativity and the identity laws.
- Proposition 4.2 of the lecture ($f$ is epic in $\mathcal{A}$ if and only if it is monic in
  $\mathcal{A}^{\mathrm{op}}$), and the fact that $(\mathcal{A}^{\mathrm{op}})^{\mathrm{op}} = \mathcal{A}$.
- For (c) only: Proposition 3.1(b) and Corollary 4.3(b). To use them you must first say why
  every identity arrow is monic and epic.

## What a complete proof must show

- [ ] In (a): the goal is stated as an equation between two named arrows with the same domain and codomain, and the step that uses "$f$ is epic" names the two test arrows it is applied to.
- [ ] In (a): every other equality is justified by associativity, an identity law or the hypothesis $g \circ f = 1_A$.
- [ ] In (b): no cancellation argument is repeated. The proof says what each of the two hypotheses becomes in $\mathcal{A}^{\mathrm{op}}$, applies (a) there, and translates the conclusion.
- [ ] In (c): each implication proved is labelled, and enough implications are proved to connect all three statements.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

In (a) the goal is an equation between two arrows $B \to B$, and you have no formula for
either. Re-read the definition of epic as a *tool for proving two arrows equal*: what would you
have to check about those two arrows in order to conclude that they are equal?

</details>

<details>
<summary>Hint 2 — what to compare</summary>

The definition of epic compares two arrows out of $B$ after each has been composed with $f$.
Compute each of those two composites separately. One of them needs the hypothesis on $g$ and
two axioms; the other needs a single axiom.

</details>

<details>
<summary>Hint 3 — dualizing</summary>

In $\mathcal{A}^{\mathrm{op}}$, $f$ is an arrow from $B$ to $A$ and $g$ is an arrow from $A$ to
$B$. Rewrite the equation $f \circ g = 1_B$ using $\circ^{\mathrm{op}}$: which of the two is now
a left inverse of the other? And what does "monic in $\mathcal{A}$" become?

</details>

<details>
<summary>Hint 4 — part (c)</summary>

Two of the implications are (a) and (b) restated. For the ones that start from (i), you need
to know that an isomorphism is monic and epic. What is $f^{-1} \circ f$, and what do the two
results you are allowed to cite say about a composite that is monic, or epic?

</details>

## Check yourself

- In (a), did you use both identity laws, one of them, or neither? Name each use.
- In (b), did you re-derive which arrow is the left inverse in $\mathcal{A}^{\mathrm{op}}$, or assume it?
- The section-and-retraction category of §7 has $r \circ s = 1_A$, yet $s$ is not an isomorphism. Which hypothesis of (a) fails for $s$, and does the classifier agree?
- In a poset every arrow is monic and epic. What does (c) then say about which arrows have a one-sided inverse?

## Write it up

Write your proof in `proofs/1b/p04_split_monics_and_epics.md`, then ask Claude to review it.
