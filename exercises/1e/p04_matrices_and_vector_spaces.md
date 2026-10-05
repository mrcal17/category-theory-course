# 1E·P04 — Matrices and finite-dimensional vector spaces

**Type:** core · **Technique:** full, faithful, essentially surjective · **Unlocked by:** `1e_equivalence` §5
**Source:** adapted from Leinster §1.3 and Riehl §1.5

## Statement

Fix a field $k$. Let $\mathbf{Mat}_k$ be the category whose objects are the natural numbers
$0, 1, 2, \dots$, in which an arrow $n \to m$ is an $m \times n$ matrix with entries in $k$,
composition is matrix multiplication, and the identity on $n$ is the identity matrix $I_n$.
Define
$$\Phi \colon \mathbf{Mat}_k \to \mathbf{FDVect}_k, \qquad \Phi(n) = k^n, \qquad \Phi(M) = \big(x \mapsto Mx\big),$$
where elements of $k^n$ are column vectors.

Prove that $\Phi$ is a functor and that it is an equivalence of categories.

## What you may use

- Theorem 2 of the lecture.
- Standard linear algebra: matrix multiplication is associative; $x \mapsto Mx$ is linear; every finite-dimensional vector space has a basis; a linear map is determined by its values on a basis, and any assignment of values on a basis extends to a linear map.
- You may treat the cases $n = 0$ or $m = 0$ briefly: $k^0$ is the zero vector space and there is exactly one matrix with no rows or no columns.

## What a complete proof must show

- [ ] Functoriality: $\Phi$ sends an arrow $n \to m$ to an arrow $\Phi(n) \to \Phi(m)$, preserves identities, and preserves composition (state which fact about matrices is used).
- [ ] Faithful: for two $m \times n$ matrices $M, M'$, if the linear maps $\Phi(M)$ and $\Phi(M')$ are equal then $M = M'$.
- [ ] Full: for every linear map $T \colon k^n \to k^m$, a matrix $M$ with $\Phi(M) = T$, and a proof that $\Phi(M)$ and $T$ agree on *every* vector, not only on some.
- [ ] Essentially surjective on objects: for every finite-dimensional $V$, a natural number $n$ and an isomorphism $k^n \to V$, with a proof that it is an isomorphism.
- [ ] A sentence saying which of your steps involved an arbitrary choice.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Four verifications, each a direct proof from a definition: functor, faithful, full, essentially
surjective. Do them in that order and keep them separate. Then quote Theorem 2.

</details>

<details>
<summary>Hint 2 — faithful and full</summary>

Both come down to one question: how do you read the entries of a matrix $M$ off from the
function $x \mapsto Mx$? Which vectors $x$ would you feed it?

</details>

<details>
<summary>Hint 3 — essentially surjective</summary>

You need an isomorphism between $k^n$ and an abstract vector space $V$ about which you know
only that it is finite-dimensional. What does finite-dimensionality give you, and how does it
determine $n$? How do you show that the map you write down is injective and surjective?

</details>

## Check yourself

- Is $\Phi$ an *isomorphism* of categories? Is it injective on objects? Surjective on objects?
- Is $\mathbf{Mat}_k$ skeletal? Is it a skeleton of $\mathbf{FDVect}_k$ in the sense of §6? (Read the definition of skeleton carefully before answering.)
- In the proof of Theorem 2, Step 1 chooses a pair $(G(B), \varepsilon_B)$. For this $\Phi$, what is such a choice called in linear algebra?

## Write it up

Write your proof in `proofs/1e/p04_matrices_and_vector_spaces.md`, then ask Claude to review it.
