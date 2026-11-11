---
layout: post
published: false
kind: Opinion
title: "Your LLM Is Not a Classifier"
date: 2026-11-11
excerpt: "We keep handing narrow, high-stakes decisions to the most general tool ever built. An LLM is a very sophisticated autocomplete, and that is exactly why it makes a poor classifier."
---

<!--
HEADLINE OPTIONS
A. Your LLM Is Not a Classifier  (current)
B. Stop Using LLMs as Classifiers
C. Why LLMs Make Poor Classifiers, and What to Use Instead
D. Not Every Decision Needs an LLM
E. Knows Everything, Has Practised Nothing
Crisp version (~2,000 words). The long version (~6,000 words) is kept in _notes/the-model-already-knows-long.md.
Re-check before publishing: model sizes (DeepSeek-V4), logprob availability, Jev claims (vendor-reported, Sep 2026).
Optional: a one-line personal anecdote in the closing paragraph.
-->

In May 2023, an instructor at Texas A&M University–Commerce pasted his students' final essays into ChatGPT and asked: *did you write this?* For a large share of the class, it said yes. Grades were withheld and some seniors' diplomas were put on hold while they proved they had written their own work. ChatGPT had no way of knowing. It produced the answer that sounded right, with the confidence that sounded right.

Two years later, ProPublica reported that a government efficiency team had used an AI model to label Veterans Affairs contracts "munchable" for cancellation. It read only the first 10,000 characters of each contract, flagged more than 500, and treated around 1,100 agreements as worth $34 million each when some were worth thousands. A former federal contracting official said judging those contracts was not something an off-the-shelf model could do "without a lot of really specialized training."

Both stories are the same mistake. We built the most general tool in the history of computing, and we keep using it for narrow, repetitive, high-stakes decisions, where generality is a cost and not a feature.

> **In short**
> - An LLM is a very sophisticated autocomplete. Its only output is the next token, so a label it gives you is generated text, and so is its confidence.
> - For fixed labels, high volume, rare positives and decisions that land on people, a small model trained and calibrated on your data is usually better, faster and cheaper.
> - Use the LLM where generality pays. Even then, a few hundred labelled examples will tell you how often it is really right.

## Sophisticated autocomplete, asked for a verdict

Building a classifier used to mean collecting labels and training a model. Today it often means a prompt and a schema:

```json
{ "label":      { "enum": ["billing", "technical", "other"] },
  "confidence": { "type": "number", "minimum": 0, "maximum": 1 } }
```

Back comes `{"label": "billing", "confidence": 0.95}`. It has a class and a number, so it looks like a classifier. Underneath is something else.

Every frontier LLM is a *decoder-only transformer*. Text is cut into tokens, each token becomes a vector, and the vectors pass through dozens of layers. At the end there is exactly one output: a probability for every token in a vocabulary of 100,000 to 200,000.

<div class="math">\[ p(t_{n+1} = v \mid t_{1..n}) \;=\; \operatorname{softmax}\big(W_U\, h_n\big)_v , \qquad v \in V . \]</div>

The model picks a token, appends it, and repeats. That is autocomplete. This year's models make it extraordinarily sophisticated. DeepSeek-V4 has 1.6 trillion parameters, of which 49 billion are active for any given token through a mixture of experts. Qwen3.5 swaps most attention layers for linear-time ones. Context windows reach a million tokens, inputs include images, and reasoning models think for thousands of tokens before they answer. Every one of these upgrades makes the model *more general*. None adds an output that means "probability of your class".

Structured outputs add one step. A grammar built from your schema masks every token outside your enum and renormalises the rest, \\(p_A(v) = p(v) / \sum_{a \in A} p(a)\\). Whatever the model wanted to say instead, whether "it depends" or a class you did not list, is quietly redistributed among your options. You get a well-formed answer, not a confident one.

<figure>
  <img src="{{ '/assets/img/posts/latent/latent-schematic.png' | relative_url }}" alt="Two pipelines: an LLM with a schema mask producing a JSON label, versus an encoder with a trained classification head and calibration producing class probabilities">
  <figcaption>The same pretrained network can sit in either pipeline. Only the second is built to output probabilities of <em>your</em> classes.</figcaption>
</figure>

## How a model knows, and how you do

The usual defence is that "the model already knows". It does, in a specific sense.

Training compresses trillions of tokens into weights. Every token and every intermediate state becomes a point in a space with thousands of dimensions, arranged so that related things sit close together: the vector for *king*, minus *man*, plus *woman*, lands near *queen*. The feed-forward layers behave like vast key-value memories that map patterns to associations. Answering a question means landing somewhere on this map and reading off what is nearby.

That works well when your input looks like the training data (*interpolation*). It fails quietly when it does not (*extrapolation*), because a softmax grows **more** confident the further an input sits from the data. Hein et al. proved that ReLU networks produce arbitrarily high confidence far enough from their training data.

<figure>
  <img src="{{ '/assets/img/posts/latent/latent-embedding.png' | relative_url }}" alt="Three clusters of training examples in an embedding space; a familiar query gets 89 percent, a query far from all data gets over 99.99 percent">
  <figcaption>Illustration with a small softmax classifier on synthetic data. A familiar ticket gets 89%. A ticket unlike anything seen gets over 99.99%.</figcaption>
</figure>

The map stores facts the way text states them. GPT-4 answers "Who is Tom Cruise's mother?" correctly 79% of the time, but "Who is Mary Lee Pfeiffer's son?" only 33% (Berglund et al.). People learn differently:

| | LLM | Person |
|---|---|---|
| Data to learn language | Trillions of tokens | Under ~100 million words by age 13 |
| A new category | Thousands of examples | Often one or two |
| Facing something new | Answers anyway | Notices, asks, defers |
| Knowing what it doesn't know | No reliable signal | Imperfect, but trainable |
| Becoming an expert | One model for every job | Practice on one job, with feedback |

People are overconfident too. But research on expertise is clear about when human intuition becomes trustworthy: in regular environments with fast, honest feedback (Kahneman and Klein). Weather forecasters, who find out every day whether their probabilities were right, are among the best-calibrated professionals ever studied. **Nobody becomes reliable at a narrow judgment by knowing a lot. They become reliable by practising it and being told when they were wrong.** Training and calibrating a specialist model is that practice. Prompting a generalist skips it.

## Four ways the generalist fails a narrow job

**1. Its confidence is more autocomplete.** `"confidence": 0.95` comes from the same next-token process as the rest of the JSON. Across several LLMs, Xiong et al. found stated confidences sit mostly between 80% and 100%, in multiples of 5. The old workaround was to read token probabilities directly, but that door is closing: OpenAI's GPT-5-family reasoning models dropped the `logprobs` option, and Anthropic's API has never returned token probabilities. Without a score, you cannot set a threshold, measure calibration or fix it.

**2. Its answers are not stable.** Sampling means the same input can get a different label on the next call. Even at temperature zero, served models vary with how requests are batched. And the prompt is part of the classifier: Zhao et al. moved GPT-3's accuracy from 54% to 93% just by reordering four examples.

**3. Its objective was never your task.** It was trained to predict internet text and to please raters. "billing" scores well because it is a plausible continuation, which correlates with, but is not, the probability that the ticket is about billing. Post-training makes this worse: in OpenAI's GPT-4 report, calibration error rose more than tenfold after RLHF.

**4. It does not know your base rate.** Suppose a detector is 90% sensitive and 90% specific, and 2% of essays really are AI-written. Then

<div class="math">\[ \text{precision} \;=\; \frac{0.9 \times 0.02}{0.9 \times 0.02 + 0.1 \times 0.98} \;\approx\; 16\% . \]</div>

<figure>
  <img src="{{ '/assets/img/posts/latent/latent-people.png' | relative_url }}" alt="100 student icons, 16 who used AI and 84 who did nothing wrong">
  <figcaption>Of every 100 students a "90% accurate" detector accuses, 84 are innocent.</figcaption>
</figure>

And the errors do not land evenly. Stanford researchers found that seven popular GPT detectors flagged 61% of essays by non-native English speakers as AI-written, while classifying US eighth-graders' essays almost perfectly (Liang et al.). Cheap AI makes this worse, not better: when a decision costs a fraction of a cent, teams point it at everything, which means more cases and rarer positives.

## When to use the generalist, and when not to

| Reach for an LLM when… | Train a specialist when… |
|---|---|
| Labels are open-ended or change weekly | The label set is fixed |
| You have no labels yet | You can get a few hundred |
| Volume is low | Volume is high |
| A person reviews every output | Outputs trigger actions automatically |
| You need extraction or explanation | You need a probability or a threshold |
| A mistake is cheap to undo | A mistake lands on a person |

Most production classification, such as spam, fraud, routing, moderation and grading, sits in the right column. The two also combine well. Let the LLM pre-label a few thousand examples, have people correct a sample, and train a small model on the result. Or let a calibrated specialist handle the confident majority and send only uncertain cases to an LLM or a person.

## The specialists are coming back

The industry is starting to agree. In September 2026 TypeSafe released **Jev**, the first of what it calls "System One models": typed outputs instead of generated text, one parallel pass instead of token-by-token sampling, a probability with every answer, and a training method named "Reinforcement Learning for Calibrated Decisions". It reports 70–500 ms per call. That is the right shape. It is also a vendor claim with no published calibration error yet, and its evaluations measure agreement with frontier LLMs rather than with ground truth, so it has to pass the same test as everything else. Alongside it, the older specialists still work: encoder classifiers such as ModernBERT, schema-driven encoders such as GLiNER2, few-shot heads such as SetFit, and TabPFN for tabular data.

## If you do use an LLM

Calibration is cheap. Temperature scaling fits one number on held-out labels. In Guo et al. it cut a ResNet's calibration error from 16.5% to 1.3%. In my simulation of an overconfident scorer, 200 labels took the error from 12.7% to about 1.8%.

<figure>
  <img src="{{ '/assets/img/posts/latent/latent-calibration.png' | relative_url }}" alt="Calibration error against number of labels, and a reliability diagram before and after temperature scaling">
  <figcaption>Simulation, not a real model: calibration error after fitting one temperature on n labels (median and 10th–90th percentile over 200 runs).</figcaption>
</figure>

If the API returns no probabilities, make a score first: ask \\(k\\) times and use the vote share, or put a small trained head on the model's embeddings. Then hold yourself to five rules:

1. **Get a score, not just a label.** Self-reported confidence does not count.
2. **Label a few hundred real examples** and report calibration alongside accuracy.
3. **Measure precision at your real base rate**, not on a balanced test set.
4. **Refit when anything changes**: the prompt, the model version or the traffic.
5. **Decide what "I don't know" means**, and route those cases to a person.

LLMs are the most remarkable general-purpose tool we have, which is exactly why they end up doing jobs a specialist would do better. Nobody hires a brilliant generalist to check ten thousand forms a day against the same three rules. They train someone for that job, and they check how often that person is wrong. Our models deserve the same treatment, and so do the people on the receiving end of their labels.

---

### Sources

- Berglund, L., et al. (2024). The Reversal Curse: LLMs trained on "A is B" fail to learn "B is A". *ICLR 2024*. https://arxiv.org/abs/2309.12288
- DeepSeek-AI (2026). DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence. https://arxiv.org/abs/2606.19348
- Frank, M. C. (2023). Bridging the data gap between children and large language models. *Trends in Cognitive Sciences*, 27(11).
- Geva, M., Schuster, R., Berant, J., & Levy, O. (2021). Transformer Feed-Forward Layers Are Key-Value Memories. *EMNLP 2021*. https://arxiv.org/abs/2012.14913
- Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On Calibration of Modern Neural Networks. *ICML 2017*. https://arxiv.org/abs/1706.04599
- He, H., & Thinking Machines Lab (2025). Defeating Nondeterminism in LLM Inference. https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/
- Hein, M., Andriushchenko, M., & Bitterwolf, J. (2019). Why ReLU networks yield high-confidence predictions far away from the training data. *CVPR 2019*. https://arxiv.org/abs/1812.05720
- Kahneman, D., & Klein, G. (2009). Conditions for intuitive expertise: A failure to disagree. *American Psychologist*, 64(6), 515–526.
- Labonne, M. (2026). Qwen3.5: Nobody Agrees on Attention Anymore. https://huggingface.co/blog/mlabonne/qwen35
- Lake, B. M., Salakhutdinov, R., & Tenenbaum, J. B. (2015). Human-level concept learning through probabilistic program induction. *Science*, 350(6266), 1332–1338.
- Liang, W., Yuksekgonul, M., Mao, Y., Wu, E., & Zou, J. (2023). GPT detectors are biased against non-native English writers. *Patterns*, 4(7). https://arxiv.org/abs/2304.02819
- Mikolov, T., Yih, W., & Zweig, G. (2013). Linguistic Regularities in Continuous Space Word Representations. *NAACL 2013*.
- Murphy, A. H., & Winkler, R. L. (1984). Probability Forecasting in Meteorology. *Journal of the American Statistical Association*, 79(387), 489–500.
- OpenAI (2023). GPT-4 Technical Report. https://arxiv.org/abs/2303.08774
- Roberts, B., & Coleman, V. (2025, June 6). Inside the AI Prompts DOGE Used to "Munch" Contracts Related to Veterans' Health. *ProPublica*. https://www.propublica.org/article/inside-ai-tool-doge-veterans-affairs-contracts-sahil-lavingia
- TypeSafe (2026). Introducing System One Models and Jev. https://typesafe.ai/blog/introducing-system-one-models-and-jev
- *The Washington Post* (2023, May 18). A professor falsely accused his class of using ChatGPT. Their diplomas are in jeopardy. (Syndicated: https://www.adn.com/nation-world/2023/05/18/a-professor-falsely-accused-his-class-of-using-chatgpt-their-diplomas-are-in-jeopardy/)
- Xiong, M., et al. (2024). Can LLMs Express Their Uncertainty? *ICLR 2024*. https://arxiv.org/abs/2306.13063
- Zhao, Z., Wallace, E., Feng, S., Klein, D., & Singh, S. (2021). Calibrate Before Use: Improving Few-Shot Performance of Language Models. *ICML 2021*. https://arxiv.org/abs/2102.09690
