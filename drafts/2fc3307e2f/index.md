---
layout: post
title: "Why Every Chatbot Picks 7"
date: 2026-11-10
kind: Opinion
permalink: /drafts/2fc3307e2f/
sitemap: false
robots: noindex
unlisted: true
excerpt: "Draft, not yet published."
---

<div class="draft-banner">Draft, not yet published. Please don't share.</div>

Try this before you read on. Open any chatbot and type: *"Pick a random number between 1 and 10. Reply with only the number."*

It said 7, didn't it?

It is not your chatbot. In a test [reported by Ian Leslie](https://www.ian-leslie.com/p/why-are-llms-fixated-on-the-number) that asked each model a hundred times, GPT said 7 on 92 occasions, Claude on 90 and Gemini every single time. A [controlled study](https://arxiv.org/abs/2502.19965) by Coronado-Blázquez (2025), across six models and 75,600 queries, found 7 was "the preferred value by far for every single model." Chance would give you 7 one time in ten.

Here is the twist: **people pick 7 too.** In a classic 1976 study by [Kubovy and Psotka](https://psycnet.apa.org/record/1977-00345-001), 28% of people asked for a random digit chose 7. The chatbot did not invent our bias. It learned it from our writing and then amplified it. Raise the human preference to roughly the third power and you get the chatbot numbers almost exactly. **Chatbots pick the way people do, cubed.**

<figure>
  <img src="{{ '/assets/img/posts/oped/oped-seven.png' | relative_url }}" alt="Left: share of answers that are 7 as human preference is amplified, with people at 28% and chatbots at 80 to 92%. Right: the five most repeated jokes out of 1,008 requests.">
  <figcaption>People sit at 28%; chatbots correspond to amplifying that preference by a power of about 3 to 4. Right: asked for a joke 1,008 times, ChatGPT returned the same scarecrow joke 140 times.</figcaption>
</figure>

That is harmless for a number. It is not harmless when the request is a cover letter, a product spec or an argument about social media, and the same pull applies.

The fixes are simple, so here they are first. The evidence and the mechanics follow for anyone who wants them.

## What to do: find your 4

A model will always offer you the 7: the most likely answer, beautifully phrased. For anything that matters, find your 4 first.

1. **Hand off the chores, not the judgment.** Know which one you are asking for.
2. **Decide what good looks like before you start.** Otherwise twenty polished options pick for you.
3. **Draft before you ask.** Let the model edit your thinking, not replace it.
4. **Make it argue with you.** Ask what is wrong with your view, not to write it for you.
5. **Read it aloud.** If it doesn't sound like you, it isn't done.

And once in a while, write something with no help at all.

## The evidence

<figure>
  <img src="{{ '/assets/img/posts/oped/oped-evidence.png' | relative_url }}" alt="Bar charts: measured convergence in four controlled studies, and the estimated share of LLM-modified abstracts in four corpora">
  <figcaption>Top: how much more alike people's writing became with an LLM in controlled studies (the metrics differ, so compare direction, not length). Bottom: estimated share of published scientific writing that is already substantially LLM-modified.</figcaption>
</figure>

- **Writing gets better, and more alike.** AI ideas made stories about 8% more novel but measurably more similar to each other (Doshi and Hauser, 293 writers). With a GPT-4o autocomplete, Indian writers drifted toward Western styles (Agarwal et al.).
- **Opinions move too.** People writing with a quietly biased assistant were about twice as likely to argue its side, and their own views shifted afterwards (Jakesch et al., 1,506 people).
- **Code converges and bloats.** Models find fewer distinct algorithms than people do, about two where people find three (EMNLP Findings 2025), and agent-written code is 2.3 times more verbose than code in human projects (SlopCodeBench, 2026). Real repositories show no consistent rise in similarity yet (Marchezan et al., 2026).
- **We trust it more than we check it.** Developers with an AI assistant wrote less secure code but were more likely to believe it was secure (Perry et al.). The mistakes are real: lawyers fined for citing cases ChatGPT invented, and Air Canada held liable for a refund policy its chatbot made up.
- **It is already everywhere.** Up to 17.5% of sentences in computer-science abstracts were substantially LLM-modified by early 2024 (Liang et al.), and "delves" became 28 times more common in PubMed than its trend predicts (Kobak et al.).

The effects are small to medium and mostly from short lab studies. The worry is how they compound across billions of uses.

## Why it happens

**Models are built to predict the likely.** A language model learns from billions of sentences how likely each possible next word is. When it writes, it does not sample evenly from that whole range. A setting called temperature controls how hard it leans toward the likeliest options. Below 1, it effectively raises every probability to a power, so the popular choice gets more popular and the rare one nearly vanishes. Picture a jukebox that plays songs in proportion to their popularity, and a knob that makes the hits play even more often. That knob is the "cubing" behind the 7.

**Tuning rewards the familiar.** After this first training, assistants are fine-tuned on human ratings: people compare two answers, pick the better one, and the model learns to produce what they prefer. Raters, like all of us, tend to prefer text that feels typical: clear, balanced, safe. Mathematically, this works like turning the temperature knob down permanently, inside the model itself. Kirk et al. measured it: this kind of tuning substantially reduces output diversity. That is why, in Padmakumar and He's essay study, writing with the raw base model did not narrow people's ideas, while writing with the tuned assistant cut unique key points by about 7%.

**The loop closes.** A growing share of what gets published is model-assisted, and the next generation of models trains on it. Each round, the rare cases disappear first, like photocopying a photocopy, where the fine detail goes before anything else. Shumailov et al. showed this in *Nature*: models trained on their own output steadily lose the tails of the original distribution. The fix is known too. Collapse is avoided when fresh human writing keeps being added alongside synthetic text rather than replaced by it (Gerstgrasser et al.).

Emails converge first because they are the most delegated. Arguments follow, because we take the model's framing along with its sentences. Ideas come last.

<details class="math-box" markdown="1">
<summary>For the curious: the math behind "cubed" (a two-minute read)</summary>

**Sharpening.** At temperature \\(T\\), a model samples from

<div class="math">\[ p_T(y) \;=\; \frac{p(y)^{1/T}}{\sum_{y'} p(y')^{1/T}} . \]</div>

For \\(T<1\\), every probability is raised to a power above one, which piles weight onto the most common answers. The 7 result fits this exactly. If people put \\(h_7 = 0.28\\) on 7 and about 0.08 on each other digit, raising those preferences to a power \\(k\\) gives

<div class="math">\[ p_7(k) \;=\; \frac{h_7^{\,k}}{h_7^{\,k} + 9\,h_{\text{other}}^{\,k}} . \]</div>

The 80% rate corresponds to \\(k \approx 2.9\\), and the 90% and 92% rates to \\(k \approx 3.5\\) and \\(3.7\\). A cubed preference is the same thing as decoding at \\(T \approx 0.3\\).

<figure>
  <img src="{{ '/assets/img/posts/oped/oped-temperature.png' | relative_url }}" alt="Effective number of phrasings and head versus tail probability mass as a function of temperature">
  <figcaption>A toy space of 10,000 phrasings with word-frequency-like (Zipf) popularity. Going from T = 1.0 to T = 0.7 cuts the effective number of phrasings from 328 to 16. The top 10 phrasings go from 41% to 81% of all output.</figcaption>
</figure>

**Tuning does the same thing.** Preference tuning has a known optimum, \\(\pi^*(y) \propto \pi_{\text{ref}}(y)\exp\big(r(y)/\beta\big)\\). If raters reward typical text, so that the reward includes a term \\(\gamma \log \pi_{\text{ref}}(y)\\), this becomes

<div class="math">\[ \pi^*(y) \;\propto\; \pi_{\text{ref}}(y)^{\,1+\gamma/\beta}\;\exp\!\big(r_{\text{true}}(y)/\beta\big), \]</div>

which is a permanent temperature below 1, even when you sample at \\(T = 1\\).

**Human writing sets the floor.** If a share \\(\alpha\\) of each new training corpus is model-written and the rest comes from the human distribution \\(q\\), then \\(p_{t+1} = (1-\alpha)\,q + \alpha\,M(p_t)\\), and because entropy is concave, \\(H(p_{t+1}) \ge (1-\alpha)\,H(q)\\), however sharp the model is.

<figure>
  <img src="{{ '/assets/img/posts/oped/oped-feedback.png' | relative_url }}" alt="Effective number of ideas and tail mass over 60 generations for synthetic shares from 0% to 100%">
  <figcaption>Simulation where each generation's output becomes part of the next corpus. At a 50% synthetic share, diversity falls from 328 to 130 effective ideas. At 90%, it falls to about 4. A toy model: it shows the shape, not a forecast.</figcaption>
</figure>

</details>

## From gargoyles to grey pipes

We have watched this happen before, slowly, in buildings. Rainwater once left Gothic cathedrals through the mouths of carved gargoyles. On Indian temples, water runs off through stone spouts carved as the makara, a mythical sea creature. In Beijing's Forbidden City it pours through rows of carved dragon heads. In Japan it runs down rain chains, kusari-doi, from cup to cup instead of through a pipe. Every culture solved the same problem its own way, and the solution told you where you were.

<figure class="drain-grid">
  <div class="drain-cells">
    <div><img src="{{ '/assets/img/posts/oped/drain-gargoyle.jpg' | relative_url }}" alt="Stone gargoyle waterspout projecting from Notre-Dame de Paris"><span>Gargoyle, Notre-Dame de Paris</span></div>
    <div><img src="{{ '/assets/img/posts/oped/drain-makara.jpg' | relative_url }}" alt="Curved stone water spout carved as a makara at the Hazara Rama Temple, Hampi"><span>Makara spout, Hazara Rama Temple, Hampi, India</span></div>
    <div><img src="{{ '/assets/img/posts/oped/drain-dragon.jpg' | relative_url }}" alt="Row of carved marble dragon-head spouts on the terrace of the Hall of Supreme Harmony"><span>Dragon-head spouts, Forbidden City</span></div>
    <div><img src="{{ '/assets/img/posts/oped/drain-rainchain.jpg' | relative_url }}" alt="Chain of metal cups hanging from the roof eave of a temple building into an autumn garden at Hogon-in, Kyoto"><span>Rain chain, Hōgon-in, Kyoto</span></div>
    <div class="drain-today"><img src="{{ '/assets/img/posts/oped/drain-modern.jpg' | relative_url }}" alt="Plain dark downpipe running down a stone wall into a ground drain"><span>Today, almost everywhere</span></div>
  </div>
  <figcaption>Five ways to move rainwater, and the one that won.
    <small class="drain-credits">Photos: <a href="https://commons.wikimedia.org/wiki/File:Cath%C3%A9drale_Notre-Dame_(g%C3%A1rgolas).004_-_Paris.jpg">Fernando Losada Rodríguez</a> / CC BY-SA 4.0; <a href="https://commons.wikimedia.org/wiki/File:Water_outlet.jpg">Soham Banerjee</a> / CC BY 2.0; <a href="https://commons.wikimedia.org/wiki/File:Chishou_gargoyles_of_Hall_of_Supreme_Harmony.jpg">そらみみ</a> / CC BY-SA 4.0; <a href="https://commons.wikimedia.org/wiki/File:%E6%9C%B1%E3%81%AB%E6%9F%93%E3%81%BE%E3%81%A3%E3%81%9F%E5%AE%9D%E5%8E%B3%E9%99%A2%E3%81%AE%E5%BA%AD%E5%9C%92_Pcs34560_IMG2312.jpg">pcs34560</a> / public domain; <a href="https://commons.wikimedia.org/wiki/File:Downspout_and_drain_-_geograph.org.uk_-_6741959.jpg">Adrian Taylor</a> / CC BY-SA 2.0. All via Wikimedia Commons; makara and rain chain photos cropped.</small>
  </figcaption>
</figure>

Today it is a plain pipe, the same almost everywhere. Nobody banned the gargoyle. The variety was never the goal. It came from friction: local materials, local craft, people making things by hand. When a cheaper, good-enough standard removed the friction, the variety went with it.

Writing is losing its friction now. The struggle over a sentence was never just a cost. It was where the voice came from.

## Keep the gargoyles

This is not an argument against LLMs. I use them every day, and I build AI tutors for a living. English is not my first language, and they help me say what I mean with a fluency I did not always have, including in this article. The standard drainpipe has real virtues too. The failure was letting the default become the only option.

For those of us who build these tools, that is the job: build them to work with people, not instead of them. Start from the user's words, measure how alike outputs become, and reward the thinking over the polish.

Seven is not a bad answer. It is everyone's answer, made more so. A world of 7s is not wrong in any single case. It is just a world where nobody picks 4, and the scarecrow joke is the only joke. Progress has always come from the less likely choice: the improbable sentence, the minority view, the person who framed the problem differently. Used carelessly, these tools hand us more 7s. Used deliberately, they give everyone the fluency to say something only they would say.

So the next time a model hands you a 7, ask yourself what your 4 is.

---

### Sources

- Coronado-Blázquez, J. (2025). Deterministic or probabilistic? The psychology of LLMs as random number generators. <https://arxiv.org/abs/2502.19965>
- Jentzsch, S., and Kersting, K. (2023). ChatGPT is fun, but it is not funny! *WASSA 2023*. <https://arxiv.org/abs/2306.04563>
- Kubovy, M., and Psotka, J. (1976). The predominance of seven and the apparent spontaneity of numerical choices. *JEP: Human Perception and Performance*. <https://psycnet.apa.org/record/1977-00345-001>
- Leslie, I. (2025). Why are LLMs fixated on the number 7? <https://www.ian-leslie.com/p/why-are-llms-fixated-on-the-number>
- Van Koevering, K., and Kleinberg, J. (2024). How Random is Random? Evaluating the Randomness and Humaneness of LLMs' Coin Flips. <https://arxiv.org/abs/2406.00092>
- Agarwal, D., Naaman, M., and Vashistha, A. (2025). AI Suggestions Homogenize Writing Toward Western Styles and Diminish Cultural Nuances. *CHI 2025*. <https://arxiv.org/abs/2409.11360>
- Doshi, A. R., and Hauser, O. P. (2024). Generative AI enhances individual creativity but reduces the collective diversity of novel content. *Science Advances*. <https://doi.org/10.1126/sciadv.adn5290>
- How Diversely Can Language Models Solve Problems? Exploring the Algorithmic Diversity of Model-Generated Code. *Findings of EMNLP 2025*. <https://arxiv.org/abs/2503.00691>
- Marchezan, L., et al. (2026). Does AI-Assisted Development Homogenize Software? An Empirical Study of Code Similarity, Quality, and Evolution. <https://arxiv.org/abs/2610.24093>
- Gerstgrasser, M., et al. (2024). Is Model Collapse Inevitable? <https://arxiv.org/abs/2404.01413>
- Jakesch, M., et al. (2023). Co-Writing with Opinionated Language Models Affects Users' Views. *CHI 2023*. <https://arxiv.org/abs/2302.00560>
- Kirk, R., et al. (2024). Understanding the Effects of RLHF on LLM Generalisation and Diversity. *ICLR 2024*. <https://arxiv.org/abs/2310.06452>
- Kobak, D., et al. (2024). Delving into LLM-assisted writing in biomedical publications through excess vocabulary. <https://arxiv.org/abs/2406.07016>
- Liang, W., et al. (2024). Mapping the Increasing Use of LLMs in Scientific Papers. <https://arxiv.org/abs/2404.01268>
- Mata v. Avianca, Inc., No. 1:22-cv-01461 (S.D.N.Y. 2023). <https://en.wikipedia.org/wiki/Mata_v._Avianca,_Inc.>
- Moffatt v. Air Canada, 2024 BCCRT 149. <https://en.wikipedia.org/wiki/Moffatt_v._Air_Canada>
- Orlanski, G., et al. (2026). SlopCodeBench: Benchmarking How Coding Agents Degrade Over Long-Horizon Iterative Tasks. <https://arxiv.org/abs/2603.24755>
- Padmakumar, V., and He, H. (2024). Does Writing with Language Models Reduce Content Diversity? *ICLR 2024*. <https://arxiv.org/abs/2309.05196>
- Perry, N., Srivastava, M., Kumar, D., and Boneh, D. (2023). Do Users Write More Insecure Code with AI Assistants? <https://arxiv.org/abs/2211.03622>
- Shumailov, I., et al. (2024). AI models collapse when trained on recursively generated data. *Nature* 631. <https://doi.org/10.1038/s41586-024-07566-y>
- Zhang, J., et al. (2025). Verbalized Sampling: How to Mitigate Mode Collapse and Unlock LLM Diversity. <https://arxiv.org/abs/2510.01171>
