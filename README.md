# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

TakeMeter is a text classifier trained on public posts collected from the r/artificial Reddit community. It classifies posts as `evidence_based`, `reasoned_opinion`, or `unsupported_reaction` according to how the author supports the post's main claim. The classifier is intended to distinguish sourced discussion, explained opinions, and unsupported reactions without judging whether the author's position is personally agreeable.


---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `evidence_based` 

**Definition:** A post whose main claim is supported by a statistic, study, named source, quotation, documented event, release note, or other independently checkable evidence.


**Example 1:**
>“Anthropic ran a 26B model across 15 off-brand Android TV boxes worth $55 each.”

**Example 2:**
>“We ran 500 questions through Gemini to see when it searches the web.”

### `reasoned_opinion`

**Definition:** A post that explains its position through reasoning, examples, comparison, or personal experience but does not provide independently checkable evidence for the main claim.

**Example 1:**
> “My theory after a year of customer support: AI makes people more confident, not more correct.”

**Example 2:**
> “AI companions may reduce loneliness and increase isolation at the same time.”
### `unsupported_reaction`

**Definition:** A post that mainly gives a judgment, prediction, emotional reaction, or question without meaningful supporting reasoning or checkable evidence.

**Example 1:**
> “Why do people blame AI for AI slop?”

**Example 2:**
> “What's the most annoying thing about using AI that nobody seems to be fixing?”

### The hardest boundary

**Which two labels:** `reasoned_opinion` and `unsupported_reaction`

**The decision rule I used every time:**
<!-- e.g. "If the post names a specific checkable fact, it's `analysis`, even
     if the tone is heated." -->
The hardest boundary is between reasoned_opinion and unsupported_reaction. If the post explains why through a causal argument, comparison, concrete example, or relevant personal experience, label it reasoned_opinion. If it mainly states a conclusion, reaction, prediction, or question without explaining why, label it unsupported_reaction. A link, named study, statistic, quotation, release, or documented event that supports the main claim moves the post to evidence_based.


---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:**
I collected 150 public posts from the `r/artificial` subreddit. I used posts from the New, Hot, and Best feeds so the dataset included news links, research discussions, personal opinions, questions, project announcements, and short reactions. Advertisements, navigation text, empty entries, and exact duplicates were removed.

**How I labelled them:**  
I used three labels: `evidence_based`, `reasoned_opinion`, and `unsupported_reaction`. Each post was labelled according to the support contained in its text, rather than its Reddit flair. AI assistance was used to propose labels, and the suggestions were checked against the written label definitions. Ambiguous cases were decided by asking whether the post contained independently checkable evidence, meaningful reasoning without external evidence, or neither.


**Counts per label:**

| Label | Count | Percentage |
|---|---:|---:|
| `evidence_based` | 59 | 39.3% |
| `reasoned_opinion` | 54 | 36.0% |
| `unsupported_reaction` | 37 | 24.7% |
| **Total** | **150** | **100%** |

The dataset is reasonably balanced. No single label accounts for more than 40% of the examples. `unsupported_reaction` is the smallest label because the subreddit contains many detailed news and discussion posts, while short unsupported reactions are less common in the main feed.

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

1. **“AI deepfakes are getting out of hand.”**  
   I considered `unsupported_reaction` because the title is primarily an emotional judgment. However, the post includes a link to a report about Microsoft Teams detecting deepfakes. I labelled it `evidence_based` because its concern is connected to an independently checkable source.

2. **“If an AI can't decide what to want, can it ever be truly conscious?”**  
   I considered `unsupported_reaction` and `reasoned_opinion`. I selected `reasoned_opinion` because the author explains the distinction between following an assigned goal and independently choosing a goal. The argument contains reasoning, but it does not rely on a study or other external evidence.

3. **“What if the AI boom goes bust?”**  
   I labelled this `unsupported_reaction` because it asks a broad question without offering supporting evidence, examples, or a developed explanation. The title expresses a concern, but there is not enough reasoning to place it under `reasoned_opinion`.

---

<!-- Your starting model, your settings, and anything you changed and why. -->

## The Training Run

**Base model:** `distilbert-base-uncased`

**Settings:** 3 epochs, learning rate `2e-5`, batch size 16, maximum sequence length 128, and random seed 42. Training ran with PyTorch 2.14.1 using Apple Silicon GPU acceleration (`mps`).

**Anything I changed from the defaults, and why:** I kept the default training hyperparameters so this first run would provide a clear baseline for comparison. I changed only the label list so it matched the labels in `labels.csv`: `evidence_based`, `reasoned_opinion`, and `unsupported_reaction`.

**Split sizes:** 104 training posts, 23 validation posts, and 23 test posts. The test split contained 9 `evidence_based`, 8 `reasoned_opinion`, and 6 `unsupported_reaction` posts. Because `unsupported_reaction` had only six test examples, its metric may vary noticeably across different random seeds.

**Initial results:** The held-out accuracy was `0.565` and macro F1 was `0.431`. Per-label F1 was `0.625` for `evidence_based`, `0.667` for `reasoned_opinion`, and `0.000` for `unsupported_reaction`. <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->



---

## How I Used AI

**Moment 1**

- *What I asked for:* I asked AI to help turn the general idea of post quality into three clear labels that could be applied consistently to posts from `r/artificial`.
- *What came back:* It suggested separating posts with checkable evidence, posts containing explained opinions, and posts containing unsupported reactions.
- *What I changed:* I refined these categories into `evidence_based`, `reasoned_opinion`, and `unsupported_reaction`. I also wrote a specific decision rule for the difficult boundary between `reasoned_opinion` and `unsupported_reaction`.

**Moment 2**

- *What I asked for:* I asked AI to check my dataset format, label distribution, and notebook configuration before training.
- *What came back:* It identified the required `text`, `label`, and `note` columns, summarized the label distribution, and noticed that the notebook’s starter labels did not match the labels in my CSV.
- *What I changed:* I corrected the CSV column name, verified the dataset contained 150 posts, and changed the notebook label list to exactly match my dataset before rerunning the training.

**Pre-labelling disclosure:** AI was used to propose labels for the collected posts and to help identify advertisements, interface text, blank entries, and duplicates. I reviewed the proposed labels against my written taxonomy and used my decision rule to resolve ambiguous cases before training.
<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->
## Stretch Features Declared Before Testing

Before running the Unit 6 experiments, I decided to attempt all three stretch features:

1. **Confidence check:** I will compare the accuracy of the model's most-confident third of predictions with its least-confident third.
2. **Per-label error write-up:** I will analyze the worst-performing label from the confusion matrix, identify which label it is confused with, and inspect what the misclassified examples have in common.
3. **Second measured improvement:** After measuring the first improvement, I will make one additional change, rerun the same three seeds, and compare a third run log against the earlier results.
---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->


| Measure | Baseline | Trained | Difference |
|---|---:|---:|---:|
| Overall accuracy | 0.435 | 0.565 | +0.130 |
| Macro F1 | 0.347 | 0.431 | +0.083 |
| F1 — `evidence_based` | 0.667 | 0.625 | -0.042 |
| F1 — `reasoned_opinion` | 0.000 | 0.667 | +0.667 |
| F1 — `unsupported_reaction` | 0.375 | 0.000 | -0.375 |

**What I predicted before I looked:** I expected the trained model to outperform the zero-shot baseline overall because it was fine-tuned on posts from the same community. I expected both models to struggle most with `unsupported_reaction` because it is the smallest label and overlaps with `reasoned_opinion`.

**What the gap actually means:** The trained model improved overall accuracy by 0.130 and macro F1 by 0.083, so fine-tuning added measurable value. Most of the improvement came from `reasoned_opinion`, whose F1 increased from 0.000 to 0.667. However, fine-tuning reduced `unsupported_reaction` F1 from 0.375 to 0.000 and slightly reduced `evidence_based` F1. Therefore, the trained model learned `reasoned_opinion` well but did not learn a balanced boundary across all three labels.
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
