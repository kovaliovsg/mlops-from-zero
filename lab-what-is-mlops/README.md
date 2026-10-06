# Lab · Spot the drift

**Last verified:** 2026-10-05 · Python 3.12 · numpy 2.5.3 · scikit-learn 1.9.1 · Windows 11, macOS, Ubuntu

**For the video:** *What is MLOps?* — Part 1 ends with this homework.

**Goal:** you can name the two kinds of drift in a model you use every day, and you have watched a model drift
in front of you — once because its inputs moved, once because the world changed while the inputs looked normal.

## Prerequisites

| You need | Why | Get it |
|---|---|---|
| Nothing for Part A | it is a pen-and-paper exercise | — |
| For Part B: VS Code with the Python extension, Python 3.12, Git | the lab runs on your machine, in VS Code | [Set up your machine](../SETUP.md) |

**Cost:** free. Nothing runs in Azure.

## Part A · Name the drift (5 minutes)

Pick one model you use every day: your email spam filter, a streaming service's "recommended for you", your
bank's fraud check, a map's arrival time. Fill in this table — on paper is fine.

| | Your model |
|---|---|
| What it predicts | |
| Two of its inputs | |
| **Data drift** — how could its *inputs* change? | |
| **Concept drift** — how could the *meaning* of those inputs change, while they look the same? | |

Two worked answers, so you can check your thinking:

| | Spam filter | Restaurant soup forecast (Part B) |
|---|---|---|
| Predicts | spam or not | portions of cold soup sold today |
| Inputs | words in the email, the sender | the temperature outside |
| Data drift | spammers switch to images and new words the model never saw | a heatwave: temperatures far above anything in training |
| Concept drift | a word that meant "spam" last year is now in normal newsletters | a competitor opens next door: same weather, fewer customers |

## Part B · Watch it happen (10 minutes, optional)

1. In VS Code, open the `lab-what-is-mlops` folder and create its environment — **Python: Create Environment** →
   **Venv** → **Python 3.12**, with `requirements.txt` ticked (the five steps in
   [Run a lab in VS Code](../SETUP.md#run-a-lab-in-vs-code)).
2. In the VS Code terminal (its prompt starts with `(.venv)`), run:

```
python drift_demo.py
```

Expected output:

```
Trained on 200 spring days (10-28 C), average 19.1 C.
Check 1, more spring days:   average 19.7 C  -> average error   3.5 portions
Check 2, a heatwave:         average 35.7 C  -> average error  56.7 portions  <- data drift: the inputs moved
Check 3, competitor opens:   average 18.4 C  -> average error  28.7 portions  <- concept drift: inputs look normal

Notice: check 3's temperatures look exactly like spring. Watching the inputs alone would miss it;
only comparing the forecast with the real sales shows the model went off.
CHECKPOINT OK
```

What just happened, in restaurant words: the model learned "hotter means more soup" from spring. In a heatwave
people stay indoors, so the model — which never saw 36 degrees — orders far too much soup (**data drift**). When
a competitor opens, the weather is ordinary, so nothing looks wrong on the input dashboard, yet the forecast is
off by almost thirty portions a day (**concept drift**).

## Checkpoint

`CHECKPOINT OK` printed, and check 2 and check 3 both show an error far larger than check 1.

## Practice questions

1. A model's inputs have the same distribution as in training, but its accuracy is falling. Which kind of drift
   is most likely, and what do you need in order to see it?
2. Why can't a healthy service dashboard (latency, errors, CPU) tell you that a model has drifted?
3. In Part B, which single number would an input-drift monitor have flagged in check 2 but not in check 3?

<details><summary>Answers</summary>

1. Concept drift — the relationship between inputs and the right answer changed. You need the real outcomes
   (labels) to compare with the predictions; input monitoring alone cannot see it.
2. Because a drifting model still answers quickly and without errors; it is the answers that are wrong. Drift
   shows in the data and in prediction quality, not in service health.
3. The average temperature: 35.7 °C against 19.1 °C in training. In check 3 it was 18.4 °C — normal.
</details>

## If it breaks

- **`python` opens the Microsoft Store (Windows):** the Store alias is in the way. Run `python3`, or turn the alias
  off in *Settings → Apps → Advanced app settings → App execution aliases*.
- **`pip` cannot find a pinned version:** the libraries moved on. Run `pip install numpy scikit-learn` without
  pins; the numbers may differ slightly but the story is the same. Then open an issue so this lab gets updated.
- **Your numbers differ a little from the expected output:** fine, as long as check 2 and check 3 are far above
  check 1 and `CHECKPOINT OK` prints.

## Hand in

Commit your Part A table as `lab-what-is-mlops/my-drift.md` to your fork of this repository.
