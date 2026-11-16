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

<p class="draft-anecdote">I spent my PhD studying how vision models break when real-world data drifts away from what they were trained on. The failures always lived in the tail, in the rare cases the training data barely covered. That is where the models went wrong, and it is also where the interesting problems were. Watching chatbots converge on 7 feels like the same experiment run in reverse. This time it is not the model losing the tail. It is us.</p>

The fixes are simple, so here they are first. The evidence and the mechanics follow for anyone who wants them.

## What to do

Every fix comes down to one idea: protect the tail.

**Write the first draft of anything that carries your judgment.** Routine notes are fine to delegate. But for the pitch, the hard feedback, the essay or the decision memo, start with your own rough version and let the model edit it. The order matters. Start from its draft and you edit toward its voice. Start from yours and it edits toward you.

**Know what you want before you ask.** A chatbot will happily hand you ten polished options. That feels like freedom, but it is a menu someone else wrote. Faced with too many choices we tire, and we settle for whichever sounds most reasonable, often something we never wanted in the first place. Decide what you are after, then use the model to get there. If you want alternatives, ask for very different ones, including ones the model thinks are bad, and judge them by your criteria, not its favourite. Ride the horse; don't let the horse ride you.

**Write some things with no help at all.** It keeps the skill alive, and every unassisted page adds to the human writing future models learn from.

**Build tools that keep people in the saddle.** If you make products on these models, measure how alike your users' outputs become against an unassisted baseline, and treat a rise as a failing test. Start from the user's words, not a generated draft.

<p class="draft-anecdote">When I build tutors, the easy thing to ship is a system that answers the student's question well. Instead, I have it answer with a question first: what the student already thinks, where they got stuck, what they would try next. The student's reasoning stays the draft, and the model only edits it.</p>

**Reward the thinking, not the polish.** Whether you are grading an essay or reading a job application, polish is no longer evidence of thought. Look at the outline, the draft and the explanation. And at the largest scale, labs should publish diversity evaluations next to capability benchmarks, because a world served by a handful of similar models loses its tail fastest.

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

## Pick 4

This is not an argument against LLMs. I use them every day, and I build AI tutors. The weakest writers gain the most from them, and that matters. Modernist architecture had real virtues too. The failure was letting the default become the only option, until every new downtown was the same glass towers.

Seven is not a bad answer. It is the most human answer, made more human than any human. A world of 7s is not wrong in any single case. It is just a world where nobody picks 4 and the scarecrow joke is the only joke. Progress lives in the tail: the improbable sentence, the minority view, the person who framed the problem differently. Used carelessly, these tools remove that tail first. Used deliberately, they give everyone the fluency to build something of their own. Pick 4 sometimes.

---

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
