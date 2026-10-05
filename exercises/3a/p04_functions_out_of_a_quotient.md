# 3A·P04 — Functions out of a quotient

**Type:** core · **Technique:** well-definedness, existence and uniqueness · **Unlocked by:** `3a_sets_and_size` §5
**Source:** adapted from Leinster §3.1

## Statement

Let $\sim$ be an equivalence relation on a set $A$, with quotient set $A/{\sim}$ and quotient
map $p \colon A \to A/{\sim}$, $p(a) = [a]$. Let $f \colon A \to B$ be a function such that
$$a \sim a' \implies f(a) = f(a') \qquad \text{for all } a, a' \in A.$$
Prove that there is exactly one function $\bar f \colon A/{\sim} \to B$ with $\bar f \circ p = f$.

## What you may use

- The definitions of equivalence relation, equivalence class, quotient set and quotient map (3A §5).
- The two facts in the reading list there: $p(a) = p(a')$ if and only if $a \sim a'$; and $p$ is surjective.
- What a function is: a rule assigning to each element of the domain **exactly one** element of the codomain.

## What a complete proof must show

- [ ] *Existence:* a definition of $\bar f$ on an arbitrary element of $A/{\sim}$.
- [ ] A proof that this definition is **well defined**: the value does not depend on anything you chose in order to write it down. This step must use the hypothesis on $f$, and must say so.
- [ ] The equation $\bar f \circ p = f$, checked at an arbitrary $a \in A$.
- [ ] *Uniqueness:* if $k \colon A/{\sim} \to B$ also satisfies $k \circ p = f$, then $k = \bar f$, checked at an arbitrary element of $A/{\sim}$.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Existence and uniqueness, as in Proposition 3 of the lecture (the equalizer). There, the delicate
point was that a function *into a subset* must have its values in the subset. Here the function
goes *out of a set of classes*, and the delicate point is the mirror image.

</details>

<details>
<summary>Hint 2 — existence</summary>

An element of $A/{\sim}$ is a class, and a class can be written as $[a]$ for many different
$a$. The equation $\bar f \circ p = f$ leaves you no choice about what $\bar f([a])$ should be.
So what is the danger in simply writing that formula down as the definition?

</details>

<details>
<summary>Hint 3 — well defined</summary>

Suppose the same class has two names, $[a] = [a']$. What do you need to be true for your
formula to give one answer and not two? Which of the listed facts connects $[a] = [a']$ with
the hypothesis on $f$?

</details>

<details>
<summary>Hint 4 — uniqueness</summary>

To show two functions on $A/{\sim}$ are equal you must compare them at an arbitrary class.
Which property of $p$ lets you write an arbitrary class in a form to which the equations
$k \circ p = f$ and $\bar f \circ p = f$ apply?

</details>

## Check yourself

- Point to the sentence where you used the hypothesis "$a \sim a'$ implies $f(a) = f(a')$". If you cannot find it, the proof has a gap.
- Did uniqueness use surjectivity of $p$? Would uniqueness hold for a non-surjective $p$?
- Recognise this in algebra: what does the statement say when $A$ is a group, $\sim$ is "same coset of a normal subgroup $N$", and $f$ is a homomorphism with $N$ in its kernel? (The set-level part only.)

## Write it up

Write your proof in `proofs/3a/p04_functions_out_of_a_quotient.md`, then ask Claude to review it.
