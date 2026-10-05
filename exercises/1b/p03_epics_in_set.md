# 1B·P03 — Epic in Set means surjective

**Type:** core · **Technique:** choosing a test object; contrapositive · **Unlocked by:** `1b_isomorphisms_duality` §2
**Source:** adapted from Riehl §1.2 (Leinster treats this in §5.2)

## Statement

Let $f \colon A \to B$ be a function between sets. Prove that $f$ is an epimorphism in
$\mathbf{Set}$ if and only if $f$ is surjective.

## What you may use

- The definition of epic (`1b_isomorphisms_duality` §2) and of surjective (0B).
- Two functions are equal when they have the same domain and codomain and agree at every element.
- You may *not* quote Proposition 2.1 and "duality": $\mathbf{Set}^{\mathrm{op}}$ is not
  $\mathbf{Set}$, so the statement about monics in $\mathbf{Set}$ does not dualize to a
  statement about epics in $\mathbf{Set}$. The structure of that proof is still a good guide.

## What a complete proof must show

- [ ] Both directions, each labelled.
- [ ] (Surjective implies epic) An arbitrary set $C$ and arbitrary functions $g, h \colon B \to C$ with $g \circ f = h \circ f$ are fixed, and $g(b) = h(b)$ is proved for **every** $b \in B$, saying where surjectivity is used.
- [ ] (Epic implies surjective) A specific set $C$ and two specific functions $B \to C$ are defined completely, it is checked that they agree after composing with $f$, and the conclusion is drawn from the definition of epic.
- [ ] The logical form of the second direction (direct, contrapositive or contradiction) is stated.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Two implications. One of them takes arbitrary test functions and argues element by element.
The other has a hypothesis of the form "for every set $C$ and all $g, h$ ..." and, as in
Proposition 2.1, you get to *choose* $C$, $g$ and $h$. Decide which is which before you start.

</details>

<details>
<summary>Hint 2 — the direction with a choice</summary>

It is easier to prove the contrapositive: if $f$ is not surjective, then $f$ is not epic. Write
out exactly what "not surjective" hands you, and exactly what "not epic" requires you to
produce.

</details>

<details>
<summary>Hint 3 — what the test functions must do</summary>

You need two functions out of $B$ that cannot be told apart by anything in the image of $f$,
yet are different functions. Where in $B$ are they allowed to differ? How many elements does
the codomain $C$ need for two functions into it to be able to differ at all?

</details>

<details>
<summary>Hint 4 — the other direction</summary>

Given $b \in B$, the equation $g \circ f = h \circ f$ only tells you about values of $g$ and
$h$ at points of the form $f(a)$. What lets you put an arbitrary $b$ in that form?

</details>

## Check yourself

- Are your two test functions defined on *all* of $B$, with their values stated everywhere?
- Did you show that they are different functions, and that they agree after composing with $f$?
- Does your argument survive when $A$ is empty? When $B$ is empty?
- Proposition 2.2 shows that in $\mathbf{Mon}$ an epic need not be surjective. Which step of your proof has no counterpart in $\mathbf{Mon}$?

## Write it up

Write your proof in `proofs/1b/p03_epics_in_set.md`, then ask Claude to review it.
