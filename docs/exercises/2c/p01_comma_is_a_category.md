# 2C·P01 — The comma category is a category

**Type:** warm-up · **Technique:** verifying axioms · **Unlocked by:** `2c_universal_arrows` §1
**Source:** adapted from Leinster §2.3

## Statement

Let $P \colon \mathcal{A} \to \mathcal{C}$ and $Q \colon \mathcal{B} \to \mathcal{C}$ be
functors. Recall that an object of $(P \Rightarrow Q)$ is a triple $(A, h, B)$ with
$h \colon P(A) \to Q(B)$ in $\mathcal{C}$, and an arrow $(A, h, B) \to (A', h', B')$ is a pair
$(f, g)$ with $f \colon A \to A'$ in $\mathcal{A}$, $g \colon B \to B'$ in $\mathcal{B}$ and
$Q(g) \circ h = h' \circ P(f)$.

Prove that $(P \Rightarrow Q)$, with componentwise composition
$(f', g') \circ (f, g) = (f' \circ f, g' \circ g)$ and identities $(1_A, 1_B)$, is a category.

## What you may use

- The definition of a category (1A), applied to $\mathcal{A}$, $\mathcal{B}$ and $\mathcal{C}$.
- The definition of a functor (1C): $P$ and $Q$ preserve composition and identities.

## What a complete proof must show

- [ ] **Composition is well defined:** if $(f, g)$ and $(f', g')$ are composable arrows of $(P \Rightarrow Q)$, the pair $(f' \circ f, g' \circ g)$ satisfies the square condition for the appropriate objects.
- [ ] **Identities are arrows:** $(1_A, 1_B)$ satisfies the square condition from $(A, h, B)$ to itself.
- [ ] Associativity and the two identity laws, each with the reason.
- [ ] Each step of the square-condition calculations is labelled with what justifies it (functoriality of $P$ or $Q$, a hypothesis on $(f, g)$ or $(f', g')$, an axiom of $\mathcal{C}$).

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Verifying axioms, as in 1A. But notice that two of the four things to check are not axioms
about equations between arrows of the new category: they are claims that certain pairs *are*
arrows of the new category at all. Those two are where the work is.

</details>

<details>
<summary>Hint 2 — composition</summary>

Draw the two commutative squares for $(f, g)$ and $(f', g')$ side by side, sharing the edge
$h'$. The square condition for the composite is the statement that the outer rectangle
commutes. Which lecture in Part 1 pasted two commutative squares together, and what did that
argument use?

</details>

<details>
<summary>Hint 3 — what must be rewritten</summary>

The condition for the composite involves $Q(g' \circ g)$ and $P(f' \circ f)$. Before either
hypothesis can be applied these must be put in a different form. What lets you do that?

</details>

## Check yourself

- Did you prove that the composite *is an arrow* before discussing associativity?
- Where exactly did you use that $P$ preserves composition? That $Q$ preserves identities?
- Why do associativity and the identity laws need almost no argument? Say precisely what they are inherited from.
- Would the proof survive if $P$ were merely a function on objects and arrows that did not preserve composition?

## Write it up

Write your proof in `proofs/2c/p01_comma_is_a_category.md`, then ask Claude to review it.
