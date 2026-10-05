# 2C·P03 — The counit is a terminal object

**Type:** core · **Technique:** terminal-object argument · **Unlocked by:** `2c_universal_arrows` §4
**Source:** adapted from Leinster §2.3

## Statement

Let $F \colon \mathcal{A} \to \mathcal{B}$ be a functor and $B$ an object of $\mathcal{B}$,
regarded as a functor $B \colon \mathbf{1} \to \mathcal{B}$. In the comma category
$(F \Rightarrow B)$:

- an object is a pair $(A, g)$ with $A$ an object of $\mathcal{A}$ and $g \colon F(A) \to B$ an arrow of $\mathcal{B}$;
- an arrow $(A', g') \to (A, g)$ is an arrow $p \colon A' \to A$ of $\mathcal{A}$ with $g \circ F(p) = g'$.

1. Check that this description agrees with the general definition of a comma category in
   2C §1.
2. Now let $G \colon \mathcal{B} \to \mathcal{A}$ be a functor with $F \dashv G$ and counit
   $\varepsilon$. Prove that for every object $B$ of $\mathcal{B}$, the pair
   $(G(B), \varepsilon_B)$ is a terminal object of $(F \Rightarrow B)$.
3. State, without proof, the dual of Corollary 4: a condition on a functor
   $F \colon \mathcal{A} \to \mathcal{B}$ alone that is equivalent to $F$ having a right adjoint.

## What you may use

- The definition of a comma category and of a terminal object.
- From 2B: the definition of the counit and Lemma 2 (both parts).
- That transposition is a bijection.
- Lemma 2 of the 2C lecture as a *model*; you may not quote it "by duality".

## What a complete proof must show

- [ ] Part 1 identifies which functor plays $P$ and which plays $Q$, and shows the square condition reduces to the stated triangle.
- [ ] Part 2 unpacks "terminal": for every object $(A, g)$ there is exactly one $p \colon A \to G(B)$ in $\mathcal{A}$ satisfying a stated equation in $\mathcal{B}$.
- [ ] Part 2 identifies the left-hand side of that equation with a transpose, citing the result used.
- [ ] Existence and uniqueness of $p$ are both drawn from a named property of transposition.
- [ ] Part 3 is a precise statement, with the comma category and the kind of object (initial or terminal) named.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Part 2 is the mirror image of Lemma 2 of the lecture. There, the condition for being an arrow
out of $(F(A), \eta_A)$ was rewritten, using a formula from 2B, as a statement about a
transpose. Do the same for arrows *into* $(G(B), \varepsilon_B)$.

</details>

<details>
<summary>Hint 2 — the equation</summary>

Write out what it means for $p \colon A \to G(B)$ to be an arrow $(A, g) \to (G(B), \varepsilon_B)$.
You will get a composite involving $\varepsilon_B$ and $F(p)$. Where in 2B did exactly that
composite appear?

</details>

<details>
<summary>Hint 3 — counting solutions</summary>

Once the equation reads "the transpose of $p$ equals $g$", how many arrows $p$ satisfy it?
Which property of the map $p \mapsto \bar{p}$ gives "at least one", and which gives "at most
one"?

</details>

## Check yourself

- Is your $p$ an arrow of $\mathcal{A}$, and is the equation it satisfies an equation in $\mathcal{B}$?
- For the free monoid adjunction, what does part 2 say in words about "multiplying out a word"?
- For a Galois connection $f \dashv g$, what is $(f \Rightarrow b)$ and which element is its terminal object? Compare with Proposition 5 of 2A.
- In part 3, did you write $(F \Rightarrow B)$ or $(B \Rightarrow F)$? Check that the arrows in your category point out of $F(A)$.

## Write it up

Write your proof in `proofs/2c/p03_counit_is_terminal.md`, then ask Claude to review it.
