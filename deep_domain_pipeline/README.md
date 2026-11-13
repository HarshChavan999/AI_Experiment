# Deep Domain Mastery: 12,000-Sample Fine-Tuning Pipeline

This directory contains the production training pipeline and dataset generator for training **Qwen 3.5 2B** on **12,000 domain-specific samples** for deep domain mastery.

---

## 1. Cost & Time Estimates for Cloud GPU Training

Training a 2B parameter model on a 12,000-sample dataset (3 epochs = ~9.3 Million tokens) is extremely efficient. Below are the exact price and time estimates across the two primary cloud configurations:

### Option A: Google Cloud Run (Jobs with GPU)
* **Configuration**: 1x NVIDIA L4 (24GB VRAM) + 4 vCPU + 16 GB RAM
* **Throughput**: ~2,800 - 3,200 tokens/sec
* **Estimated Training Time**: **~45 to 55 minutes**
* **Hourly Rate**: ~$0.70/hr (L4 GPU) + ~$0.15/hr (vCPU/RAM) = **~$0.85/hr**
* **Total Run Cost**: **~$0.65 – $0.80 USD**

### Option B: RunPod (GPU Pods)
* **Configuration 1 (RTX 4090 - 24GB VRAM)**:
  * **Hourly Rate**: ~$0.34 to $0.44/hr
  * **Training Time**: **~35 to 45 minutes**
  * **Total Run Cost**: **~$0.25 – $0.35 USD**
* **Configuration 2 (NVIDIA A100 - 80GB VRAM)**:
  * **Hourly Rate**: ~$1.64 to $1.89/hr
  * **Training Time**: **~15 to 20 minutes**
  * **Total Run Cost**: **~$0.45 – $0.65 USD**

> **Summary**: Regardless of which cloud platform you choose, the entire fine-tuning run will finish in **under 1 hour** and cost **less than $1.00 USD**.

---

## 2. Directory Structure

```text
deep_domain_pipeline/
├── data/
│   ├── train.jsonl             # 10,800 training pairs (4.0 MB)
│   └── valid.jsonl             # 1,200 validation pairs (463 KB)
├── generate_dataset.py         # Synthetic generation script for 12,000 samples
├── train.py                    # PyTorch + PEFT/LoRA + TRL training script
├── Dockerfile                  # Container image definition for Cloud Run / RunPod
├── requirements.txt            # Python dependencies (torch, transformers, peft, trl)
├── deploy_cloud_run.sh         # Google Cloud Run deployment script
└── README.md                   # Documentation & cost analysis
```

---

## 3. How to Run on Google Cloud Run (Jobs)

When you are ready to provide GCP credentials:

```bash
# 1. Authenticate with your Google Cloud account
gcloud auth login
gcloud config set project <YOUR_GCP_PROJECT_ID>

# 2. Enable Cloud Run and Container Registry APIs
gcloud services enable run.googleapis.com containerregistry.googleapis.com

# 3. Deploy and execute the training job
cd /Users/harshchavan/Documents/GitHub/AI_Experiment/deep_domain_pipeline
chmod +x deploy_cloud_run.sh
./deploy_cloud_run.sh
```

---

## 4. How to Run on RunPod (Web UI or CLI)

1. Go to [RunPod.io](https://runpod.io) and deploy a **1x RTX 4090 (24GB)** pod with the standard `PyTorch 2.2` template.
2. In the Web Terminal or SSH:
   ```bash
   git clone <YOUR_REPO>
   cd AI_Experiment/deep_domain_pipeline
   pip install -r requirements.txt
   python3 train.py
   ```
3. Once completed, your trained LoRA adapter will be saved in `./output/final_lora_adapters`.

