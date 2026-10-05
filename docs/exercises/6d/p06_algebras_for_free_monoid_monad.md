# 6D·P06 — Algebras for the free monoid monad are monoids

**Type:** stretch · **Technique:** translating between two definitions · **Unlocked by:** `6d_monads` §3
**Source:** adapted from Riehl §5.2

## Statement

Let $T$ be the free monoid monad on $\mathbf{Set}$: $TA = A^*$ is the set of finite words in $A$,
$\eta_A(x)$ is the one-letter word $x$, and $\mu_A$ concatenates a word of words. Write $()$ for
the empty word and $(x_1, \ldots, x_n)$ for a word.

1. Let $(M, \cdot, e)$ be a monoid. Show that $a \colon M^* \to M$,
   $a(m_1, \ldots, m_n) = m_1 \cdot \ldots \cdot m_n$ and $a() = e$, is a $T$-algebra structure on $M$.
2. Let $(A, a)$ be a $T$-algebra. Define $x \cdot y = a(x, y)$ and $e = a()$. Prove that
   $(A, \cdot, e)$ is a monoid, and that $a(x_1, \ldots, x_n) = x_1 \cdot \ldots \cdot x_n$ for all $n \ge 1$.
3. Deduce that the constructions of parts 1 and 2 are mutually inverse bijections between monoid
   structures on a set $A$ and $T$-algebra structures on $A$.
4. Show that a function $f \colon A \to B$ between two such objects is a map of $T$-algebras if and
   only if it is a monoid homomorphism.

## What you may use

- The definitions of a monoid and a monoid homomorphism (0C).
- The definitions of the free monoid monad, a $T$-algebra and a map of algebras.
- Induction on the length of a word.
- That in a monoid the product $m_1 \cdot \ldots \cdot m_n$ does not depend on bracketing (generalised associativity), in part 1.

## What a complete proof must show

- [ ] In part 1: both algebra axioms, checked on an arbitrary word and an arbitrary word of words.
- [ ] In part 2: associativity and both unit laws of $\cdot$, each obtained by applying the associativity axiom $a \circ \mu_A = a \circ T(a)$ to a *specific, written-out* word of words, together with the unit axiom.
- [ ] In part 2: the formula for $a$ on words of length $n$, by induction.
- [ ] In part 3: both round trips.
- [ ] In part 4: both directions.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Part 2 is the heart. Your only tools are two equations: $a(x) = x$ for a one-letter word, and
$a \circ \mu_A = a \circ T(a)$ on words of words. To prove a law about $\cdot$ you must choose a word
of words to feed into the second equation. The whole skill is choosing it.

</details>

<details>
<summary>Hint 2 — associativity</summary>

You want to compare $a(a(x, y), z)$ with $a(x, a(y, z))$. Think about $T(a)$: it applies $a$ to each
letter of a word of words. Which word of words does $T(a)$ send to the two-letter word
$(a(x, y), z)$? The unit axiom tells you how to write $z$ as $a$ of something. What does $\mu_A$ do
to that same word of words?

</details>

<details>
<summary>Hint 3 — the unit laws</summary>

The element $e$ is $a$ of the empty word. Which word of words has an empty word as one of its
letters and concatenates to a one-letter word?

</details>

<details>
<summary>Hint 4 — the general formula</summary>

Induct on $n$. To pass from $n$ to $n + 1$, find a word of words whose concatenation is
$(x_1, \ldots, x_{n+1})$ and whose image under $T(a)$ is a two-letter word.

</details>

## Check yourself

- Where exactly did associativity of $\cdot$ come from: the unit axiom, the associativity axiom, or both?
- In part 3, which round trip needed the formula proved by induction in part 2?
- The lecture's non-example $a(n_1, \ldots, n_k) = k$ on $\mathbb{N}$ fails the unit axiom. Does it satisfy the associativity axiom?

## Write it up

Write your proof in `proofs/6d/p06_algebras_for_free_monoid_monad.md`, then ask Claude to review it.
