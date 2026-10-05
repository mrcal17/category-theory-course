# 3A·P06 — A fixed-point form of the diagonal argument

**Type:** stretch · **Technique:** diagonal argument · **Unlocked by:** `3a_sets_and_size` §3, §6
**Source:** adapted from Leinster §3.2 (Cantor's theorem), in the general form due to Lawvere

## Statement

Let $A$ and $B$ be sets. A **fixed point** of a function $t \colon B \to B$ is an element
$b \in B$ with $t(b) = b$.

1. Suppose there is a surjection $\varphi \colon A \to B^A$. Prove that **every** function
   $t \colon B \to B$ has a fixed point.
2. Deduce that there is no surjection $\mathbb{N} \to \mathbb{N}^{\mathbb{N}}$: the functions
   $\mathbb{N} \to \mathbb{N}$ cannot be listed as $\varphi(0), \varphi(1), \varphi(2), \dots$

## What you may use

- The definition of the function set $B^A$ (3A §3): for $a \in A$, $\varphi(a)$ is a function $A \to B$, so $\varphi(a)(a')$ is an element of $B$ for every $a' \in A$.
- The definition of surjection.
- The proof of Cantor's theorem (Theorem 4) as a model, but not its statement: part 1 is not a consequence of Theorem 4.

## What a complete proof must show

- [ ] Part 1: for an arbitrary $t \colon B \to B$, a specific function $A \to B$ built from $\varphi$ and $t$, with a check that it is a function $A \to B$.
- [ ] The step where surjectivity of $\varphi$ is applied, and to which element of $B^A$.
- [ ] An explicit element $b \in B$ and a verification that $t(b) = b$, with each equality justified.
- [ ] Part 2: a specific function $\mathbb{N} \to \mathbb{N}$ to play the role of $t$, the verification of the property of it that you need, and the logical form of the deduction (contrapositive or contradiction).

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Part 1 is a direct proof of a "for every $t$ there exists $b$" statement, so you must construct
$b$ from $t$ and $\varphi$. Part 2 uses part 1 in contrapositive form: to show that no
surjection exists, find one function $t$ that part 1 says cannot exist alongside a surjection.

</details>

<details>
<summary>Hint 2 — reread Cantor's proof with $B$ in mind</summary>

In Theorem 4, think of a subset of $A$ as a function $A \to 2$ (exercise P01). The set $D$ was
defined by looking at "$a \in f(a)$", which uses $a$ twice, and then *flipping* the answer.
What is the analogue of "using $a$ twice" for $\varphi \colon A \to B^A$? And what plays the
role of the flip?

</details>

<details>
<summary>Hint 3 — using surjectivity</summary>

Once you have built a function $A \to B$, surjectivity of $\varphi$ gives you an element of $A$
with a certain property. In Cantor's proof, the contradiction came from asking a question about
that very element. Ask the analogous question here; this time the answer is not a contradiction
but the conclusion.

</details>

<details>
<summary>Hint 4 — part 2</summary>

You need a function $\mathbb{N} \to \mathbb{N}$ that moves every natural number. The simplest
function on $\mathbb{N}$ that is not the identity will do.

</details>

## Check yourself

- In part 1, did you verify $t(b) = b$ by a chain of equalities each with a reason, or did you only assert it?
- Take $B = 2$. Which function $t \colon 2 \to 2$ has no fixed point, and which theorem of the lecture do you recover?
- Your proof of part 1 should not have used anything about $B$. Does it? What if $B$ has exactly one element: is the conclusion still correct, and is the hypothesis satisfiable?

## Write it up

Write your proof in `proofs/3a/p06_diagonal_fixed_point.md`, then ask Claude to review it.
