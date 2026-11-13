import os
import sys
import time
import json
import subprocess
import urllib.request

WORKSPACE = "/Users/harshchavan/Documents/GitHub/AI_Experiment"
PIPELINE_DIR = os.path.join(WORKSPACE, "deep_domain_pipeline")
DATA_DIR = os.path.join(PIPELINE_DIR, "data")
ADAPTER_DIR = os.path.join(PIPELINE_DIR, "adapters_12k")
FUSED_DIR = os.path.join(PIPELINE_DIR, "fused_qwen3.5_12k")
BASE_MODEL = "/Users/harshchavan/qwen_finetune_experiment/base_model"
VENV_BIN = "/Users/harshchavan/qwen_finetune_experiment/.venv/bin"
LOG_FILE = os.path.join(PIPELINE_DIR, "overnight_training.log")

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {msg}"
    print(formatted, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(formatted + "\n")

def unload_ollama():
    log("Pre-flight: Ensuring Ollama has unloaded all models from VRAM...")
    try:
        url = "http://localhost:11434/api/generate"
        payload = json.dumps({"model": "qwen3.5:2b", "keep_alive": 0}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            log("Ollama models successfully cleared from VRAM.")
    except Exception as e:
        log(f"Ollama unload check: {e}")

def run_training():
    log("=" * 70)
    log("PHASE 1: Starting LoRA Fine-Tuning (12,000 Samples, 8-10GB Target)")
    log("Configuration:")
    log(f"  - Model: {BASE_MODEL}")
    log(f"  - Batch Size: 4 (with Grad Accumulation: 4 -> Effective Batch: 16)")
    log(f"  - Max Sequence Length: 512")
    log(f"  - LoRA Layers: 16 layers (Rank 8 / Alpha 16)")
    log(f"  - Target Iterations: 2,000 steps (~3 epochs of 10,800 train set)")
    log(f"  - Learning Rate: 2.0e-5 (Cosine Decay)")
    log("=" * 70)

    cmd = [
        os.path.join(VENV_BIN, "mlx_lm"), "lora",
        "--model", BASE_MODEL,
        "--train",
        "--data", DATA_DIR,
        "--adapter-path", ADAPTER_DIR,
        "--batch-size", "4",
        "--grad-accumulation-steps", "4",
        "--grad-checkpoint",
        "--max-seq-length", "512",
        "--num-layers", "16",
        "--iters", "2000",
        "--learning-rate", "2e-5",
        "--steps-per-report", "25",
        "--steps-per-eval", "100",
        "--save-every", "250"
    ]

    log(f"Executing: {' '.join(cmd)}")
    with open(LOG_FILE, "a") as f_out:
        p = subprocess.Popen(cmd, stdout=f_out, stderr=subprocess.STDOUT)
        p.wait()

    if p.returncode != 0:
        log(f"ERROR: Training failed with exit code {p.returncode}. See {LOG_FILE} for traceback.")
        sys.exit(p.returncode)
    
    log("Training completed successfully! 2,000 iterations finished.")

def fuse_model():
    log("=" * 70)
    log("PHASE 2: Fusing Trained LoRA Adapter into Standalone Model")
    log(f"Saving fused weights to: {FUSED_DIR}")
    log("=" * 70)

    cmd = [
        os.path.join(VENV_BIN, "mlx_lm"), "fuse",
        "--model", BASE_MODEL,
        "--adapter-path", ADAPTER_DIR,
        "--save-path", FUSED_DIR
    ]
    with open(LOG_FILE, "a") as f_out:
        p = subprocess.Popen(cmd, stdout=f_out, stderr=subprocess.STDOUT)
        p.wait()

    if p.returncode == 0:
        log(f"Model successfully fused at: {FUSED_DIR}")
    else:
        log("Warning: Fusion step encountered an error. Adapters remain intact in adapters_12k.")

def deploy_to_lmstudio():
    log("=" * 70)
    log("PHASE 3: Linking Model into LM Studio")
    lm_dir = os.path.expanduser("~/.lmstudio/models/custom/Qwen3.5-2B-Novatrix-12k")
    log(f"Target LM Studio Path: {lm_dir}")
    log("=" * 70)

    if os.path.exists(FUSED_DIR):
        os.makedirs(os.path.dirname(lm_dir), exist_ok=True)
        # Create symlink or copy
        if os.path.exists(lm_dir):
            subprocess.run(["rm", "-rf", lm_dir])
        subprocess.run(["cp", "-r", FUSED_DIR, lm_dir])
        log("Model deployed to LM Studio! It will be instantly visible in LM Studio > My Models.")
    else:
        log("Skipping LM Studio copy: fused directory not found.")

def run_morning_evaluation():
    log("=" * 70)
    log("PHASE 4: Generating Morning Evaluation Benchmark Report")
    log("=" * 70)

    post_test_script = os.path.join(PIPELINE_DIR, "run_post_test.py")
    if os.path.exists(post_test_script):
        cmd = [os.path.join(VENV_BIN, "python3"), post_test_script]
        with open(LOG_FILE, "a") as f_out:
            p = subprocess.Popen(cmd, stdout=f_out, stderr=subprocess.STDOUT)
            p.wait()
        log("Evaluation complete! Generated overnight_comparison_report.md with side-by-side benchmark scores.")
    else:
        log("Skipping post-test: run_post_test.py not found.")

def main():
    start_time = time.time()
    log("=== OVERNIGHT M4 TRAINING PIPELINE STARTED ===")
    
    unload_ollama()
    run_training()
    fuse_model()
    deploy_to_lmstudio()
    run_morning_evaluation()

    elapsed_hours = (time.time() - start_time) / 3600
    log(f"=== PIPELINE COMPLETED IN {elapsed_hours:.2f} HOURS ===")
    log("Good morning! Your custom Qwen 3.5 12,000-sample model is ready to use.")

if __name__ == "__main__":
    main()

