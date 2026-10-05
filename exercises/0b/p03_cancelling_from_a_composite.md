# 0B·P03 — What a composite tells you about its factors

**Type:** core · **Technique:** direct proof; using a hypothesis about a composite · **Unlocked by:** `0b_proof_toolkit_definitions` §4
**Source:** adapted from Hammack Ch 12

## Statement

Let $f \colon A \to B$ and $g \colon B \to C$ be functions. Prove both of the following.

**(a)** If $g \circ f$ is injective, then $f$ is injective.

**(b)** If $g \circ f$ is surjective, then $g$ is surjective.

## What you may use

- The definitions of function, composite, injective and surjective (0B §1, §3, §4).
- Do not use left or right inverses: the statement makes no claim that any exist.

## What a complete proof must show

- [ ] Parts (a) and (b) are proved separately, each with its own Goal and Given.
- [ ] In each part the first sentence is the one dictated by the definition of the property
      being proved (of $f$ in (a), of $g$ in (b)), not of $g \circ f$.
- [ ] The hypothesis about $g \circ f$ is applied to explicitly named elements.
- [ ] In (b), a witness is named, the set it belongs to is stated, and the required equation is
      verified.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Two direct proofs. In each, be careful about which function the *goal* is about and which
function the *hypothesis* is about; they are different functions with different domains or
codomains. Write the first and last lines of each part before attempting the middle.

</details>

<details>
<summary>Hint 2 — part (a)</summary>

Your first line gives you an equation between two elements of $B$. The hypothesis can only be
applied to an equation between two elements of $C$ of a particular form. What are you always
allowed to do to both sides of an equation between elements of $B$, given the functions
available?

</details>

<details>
<summary>Hint 3 — part (b)</summary>

Your first line gives you an element of $C$. The hypothesis then hands you an element, but of
which set? The goal wants an element of which set? The functions in the statement give you a
way to get from the one set to the other.

</details>

## Check yourself

- In (a), did you need $g$ to be injective? In (b), did you need $f$ to be surjective?
- The lecture's example $v \circ u = 1_{\mathbb{N}}$ shows that in (a) nothing can be concluded
  about $g$. What does the same example say about $f$ in (b)?
- Which earlier result becomes a special case of (a) when $g \circ f$ is an identity function?
  What does (b) give in the same way?

## Write it up

Write your proof in `proofs/0b/p03_cancelling_from_a_composite.md`, then ask Claude to review it.
