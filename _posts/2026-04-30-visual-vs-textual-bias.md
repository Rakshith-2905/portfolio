---
layout: post
published: false
kind: Opinion
title: "Do LLMs trust their eyes or their words?"
date: 2026-04-30
excerpt: "When visual and textual cues conflict, which does a multimodal model believe? An opinion on visual vs. textual bias."
---

> Draft for review. Hidden from the site until approved. The evaluation harness (SB-Bench, multi-provider VLM wrappers) exists; results are not in yet.

When the image says one thing and the text says another, which does a multimodal model believe?

It matters more than it sounds. A vision-language model reading a chart with a misleading caption, a photo of a person paired with a stereotyped question, or a screenshot with instructions embedded in it is making a choice about which modality to trust, and it rarely tells you which one it picked.

## Where the bias comes from

Most VLMs are a strong language model with vision bolted on. The language side has seen vastly more data and carries strong priors. When the visual evidence is ambiguous, or even when it isn't, the model can fall back on what the text implies. That is how a model ends up answering a question about a person from the stereotype the question invites rather than from what is actually in the image.

## How I'm testing it

I'm building an evaluation harness on **SB-Bench**, a benchmark of 14,578 real (non-synthetic) image–question pairs across nine stereotype categories, from age and gender to disability and socioeconomic status. Each question has three answer options, so you can see whether a model answers from the image or from the prior. The harness runs the same items through models from OpenAI, Anthropic, Google, xAI, and open models via Ollama and Hugging Face, and uses an LLM to extract the chosen answer reliably from free-form responses.

## Why it matters

If a model leans on its words over its eyes, adding an image doesn't make it more grounded; it just makes it look more grounded. The fix starts with measuring the lean, per model and per category, before trusting a VLM with anything that involves people.
