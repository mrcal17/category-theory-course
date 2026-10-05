# 4B·P06 — Natural operations on groups

**Type:** stretch · **Technique:** transporting the Yoneda bijection along a representation · **Unlocked by:** `4b_yoneda_lemma` §8
**Source:** adapted from Riehl §2.2

## Statement

Let $U \colon \mathbf{Grp} \to \mathbf{Set}$ be the forgetful functor. For each integer $n$ and each
group $G$ (written multiplicatively) define

$$\pi^n_G \colon U(G) \to U(G), \qquad \pi^n_G(x) = x^n .$$

1. Prove that for each $n \in \mathbb{Z}$, the family $\pi^n = (\pi^n_G)_G$ is a natural
   transformation $U \Rightarrow U$. (Note that $\pi^n_G$ is usually not a homomorphism; it does
   not have to be.)
2. Prove that every natural transformation $\alpha \colon U \Rightarrow U$ is equal to $\pi^n$ for
   **exactly one** integer $n$.

So the only operations $G \to G$ that can be defined "uniformly for all groups at once" are the
power maps.

## What you may use

- From 4A §2: for every group $G$ and every $x \in G$ there is exactly one homomorphism
  $\varphi_x \colon \mathbb{Z} \to G$ with $\varphi_x(1) = x$, and $\varphi_x(k) = x^k$.
- The definition of a natural transformation; homomorphisms preserve powers.
- Optionally, if you have completed it: the covariant Yoneda lemma (4B·P03) together with the
  representation $U \cong H^{\mathbb{Z}}$. If you take this route you must track carefully how a
  natural transformation $U \Rightarrow U$ corresponds to one $H^{\mathbb{Z}} \Rightarrow U$.

## What a complete proof must show

- [ ] Part 1: naturality of $\pi^n$ is stated for an arbitrary homomorphism $\theta \colon G \to G'$
      and verified, including for negative $n$ and $n = 0$.
- [ ] Part 2, existence: an integer $n$ is extracted from $\alpha$, and $\alpha_G(x) = x^n$ is proved
      for every group $G$ and every $x \in G$.
- [ ] Part 2, uniqueness: if $\pi^m = \pi^n$ then $m = n$, with a specific group and element
      exhibited.
- [ ] Wherever the group $\mathbb{Z}$ appears, it is clear whether it is being written additively,
      and what "$x^k$" means there.

## Hints — one at a time

<details>
<summary>Hint 1 — the shape of the proof</summary>

Part 1 is a routine naturality check. Part 2 is a "follow the identity" argument in disguise: $U$
is representable, so a natural transformation out of $U$ should be determined by a single value.
Decide first *where* that single value lives: in which group, and at which element.

</details>

<details>
<summary>Hint 2 — where to evaluate</summary>

Under the representation $H^{\mathbb{Z}} \cong U$, the identity homomorphism $1_{\mathbb{Z}}$
corresponds to a particular element of a particular group. That element is where $\alpha$ should
be evaluated. The value you get is an element of the same group. What kind of thing is it?

</details>

<details>
<summary>Hint 3 — spreading the value to every group</summary>

Given a group $G$ and $x \in G$, there is a homomorphism into $G$ that sends your special element
to $x$. Write down the naturality square of $\alpha$ at that homomorphism and evaluate it at the
special element. Be careful translating between additive notation in $\mathbb{Z}$ and
multiplicative notation in $G$.

</details>

<details>
<summary>Hint 4 — uniqueness</summary>

To show that $\pi^m$ and $\pi^n$ are different when $m \ne n$ you need one group and one element
on which they disagree. The group you used in Hint 2 has an element on which all the power maps
take different values.

</details>

## Check yourself

- In $\mathbb{Z}$ written additively, what is "$x^n$"? Did you use this consistently?
- Which $n$ gives the identity transformation? Which gives the transformation sending everything
  to the identity element? Which gives inversion?
- What is the composite $\pi^m \circ \pi^n$? Does this match a familiar operation on $\mathbb{Z}$?

## Write it up

Write your proof in `proofs/4b/p06_natural_operations_on_groups.md`, then ask Claude to review it.
