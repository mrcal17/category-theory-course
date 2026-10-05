# 6C·P06 — A limit of the identity functor is an initial object

**Type:** stretch · **Technique:** uniqueness argument with a large cone · **Unlocked by:** `6c_adjoints_and_limits` §5
**Source:** adapted from Leinster Appendix A

## Statement

Let $\mathcal{B}$ be a category. A *cone on the identity functor* $1_{\mathcal{B}}$ with vertex $L$
is a family of maps $(p_B \colon L \to B)_{B \in \mathcal{B}}$, one for every object of $\mathcal{B}$,
such that $f \circ p_B = p_{B'}$ for every map $f \colon B \to B'$ of $\mathcal{B}$. It is a *limit
cone* if it has the usual universal property among such cones. (No smallness is assumed: the
"diagram" is all of $\mathcal{B}$.)

Suppose $(p_B \colon L \to B)_{B \in \mathcal{B}}$ is a limit cone on $1_{\mathcal{B}}$. Prove that
$L$ is an initial object of $\mathcal{B}$.

This is the lemma behind the adjoint functor theorems: in a poset it says that a meet of *all*
elements is a least element, which was the key step of Theorem 2.

## What you may use

- The definition of a limit cone, and joint monicity of its projections (6B, Section 1): two maps
  into $L$ that agree after composing with every $p_B$ are equal.
- The definition of an initial object.

## What a complete proof must show

- [ ] Existence: for each object $B$, a map $L \to B$.
- [ ] Uniqueness: for each object $B$ and each map $f \colon L \to B$, a proof that $f$ equals the map found above.
- [ ] The step at which the universal property (and not merely the cone condition) is used is pointed out.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Existence costs nothing: the cone hands you a map to every object. All the work is in uniqueness.
Take an arbitrary $f \colon L \to B$. The cone condition can be applied to *any* map of
$\mathcal{B}$, including $f$. What does it say then?

</details>

<details>
<summary>Hint 2 — one map decides everything</summary>

After Hint 1, uniqueness comes down to knowing a single map: the component of the cone at the
object $L$ itself. It is a map $L \to L$. What would you like it to be?

</details>

<details>
<summary>Hint 3 — proving two maps into a limit equal</summary>

To show two maps into the vertex of a limit cone are equal, compare them after every projection.
What does the cone condition say when the map $f$ is itself one of the projections $p_B$?

</details>

## Check yourself

- Point to the line where you used that the cone is a *limit* cone. If there is no such line, the proof has a gap: find a category with a cone on the identity whose vertex is not initial.
- In a poset, what do your steps become?
- Conversely, if $\mathcal{B}$ has an initial object, does the identity functor have a limit? You were not asked, but it is a good test of understanding.

## Write it up

Write your proof in `proofs/6c/p06_limit_of_identity_is_initial.md`, then ask Claude to review it.
