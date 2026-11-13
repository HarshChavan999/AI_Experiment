import os
import sys
import json
import time
from mlx_lm import load, generate

PIPELINE_DIR = "/Users/harshchavan/Documents/GitHub/AI_Experiment/deep_domain_pipeline"
VALID_PATH = os.path.join(PIPELINE_DIR, "data", "valid.jsonl")
BASE_MODEL_PATH = "/Users/harshchavan/qwen_finetune_experiment/base_model"
OUT_JSON = os.path.join(PIPELINE_DIR, "pre_test_benchmark.json")
OUT_MD = os.path.join(PIPELINE_DIR, "pre_test_results.md")

def clean_output(text):
    for token in ["<|im_end|>", "<|endoftext|>", "<|im_start|>"]:
        text = text.replace(token, "")
    return text.strip()

def load_validation_sample(count=60):
    samples = []
    with open(VALID_PATH, "r") as f:
        for line in f:
            if line.strip():
                item = json.loads(line)
                q = item["messages"][0]["content"]
                gt = item["messages"][1]["content"]
                samples.append({"question": q, "ground_truth": gt})
    
    # Evenly pick 'count' samples to cover all topics
    step = max(1, len(samples) // count)
    selected = samples[::step][:count]
    return selected

def main():
    print("=" * 70)
    print("PRE-TRAINING BENCHMARK EVALUATION (BEFORE FINE-TUNING)")
    print("=" * 70)

    samples = load_validation_sample(count=60)
    print(f"Selected {len(samples)} representative validation questions from valid.jsonl.")

    print(f"Loading Base Model in MLX on M4 GPU from: {BASE_MODEL_PATH}")
    model, tokenizer = load(BASE_MODEL_PATH)
    print("Model loaded successfully. Starting pre-test evaluation...\n")

    results = []
    t_start = time.time()

    for i, s in enumerate(samples, 1):
        q = s["question"]
        gt = s["ground_truth"]
        prompt = f"<|im_start|>user\n{q}\nProvide a concise, direct answer in 1-2 sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n</think>\n"
        
        t0 = time.time()
        raw = generate(model, tokenizer, prompt=prompt, max_tokens=85)
        elapsed = time.time() - t0
        ans = clean_output(raw)

        print(f"[{i:02d}/{len(samples)}] ({elapsed:.2f}s) Q: {q[:45]}...")
        print(f"     -> Pre-test Base Answer: {ans[:70]}...\n")

        results.append({
            "index": i,
            "question": q,
            "ground_truth": gt,
            "pre_training_answer": ans,
            "latency": elapsed
        })

    total_time = time.time() - t_start
    avg_lat = sum(r["latency"] for r in results) / len(results)

    # 1. Save benchmark JSON for post-training comparison
    with open(OUT_JSON, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved structured benchmark to: {OUT_JSON}")

    # 2. Save human-readable Markdown
    with open(OUT_MD, "w") as f:
        f.write("# Pre-Training Benchmark Evaluation (Before Fine-Tuning)\n\n")
        f.write(f"- **Model**: Pure `Qwen 3.5 2B` Base Weights (Zero fine-tuning)\n")
        f.write(f"- **Engine**: Apple MLX on M4 GPU\n")
        f.write(f"- **Evaluated Samples**: {len(results)} questions sampled from `data/valid.jsonl`\n")
        f.write(f"- **Average Latency**: {avg_lat:.2f}s per query\n")
        f.write(f"- **Total Benchmark Duration**: {total_time:.2f}s\n\n")
        f.write("---\n\n")

        for item in results:
            f.write(f"### Q{item['index']}: {item['question']}\n\n")
            f.write(f"| Source / Model | Response | Latency / Notes |\n")
            f.write(f"| :--- | :--- | :--- |\n")
            f.write(f"| **🎯 Ground Truth (Target)** | **{item['ground_truth']}** | Target specification from `valid.jsonl` |\n")
            f.write(f"| **❌ Pre-Training Base Model** | {item['pre_training_answer']} | {item['latency']:.2f}s (Untrained baseline) |\n\n")
            f.write("---\n\n")

    print(f"Saved human-readable report to: {OUT_MD}")
    print("=" * 70)
    print("PRE-TEST COMPLETED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    main()

