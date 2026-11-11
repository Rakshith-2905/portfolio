---
layout: post
kind: Project
title: "CertiSeal: certifying real images in the age of deepfakes"
date: 2026-06-18
excerpt: "A training-free scheme that seals an image so anyone can later verify whether it has been tampered with, where, and who vouched for it — built on tolerance-calibrated, signed region fingerprints."
---

Deepfakes made "is this image real?" the wrong question. Detectors that guess *AI-vs-real* are in an arms race they keep losing. **CertiSeal** doesn't play that game — it never says "not AI." It flips the problem: let the *source* seal an image at creation, so anyone can later answer a narrower, provable question — **is this the sealed original, has it changed, where, and who vouched for it?**

The rest of this post is the actual construction. It's training-free: no model to fine-tune or fool, just a fingerprint calibrated to be invariant to the edits we tolerate and fragile to the ones we don't.

## Setup

An image is mapped to a canonical luma–chroma array {::nomarkdown}\(\tilde I \in [0,1]^{S\times S\times 3}\){:/nomarkdown} (YCbCr, Lanczos-resampled, {::nomarkdown}\(S=512\){:/nomarkdown}). We define a global region {::nomarkdown}\(R_0\){:/nomarkdown} (the whole frame) and {::nomarkdown}\(49\){:/nomarkdown} local regions {::nomarkdown}\(R_1,\dots,R_{49}\){:/nomarkdown}: {::nomarkdown}\(128\times128\){:/nomarkdown} windows on a stride-{::nomarkdown}\(64\){:/nomarkdown} grid, i.e. a {::nomarkdown}\(7\times 7\){:/nomarkdown} lattice at 50% overlap. Overlap matters — a tamper on a region boundary still lands squarely inside a neighbor.

## 1 — The region fingerprint

For a region with luma window {::nomarkdown}\(x\in\mathbb R^{w\times w}\){:/nomarkdown}, first remove first-order photometry:

{::nomarkdown}\[ \mu = \tfrac{1}{w^2}\textstyle\sum_{i} x_i,\qquad g=\max\big(\sigma(x),\,0.04\big),\qquad \hat x = \frac{x-\mu}{g}. \]{:/nomarkdown}

Subtracting {::nomarkdown}\(\mu\){:/nomarkdown} and dividing by the gain {::nomarkdown}\(g\){:/nomarkdown} makes {::nomarkdown}\(\hat x\){:/nomarkdown} invariant to any affine tone map {::nomarkdown}\(x\mapsto \alpha x+\beta\){:/nomarkdown} — so global brightness/contrast shifts don't move these coefficients. The photometry is not thrown away, though: it is recorded separately, with its own tolerance, below. Take the orthonormal 2-D DCT {::nomarkdown}\(\mathcal D\){:/nomarkdown} and keep the {::nomarkdown}\(k=12\){:/nomarkdown} lowest AC coefficients along the zig-zag {::nomarkdown}\(\zeta\){:/nomarkdown}:

{::nomarkdown}\[ a \;=\; \frac{W_0}{w}\Big(\,[\mathcal D\hat x]_{\zeta(1)},\dots,[\mathcal D\hat x]_{\zeta(k)}\Big)\in\mathbb R^{12}. \]{:/nomarkdown}

Here {::nomarkdown}\(W_0=128\){:/nomarkdown} is the local window size, so the factor is 1 for local regions and only rescales the 512-pixel global region. It keeps coefficients {::nomarkdown}\(O(1)\){:/nomarkdown} and independent of window size. The full per-region feature vector appends the two chroma means and the photometry it factored out:

{::nomarkdown}\[ \varphi(R)=\big(\,a\in\mathbb R^{12},\ \bar c_b,\ \bar c_r,\ \mu,\ \ln g\,\big)\in\mathbb R^{16}. \]{:/nomarkdown}

**Why an orthonormal transform.** Because {::nomarkdown}\(\mathcal D\){:/nomarkdown} is unitary, Parseval gives the non-expansive (1-Lipschitz) bound

{::nomarkdown}\[ \big\|\mathcal D\hat x-\mathcal D\hat x'\big\|_2=\big\|\hat x-\hat x'\big\|_2 . \tag{1} \]{:/nomarkdown}

Coefficient drift is therefore *bounded by* normalized-pixel drift — never amplified. This is what lets us reason about tolerances in coefficient space and have them mean something in pixel space.

## 2 — Tolerance as a dithered-bin fuzzy commitment

Each scalar feature {::nomarkdown}\(c_m\){:/nomarkdown} carries a tolerance half-width {::nomarkdown}\(t_m\){:/nomarkdown}, i.e. a bin width {::nomarkdown}\(w_m=2t_m\){:/nomarkdown}. For profile 1: {::nomarkdown}\(t=8\){:/nomarkdown} for the luma coefficients, {::nomarkdown}\(0.05\){:/nomarkdown} for chroma means, {::nomarkdown}\(0.08\){:/nomarkdown} for {::nomarkdown}\(\mu\){:/nomarkdown}, {::nomarkdown}\(0.15\){:/nomarkdown} for {::nomarkdown}\(\ln g\){:/nomarkdown}. We quantize each feature to a bin, but first **dither** it to the bin center. Let {::nomarkdown}\(\Delta_5=w_m/2^{5}\){:/nomarkdown} and

{::nomarkdown}\[ d_m=\Delta_5\!\cdot\!\operatorname{round}\!\Big(\tfrac{1}{\Delta_5}\big[(\tfrac{w_m}{2}-c_m)\bmod w_m\big]\Big),\qquad b_m=\Big\lfloor \tfrac{c_m+d_m}{w_m}\Big\rfloor . \]{:/nomarkdown}

**Centering lemma.** By construction {::nomarkdown}\(c_m+d_m\equiv \tfrac{w_m}{2}\pmod{w_m}\){:/nomarkdown}: the feature sits at the middle of its bin. Hence for any re-measured {::nomarkdown}\(c_m'\){:/nomarkdown},

{::nomarkdown}\[ |c_m'-c_m|<t_m \;\Longrightarrow\; \Big\lfloor \tfrac{c_m'+d_m}{w_m}\Big\rfloor=b_m . \tag{2} \]{:/nomarkdown}

A drift smaller than the half-width leaves the bin index untouched; a larger one flips it. That inequality *is* the tolerance.

The region's commitment hashes its bin indices under a per-image salt {::nomarkdown}\(s\){:/nomarkdown}, truncated to 96 bits:

{::nomarkdown}\[ \kappa_R=\Big[\operatorname{SHA256}\!\big(s\,\|\,R\,\|\,b_1\,\|\cdots\|\,b_{16}\big)\Big]_{0:96}. \]{:/nomarkdown}

The published payload for a region is only {::nomarkdown}\((d_1,\dots,d_{16},\ \kappa_R)\){:/nomarkdown}. The dithers leak nothing beyond sub-bin position, and {::nomarkdown}\(\kappa_R\){:/nomarkdown} is a one-way commitment to the bins — this is a *fuzzy commitment*: exact within the tolerance box, cryptographically binding outside it. Verification is a hash equality, so a region passes **iff every feature stayed in-bin**:

{::nomarkdown}\[ \textsf{ok}(R)=1 \iff \big[\operatorname{SHA256}(s\|R\|b_1'\|\cdots\|b_{16}')\big]_{0:96}=\kappa_R \iff \forall m:\ |c_m'-c_m|<t_m . \]{:/nomarkdown}

## 3 — Signing and lineage

The assertion {::nomarkdown}\(P\){:/nomarkdown} bundles the profile, issuer class, signer id, timestamp, salt, the per-region records {::nomarkdown}\(\{(R,d_R,\kappa_R)\}\){:/nomarkdown}, and an optional `parent_ref`. It is hashed and signed with ECDSA over P-256:

{::nomarkdown}\[ h=\operatorname{SHA256}\big(\textsf{canon}(P)\big),\qquad \sigma=\textsf{ECDSA-P256}_{sk}(h)=(r,s'). \]{:/nomarkdown}

A registry maps {::nomarkdown}\(\textsf{id}\mapsto(\text{class},\ pk)\){:/nomarkdown}. Acceptance requires the digest to recompute, {::nomarkdown}\(\sigma\){:/nomarkdown} to verify under {::nomarkdown}\(pk\){:/nomarkdown}, the class to match the certificate, and a **lineage-typing** rule:

{::nomarkdown}\[ \text{class}=\textsf{editor}\ \Longrightarrow\ \texttt{parent\_ref}\neq\varnothing . \]{:/nomarkdown}

Editors may only issue *derivative* seals that name a parent; an editor key that tries to assert `origin` is rejected **at seal time**. That single typing rule is what stops "wash a doctored image through a fresh seal and call it original."

## 4 — The verdict

Verification recomputes {::nomarkdown}\(\varphi\){:/nomarkdown} for every region and collects the failing set {::nomarkdown}\(F=\{R:\textsf{ok}(R)=0\}\){:/nomarkdown}. With local failures {::nomarkdown}\(F_{\text{loc}}=F\setminus\{R_0\}\){:/nomarkdown}, {::nomarkdown}\(n=49\){:/nomarkdown}, and threshold {::nomarkdown}\(\tau=0.80\){:/nomarkdown}:

{::nomarkdown}\[ \textsf{verdict}=\begin{cases} \textsf{UNALIGNABLE}, & R_0\in F \ \wedge\ |F_{\text{loc}}|\ge \tau n,\\[2pt] \textsf{INTACT}, & F=\varnothing,\\[2pt] \textsf{TAMPERED}\ (\text{flag } F_{\text{loc}}), & \text{otherwise.} \end{cases} \]{:/nomarkdown}

The logic: a genuine local edit trips a *sparse* set of regions, which we report as a heatmap. A global desync (wholesale replacement, or a large crop or rotation) trips the global region *and* almost everything at once — that's `UNALIGNABLE`, not a localization claim. Small crops and rotations can fall short of that threshold and show up as widespread `TAMPERED` instead (see the sweep below). Pixels are always rechecked, even when the signature is valid, so a **valid manifest stapled onto different content** fails the fingerprint rather than passing.

**Separation, informally.** A benign transform {::nomarkdown}\(T\){:/nomarkdown} whose per-feature drift stays below every {::nomarkdown}\(t_m\){:/nomarkdown} keeps all regions in-bin by (2), so {::nomarkdown}\(F=\varnothing\Rightarrow\textsf{INTACT}\){:/nomarkdown}. A tamper supported on a pixel set {::nomarkdown}\(\mathcal S\){:/nomarkdown} will, if it is large enough relative to a region, force some coefficient drift {::nomarkdown}\(\ge t_m\){:/nomarkdown} in the regions overlapping {::nomarkdown}\(\mathcal S\){:/nomarkdown} (the change is real and, by (1), visible in coefficient space), so those regions enter {::nomarkdown}\(F_{\text{loc}}\){:/nomarkdown} and are localized. Calibrating the {::nomarkdown}\(t_m\){:/nomarkdown} is exactly choosing the boundary between "benign" and "tamper," and an edit that is small relative to its region can stay below it. The sensitivity test below measures where that happens.

## 5 — The pixel tier

Metadata gets stripped, so a 192-bit record is also carried *in the pixels* —

{::nomarkdown}\[ \textsf{magic}_{16}\ \|\ \operatorname{SHA256}(\textsf{id})_{0:32}\ \|\ \textsf{ts}_{32}\ \|\ h_{0:96}\ \|\ \textsf{CRC}_{16}, \]{:/nomarkdown}

embedded by dithered **QIM** on mid-band {::nomarkdown}\(8\times8\){:/nomarkdown} block-DCT luma coefficients with step {::nomarkdown}\(\delta=14\){:/nomarkdown}. To write bit {::nomarkdown}\(b\){:/nomarkdown} into coefficient {::nomarkdown}\(c\){:/nomarkdown}:

{::nomarkdown}\[ q=\operatorname{round}\!\Big(\tfrac{c}{\delta}-\tfrac{b}{2}\Big),\qquad c'=\Big(q+\tfrac{b}{2}\Big)\delta, \]{:/nomarkdown}

i.e. the two bit values quantize to interleaved lattices offset by {::nomarkdown}\(\delta/2\){:/nomarkdown}; a nearest-lattice decoder recovers {::nomarkdown}\(b\){:/nomarkdown} under any perturbation {::nomarkdown}\(|\Delta c|<\delta/4\){:/nomarkdown}. Slots are chosen by a fixed PRF assignment, and each bit is repetition-coded with majority vote (a stand-in for Raptor codes). On verify, the recovered {::nomarkdown}\(h_{0:96}\){:/nomarkdown} is cross-checked against the manifest digest — a mismatch flags a transplanted manifest.

## Worked examples

Everything below is a real run of the reference build on a real photograph (NASA's public-domain portrait of astronaut Eileen Collins): sealed once, then edited and checked.

First, the seal is imperceptible. The pixel-tier record moves no pixel by more than **5/255** (mean 0.49), yet it can be read back on verify:

<figure>
  <img src="{{ '/assets/img/posts/certiseal-seal-invisible.jpg' | relative_url }}" alt="Original, sealed, and 20x-amplified difference showing the invisible watermark">
  <figcaption>Original and sealed are visually identical; the difference (×20) is the embedded pixel-tier record.</figcaption>
</figure>

Then five realistic edits of the kind people actually make. (Seven more photos, a 272-check robustness sweep, ten Stable Diffusion inpainting edits and a 2,880-trial sensitivity test follow in the next section.) Each edited image is shown above the verifier's heatmap of the regions that failed their commitment:

<figure>
  <img src="{{ '/assets/img/posts/certiseal-tamper-gallery.jpg' | relative_url }}" alt="Five edits of a sealed photo and the regions CertiSeal flagged for each">
  <figcaption>Copy-move, object removal, a splice from another photo and a recolor are all flagged and localized. A light face retouch (slight blur and +6% brightness) stays inside the tolerance and verifies INTACT, which is the benign envelope doing its job.</figcaption>
</figure>

That last column is a deliberate trade-off, not a bug: the tolerance box is meant to let mild adjustments pass and structural changes fail. Where that line sits is a choice made per profile, and the retouch shows where profile 1 draws it on this photo. (The sweep in the next section shows the line is not yet in the right place for brightness on every photo.)

The complete verdict table from the run, every row a real output:

| Input | Verdict | Detail |
|---|---|---|
| untouched | `INTACT` | origin: flux-2-server-01 (generator) |
| JPEG q85 | `INTACT` | |
| JPEG q75, ×5 recompressions | `INTACT` | |
| resize 0.75× | `INTACT` | |
| brightness +8% | `INTACT` | |
| contrast +10% | `INTACT` | |
| copy-move (patch cloned onto helmet) | `TAMPERED` | 6 regions |
| object removal (shuttle painted out) | `TAMPERED` | 15 regions |
| splice (coffee cup from another photo) | `TAMPERED` | 7 regions |
| suit recolored orange to blue | `TAMPERED` | 15 regions + global |
| light face retouch | `INTACT` | inside the tolerance |
| synthetic splice → resize 0.9 → JPEG80 | `TAMPERED` | same 9 regions survive laundering |
| small low-contrast recolor patch | `INTACT` | below the tolerance on this photo |
| manifest stripped | `NO-CREDENTIALS` | pixel tier still recovers the signer tag |
| stolen manifest on other image | `UNALIGNABLE` | global + near-all regions mismatch |
| editor key claims `origin` | **REJECTED** | at seal time, by lineage typing |

## Beyond one photo

One photograph is a demo, not evidence. So I ran the same build on seven more freely licensed test images from the scikit-image library, chosen to stress different things: a close-up portrait of a cat, a coffee cup, a night-time launch pad, a grayscale street photo, a scanned document, a Hubble deep field full of tiny bright points, and a stained microscopy slide. Six of them were sealed, given one realistic hand-made edit, and checked; the cat is saved for the AI inpainting test further down. Each was also put through a harmless resize-and-recompress (0.8× then JPEG quality 80) to look for false alarms.

<figure>
  <img src="{{ '/assets/img/posts/certiseal-gallery-varied.jpg' | relative_url }}" alt="Six photos, each shown sealed, edited and with the verifier's heatmap, plus one false positive">
  <figcaption>Sealed, edited and heatmap for each photo. All six edits are caught and localized, including a deleted line of text, a duplicated galaxy and a duplicated tissue region (the classic research-image fraud). The two rows in red are a failure: the grayscale street photo throws a false positive on a harmless 0.8× resize, in one region of high-frequency grass.</figcaption>
</figure>

### Where harmless edits stop passing

Next, every photo went through 34 common transformations, 272 checks in all:

<figure>
  <img src="{{ '/assets/img/posts/certiseal-robustness.png' | relative_url }}" alt="Grid of verdicts for 8 photos under 34 transformations">
  <figcaption>Green passes, red is flagged (the number is how many of the 49 regions failed), grey is UNALIGNABLE. Every cell is a real verification.</figcaption>
</figure>

The pattern is clear, and more useful than any single headline number:

- **Compression is solved.** All 8 photos pass every JPEG quality down to 40, and five rounds of recompression at 75. The only failure in 64 JPEG checks is one region at quality 30.
- **Upscaling and mild downscaling are fine. Strong downscaling is not.** Every photo passes at 1.25× and 1.5×, and 30 of 32 checks pass from 0.75× upward. At 0.6× and below, the three most textured photos (coffee, rocket, cameraman) start to fail, and the deep field joins them at 0.4×.
- **Photometric edits are the weak spot.** At ±10% brightness only 10 of 16 checks pass, and at ±20% none do. Contrast at ±10% passes 13 of 16. The tolerance was calibrated on synthetic images, and natural photos with large flat or dark areas sit closer to the bin edges. This is the strongest argument for re-fitting the tolerances on real photo corpora.
- **Blur of σ = 1 or more, and any crop or rotation, fail everywhere.** That is expected without a geometric sync template. Note that small crops and rotations show up as TAMPERED across many regions, not as UNALIGNABLE, so for now a 2% crop is indistinguishable from heavy tampering.

### Against real AI inpainting

Hand-made edits are one thing. The edits people actually worry about now come from generative inpainting. So I sealed four photos and edited each with Stable Diffusion 1.5 inpainting, run locally (30 steps, guidance 7.5, fixed seed). Each edit was checked in two forms. *Composited* pastes only the generated pixels back into the sealed photo, which is roughly what Generative Fill does. *Raw* takes the model's whole output, so every pixel of the photo has passed through the diffusion model's autoencoder.

<figure>
  <img src="{{ '/assets/img/posts/certiseal-ai-inpaint.jpg' | relative_url }}" alt="Five Stable Diffusion inpainting edits with CertiSeal heatmaps for composited and fully regenerated versions">
  <figcaption>Columns: the sealed original, the AI-inpainted edit, the verifier's heatmap, and the heatmap when the whole image comes straight out of the model. All ten are flagged, and the flagged regions sit on the edits.</figcaption>
</figure>

| Edit | Area masked | Composited | Raw |
|---|---|---|---|
| eyes recoloured blue (cat) | 6.7% | `TAMPERED`, 15 regions, all on the edit | `TAMPERED`, 15 regions, all on the edit |
| second rocket added | 8.9% | `TAMPERED`, 16 regions, all on the edit | `TAMPERED`, 15 regions, 1 off the edit |
| spoon region regenerated (coffee) | 7.7% | `TAMPERED`, 12 regions, all on the edit | `TAMPERED`, 12 regions, all on the edit |
| shuttle region regenerated (astronaut) | 18.4% | `TAMPERED`, 13 regions, all on the edit | `TAMPERED`, 13 regions, all on the edit |
| face regenerated (astronaut) | 3.6% | `TAMPERED`, 3 regions, all on the edit | `TAMPERED`, 2 regions, all on the edit |

All four untouched sealed photos verified `INTACT`, and all ten AI edits came back `TAMPERED`. Three things stand out:

- **Regenerating the whole frame is not a free pass, and not a false alarm either.** The raw outputs re-encode every pixel, yet the untouched parts of each photo stayed inside the tolerance. Only one region in ten edits was flagged off the edit. Whole-image VAE regeneration behaves like a benign recompression, and the edit still stands out.
- **A small edit can still light up widely.** The blue eyes cover under 7% of the frame, but Stable Diffusion redraws texture as well as colour, and 15 overlapping regions failed.
- **The thinnest margin is the most deepfake-like edit.** Asked to add sunglasses, the model instead redrew the face as a different-looking woman, which is effectively a small face swap. It was flagged, but only 2–3 of the 8 regions under the mask failed. Small, texture-matched face edits are where profile 1 is closest to its limit, and they are the case to calibrate on next.

In fairness to the model: it did not follow two of the prompts. It redrew the spoon rather than removing it, and it painted an object where the shuttle had been rather than plain background. Those are still realistic generative edits of exactly the regions masked, just not the edits intended.

### How small an edit can it see?

Finally, a sensitivity test. I pasted patches from other photos into random positions on all 8 images, varying the patch size and how opaque it was: 36 settings × 80 trials = 2,880 verifications.

<figure>
  <img src="{{ '/assets/img/posts/certiseal-sensitivity.png' | relative_url }}" alt="Heatmap of detection rate by patch size and opacity">
  <figcaption>Detection rate rises smoothly with both size and strength. A hard splice whose side is 8% or more of the image's short side is caught 92–100% of the time. At 5% the rate drops to 79%, and at 3% to 31%. Faint overlays at 10% opacity are caught 76% of the time only when the patch is a quarter of the short side across.</figcaption>
</figure>

That curve is the honest answer to "does it work?". Profile 1 reliably catches edits a viewer would notice at a glance. It misses edits only a few percent of the image across, and nearly transparent ones. Those need a finer region grid, which costs a bigger manifest and more benign failures. The trade-off is now measured rather than guessed.

### Missed cases

Every edit that came back `INTACT` when it shouldn't have, in one place:

| Edit | Size | Why it slipped through |
|---|---|---|
| Cat's irises recoloured blue **by hand** (a plain hue shift, no texture change) | two irises, about 4% of the frame | Only the colour changed, and each iris is a small part of its 128-pixel region, so the chroma mean stayed inside its tolerance. The same edit made with Stable Diffusion, shown above, was caught because it redraws texture too. |
| Light face retouch on the astronaut (slight blur, +6% brightness) | the face only | Deliberately mild; it sits inside profile 1's benign envelope. |
| Small low-contrast recolour patch on the astronaut | a small patch | Below the chroma tolerance on that photo. |
| Random hard splices at 3% of the short side | about 0.1% of the frame | Caught only 31% of the time in the sensitivity test. |

The common thread is size and subtlety. An edit that changes only colour, or covers a small fraction of a region, can stay inside the tolerance box. Catching it needs a finer region grid, which means a bigger manifest and more false alarms on harmless edits.

## What doesn't hold yet

I'd rather be exact about the edges than oversell:

- **No geometric sync template.** Even a 2% crop or a 1° rotation fails, either as widespread `TAMPERED` or as `UNALIGNABLE` (40 of 40 checks above), and the verifier can't yet tell a crop from a wholesale swap. Top of the list.
- The pixel tier's repetition+CRC is weaker than the manifest under heavy recompression — it dies first, before the manifest does.
- Mild **local** retouching that stays inside the tolerance (like the light face retouch above) verifies `INTACT`. Catching it means a tighter profile, which in turn passes fewer benign edits.
- Highlight **clipping** on already-saturated content is a genuine structural change, so aggressive brightness can legitimately flag regions.
- The {::nomarkdown}\(t_m\){:/nomarkdown} are calibrated on synthetic images, and the sweep above shows the cost: ±10% brightness fails on 6 of 16 natural-photo checks. They must be re-fit on natural photo corpora before any deployment.
- **Small edits are missed.** Hard splices under about 5% of the short side are caught less than 80% of the time.
- There has been **no security audit**. This is research code.

## Where it sits

CertiSeal is a v0.1 reference implementation with a paper draft behind it. It's the same thread that runs through the rest of my work: **knowing when something has changed, and being calibrated about what "changed" even means.** As the fakes get better, the durable move isn't detecting them — it's letting the real thing vouch for itself.
