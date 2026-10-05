# 1A·P02 — A category with thin hom-sets is a preorder

**Type:** warm-up · **Technique:** unpacking a definition · **Unlocked by:** `1a_categories` §5
**Source:** adapted from Leinster §1.1–1.2 and Riehl §1.1

## Statement

Let $\mathcal{A}$ be a category whose objects form a set and in which, for all objects $X, Y$,
the hom-set $\mathcal{A}(X, Y)$ has **at most one** element. Define a relation $\le$ on
$\mathrm{ob}(\mathcal{A})$ by

$$X \le Y \quad\text{if and only if}\quad \mathcal{A}(X, Y) \text{ is non-empty.}$$

(a) Prove that $\le$ is a preorder: it is reflexive and transitive.

(b) Show by an explicit example that $\le$ need not be antisymmetric. Your example must be a
category satisfying the hypothesis, and you must say why it is a category.

## What you may use

- The definition of a category.
- The definitions of reflexive, transitive and antisymmetric relations (0C).
- For (b): Proposition 5.1 of the lecture (every preorder gives a category), if you find it helpful.

## What a complete proof must show

- [ ] Reflexivity: for **every** object $X$, an arrow $X \to X$ is exhibited, together with the part of the definition of a category that provides it.
- [ ] Transitivity: from an arrow $X \to Y$ and an arrow $Y \to Z$, an arrow $X \to Z$ is exhibited, together with the part of the definition that provides it.
- [ ] For (b): two **different** objects $X, Y$ with $X \le Y$ and $Y \le X$, in a category whose arrows and composites are completely specified.
- [ ] It says where (if anywhere) the hypothesis "at most one element" was used.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Each half of (a) is an existence statement: "there is an arrow from ... to ...". An existence
statement is proved by pointing at a specific arrow. Go through the four pieces of data in the
definition of a category and ask which of them hands you an arrow.

</details>

<details>
<summary>Hint 2 — matching data to properties</summary>

Proposition 5.1 used reflexivity to get one piece of the category structure and transitivity
to get another. You are now going in the opposite direction. Which piece of structure gives
back which property?

</details>

<details>
<summary>Hint 3 — for part (b)</summary>

You need the smallest situation in which antisymmetry could fail: two objects. What arrows
must there be between them, and what arrows are there from each object to itself? Once you
know the hom-sets, how many choices are there for each composite?

</details>

## Check yourself

- In (a), did you actually need the hypothesis that hom-sets have at most one element? If not, what is that hypothesis for?
- In (b), what does the composite of your two non-identity arrows have to be, and why is there no choice?
- Start from a preorder $P$, build its category as in §5, and then apply this exercise. Do you get back the relation you started with?

## Write it up

Write your proof in `proofs/1a/p02_thin_categories_are_preorders.md`, then ask Claude to review it.
