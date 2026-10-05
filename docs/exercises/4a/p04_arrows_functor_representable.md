# 4A·P04 — The arrows of a category

**Type:** core · **Technique:** exhibiting a representation · **Unlocked by:** `4a_representables` §2
**Source:** adapted from Leinster §4.1

## Statement

Let $\mathbf{Cat}$ be the category of small categories and functors. Define
$M \colon \mathbf{Cat} \to \mathbf{Set}$ as follows: for a small category $\mathcal{C}$, $M(\mathcal{C})$
is the set of all arrows of $\mathcal{C}$; for a functor $F \colon \mathcal{C} \to \mathcal{D}$,
$M(F)$ sends an arrow $f$ of $\mathcal{C}$ to the arrow $F(f)$ of $\mathcal{D}$.

You may take it as given that $M$ is a functor. Prove that $M$ is representable.

## What you may use

- The definitions of category, functor and composition of functors (1A, 1C).
- The definition of a representable functor and of a representation (4A §2).
- That $\mathbf{Cat}$ is locally small.

## What a complete proof must show

- [ ] A specific small category $\mathcal{T}$ is described completely: objects, arrows, identities,
      composition.
- [ ] For every small category $\mathcal{C}$, a function
      $\mathbf{Cat}(\mathcal{T}, \mathcal{C}) \to M(\mathcal{C})$ is defined.
- [ ] That function is shown to be injective *and* surjective. Surjectivity requires you to build a
      functor and verify that it is one.
- [ ] Naturality in $\mathcal{C}$ is stated and verified for an arbitrary functor
      $F \colon \mathcal{C} \to \mathcal{D}$.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

You must *find* the representing object before you can prove anything. A representing object
$\mathcal{T}$ is a small category such that "a functor $\mathcal{T} \to \mathcal{C}$" carries
exactly the same information as "an arrow of $\mathcal{C}$". Once you have a candidate, the proof
is the usual checklist: function, bijection, naturality.

</details>

<details>
<summary>Hint 2 — look for the special element</summary>

In both worked representations of 4A the representing object contained one distinguished thing
(the element $\star$ of $1$, the subset $\{1\}$ of $2$), and every other instance was its image.
Here the instances are arrows. So $\mathcal{T}$ should contain one distinguished arrow, and as
little else as possible. What is the least a category must contain if it contains an arrow
between two different objects?

</details>

<details>
<summary>Hint 3 — why is a functor out of your category determined by one arrow?</summary>

List everything a functor out of your $\mathcal{T}$ has to specify. Which of those choices are
forced by the functor axioms once the image of the distinguished arrow is known? Conversely, given
any arrow $f \colon X \to Y$ of $\mathcal{C}$, what are you forced to write down, and which axioms
remain to be checked?

</details>

## Check yourself

- Does your argument still work when the arrow $f$ of $\mathcal{C}$ is an identity, or an
  endomorphism $X \to X$? Your functor out of $\mathcal{T}$ need not be injective on objects.
- Which small category represents the functor "set of objects of $\mathcal{C}$"? You should be
  able to answer this in one line now.
- Did you verify naturality for functors $F$, or only say that the construction "is the same for
  every $\mathcal{C}$"?

## Write it up

Write your proof in `proofs/4a/p04_arrows_functor_representable.md`, then ask Claude to review it.
