# 3A·P02 — Elements are maps from the one-element set

**Type:** warm-up · **Technique:** explicit bijection; equality of functions · **Unlocked by:** `3a_sets_and_size` §1
**Source:** adapted from Leinster §3.1

## Statement

Let $1 = \{\ast\}$ be a one-element set. For each set $A$ define
$$E_A \colon \mathbf{Set}(1, A) \to A, \qquad E_A(e) = e(\ast).$$

1. Prove that $E_A$ is a bijection, for every set $A$. (So an element of $A$ "is" a function
   $1 \to A$.)
2. Prove that these bijections are compatible with functions: for every function
   $f \colon A \to B$ and every $e \colon 1 \to A$,
   $$E_B(f \circ e) = f(E_A(e)).$$
3. Deduce that two functions $f, g \colon A \to B$ are equal if and only if
   $f \circ e = g \circ e$ for every function $e \colon 1 \to A$.

## What you may use

- What a function is, and that two functions with the same domain and codomain are equal when they agree at every element of the domain (0B, 3A §1).
- A function is a bijection if and only if it is injective and surjective, or equivalently has a two-sided inverse (0B).
- In part 3 you may use parts 1 and 2.

## What a complete proof must show

- [ ] Part 1: either injectivity and surjectivity of $E_A$, or an inverse with both composites checked.
- [ ] In part 1, a clear distinction between an element $a \in A$ and the function $1 \to A$ that corresponds to it.
- [ ] Part 1 must cover $A = \emptyset$; say how your argument handles it.
- [ ] Part 2: both sides identified as elements of $B$, and each equality justified by a definition.
- [ ] Part 3: both directions, with the place where surjectivity of $E_A$ is used marked.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Part 1 is a bijection proof; decide first whether you will exhibit an inverse or prove
injectivity and surjectivity. Part 2 is an unfolding of definitions. Part 3 is an "if and only
if" in which one direction needs no work and the other is where parts 1 and 2 are used.

</details>

<details>
<summary>Hint 2 — part 1</summary>

A function out of $1$ has only one value to specify. Given $a \in A$, what is the function
$1 \to A$ you would associate with it? And if two functions $1 \to A$ have the same value at
$\ast$, at how many elements of their domain do they agree?

</details>

<details>
<summary>Hint 3 — part 3</summary>

To show $f = g$ you must show they agree at an arbitrary $a \in A$. The hypothesis is about
functions out of $1$, not about elements. Which part tells you that the element $a$ comes from
such a function, and which part lets you move $f$ past $E$?

</details>

## Check yourself

- In part 1, did you check both composites (or both of injective and surjective)?
- How many functions $1 \to \emptyset$ are there, and is that consistent with part 1?
- Part 3 says that functions out of $1$ are enough to tell any two functions apart. Would functions out of $\emptyset$ do the same job? Would functions out of a two-element set?
- Is there a set $T$ such that functions $T \to A$ correspond to *pairs* of elements of $A$? (No proof asked for.)

## Write it up

Write your proof in `proofs/3a/p02_elements_as_maps.md`, then ask Claude to review it.
