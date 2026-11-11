---
layout: post
published: false
kind: Opinion
title: "Reliability is the whole game"
date: 2026-07-10
excerpt: "LLMs are probabilistic; reliability is deterministic. How do you reconcile the two — without making the model sound dumb under a pile of guardrails?"
---

> Draft for review. Hidden from the site until approved.

LLMs are **probabilistic** by nature. Reliability, the thing real products actually need, is a **deterministic** requirement. A tutor that is right 97% of the time is still wrong for three students in every hundred, and those students don't experience a percentage. They experience a wrong answer delivered with confidence.

The whole game is living in that tension honestly.

## The tempting fix makes it worse

The first instinct is to wrap the model in rules: block this, refuse that, append a disclaimer, force a template. Each rule fixes a failure you've seen. Together they produce a model that hedges everything, refuses reasonable requests and sounds noticeably dumber than the one underneath. You've traded visible errors for invisible ones: users stop asking the hard questions.

## What actually works

**Check, don't constrain.** Instead of narrowing what the model may say, have something independent check what it did say. In the tutor we built, several models check each other in real time. Disagreement between them is a far better signal of "this might be wrong" than any single model's confidence. It's the same idea as my DECIDER paper: an independent view of the task, with disagreement treated as a warning.

**Know when you don't know.** Calibration is underrated. A system that can say "I'm not sure, let's check" at the right moments earns more trust than one that is slightly more accurate but always certain. Uncertainty estimation belongs in the product loop, not just in the eval report.

**Put determinism where it belongs.** Anything that must be exactly right, a grade, a citation, a number from a document, should come from a deterministic step the model calls, not from the model's free text. Let the model do what it's good at (understanding, explaining, planning) and hand the parts that need to be exact to tools.

**Measure drift, not just accuracy.** Models behave differently on turn ten than on turn one, and differently under pressure. My political-bias work measures how many nudges it takes to move a model. Products should ask the same question about their own failure modes.

## The standard

Reliability isn't a guardrail layer you add at the end. It's an architecture decision: what checks what, where uncertainty is surfaced, and which parts are allowed to be probabilistic at all. Get that right and you don't have to make the model sound dumb to make it safe.
