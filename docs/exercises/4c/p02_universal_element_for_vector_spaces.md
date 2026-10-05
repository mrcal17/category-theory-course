# 4C·P02 — A universal element for vector spaces

**Type:** warm-up · **Technique:** verifying a universal element · **Unlocked by:** `4c_yoneda_consequences` §1
**Source:** adapted from Leinster §4.3

## Statement

Let $k$ be a field and $U \colon \mathbf{Vect}_k \to \mathbf{Set}$ the forgetful functor, which sends
a vector space to its underlying set and a linear map to itself as a function. Regard $k$ as a
one-dimensional vector space over itself.

1. Prove that $(k, 1)$ is a universal element of $U$ in the covariant sense of 4C §1: for every
   vector space $V$ and every $v \in U(V)$, there is a unique linear map $\bar{v} \colon k \to V$
   with $\bar{v}(1) = v$.
2. Determine, with proof, all $\lambda \in k$ for which $(k, \lambda)$ is a universal element of $U$.
3. State what Theorem 1.1 (in its covariant form) lets you conclude about $U$.

## What you may use

- The definition of a vector space and of a linear map.
- The covariant definition of a universal element, and the covariant form of Theorem 1.1 (4C §1).

## What a complete proof must show

- [ ] Part 1 proves existence (a map is defined and shown to be linear) and uniqueness (any two
      linear maps with the required property are equal) as separate steps.
- [ ] Part 2 gives a complete answer: every $\lambda$ is classified, with a proof for those that
      work and a proof for those that do not.
- [ ] For a $\lambda$ that fails, it is said which of existence or uniqueness fails, with a specific
      $V$ and $v$.
- [ ] Part 3 is a precise statement naming a functor and an object, not "so it is representable".

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

An existence-and-uniqueness proof, as in 0C. Do uniqueness first: assume a linear map with the
required property and work out what it must do to an arbitrary element of $k$. That calculation
also tells you how to define the map for existence.

</details>

<details>
<summary>Hint 2 — every element of $k$ in terms of $1$</summary>

An arbitrary element $\mu \in k$ can be written using the scalar multiplication of the vector
space $k$ and the vector $1$. Which axiom of a linear map then determines its value at $\mu$?

</details>

<details>
<summary>Hint 3 — part 2</summary>

Try to repeat your argument from part 1 with $\lambda$ in place of $1$. At what point do you need
to divide? For the value of $\lambda$ where that is impossible, look for a vector space $V$ and a
vector $v$ that no linear map can reach.

</details>

## Check yourself

- Is your map $\bar{v}$ checked to be additive *and* compatible with scalars?
- For two different universal elements $(k, \lambda)$ and $(k, \lambda')$ from part 2, which linear
  isomorphism $k \to k$ carries one to the other? Compare Proposition 5.2.
- How does this exercise relate to Proposition 6.2 of 4A?

## Write it up

Write your proof in `proofs/4c/p02_universal_element_for_vector_spaces.md`, then ask Claude to review it.
