# 6C·P04 — Laws of exponents in a cartesian closed category

**Type:** core · **Technique:** one-line Yoneda proof, made honest · **Unlocked by:** `6c_adjoints_and_limits` §7
**Source:** adapted from Leinster §6.3

## Statement

Let $\mathcal{A}$ be a locally small cartesian closed category, with terminal object $1$. Prove
that for all objects $A, B, C$:

1. $C^1 \cong C$;
2. $(C^B)^A \cong C^{A \times B}$.

## What you may use

- The defining adjunction $\mathcal{A}(X \times B, C) \cong \mathcal{A}(X, C^B)$, natural in $X$ and $C$.
- From 4C: if $\mathcal{A}(X, P) \cong \mathcal{A}(X, Q)$ naturally in $X$, then $P \cong Q$.
- The isomorphisms $X \times 1 \cong X$ and $(X \times A) \times B \cong X \times (A \times B)$, natural in $X$. (No lecture proves these; they follow from the universal property of the product in 5A, and you may assume them here.)
- That a composite of natural isomorphisms is a natural isomorphism, and that precomposing a
  hom-functor $\mathcal{A}(-, Q)$ with a natural isomorphism of functors gives a natural isomorphism.

## What a complete proof must show

- [ ] For each part, a chain of bijections starting at $\mathcal{A}(X, \text{one side})$ and ending at $\mathcal{A}(X, \text{other side})$.
- [ ] For each link of the chain: which adjunction or product isomorphism it is, and why it is natural in $X$.
- [ ] The final appeal to 4C, with its hypothesis (naturality in $X$) explicitly satisfied.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

To prove two objects isomorphic without constructing a map between them, compare the functors
they represent. Which variable should your isomorphisms be natural in, and why that one?

</details>

<details>
<summary>Hint 2 — peel one exponent at a time</summary>

Start from $\mathcal{A}(X, (C^B)^A)$. The outermost exponent is $A$. Which adjunction removes it,
and what does the left-hand object become? Then repeat.

</details>

<details>
<summary>Hint 3 — the step that is not an adjunction</summary>

Somewhere you will need to rearrange a product. That step is a bijection of hom-sets induced by
an isomorphism in the first variable. What must you know about that isomorphism for the step to
be natural in $X$?

</details>

<details>
<summary>Hint 4 — is the chain a proof?</summary>

Section 1 of the lecture lists what must be true for a chain of isomorphisms to prove a theorem.
Here you only want two *objects* to be isomorphic. Which of those conditions still matter?

</details>

## Check yourself

- In $\mathbf{Set}$, what do the two laws say about numbers of elements?
- Did you ever need naturality in $C$?
- A third law, $(B \times C)^A \cong B^A \times C^A$, has a proof using a theorem of this module in one line. Which theorem?

## Write it up

Write your proof in `proofs/6c/p04_exponential_laws.md`, then ask Claude to review it.
