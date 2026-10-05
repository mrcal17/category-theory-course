# 0B·P06 — Injective functions are the ones whose images respect intersections

**Type:** stretch · **Technique:** if-and-only-if; equality of sets; choosing what to plug in · **Unlocked by:** `0b_proof_toolkit_definitions` §4, §7
**Source:** adapted from Hammack Ch 12

## Statement

Let $f \colon A \to B$ be a function. For a subset $S \subseteq A$, the *image* of $S$ under $f$
is the subset of $B$

$$f(S) = \{\, b \in B : \text{there exists } s \in S \text{ with } f(s) = b \,\}.$$

Prove that $f$ is injective if and only if

$$f(S \cap T) = f(S) \cap f(T) \quad \text{for all subsets } S, T \subseteq A.$$

## What you may use

- The definitions of function, injective, image (above), intersection and subset.
- Two sets $X$ and $Y$ are equal exactly when $X \subseteq Y$ and $Y \subseteq X$; and
  $X \subseteq Y$ means: for all $x$, if $x \in X$ then $x \in Y$.

## What a complete proof must show

- [ ] The two directions are proved separately and labelled, each with its own Goal and Given.
- [ ] ($\Rightarrow$) The set equality is proved as two inclusions, each beginning "Let $b$ be an
      element of ...".
- [ ] ($\Rightarrow$) The proof says which inclusion holds for every function and which one uses
      injectivity, and uses different letters for different witnesses.
- [ ] ($\Leftarrow$) The proof starts the way a proof of injectivity must start, and names
      specific subsets $S$ and $T$ to which the hypothesis is applied.
- [ ] ($\Leftarrow$) Every claim about $f(S)$, $f(T)$ and $S \cap T$ for those subsets is
      justified from the definitions.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Two directions. In ($\Rightarrow$) the goal is "for all $S, T$, an equality of sets", and an
equality of sets is two inclusions; each inclusion is a "for all elements" statement. In
($\Leftarrow$) the goal is injectivity, and the hypothesis is a "for all $S, T$" statement. A
"for all" hypothesis is used by applying it to something of your own choosing.

</details>

<details>
<summary>Hint 2 — the forward direction</summary>

Unpack "$b \in f(S) \cap f(T)$" completely: it contains two "there exists" statements. Unpack
each with its own letter. You now have two elements of $A$ and some equations. What does
injectivity let you conclude, and why is that what you need for $b \in f(S \cap T)$?

</details>

<details>
<summary>Hint 3 — the backward direction: what to plug in</summary>

You begin with two elements $a, a' \in A$ with $f(a) = f(a')$. The hypothesis is about subsets
of $A$, not elements. What are the smallest subsets of $A$ that carry the information of $a$
and of $a'$?

</details>

<details>
<summary>Hint 4 — reading off the conclusion</summary>

For the subsets you chose, work out $f(S)$ and $f(T)$ from the definition of image. Is their
intersection empty? What does the hypothesis then say about $f(S \cap T)$, and what does *that*
say about $S \cap T$?

</details>

## Check yourself

- Which of the two inclusions in ($\Rightarrow$) never used injectivity? Can you find a
  non-injective function and two subsets for which the other inclusion fails?
- In ($\Leftarrow$), did the subsets you chose depend on $a$ and $a'$? Were they introduced after
  $a$ and $a'$?
- Is the image of the empty set empty? Did you use that, and if so did you justify it?

## Write it up

Write your proof in `proofs/0b/p06_injective_iff_images_preserve_intersections.md`, then ask Claude to review it.
