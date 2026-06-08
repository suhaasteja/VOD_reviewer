## Clash Royale VOD Reviewer 👑

> 🚀 **Try it live:** [huggingface.co/spaces/suhaas-teja/clash-royale-vod-reviewer](https://huggingface.co/spaces/suhaas-teja/clash-royale-vod-reviewer)
>
> No setup required — upload a clip and get coaching in your browser. This repo holds the step-by-step Colab notebook the Space was built from, plus a long-form [writeup](WRITEUP.md).

🎥 **Demo video:** [demo.mp4](demo.mp4) — walkthrough of the Hugging Face Space (sample clip + card tracking flow, live Mk1 streaming).

---

https://github.com/user-attachments/assets/f27e284e-c578-4fc2-88be-6712145890bd

---

Clash Royale is a fast-paced competitive mobile game where players deploy troops
to destroy the opponent's towers — whoever captures the most towers before the
clock runs out wins.

**What's a VOD?**
VOD stands for *Video on Demand* — in gaming, it refers to a recorded replay of
a match. Reviewing your own VODs is one of the most effective ways to improve:
you see your decisions from the outside, spot patterns you missed in the moment,
and identify exactly where a game was won or lost. Pro players and coaches do
this constantly. The problem is it's time-consuming and requires a trained eye.

**Where Perceptron comes in**
This notebook uses Perceptron Mk1 — a vision model that understands video — to
automate that review process. Instead of scrubbing through footage manually, you
ask a question in plain English and get a grounded, timestamped answer backed by
what the model actually saw on screen. No transcripts, no audio analysis, no
game-specific training data — pure visual reasoning on the gameplay footage itself.

The final 30 seconds are where matches are decided. That's the window we focus on.

**What it does:**
- **VOD analysis** — reviews the last 30s of a match and diagnoses the single
  defining play: the outplay that secured the win, or the mistake that cost the loss
- **Card tracking** — upload a reference image of any troop card and the model
  will track how many times it was deployed and the damage it dealt (powered by
  in-context learning — no retraining required)
