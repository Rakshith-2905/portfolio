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

It is not a coincidence, and it is not your chatbot. In a test that asked each model a hundred times, GPT answered 7 on 92 occasions and Claude on 90. Gemini answered 7 every single time. A controlled study of six models across 75,600 queries found that 7 is "the preferred value by far for every single model." A truly random pick would land on 7 one time in ten.

Most people laugh this off: computers are bad at randomness. That explanation is wrong, and the right one is the most useful thing I know about where AI-assisted writing is heading.

## People pick 7 too

In a classic 1976 experiment, Kubovy and Psotka asked 558 people for a random digit, and 28% chose 7, almost three times what chance predicts. Seven *feels* random. It is odd, prime, and sits neither at the edge nor in the middle.

So the chatbot did not invent a bias. It learned ours from the text we wrote, and then amplified it. If you take the human preference and raise it to roughly the third power, you get the chatbot numbers almost exactly. **Chatbots pick numbers the way people do, cubed.**

<figure>
  <img src="{{ '/assets/img/posts/oped/oped-seven.png' | relative_url }}" alt="Left: share of answers that are 7 as human preference is amplified, with people at 28% and chatbots at 80 to 92%. Right: the five most repeated jokes out of 1,008 requests.">
  <figcaption>Left: people sit at 28%; chatbot measurements correspond to amplifying that preference by a power of about 3 to 4. Right: asked for a joke 1,008 times, ChatGPT returned the same scarecrow joke 140 times.</figcaption>
</figure>

Cubing sounds harmless until you count what it does to choice. People picking a digit behave as if choosing among about nine real options. A chatbot at 92% behaves as if choosing among fewer than two. The pattern repeats wherever researchers look. Asked for a joke 1,008 times, ChatGPT returned the same 25 jokes over 90% of the time. Asked to flip coins, GPT and Llama models started more than 88% of sequences with heads, a stronger version of a human habit. The authors of that study concluded that the models "not only replicated human biases, but exacerbated them."

That sentence is the whole essay. Now replace "a number between 1 and 10" with "a cover letter," "a performance review" or "an argument about social media."

<p class="draft-anecdote">I noticed it first at work. At Axio I spend a lot of time with faculty, and a version of the same remark kept coming up: student writing had started to sound alike. Not wrong, not copied, just the same polished structure and the same safe conclusion, submission after submission. It took me back to my PhD, which I spent studying how vision models break when real-world data drifts away from what they were trained on. The failures always lived in the tail, in the rare cases the training data barely covered. Reading that writing, it felt like the same experiment run in reverse. This time it was not the model losing the tail. It was us.</p>

## From numbers to paragraphs

A random number is a toy. The question is whether the same pull shows up in stories, essays and opinions. The controlled evidence says it does.

<figure>
  <img src="{{ '/assets/img/posts/oped/oped-evidence.png' | relative_url }}" alt="Bar charts: measured convergence in four controlled studies, and the estimated share of LLM-modified abstracts in four corpora">
  <figcaption>Left: convergence in controlled writing studies (metrics differ, so compare direction, not length). Right: estimated share of LLM-modified abstracts. Sources at the end.</figcaption>
</figure>

**Individuals improve while the collection narrows.** In Doshi and Hauser's study of 300 writers, those who saw AI-generated ideas wrote stories rated about 8% more novel, and the weakest writers gained most. Yet their stories were about 11% more similar to one another. Everyone moved up, and the cloud of stories shrank.

**The narrowing is in ideas, not just words.** Padmakumar and He had professional writers produce argumentative essays alone or with a model. With an instruction-tuned model, the share of unique key points dropped by about 7%. With the raw base model, there was no significant effect. Hold on to that contrast.

**The narrowing has a direction.** When Agarwal, Naaman and Vashistha gave Indian and American writers a GPT-4o autocomplete, their essays became measurably more alike, and the authors found Indian participants drifting toward Western styles. Both groups also wrote about a third faster. Speed and sameness arrived together.

**Opinions move too.** In Jakesch et al.'s study of 1,506 people, those writing with an assistant quietly biased toward one side were about twice as likely to argue that side, and their own stated views shifted afterwards.

**And the exposure is already large.** Liang et al. estimated that by early 2024 up to 17.5% of sentences in computer-science abstracts were substantially LLM-modified. Kobak et al. put a lower bound of 13.5% on 2024 PubMed abstracts, partly by noticing that "delves" had become 28 times more common than its trend predicts.

To be fair, these effects are small to medium, and most studies are short lab sessions. The real question is what happens when a small effect compounds across billions of uses and several model generations.

## Why the machine pulls toward the middle

Three mechanisms explain it, and each suggests a fix.

**Sharpening.** A model learns a distribution over what could come next, but we rarely read that distribution directly. Low-temperature decoding raises every probability to a power, which piles weight onto the most common phrasing. That is the "cubing" in the 7 example.

**Alignment rewards the familiar.** Assistants are tuned on human ratings, and raters prefer text that feels typical. Researchers have found this "typicality bias" in preference data, and Kirk et al. found that this kind of tuning substantially reduces output diversity. The effect is mathematically the same as turning the temperature down permanently. It is why the instruction-tuned model homogenized essays and the base model did not.

**The loop closes.** As more of the web is model-written, future models train on it. Shumailov et al. showed in *Nature* that models trained on their own output lose the rare cases first. Fresh human writing is the only thing that reliably puts them back: in simulations, diversity degrades gently until roughly half of new text is synthetic, then falls off a cliff. Gerstgrasser et al. reach the same conclusion for real models: collapse is avoided when human data accumulates alongside synthetic data rather than being replaced by it.

<figure>
  <img src="{{ '/assets/img/posts/oped/oped-feedback.png' | relative_url }}" alt="Effective number of ideas and tail mass over 60 generations for synthetic shares from 0% to 100%">
  <figcaption>Simulation of a corpus where each generation's output becomes part of the next generation's training data. Diversity holds up reasonably at a 50% synthetic share and collapses past about 75%. A toy model: it shows the shape of the dynamics, not a forecast.</figcaption>
</figure>

Put together, the trajectory is not a vibe; it is arithmetic. Each model is sharpened. Wide adoption multiplies that across a population. A handful of vendors removes the variety that many different models would add back. Recursive training compounds the loss. Emails converge first because they are the most delegated. Arguments follow, because we accept the model's framing along with its sentences. Ideas come last, because the space of things that feel sayable shrinks toward what the model finds probable.

## This is not an argument against LLMs

I use these tools every day, and the company I help lead builds AI tutors. The least creative writers gained the most in Doshi and Hauser's study, and fluency and access are real goods. Modernist architecture had real virtues too: cheap, fast, hygienic housing at scale. The failure was letting the default become the only option, until every new downtown became the same glass towers. The goal is not to stop using the tools. It is to stop letting them decide for us.

## What to do, depending on who you are

**Everyone: draft your own emails.** An email is the smallest unit of your voice, and it is the first thing most of us hand over. Write the first draft yourself, even if it is rough, then let the model fix grammar or tone. The order matters. Start from the model's draft and you edit toward its voice. Start from yours and it edits toward you. Readers can feel the difference, and more and more they can tell when nobody was really there. Two lines that sound like you beat three polished paragraphs that sound like everyone.

- *Think first, prompt second.* Form your view in your own words before opening a chatbot. Let the model stress-test the idea, not originate it.
- *Ask for the spread, not the answer.* Request five very different options, including ones the model thinks are bad. Zhang et al. report that asking a model to list several options with rough probabilities recovers much of the diversity that tuning removes.
- *Write some things with no help at all.* Every unassisted page adds to the pool of human writing that future models depend on.

**Engineers: don't let autocomplete choose your design.** Code assistants pull toward the most common pattern, library and structure in their training data. For boilerplate that is fine; boring code is good code. But the same suggestion repeated across millions of codebases means shared defaults and shared mistakes. Sketch the design yourself before asking for code. Ask for two or three alternatives with their trade-offs. Read what you accept as if a stranger wrote it. And keep the interesting parts of the system yours, because that is where your judgment is the product.

**Product builders: measure sameness like a regression.**

- *Ship a homogenization metric.* Track how similar outputs are across users against an unassisted baseline, and treat a rise as a failing test.
- *Default to the user's draft.* Interfaces that open with a generated draft maximize deference. Interfaces that start from the user's words minimize it.
- *Expose the dial.* Let people choose between "polished" and "divergent," and show them what it changes.

**Educators and students: grade the thinking, not the polish.** The best tutoring interaction is often a question back to the student, not a finished answer.

<p class="draft-anecdote">When we built the tutor at Axio, the easy thing to ship was a system that answers the student's question well. We chose to have it answer with a question first: what the student already thinks, where they got stuck, what they would try next. Because the tutor works from a knowledge graph of the course, it can aim that question at the specific concept the student is missing instead of handing over a model-written explanation. The student's reasoning stays the draft, and the model only edits it.</p>

- *Teachers* can make thinking visible again by assessing process: outlines, drafts, oral explanations and in-class writing.
- *Students* should use the model as a sparring partner after forming a view, not before. Ask it to argue the other side, then decide who is right.

**Institutions: protect human writing and model variety.**

- *Employers* should stop paying for polish as a proxy for thought.
- *Publishers and platforms* should keep provenance and protect clearly human spaces, for readers and for every future model's training data.
- *AI labs* should publish diversity evaluations next to capability benchmarks, and *policymakers* should see a concentrated model market as a diversity risk, not only a competition risk.

## Pick 4

Seven is not a bad answer. It is the most human answer, made more human than any human. That is precisely the danger. A world of 7s is not wrong in any single case. It is just a world where nobody picks 4, nobody picks 10, and the scarecrow joke is the only joke. Progress has always lived in the tail: the improbable sentence, the minority view, the person who framed the problem differently. That tail is exactly what these systems remove first, and only fresh human writing puts it back.

LLMs are the most powerful writing tools we have built. Used carelessly, they give us a world of perfectly reasonable 7s. Used deliberately, they give everyone the fluency to build something of their own. Let's choose on purpose.

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
