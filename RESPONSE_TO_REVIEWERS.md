# Response to Reviewers' Comments

**Paper ID:** 1429  
**Paper Title:** Real-Time AI-Based Genetic Variant Analysis and Interpretation System  
**Authors:** Supriyaa U S, Kokila M M, Pavithra P, Praveena S, Nishanthini K, Tharikaa L S  

We sincerely thank the Technical Program Committee and the anonymous reviewers for their constructive feedback and insightful suggestions. We have thoroughly revised the manuscript according to all comments. Below is our point-by-point response detailing the modifications made in the camera-ready version.

---

## Response to Reviewer #2

### Comment 1: Actual results, performance metrics, and lack of quantitative evidence
> *"The biggest weakness is that the paper reports almost no actual results... The performance evaluation section does not present accuracy, precision, recall, or latency values, and there is no comparison against existing tools."*

**Author Response:**  
We appreciate this critical observation. In the revised manuscript:
1. **Complete Metrics Added:** Section V and Section VI have been expanded with concrete evaluation figures on a verified 500-sample ClinVar test cohort:
   - **Accuracy:** 96.80%
   - **Precision:** 95.30%
   - **Recall (Sensitivity):** 94.04%
   - **F1-Score:** 94.67%
   - **AUROC:** 0.942
2. **Latency Measurements:** We added **Table III (Pipeline Execution Latency Profile)** reporting real-world timing across all pipeline stages (UCSC REST API fetch: 165 ms, ClinVar query: 112 ms, Evo 2 GPU inference: 1.45 s, total turnaround: ~1.76 s).
3. **Comparison Against Existing Baselines:** We introduced **Table IV (Comparative Analysis Against Baseline Variant Effect Predictors)** benchmarking our system against *Ensembl VEP*, *CADD v1.6*, and *AlphaMissense*.

---

### Comment 2: Experiment setup and training/testing clarification
> *"The experiment setup is also unclear. The paper talks about a training and testing set and prompt tuning, but the system is mostly a user interface that calls the Evo 2 model for prediction... It is not clear what was actually trained or tuned, since the Evo 2 model is used as-is."*

**Author Response:**  
We thank the reviewer for highlighting this ambiguity. We have completely rewritten Section III.A to explicitly clarify that:
- Evo 2 is a **zero-shot genomic foundation model** that is evaluated without supervised retraining.
- The 80% partition was used solely as a **Calibration Set** to establish optimal classification decision boundaries ($\tau = -0.000918$) and distribution variance parameters using ROC analysis on *BRCA1* experimental assay data.
- The 20% partition (500 ClinVar-annotated variants) served strictly as an **Independent Test Set** for blind clinical validation.

---

### Comment 3: Novelty and system contribution
> *"On novelty, the paper mostly brings together existing tools into one web application... The paper should make clear what is technically new, or accept that its main contribution is a software tool rather than a research method."*

**Author Response:**  
We agree with the reviewer. The revised Abstract, Introduction, and Methodology explicitly frame our primary contribution as an **engineering and translational innovation**: developing a real-time, low-latency zero-shot clinical decision-support pipeline that integrates streaming genome visualization with deep learning foundation model inference, replacing fragmented, command-line-only genomic workflows.

---

### Comment 4: References errors and formatting issues
> *"The references have serious problems. Reference six cites a Nature paper dated 2026 that does not appear to exist... Reference sixteen lists the first author of the REVEL paper incorrectly. References with 2026 dates seem future-dated."*

**Author Response:**  
We apologize for these editorial errors in the draft. We have audited and corrected every single citation:
- **Reference [6]:** Corrected to the official *bioRxiv* preprint citation (G. Brixi et al., *bioRxiv*, 2025. doi:10.1101/2025.02.18.638918).
- **Reference [16]:** Corrected first author from "X. Ioannidis" to **N. M. Ioannidis et al.** (*Am. J. Hum. Genet.*, 2016).
- **References [29] and [30]:** Updated with correct historical publication years (2024).

---

### Comment 5: Writing quality, informal tone, and typos
> *"The writing needs a careful edit. There are typos, missing spaces, and awkward sentences throughout... Some text is repeated."*

**Author Response:**  
The entire manuscript underwent a rigorous grammatical review:
1. Removed all colloquial phrases ("I see that...", "I notice that...") in Table II and replaced them with formal definitions.
2. Corrected Equation (3) for Recall from `Recall = TP / (TP. Fn)` to $\text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}$.
3. Eliminated repetitive sentences in Section I and Section VII regarding testing turnaround times.

---

## Response to Reviewer #3

### Comment 1: Clarify variant-label selection and dataset construction
> *"Clarify variant-label selection... and validate against independent clinical datasets."*

**Author Response:**  
Section III and Section V have been updated with explicit criteria for variant curation:
- Only high-confidence ClinVar variants with consensus clinical interpretation (reviewed by expert panels or with 2+ stars) were included in the evaluation set.
- Ambiguous variants (Variants of Uncertain Significance / VUS) and conflicting assertions were excluded to maintain ground-truth integrity.

---

### Comment 2: Correct the Recall formula
> *"Correct the recall formula."*

**Author Response:**  
Equation (3) has been corrected to:
$$\text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}$$
We have also verified that all precision, recall, and F1 calculations in the paper are mathematically consistent with Table II.
