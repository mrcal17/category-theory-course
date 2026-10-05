# 5C·P05 — The forgetful functor creates equalizers

**Type:** core · **Technique:** creation proof, imitating a model · **Unlocked by:** `5c_functors_and_limits` §4
**Source:** adapted from Leinster §5.3

## Statement

Let $U \colon \mathbf{Grp} \to \mathbf{Set}$ be the forgetful functor, let $s, t \colon G \to H$ be
group homomorphisms, and let $q \colon B \to U G$ be **any** equalizer of the functions
$U s, U t \colon U G \to U H$ in $\mathbf{Set}$. (So $B$ is just a set and $q$ just a function;
$B$ need not be a subset of $G$.)

Prove:

1. there is exactly one group structure on the set $B$ for which $q$ is a group homomorphism;
2. with that group structure, $q \colon B \to G$ is an equalizer of $s$ and $t$ in $\mathbf{Grp}$.

(This is what "creates equalizers" means for $U$, phrased with forks. In the language of cones a
limit cone on a parallel pair also has a leg to $H$, but that leg is determined by the leg to
$G$, as in 5A §4.)

## What you may use

- The definition of an equalizer (5A §2) in $\mathbf{Set}$ and in $\mathbf{Grp}$.
- From 5A §2: every equalizer is monic; and that monics in $\mathbf{Set}$ are the
  injective functions.
- The universal property of $q$ applied to the one-element set, as in the "Given" of Proof 4 of
  the lecture.
- The group axioms and the definition of a homomorphism. A function between groups that
  preserves multiplication is a homomorphism.
- Proof 4 of the lecture as a *model*. Do not merely say "similarly": the details differ.

## What a complete proof must show

- [ ] Uniqueness of the group structure: any structure making $q$ a homomorphism is forced.
- [ ] Existence of the group structure: a multiplication, an identity and inverses on $B$ are
      defined, each definition is shown to make sense (the required element of $B$ exists), and
      the group axioms are verified.
- [ ] $q$ is a homomorphism and $s q = t q$ in $\mathbf{Grp}$.
- [ ] For an arbitrary group $A$ and homomorphism $f \colon A \to G$ with $s f = t f$:
      existence of a mediating **homomorphism**, and separately its uniqueness.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Follow the four stages of Proof 4: uniqueness of the lift, existence of the lift, then the two
halves of the universal property upstairs. First write down the analogues, for an equalizer in
$\mathbf{Set}$, of the two facts called (E) and (U) there. One of them is simpler than for a
product; the other needs an extra condition.

</details>

<details>
<summary>Hint 2 — which elements of G are hit?</summary>

For a product, *every* pair $(x, y)$ came from an element of $B$. For an equalizer, which
elements $x \in G$ are of the form $q(b)$? You need a precise answer, with a proof that uses the
universal property of $q$ in one direction and the fork equation in the other.

</details>

<details>
<summary>Hint 3 — why the operations land in B</summary>

To define $b \cdot b'$ you want "the element of $B$ whose image under $q$ is $q(b)\,q(b')$". By
Hint 2 such an element exists only if $q(b)\,q(b')$ satisfies a certain condition. Which
hypothesis on $s$ and $t$ makes the condition hold? The same question arises for the identity
and for inverses.

</details>

<details>
<summary>Hint 4 — the universal property upstairs</summary>

The mediating *function* is handed to you by the universal property in $\mathbf{Set}$. What
remains is to show it preserves multiplication. In Proof 4 this was done by comparing images
under the projections. What plays the role of the projections here, and what property of it do
you need?

</details>

## Check yourself

- Where exactly did you use that $s$ and $t$ are homomorphisms, and not just functions?
- Did you verify associativity, identity and inverses in $B$, or assume $B$ is a subgroup of
  $G$? ($B$ is not a subset of $G$.)
- What is the corresponding statement for $\mathbf{Top}$, and which step of your proof has no
  analogue there?

## Write it up

Write your proof in `proofs/5c/p05_forgetful_creates_equalizers.md`, then ask Claude to review it.
