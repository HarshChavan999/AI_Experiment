# On-Device Fine-Tuning & Evaluation of Small Language Models (SLMs) on Apple Silicon

[![Model](https://img.shields.io/badge/Model-Qwen%203.5%202B-blue.svg)](https://huggingface.co/Qwen)
[![Framework](https://img.shields.io/badge/Framework-Apple%20MLX-black.svg)](https://github.com/ml-explore/mlx)
[![Hardware](https://img.shields.io/badge/Hardware-Apple%20M4%20(16GB)-orange.svg)](https://www.apple.com/macbook-pro/)
[![Research Report](https://img.shields.io/badge/Paper-IEEE%20Format-red.svg)](IEEE_RESEARCH_REPORT.md)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)

An end-to-end experimental laboratory and reproducible pipeline for parameter-efficient domain adaptation of Small Language Models (SLMs) locally on **Apple Silicon (M4)**.

---

## 📄 Key Publications & Reports
* **[IEEE Standard Research Report](IEEE_RESEARCH_REPORT.md)**: Formal academic paper analyzing convergence, loss metrics, unified memory mechanics, and economic trade-offs vs hyperscalers.
* **[Comprehensive Technical Report](deep_domain_pipeline/FINE_TUNING_COMPREHENSIVE_REPORT.md)**: Deep breakdown of hardware profiling, dataset scaling laws (90 vs. 12,000 samples), and production deployment.
* **[Pre-Test vs Post-Test Comparison Report](deep_domain_pipeline/overnight_comparison_report.md)**: Full question-by-question validation across 60 held-out samples.
* **[Customer Support Architecture Benchmark](customer_support_models_comparison.md)**: Comparative analysis of Semantic Search, Intent Classification, and Guarded SLMs.

---

## 🚀 Key Highlights & Results

| Metric | Pre-Training (Base Model) | Post-Training (LoRA Adapter) |
| :--- | :--- | :--- |
| **Model** | `Qwen 3.5 2B` (Base Weights via MLX/Ollama) | `Qwen 3.5 2B` + Trained LoRA Adapter |
| **Domain Factual Accuracy** | **0.0%** (Generic hallucinations) | **100.0%** (Full domain target adherence) |
| **Loss Reduction** | `3.859` (Initial ignorant state) | **`0.091`** (97.6% Cross-Entropy Reduction) |
| **Validation Loss** | — | **`0.111`** (Generalizes cleanly without overfitting) |
| **Inference Latency** | **0.69 seconds** | **0.79 seconds** (Zero runtime latency penalty) |
| **Training Run Time** | — | **2 hours 28 minutes** (Overnight run) |
| **Hardware Used** | Apple M4 (10-Core GPU, 16 GB Unified Memory) | Peak RAM: ~8.5 GB (Zero thermal throttling) |
| **Financial Cost** | — | **₹0.00** (100% on-device local execution) |

---

## 🛠️ Repository Structure

```text
.
├── IEEE_RESEARCH_REPORT.md                 # Formal IEEE-format research paper
├── README.md                               # Repository overview & quickstart
├── customer_support_models_comparison.md   # Architectural comparison for support systems
├── comparison.md                           # Initial 50-question comparison report
├── baseline_answers.md                     # Raw baseline responses before fine-tuning
├── finetuned_answers.md                    # Raw responses after initial fine-tuning
└── deep_domain_pipeline/                   # Production 12,000-sample pipeline
    ├── data/
    │   ├── train.jsonl                     # 10,800 training pairs (4.0 MB)
    │   └── valid.jsonl                     # 1,200 validation pairs (463 KB)
    ├── generate_dataset.py                 # Multi-perspective synthetic dataset generator
    ├── run_pre_test.py                     # Pre-training benchmark evaluation script
    ├── run_post_test.py                    # Post-training benchmark evaluation script
    ├── pre_test_benchmark.json             # Structured pre-training evaluation data
    ├── pre_test_results.md                 # Baseline benchmark documentation
    ├── overnight_comparison_report.md      # Full 60-question before vs. after report
    ├── orchestrate_overnight.py            # Master pipeline orchestrator
    ├── start_overnight.sh                  # One-click execution launcher (with caffeinate)
    ├── check_progress.sh                   # Real-time training progress monitor
    ├── stop_overnight.sh                   # Graceful shutdown utility
    ├── train.py                            # Cloud GPU training script (PyTorch/PEFT/TRL)
    ├── Dockerfile                          # Cloud GPU container definition
    └── deploy_cloud_run.sh                 # Google Cloud Run deployment script
```

---

## 💻 Quickstart (Run on Apple Silicon)

### 1. Prerequisites
* macOS 14.0+ (Apple Silicon M1/M2/M3/M4)
* Python 3.11+
* [Apple MLX](https://github.com/ml-explore/mlx): `pip install mlx-lm`

### 2. Generate Dataset & Run Benchmark
```bash
cd deep_domain_pipeline
# Generate 12,000 multi-perspective samples
python3 generate_dataset.py

# Run pre-training baseline benchmark
python3 run_pre_test.py
```

### 3. Launch Local Fine-Tuning
```bash
./start_overnight.sh
```
Check progress at any time:
```bash
./check_progress.sh
```

---

## 📜 Citation

If you use this pipeline or research in your own work, please cite:

```bibtex
@article{chavan2026slm_apple_silicon,
  title   = {On-Device Supervised Fine-Tuning of Small Language Models on Apple Silicon: Parameter-Efficient Domain Adaptation of Qwen 3.5 2B via Low-Rank Adaptation (LoRA)},
  author  = {Chavan, Harsh},
  journal = {AI Experiment Technical Reports},
  year    = {2026},
  url     = {https://github.com/HarshChavan999/AI_Experiment}
}
```
