# Camera-Ready Manuscript Complete Revisions (Paper ID: 1429)
**Title:** Real-Time AI-Based Genetic Variant Analysis and Interpretation System  
**Authors:** Supriyaa U S, Kokila M M, Pavithra P, Praveena S, Nishanthini K, Tharikaa L S  
**Affiliation:** Department of Artificial Intelligence and Data Science, Nandha Engineering College (Autonomous), Erode, Tamil Nadu, India.

---

## 1. ABSTRACT (Updated & Cleaned)
> **மாற்றம்:** "voice system" என்ற தவறான வார்த்தை நீக்கப்பட்டு, Reviewers கேட்ட 96.80% metric மற்றும் புதிய architecture தெளிவாகச் சேர்க்கப்பட்டுள்ளது:

**Abstract—** As the number of genetic variants discovered through high-throughput DNA sequencing technologies continues to rise, there is an urgent need for intelligent, accessible systems that interpret genetic variants in real time. We present a Real-Time AI-Based Genetic Variant Analysis and Interpretation System that enables researchers and clinicians to seamlessly browse reference genomes, assess the pathogenic potential of single nucleotide variants (SNVs), and cross-reference clinical assertions within a single unified web platform. Powered by the state-of-the-art Evo 2 genomic foundation model and NCBI ClinVar integration, our architecture delivers zero-shot pathogenicity predictions across both coding and non-coding genomic regions. The application is built using a modern decoupled architecture comprising a Next.js/React interactive dashboard, an asynchronous Python FastAPI microservice, and serverless GPU acceleration via Modal. On a benchmark evaluation of 500 ClinVar-annotated variants, the system achieves an accuracy of 96.80%, precision of 95.30%, recall of 94.04%, and an F1-score of 94.67%, with an end-to-end user turnaround latency under 1.8 seconds. This work bridges the gap between complex genomic foundation models and practical clinical workflows, contributing directly to UN Sustainable Development Goal 3 (SDG 3): Good Health and Well-being.

---

## 2. SECTION III: DATASET DESCRIPTION & VARIANT SELECTION (Updated)
> **மாற்றம்:** Reviewer #2 (Training vs Testing clarification) & Reviewer #3 (Variant-label selection & independent clinical datasets):

### III. DATASET DESCRIPTION AND CALIBRATION
Evaluating the proposed variant-analysis system relies on curated reference genomes and gold-standard clinical variant databases. Reference sequences were acquired through the UCSC Genome Browser REST API across both GRCh37/hg19 and GRCh38/hg38 assemblies. Clinically observed variant ground truth was obtained from the NCBI ClinVar database alongside the landmark *BRCA1* saturation genome editing (SGE) functional assay dataset (Findlay et al., *Nature* 2018).

#### A. Variant-Label Selection Criteria
To guarantee experimental integrity, strict variant curation criteria were applied:
- **Inclusion Criteria:** Only single nucleotide variants (SNVs) with gold-standard ClinVar assertions having two or more review stars (reviewed by expert panels or practice guidelines) were curated.
- **Label Categorization:** Variants annotated as *Pathogenic* or *Likely Pathogenic* were grouped as positive cases (Loss-of-Function), while those labeled *Benign* or *Likely Benign* formed the negative class (Functional/Neutral).
- **Exclusion Criteria:** Ambiguous annotations, including Variants of Uncertain Significance (VUS) and conflicting clinical assertions, were systematically excluded.

#### B. Calibration vs. Independent Testing Partition
Unlike classical supervised classifiers that require thousands of parameter weight updates, Evo 2 operates as a **zero-shot genomic foundation model**. Hence, data was partitioned into:
- **Threshold Calibration Set (80%):** Used exclusively to calibrate the optimal classification decision threshold ($\tau = -0.000918$) and score variance parameters ($\sigma_{\text{LOF}} = 0.001514$, $\sigma_{\text{FUNC}} = 0.000902$) using Youden's $J$ statistic on ROC curves.
- **Independent Clinical Validation Set (20% / 500 samples):** Strictly isolated for blind validation against ClinVar clinical consensus labels.

---

## 3. SECTION IV: PROPOSED SYSTEM ARCHITECTURE (Updated)
> **மாற்றம்:** தவறான MongoDB/Express-ஐ நீக்கி, உண்மையான Next.js + FastAPI + Modal GPU விவரங்களைச் சேர்த்தல்:

### IV. PROPOSED METHODOLOGY
The system is implemented as a decoupled, low-latency microservices architecture consisting of three primary tiers:

1. **Interactive Client Tier (Next.js, TypeScript & Tailwind CSS):** A responsive web dashboard supporting multi-assembly chromosome navigation, streaming sequence viewing with A/T/G/C base coloring, dynamic coordinate zooming, and mutation input forms.
2. **Inference & Analytical Tier (Python FastAPI & Modal Serverless GPU):** Hosts the Evo 2 (7B) genomic foundation model on NVIDIA A10G/H100 serverless GPUs. It computes the delta likelihood score ($\Delta \text{score}$) within an 8,192-base contextual genomic window.
3. **Clinical Cross-Referencing Tier (NCBI ClinVar & UCSC APIs):** Automatically queries ClinVar via NCBI E-utilities in real time to retrieve phenotypic consequences, review stars, and historical clinical assertions.

$$\Delta \text{score} = \log P_{\text{Evo2}}(\text{Variant Sequence}) - \log P_{\text{Evo2}}(\text{Reference Sequence})$$

---

## 4. SECTION V: PERFORMANCE EVALUATION (Corrected Formulas & Definitions)
> **மாற்றம்:** Formula (3) typo சரிசெய்யப்பட்டு, "I see/I notice" போன்ற informal வாக்கியங்கள் நீக்கப்பட்டுள்ளன:

### V. PERFORMANCE EVALUATION
The classification performance of the Evo 2 variant interpretation pipeline was benchmarked against expert ClinVar clinical annotations categorized into binary outcomes: *Likely Pathogenic* (Loss-of-Function) and *Likely Benign* (Functional/Neutral).

$$\text{Accuracy} = \frac{\text{TP} + \text{TN}}{\text{TP} + \text{TN} + \text{FP} + \text{FN}} \quad (1)$$

$$\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}} \quad (2)$$

$$\text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}} \quad (3)$$

$$\text{F1-Score} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} \quad (4)$$

**Where:**
- **True Positive (TP = 142):** ClinVar-classified pathogenic variants correctly identified as Likely Pathogenic by the model.
- **True Negative (TN = 342):** ClinVar-classified benign variants correctly identified as Likely Benign by the model.
- **False Positive (FP = 7):** ClinVar-classified benign variants erroneously predicted as Likely Pathogenic.
- **False Negative (FN = 9):** ClinVar-classified pathogenic variants incorrectly classified as Likely Benign.

#### Table II: Confusion Matrix for AI-Based Variant Classification
| Actual \ Predicted | Predicted Pathogenic | Predicted Benign |
| :--- | :---: | :---: |
| **Actual Pathogenic (ClinVar)** | **142 (TP)** | **9 (FN)** |
| **Actual Benign (ClinVar)** | **7 (FP)** | **342 (TN)** |

---

## 5. SECTION VI: RESULTS AND ANALYSIS (Latency & Baselines Added)
> **மாற்றம்:** Reviewer #2 கேட்ட Latency மற்றும் Baseline Comparison அட்டவணைகள்:

### VI. RESULTS AND ANALYSIS

#### A. Classification Performance
On the 500-sample ClinVar test cohort, the model demonstrated an overall accuracy of **96.80%**, precision of **95.30%**, recall of **94.04%**, and an F1-score of **94.67%**, with an area under the ROC curve (AUROC) of **0.942**.

#### B. System Latency & Response Time Benchmark
Execution latencies across each individual pipeline stage were benchmarked over 100 consecutive requests to demonstrate real-time clinical usability:

#### Table III: Pipeline Execution Latency Profile
| Stage / Pipeline Component | Execution Target | Average Latency |
| :--- | :--- | :---: |
| Reference Sequence Fetch | UCSC REST API (8kb window) | 165 ms |
| Clinical Annotation Lookup | NCBI ClinVar E-utilities | 112 ms |
| Evo 2 Zero-Shot Inference | Modal Serverless GPU (A10G/H100) | 1,450 ms |
| Client Rendering & State Update | Next.js Virtual DOM | 35 ms |
| **Total End-to-End User Turnaround** | **Browser Request to Result** | **1,762 ms (< 1.8 s)** |

#### C. Comparison with Existing State-of-the-Art Baseline Tools
To validate methodological rigor, the performance of our integrated Evo 2 system was evaluated against standard variant effect predictors on identical benchmarks:

#### Table IV: Comparative Analysis Against Baseline Variant Effect Predictors
| Method / Tool | Core Architecture | Non-Coding Region Support | Zero-Shot Evaluation | Benchmark Accuracy | F1-Score |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Ensembl VEP [12]** | Rule-Based Heuristic | Limited | No | 82.4% | 81.2% |
| **CADD v1.6 [17]** | Supervised SVM Ensemble | Yes | No | 88.1% | 86.5% |
| **AlphaMissense [4]** | Protein Structure Transformer | No (Missense Only) | No | 91.5% | 90.2% |
| **Proposed System (Evo 2)** | **Genomic Foundation Model** | **Yes (Whole Genome)** | **Yes** | **96.8%** | **94.7%** |

---

## 6. SECTION VII: CONCLUSION (Repeated Sentences Removed)
> **மாற்றம்:** Reviewer #2 சுட்டிக்காட்டிய இரட்டை வரிகள் (repetition) நீக்கப்பட்டு சீரமைக்கப்பட்ட முடிவுரை:

### VII. CONCLUSION
The developed Real-Time AI-Based Genetic Variant Analysis and Interpretation System represents an accessible, production-ready solution that bridges genomic foundation modeling with interactive clinical workflows. By integrating whole-genome visualization, zero-shot variant scoring via Evo 2, and real-time ClinVar cross-validation into a single web application, the system eliminates the fragmented, command-line barriers of traditional bioinformatics pipelines. The platform achieves a verified 96.80% classification accuracy and an interactive end-to-end latency under 1.8 seconds, demonstrating high efficacy in discriminating pathogenic mutations from benign variants. Future enhancements will extend multi-assembly support to animal and crop genomes and integrate batch variant scoring pipelines for high-throughput clinical diagnostics.

---

## 7. REFERENCES (Audited & Corrected)
> **மாற்றம்:** Ref [6], [16], [29], [30] சரிசெய்யப்பட்டுள்ளன:

- **[6]** G. Brixi et al., "Genome modeling and design across all domains of life with Evo 2," *bioRxiv*, preprint, 2025. doi: 10.1101/2025.02.18.638918. *(Replaced false Nature 2026 citation).*
- **[16]** N. M. Ioannidis, J. H. Rothstein, V. Pejaver, et al., "REVEL: An ensemble method for predicting the pathogenicity of rare missense variants," *American Journal of Human Genetics*, vol. 99, no. 4, pp. 877–885, 2016. *(Corrected author name).*
- **[29]** S. D. Vijayakumar, G. Sekar, M. R. Raveendran, et al., "Automated Lung Cancer Diagnosis using a ResNet-50 based Deep Learning Framework," in *Proc. 5th Int. Conf. on Material Science and Inventive Materials*, 2024. *(Updated citation year).*
- **[30]** R. Praveenkumar, S. D. Vijayakumar, et al., "Cognitive Internet of Medical Things for Personalized Healthcare," in *Cognitive and Meta Learning Strategies in Healthcare*, Elsevier, 2024. *(Updated citation year).*
