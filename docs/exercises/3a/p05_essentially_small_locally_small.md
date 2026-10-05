# 3A·P05 — An essentially small category is locally small

**Type:** core · **Technique:** transporting a property along a full and faithful functor · **Unlocked by:** `3a_sets_and_size` §7 (and `1e_equivalence` §4)
**Source:** adapted from Leinster §3.2

## Statement

Let $\mathcal{A}$ be an essentially small category: there is a small category $\mathcal{B}$ and
an equivalence between $\mathcal{A}$ and $\mathcal{B}$. Prove that $\mathcal{A}$ is locally
small: for every pair of objects $A, A'$ of $\mathcal{A}$, the class $\mathcal{A}(A, A')$ is a
set.

## What you may use

- The definitions of small, locally small and essentially small (3A §7).
- Theorem 2 of 1E, "only if" direction: a functor that is part of an equivalence is full and faithful (and essentially surjective on objects).
- Two working rules about classes, at the informal level of the lecture: (i) a subclass of a set is a set; (ii) a class that is in bijection with a set is a set.

## What a complete proof must show

- [ ] Which functor you use, between which categories and in which direction.
- [ ] For fixed objects $A, A'$ of $\mathcal{A}$: the function between hom-classes that you consider, with its domain and codomain.
- [ ] Why that function is a bijection, naming the properties of the functor that give injectivity and surjectivity.
- [ ] Why the codomain of that function is a set, using smallness of $\mathcal{B}$.
- [ ] The conclusion, citing the working rule used.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

A direct proof. Fix two objects $A, A'$ of $\mathcal{A}$; the goal is a statement about the one
class $\mathcal{A}(A, A')$. You know nothing about its size directly, so you must compare it
with something whose size you do know.

</details>

<details>
<summary>Hint 2 — what to compare with</summary>

An equivalence gives you a functor $F \colon \mathcal{A} \to \mathcal{B}$. What does a functor
do to the arrows from $A$ to $A'$? Write that as a function between two hom-classes.

</details>

<details>
<summary>Hint 3 — the two halves</summary>

Look again at the definitions of "full" and "faithful" in 1E §3: each is a statement about
exactly the function you wrote down in Hint 2. Separately: the class of **all** arrows of
$\mathcal{B}$ is a set. What does that say about one hom-class of $\mathcal{B}$?

</details>

## Check yourself

- Did you use essential surjectivity? Should you have needed it?
- Is the converse true: is every locally small category essentially small? Name a category from the lecture that settles this.
- You used two "working rules" about classes. Would your proof survive if "class" were made formal in some particular way? You are not asked to answer; notice that the question exists.

## Write it up

Write your proof in `proofs/3a/p05_essentially_small_locally_small.md`, then ask Claude to review it.
