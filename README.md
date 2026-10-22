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
|---|---:|---:|---:|---:|---|
| 1. Overall accuracy | ≥ 0.55 | 0.565 | 0.522 | 0.391 | MISSED |
| 2. Macro F1 | ≥ 0.45 | 0.431 | 0.403 | 0.282 | MISSED |
| 3. F1 — `evidence_based` | ≥ 0.55 | 0.625 | 0.615 | 0.286 | MISSED |
| 4. F1 — `reasoned_opinion` | ≥ 0.55 | 0.667 | 0.593 | 0.560 | MET |
| 5. F1 — `unsupported_reaction` | ≥ 0.35 | 0.000 | 0.000 | 0.000 | MISSED |

### Confusion matrix

**Device:** `mps` — Apple Silicon GPU, PyTorch 2.14.1.

| true \ predicted | `evidence_based` | `reasoned_opinion` | `unsupported_reaction` |
|---|---:|---:|---:|
| **`evidence_based`** | 5 | 4 | 0 |
| **`reasoned_opinion`** | 0 | 8 | 0 |
| **`unsupported_reaction`** | 2 | 4 | 0 |

**My biggest off-diagonal number, and what it means:**

Four real `evidence_based` posts were predicted as `reasoned_opinion`, while zero real `reasoned_opinion` posts were predicted as `evidence_based`. Four real `unsupported_reaction` posts were also predicted as `reasoned_opinion`. Most importantly, the model never predicted `unsupported_reaction`; all six real examples were assigned to another label. This shows that the model did not learn a usable boundary for `unsupported_reaction`.
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->


---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---:|---|---|
| 1 | Overall accuracy | ≥ 0.55 | MISSED | Only Seed 42 reached the target. Seeds 7 and 2024 scored 0.522 and 0.391. |
| 2 | Macro F1 | ≥ 0.45 | MISSED | None of the three seeds reached 0.45; the highest macro F1 was 0.431. |
| 3 | F1 — `evidence_based` | ≥ 0.55 | MISSED | Seeds 42 and 7 passed, but Seed 2024 scored only 0.286. The target had to hold across all three seeds. |
| 4 | F1 — `reasoned_opinion` | ≥ 0.55 | MET | All three scores—0.667, 0.593, and 0.560—met the target. |
| 5 | F1 — `unsupported_reaction` | ≥ 0.35 | MISSED | Its F1 was 0.000 for every seed, so it never reached the target. |
**Diagnoses**

Criteria 1 and 2 were missed because the classifier was unstable across random splits. Overall accuracy changed by 0.174 and macro F1 changed by 0.149. With only 150 posts, moving a small number of difficult examples between training and testing substantially changed the results.

Criterion 3 was missed because `evidence_based` was unstable across splits. Its F1 fell from 0.625 and 0.615 to 0.286 for Seed 2024. The Seed 42 confusion matrix shows that four of nine real `evidence_based` posts were classified as `reasoned_opinion`, demonstrating a difficult one-directional boundary between those labels.

Criterion 5 was the clearest failure. `unsupported_reaction` received an F1 of 0.000 for every seed. In the Seed 42 confusion matrix, four of its six test examples were predicted as `reasoned_opinion` and two as `evidence_based`. The model never predicted `unsupported_reaction`.

The agreement report produced 30 out of 30 matches under the staff taxonomy. Therefore, it does not provide evidence that I inconsistently applied clearly written rules. The more strongly supported cause is limited learning from a small and uneven dataset: `unsupported_reaction` has only 37 examples, compared with 54 `reasoned_opinion` and 59 `evidence_based` examples. Its wording may also overlap with unsupported opinions, making this boundary difficult for the model.

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

## Agreement Report

**Agreement rate:** **30 / 30 = 100%**

**Disagreements**

There were no disagreements. I assigned the same label as the staff for all 30 posts, so there were no cases to adjudicate or place into piles (a), (b), or (c).

**What the pattern in my disagreements tells me:**

The staff set was relatively easy because its examples closely followed the written distinctions: `analysis` used load-bearing facts, `hot_take` made general unsupported claims, and `reaction` described immediate personal experiences. However, matching all 30 examples still shows that I can consistently apply a clearly written taxonomy. Therefore, the poor `unsupported_reaction` performance in my trained classifier is not supported as a general rule-application problem by this agreement test. The stronger evidence points toward the smaller number of `unsupported_reaction` examples and the model failing to learn that boundary from the available data.

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

I increased training from 3 epochs to 5 epochs while keeping the model, dataset, learning rate, batch size, seeds, and evaluation procedure unchanged.

**Which diagnosis pointed at it:**

The model produced an F1 of 0.000 for `unsupported_reaction` across all three seeds and never predicted that label in the Seed 42 confusion matrix. Because the agreement report showed 100% agreement under clearly written rules, I tested whether the model was undertrained rather than immediately changing the labels. Two additional epochs give it more opportunities to learn patterns associated with the smallest label.

## Second Improvement — Balanced Training Data

**What I changed:**

I balanced only the training portion of each split by randomly duplicating examples from the smaller labels until every training label had the same number of examples as the largest label. Validation and test examples were not duplicated or changed.

**Which diagnosis pointed at it:**

After five epochs, `unsupported_reaction` still had F1 scores of 0.000, 0.000, and 0.250. It was the smallest label in the original dataset, with 37 examples compared with 54 `reasoned_opinion` and 59 `evidence_based` examples. Additional epochs improved overall performance but did not make the model reliably predict the minority class, so the second change directly addresses class imbalance.

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---:|---:|---:|---:|---|
| 1. Overall accuracy | ≥ 0.55 | 0.652 | 0.696 | 0.478 | MISSED |
| 2. Macro F1 | ≥ 0.45 | 0.502 | 0.535 | 0.420 | MISSED |
| 3. F1 — `evidence_based` | ≥ 0.55 | 0.778 | 0.842 | 0.400 | MISSED |
| 4. F1 — `reasoned_opinion` | ≥ 0.55 | 0.727 | 0.762 | 0.609 | MET |
| 5. F1 — `unsupported_reaction` | ≥ 0.35 | 0.000 | 0.000 | 0.250 | MISSED |

## Second Measured Improvement — Balanced Training

### Run Log — After Balanced Training

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---:|---:|---:|---:|---|
| 1. Overall accuracy | ≥ 0.55 | 0.696 | 0.739 | 0.609 | MET |
| 2. Macro F1 | ≥ 0.45 | 0.608 | 0.689 | 0.575 | MET |
| 3. F1 — `evidence_based` | ≥ 0.55 | 0.778 | 0.842 | 0.588 | MET |
| 4. F1 — `reasoned_opinion` | ≥ 0.55 | 0.762 | 0.824 | 0.737 | MET |
| 5. F1 — `unsupported_reaction` | ≥ 0.35 | 0.286 | 0.400 | 0.400 | MISSED |

#### Confusion Matrix After Improvement — Seed 42

| true \ predicted | `evidence_based` | `reasoned_opinion` | `unsupported_reaction` |
|---|---:|---:|---:|
| **`evidence_based`** | 7 | 2 | 0 |
| **`reasoned_opinion`** | 0 | 8 | 0 |
| **`unsupported_reaction`** | 2 | 4 | 0 |

The largest off-diagonal error was four real `unsupported_reaction` posts classified as `reasoned_opinion`, while zero real `reasoned_opinion` posts were classified as `unsupported_reaction`. The model therefore continued to favor `reasoned_opinion` over `unsupported_reaction`.

**Did it help, and how do I know:**

Yes, but only partially. Increasing training from 3 to 5 epochs improved accuracy for every seed: from 0.565, 0.522, and 0.391 to 0.652, 0.696, and 0.478. Macro F1 also increased from 0.431, 0.403, and 0.282 to 0.502, 0.535, and 0.420.

The improvement especially helped `evidence_based` and `reasoned_opinion`. In the Seed 42 confusion matrix, correct `evidence_based` predictions increased from 5 to 7.

However, it did not fully fix `unsupported_reaction`. Its F1 remained 0.000 for Seeds 42 and 7 and reached only 0.250 for Seed 2024. The model still never predicted that label in the Seed 42 matrix.

The change also did not improve stability. Accuracy spread increased from 0.174 before the change to 0.217 afterward. Therefore, additional epochs improved average performance but made the results more dependent on the random split.

## What's Still Broken

Criteria 1, 2, 3, and 5 remain missed because their targets did not hold across all three seeds. Seed 2024 continued to perform substantially worse than the other splits, and accuracy spread increased to 0.217.

The largest remaining failure is `unsupported_reaction`. Its F1 was 0.000, 0.000, and 0.250 after the improvement. The model still preferred `reasoned_opinion` for unsupported statements and did not reliably learn the smallest class.

I stopped this improvement at 5 epochs because more training alone had already increased split sensitivity and had not consistently fixed the minority label. My next change would directly address class imbalance rather than continuing to increase epochs.

**The gap between what I meant my labels to capture and what the model learned:**

I intended `unsupported_reaction` to capture short, unsupported emotional or immediate responses, while `reasoned_opinion` should contain an explained viewpoint. The confusion matrix shows that the model mainly learned the broader language of opinions and repeatedly absorbed `unsupported_reaction` into `reasoned_opinion`.
<!-- For each criterion still missed: what you'd do, and why you stopped. -->


<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->
### Confusion Matrix After Balanced Training — Seed 42

| true \ predicted | `evidence_based` | `reasoned_opinion` | `unsupported_reaction` |
|---|---:|---:|---:|
| **`evidence_based`** | 7 | 2 | 0 |
| **`reasoned_opinion`** | 0 | 8 | 0 |
| **`unsupported_reaction`** | 2 | 3 | 1 |

The largest remaining confusion was three real `unsupported_reaction` posts classified as `reasoned_opinion`, while zero real `reasoned_opinion` posts were classified as `unsupported_reaction`. The model still leans toward the broader `reasoned_opinion` label, but it now correctly predicts at least one `unsupported_reaction` example.

**Did the second improvement help, and how do I know:**

Yes. Balancing the training split produced the strongest results of all three experiments.

Compared with the five-epoch run, overall accuracy improved from 0.652, 0.696, and 0.478 to 0.696, 0.739, and 0.609. Macro F1 improved from 0.502, 0.535, and 0.420 to 0.608, 0.689, and 0.575.

The most important improvement was for `unsupported_reaction`. Its F1 changed from 0.000, 0.000, and 0.250 to 0.286, 0.400, and 0.400. Although Seed 42 remained below the target of 0.35, the model no longer completely ignored the label.

Performance also became more stable. Accuracy spread decreased from 0.217 after the first improvement to 0.130 after balanced training. This is still greater than 0.10, so the dataset remains sensitive to the random split, but the instability was reduced.

Four of the five acceptance criteria were met after balanced training. Criterion 5 remained missed because its target had to hold across all three seeds and Seed 42 reached only 0.286.

## What's Still Broken

The remaining missed criterion is the `unsupported_reaction` F1 target. Its three scores were 0.286, 0.400, and 0.400, so Seed 42 remained below the required 0.35.

The Seed 42 confusion matrix shows that only one of six real `unsupported_reaction` posts was classified correctly. Three were classified as `reasoned_opinion`, and two were classified as `evidence_based`. This means the model still does not have a consistently reliable boundary for short unsupported reactions.

The agreement exercise produced 30 out of 30 matches, so it did not provide evidence that I inconsistently applied the staff’s written rules. The remaining problem is better supported as a combination of limited data, overlap between reaction and opinion language, and split sensitivity. Accuracy still varied by 0.130 across seeds.

With more time, I would collect additional naturally occurring `unsupported_reaction` examples, especially difficult examples that resemble `reasoned_opinion`, rather than continuing to duplicate the existing examples.

**The gap between what I meant my labels to capture and what the model learned:**

I intended `unsupported_reaction` to capture unsupported emotional or immediate responses, while `reasoned_opinion` should contain an explained viewpoint. Balanced training helped the model recognize some reactions, but the confusion matrix shows that it still treats many reactions as general opinions.
---




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
