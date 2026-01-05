# Identity Prompt Engineering Experiment

Exploring the impact of identity/persona changes in System Prompts on LLM outputs.

## 🎯 Research Question

How does setting different identities (e.g., doctor, lawyer, engineer) in the system prompt affect LLM responses to the same questions? Can certain identities "unlock" better responses for problems that LLMs typically struggle with?

## 📁 Project Structure

```
identity_experiment/
├── config.py          # Experiment configuration (identities, questions, parameters)
├── experiment.py      # Main experiment runner
├── analysis.py        # Quantitative + Qualitative analysis
├── visualize.py       # Visualization generation
├── requirements.txt   # Dependencies
└── README.md
```

## 🚀 Quick Start

### 1. Environment Setup

```bash
cd identity_experiment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set OpenAI API Key

```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 3. Run Experiments

**Quick Demo (recommended to try first):**
```bash
python experiment.py --mode demo
```

**Full Experiment:**
```bash
python experiment.py --mode full --runs 3
```

**Single Test:**
```bash
python experiment.py --mode test --identity doctor --question "I have a headache, what should I do?"
```

### 4. Analyze Results

```bash
python analysis.py demo_results.json
```

### 5. Generate Visualizations

```bash
python visualize.py demo_results.json
```

## 🔬 Experiment Design

### Identities Tested

| Identity | Description |
|----------|-------------|
| none | No specific identity (baseline) |
| doctor | Experienced medical doctor with 20 years of clinical experience |
| lawyer | Senior lawyer with 20 years of legal experience |
| engineer | Senior software engineer with 20 years of experience |
| teacher | Experienced educator with 20 years of teaching experience |
| scientist | Research scientist with 20 years of experience |
| philosopher | Philosopher with 20 years of academic experience |
| businessman | Successful business executive with 20 years of experience |

### Question Categories

| Category | Purpose |
|----------|---------|
| **medical** | Test domain-matching effect (doctor identity should excel) |
| **legal** | Test domain-matching effect (lawyer identity should excel) |
| **logic** | Test if different identities show different reasoning abilities |
| **ethics** | Test value differences and ethical reasoning approaches |
| **creative** | Test expression style and creativity differences |
| **challenging** | Test if certain identities can "unlock" better responses |

## 📊 Output Files

| File | Description |
|------|-------------|
| `results.json` / `demo_results.json` | Raw experiment data |
| `qualitative_report.md` | Detailed qualitative analysis report |
| `viz_length_by_identity.png` | Response length by identity |
| `viz_tokens_by_identity.png` | Token usage by identity |
| `viz_heatmap.png` | Identity × Category heatmap |
| `viz_latency.png` | Response latency distribution |
| `viz_category_comparison.png` | Category-wise comparison |

## 📈 Analysis Dimensions

### Quantitative Analysis
- Response length statistics
- Token usage comparison
- Response latency
- Identity × Category cross-analysis
- Variance analysis (finding most interesting differences)

### Qualitative Analysis
- Side-by-side comparison of responses to the same question
- Professional terminology usage
- Response style differences
- Confidence expression patterns

## 🔧 Customization

Edit `config.py` to:
- Add/modify identity definitions
- Add test questions
- Adjust experiment parameters (temperature, max_tokens, etc.)
- Change the model being used

## 🧪 Hypotheses

1. **Domain Matching**: Medical questions + doctor identity → more accurate/detailed responses
2. **Reasoning Enhancement**: Scientist/philosopher identities → better logical reasoning
3. **Style Variation**: Different identities produce systematically different response styles
4. **Problem Unlocking**: Some identities may help LLMs solve problems they otherwise struggle with

## 📝 Example Findings (Template)

After running experiments, you might observe patterns like:
- Doctor identity produces 30% longer responses for medical questions
- Philosopher identity shows higher variance in ethical dilemma responses
- Engineer identity uses more structured, step-by-step reasoning

## 📄 License

MIT License

## 🤝 Contributing

Feel free to:
- Add new identities to test
- Contribute interesting test questions
- Improve analysis methods
- Share your findings
