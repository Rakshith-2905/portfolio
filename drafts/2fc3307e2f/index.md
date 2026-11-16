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

It is not your chatbot. In a test that asked each model a hundred times, GPT said 7 on 92 occasions, Claude on 90 and Gemini every single time. A controlled study across six models and 75,600 queries found 7 was "the preferred value by far for every single model." Chance would give you 7 one time in ten.

Here is the twist: **people pick 7 too.** In a classic 1976 study, 28% of people asked for a random digit chose 7. The chatbot did not invent our bias. It learned it from our writing and then amplified it. Raise the human preference to roughly the third power and you get the chatbot numbers almost exactly. **Chatbots pick the way people do, cubed.**

<figure>
  <img src="{{ '/assets/img/posts/oped/oped-seven.png' | relative_url }}" alt="Left: share of answers that are 7 as human preference is amplified, with people at 28% and chatbots at 80 to 92%. Right: the five most repeated jokes out of 1,008 requests.">
  <figcaption>People sit at 28%; chatbots correspond to amplifying that preference by a power of about 3 to 4. Right: asked for a joke 1,008 times, ChatGPT returned the same scarecrow joke 140 times.</figcaption>
</figure>

That is harmless for a number. It is not harmless when the request is a cover letter, a product spec or an argument about social media, and the same pull applies.

The fixes are simple, so here they are first. The evidence and the mechanics follow for anyone who wants them.

## What to do: pick the destination yourself

Think of a model like GPS. It is brilliant at getting you somewhere, and it sends everyone down the same route. Choose where you are going yourself, and let it handle the turns.

- **Think before you prompt.** Write your rough take first, even three bullet points. The model should edit your thinking, not replace it.
- **Hand off the chores, not the judgment.** Formatting, summaries, boilerplate: delegate freely. The idea, the argument, the decision: keep.
- **Decide what good looks like before you see options.** Otherwise twenty polished choices pick for you, and you end up with something you never wanted.
- **Make it argue with you.** Ask what is wrong with your view, not to write your view for you.
- **If it doesn't sound like you, it isn't done.** Read it aloud before you send it.

And once in a while, write something with no help at all.

**If you build these tools, build them to work with people, not instead of them.**

> When I build tutors, the easy thing to ship is a system that answers the student's question well. Instead, I have it answer with a question first: what the student already thinks, where they got stuck, what they would try next. The student's reasoning stays the draft, and the model only edits it.

Start from the user's words, measure how alike your outputs become, and reward the thinking over the polish.

## The evidence

<figure>
  <img src="{{ '/assets/img/posts/oped/oped-evidence.png' | relative_url }}" alt="Bar charts: measured convergence in four controlled studies, and the estimated share of LLM-modified abstracts in four corpora">
  <figcaption>Left: convergence in controlled writing studies (metrics differ, so compare direction, not length). Right: estimated share of LLM-modified abstracts.</figcaption>
</figure>

- **Better individually, narrower together.** In Doshi and Hauser's study of 300 writers, AI ideas made stories about 8% more novel, but about 11% more similar to each other.
- **Ideas, not just words.** Writing with an instruction-tuned model cut the share of unique key points in essays by about 7% (Padmakumar and He). The raw base model had no significant effect.
- **A direction.** With a GPT-4o autocomplete, Indian writers' essays drifted toward Western styles (Agarwal et al.).
- **Opinions too.** People writing with a quietly biased assistant were about twice as likely to argue its side, and their own views shifted (Jakesch et al., 1,506 people).
- **Already widespread.** Up to 17.5% of sentences in computer-science abstracts were substantially LLM-modified by early 2024 (Liang et al.). In PubMed, "delves" became 28 times more common than its trend predicts (Kobak et al.).

The effects are small to medium and mostly from short lab studies. The worry is how they compound across billions of uses.

## Why it happens

**Sharpening.** Low-temperature decoding raises every probability to a power, which piles weight onto the most common phrasing. That is the "cubing" behind the 7.

**Tuning rewards the familiar.** Raters prefer text that feels typical, and tuning on their preferences acts like turning the temperature down permanently. Kirk et al. found this kind of tuning substantially reduces output diversity, which is why the tuned model narrowed essays and the base model did not.

**The loop closes.** Models trained on model-written text lose the rare cases first (Shumailov et al., *Nature*). Fresh human writing is what puts them back. Collapse is avoided when human data accumulates alongside synthetic data rather than being replaced by it (Gerstgrasser et al.).

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

We have watched this happen before, slowly, in buildings. Rainwater once left Gothic cathedrals through the mouths of carved gargoyles. In Japan it ran down rain chains of ringing cups. In Beijing's Forbidden City it poured through rows of carved dragon heads. Every culture solved the same problem its own way, and the solution told you where you were.

<figure class="drain-grid">
  <div class="drain-cells">
    <div><img src="{{ '/assets/img/posts/oped/drain-gargoyle.jpg' | relative_url }}" alt="Stone gargoyle waterspout projecting from Notre-Dame de Paris"><span>Gargoyle, Notre-Dame de Paris</span></div>
    <div><img src="{{ '/assets/img/posts/oped/drain-rainchain.jpg' | relative_url }}" alt="Metal rain chain of linked cups hanging from a temple roof in Yanaka, Tokyo"><span>Rain chain, Japan</span></div>
    <div><img src="{{ '/assets/img/posts/oped/drain-dragon.jpg' | relative_url }}" alt="Row of carved marble dragon-head spouts on the terrace of the Hall of Supreme Harmony"><span>Dragon-head spouts, Forbidden City</span></div>
    <div><img src="{{ '/assets/img/posts/oped/drain-modern.jpg' | relative_url }}" alt="Plain dark downpipe running down a stone wall into a ground drain"><span>Today, almost everywhere</span></div>
  </div>
  <figcaption>Four ways to move rainwater.
    <small class="drain-credits">Photos: <a href="https://commons.wikimedia.org/wiki/File:Cath%C3%A9drale_Notre-Dame_(g%C3%A1rgolas).004_-_Paris.jpg">Fernando Losada Rodríguez</a> / CC BY-SA 4.0; <a href="https://commons.wikimedia.org/wiki/File:At_a_Yanaka_Temple,_Tokyo_JP.jpg">Stefano Vigorelli</a> / CC BY-SA 4.0; <a href="https://commons.wikimedia.org/wiki/File:Chishou_gargoyles_of_Hall_of_Supreme_Harmony.jpg">そらみみ</a> / CC BY-SA 4.0; <a href="https://commons.wikimedia.org/wiki/File:Downspout_and_drain_-_geograph.org.uk_-_6741959.jpg">Adrian Taylor</a> / CC BY-SA 2.0. All via Wikimedia Commons.</small>
  </figcaption>
</figure>

Today it is a plain pipe, the same almost everywhere. Nobody banned the gargoyle. The variety was never the goal. It came from friction: local materials, local craft, people making things by hand. When a cheaper, good-enough standard removed the friction, the variety went with it.

Writing is losing its friction now. The struggle over a sentence was never just a cost. It was where the voice came from.

## Pick 4

This is not an argument against LLMs. I use them every day, and I build AI tutors for a living. The weakest writers gain the most from them, and that matters. The standard drainpipe has real virtues too. The failure was letting the default become the only option.

Seven is not a bad answer. It is the most human answer, made more human than any human. A world of 7s is not wrong in any single case. It is just a world where nobody picks 4 and the scarecrow joke is the only joke. Progress lives in the tail: the improbable sentence, the minority view, the person who framed the problem differently. Used carelessly, these tools remove that tail first. Used deliberately, they give everyone the fluency to build something of their own. Pick 4 sometimes.

---

*A note on how this was written: I wrote the first draft, and the idea, the argument and the final calls are mine. I then used an AI assistant to tighten the prose, research and check sources, and pushed back on it until the piece said what I meant. That is the point. These tools are remarkable when you do the thinking.*

*Rakshith Subramanyam is a technical founder and AI researcher who builds AI tutoring products.*

### Sources

- Coronado-Blázquez, J. (2025). Deterministic or probabilistic? The psychology of LLMs as random number generators. <https://arxiv.org/abs/2502.19965>
- Jentzsch, S., and Kersting, K. (2023). ChatGPT is fun, but it is not funny! *WASSA 2023*. <https://arxiv.org/abs/2306.04563>
- Kubovy, M., and Psotka, J. (1976). The predominance of seven and the apparent spontaneity of numerical choices. *JEP: Human Perception and Performance*. <https://psycnet.apa.org/record/1977-00345-001>
- Leslie, I. (2025). Why are LLMs fixated on the number 7? <https://www.ian-leslie.com/p/why-are-llms-fixated-on-the-number>
- Van Koevering, K., and Kleinberg, J. (2024). How Random is Random? Evaluating the Randomness and Humaneness of LLMs' Coin Flips. <https://arxiv.org/abs/2406.00092>
- Agarwal, D., Naaman, M., and Vashistha, A. (2025). AI Suggestions Homogenize Writing Toward Western Styles and Diminish Cultural Nuances. *CHI 2025*. <https://arxiv.org/abs/2409.11360>
- Doshi, A. R., and Hauser, O. P. (2024). Generative AI enhances individual creativity but reduces the collective diversity of novel content. *Science Advances*. <https://doi.org/10.1126/sciadv.adn5290>
- Gerstgrasser, M., et al. (2024). Is Model Collapse Inevitable? <https://arxiv.org/abs/2404.01413>
- Jakesch, M., et al. (2023). Co-Writing with Opinionated Language Models Affects Users' Views. *CHI 2023*. <https://arxiv.org/abs/2302.00560>
- Kirk, R., et al. (2024). Understanding the Effects of RLHF on LLM Generalisation and Diversity. *ICLR 2024*. <https://arxiv.org/abs/2310.06452>
- Kobak, D., et al. (2024). Delving into LLM-assisted writing in biomedical publications through excess vocabulary. <https://arxiv.org/abs/2406.07016>
- Liang, W., et al. (2024). Mapping the Increasing Use of LLMs in Scientific Papers. <https://arxiv.org/abs/2404.01268>
- Padmakumar, V., and He, H. (2024). Does Writing with Language Models Reduce Content Diversity? *ICLR 2024*. <https://arxiv.org/abs/2309.05196>
- Shumailov, I., et al. (2024). AI models collapse when trained on recursively generated data. *Nature* 631. <https://doi.org/10.1038/s41586-024-07566-y>
- Zhang, J., et al. (2025). Verbalized Sampling: How to Mitigate Mode Collapse and Unlock LLM Diversity. <https://arxiv.org/abs/2510.01171>
