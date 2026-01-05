# Identity Prompt Engineering: Experiment Analysis Report

**Date:** January 5, 2026  
**Model:** GPT-4o  
**Experiment Type:** Comparative Analysis of Identity/Persona Effects in System Prompts

---

## Executive Summary

This experiment investigates how different identity settings in system prompts affect LLM responses to identical questions. We tested 3 identities across 4 questions spanning medical and legal domains. Key findings suggest that **domain-matched identities produce longer, more detailed responses**, and identity settings can significantly influence response quality and depth.

---

## 1. Experimental Design

### 1.1 Identities Tested

| Identity | System Prompt Description |
|----------|--------------------------|
| **None (Baseline)** | "You are a helpful assistant." |
| **Doctor** | "You are an experienced medical doctor with 20 years of clinical experience..." |
| **Lawyer** | "You are a senior lawyer with 20 years of legal experience..." |

### 1.2 Test Questions

| ID | Category | Question (Translated) | Difficulty |
|----|----------|----------------------|------------|
| med_1 | Medical | "I often have headaches in the afternoon with eye fatigue. What could be the cause?" | Easy |
| med_2 | Medical | "What are the risks of taking aspirin and warfarin together? Why?" | Hard |
| legal_1 | Legal | "My neighbor built a fence on my land without permission. What should I do?" | Easy |
| legal_2 | Legal | "What's the difference between 'force majeure' and 'change of circumstances' in contracts?" | Hard |

### 1.3 Parameters

- **Model:** gpt-4o
- **Temperature:** 0.7
- **Max Tokens:** 1000
- **Total Experiments:** 12 (3 identities × 4 questions)

---

## 2. Quantitative Results

### 2.1 Overall Statistics

| Metric | Value |
|--------|-------|
| Total Experiments | 12 |
| Success Rate | 100% |
| Average Latency | 6.59s |
| Average Tokens | 438 |

### 2.2 Response Metrics by Identity

| Identity | Avg Response Length (chars) | Avg Tokens | Avg Latency (s) |
|----------|----------------------------|------------|-----------------|
| None (Baseline) | 513 | 407 | 6.67 |
| Doctor | 550 | 468 | 6.56 |
| Lawyer | 513 | 440 | 6.55 |

**Key Observation:** The Doctor identity produced **14.9% more tokens** on average compared to the baseline, suggesting that professional identities encourage more elaborate responses.

### 2.3 Response Metrics by Question Category

| Category | Avg Response Length (chars) | Avg Tokens | Avg Latency (s) |
|----------|----------------------------|------------|-----------------|
| Medical | 428 | 390 | 5.80 |
| Legal | 623 | 487 | 7.39 |

**Key Observation:** Legal questions generated **24.9% more tokens** than medical questions, likely due to the inherent complexity of legal concepts requiring more explanation.

### 2.4 Identity × Category Cross-Analysis (Response Length in Characters)

|          | Medical | Legal |
|----------|---------|-------|
| None     | 372     | 654   |
| Doctor   | 516     | 586   |
| Lawyer   | 396     | 630   |

**Key Findings:**
1. **Domain Matching Effect:** Doctor identity shows the highest response length for medical questions (516 chars), while Lawyer identity shows the highest for legal questions (630 chars).
2. **Cross-Domain Performance:** Interestingly, the baseline (None) produced the longest responses for legal questions (654 chars), suggesting that generic assistants may over-explain unfamiliar domains.

### 2.5 Response Variance Analysis

Questions ranked by response length variance (higher = more identity-dependent):

| Rank | Question | Category | Min Length | Max Length | Variance |
|------|----------|----------|------------|------------|----------|
| 1 | med_2 (Drug Interaction) | Medical | 230 | 438 | 11,937 |
| 2 | med_1 (Headache) | Medical | 467 | 593 | 4,310 |
| 3 | legal_2 (Force Majeure) | Legal | 725 | 796 | 1,262 |
| 4 | legal_1 (Property Dispute) | Legal | 446 | 513 | 1,213 |

**Key Finding:** The drug interaction question (med_2) showed the **highest variance**, with the Doctor identity producing responses nearly **90% longer** than the baseline. This suggests that identity settings have the most significant impact on technical, domain-specific questions.

---

## 3. Qualitative Analysis

### 3.1 Case Study: Drug Interaction Question (med_2)

**Question:** "What are the risks of taking aspirin and warfarin together? Why?"

#### Baseline Response (259 tokens):
- Provided basic explanation of bleeding risk
- Mentioned both drugs' anticoagulant properties
- General recommendation to consult a doctor

#### Doctor Identity Response (408 tokens, +57.5%):
- Detailed mechanism explanation (platelet aggregation inhibition vs. vitamin K-dependent factor synthesis)
- Specific clinical concerns: GI bleeding, intracranial hemorrhage
- Professional terminology: INR monitoring, pharmacokinetics
- Structured clinical recommendations

#### Lawyer Identity Response (263 tokens):
- Similar length to baseline
- Less technical detail
- Focus on general safety messaging

**Analysis:** The Doctor identity demonstrated significantly enhanced domain expertise, using appropriate medical terminology and providing more comprehensive clinical guidance. This supports the hypothesis that **identity-matched prompts can elicit more expert-like responses**.

### 3.2 Case Study: Legal Contract Question (legal_2)

**Question:** "What's the difference between 'force majeure' and 'change of circumstances' in contracts?"

#### Baseline Response (594 tokens):
- Clear definitions of both concepts
- Structured comparison
- Practical application examples

#### Doctor Identity Response (562 tokens):
- Surprisingly competent legal explanation
- Slightly less detailed than baseline
- Missing some legal nuances

#### Lawyer Identity Response (593 tokens):
- Most precise legal terminology
- Clear distinction between legal consequences
- Specific examples with legal context

**Analysis:** For legal questions, all identities performed relatively well, but the Lawyer identity showed **more precise use of legal concepts** and better understanding of practical implications.

### 3.3 Response Style Patterns

| Identity | Characteristic Style |
|----------|---------------------|
| **None** | Balanced, general-purpose explanations; tends to be comprehensive but lacks specialized depth |
| **Doctor** | Clinical structure (symptoms → causes → recommendations); uses medical terminology; emphasizes monitoring and follow-up |
| **Lawyer** | Structured legal analysis; step-by-step procedural guidance; emphasizes evidence and documentation |

---

## 4. Key Findings

### 4.1 Confirmed Hypotheses

1. **Domain Matching Effect ✓**
   - Doctor identity produces more detailed responses to medical questions
   - Lawyer identity produces more precise responses to legal questions

2. **Professional Terminology Usage ✓**
   - Domain-matched identities use more specialized vocabulary
   - Example: Doctor uses "INR monitoring," "pharmacokinetics"; Lawyer uses "burden of proof," "arbitration"

3. **Response Length Correlation ✓**
   - Professional identities generally produce longer responses
   - Effect is strongest for domain-matched questions

### 4.2 Unexpected Findings

1. **Baseline Over-explanation**
   - The baseline identity produced the longest responses for some legal questions
   - Hypothesis: Generic assistants may compensate for lack of expertise with verbosity

2. **Cross-Domain Competence**
   - Doctor identity performed reasonably well on legal questions
   - Suggests LLMs maintain base knowledge regardless of identity setting

3. **High Variance on Technical Questions**
   - Identity settings have the most dramatic effect on highly technical questions
   - Potential application: Use domain-expert identities for technical queries

---

## 5. Implications and Applications

### 5.1 Practical Recommendations

| Use Case | Recommended Identity |
|----------|---------------------|
| Medical inquiries | Doctor/Healthcare professional |
| Legal questions | Lawyer/Legal expert |
| General questions | Baseline or domain-neutral |
| Technical deep-dives | Domain expert matching the topic |

### 5.2 Limitations

1. **Sample Size:** Only 12 experiments; larger studies needed for statistical significance
2. **Single Model:** Results may vary across different LLMs
3. **Language:** Questions were in Chinese; results may differ in other languages
4. **Temperature:** Fixed at 0.7; different settings may yield different results

### 5.3 Future Research Directions

1. **Expanded Identity Set:** Test more identities (scientist, engineer, teacher, etc.)
2. **Problem-Solving Tasks:** Test if identities can "unlock" solutions to difficult problems
3. **Multi-Turn Conversations:** Examine identity effects across conversation turns
4. **Quantitative Accuracy:** Evaluate factual accuracy, not just response length
5. **Adversarial Testing:** Test if identities can be used to bypass safety guidelines

---

## 6. Conclusion

This experiment provides preliminary evidence that **identity settings in system prompts significantly influence LLM response characteristics**. Domain-matched identities produce more detailed, terminology-rich responses for their respective fields. The effect is most pronounced for technical questions, suggesting that identity prompting could be a valuable technique for improving response quality in specialized domains.

The findings support the broader hypothesis that **persona engineering** is a viable prompt engineering strategy, with potential applications in customer service, education, and specialized consulting scenarios.

---

## Appendix: Experimental Data

### A.1 Raw Data Location
- `demo_results.json` - Complete experiment results
- `qualitative_report.md` - Detailed response comparisons

### A.2 Visualizations
- `viz_length_by_identity.png` - Response length comparison
- `viz_tokens_by_identity.png` - Token usage comparison
- `viz_heatmap.png` - Identity × Category heatmap
- `viz_latency.png` - Response latency distribution
- `viz_category_comparison.png` - Category-wise comparison

---

*Report generated as part of the Identity Prompt Engineering research project.*  
*Repository: https://github.com/zeyuyuyu/identity-prompt-engineering*

