"""
Production Cloud GPU Training Script for Qwen 3.5 2B Fine-Tuning.
Optimized for NVIDIA L4 (Google Cloud Run) or NVIDIA RTX 4090 / A100 (RunPod).
"""

import os
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer, SFTConfig

def main():
    model_id = os.environ.get("MODEL_ID", "Qwen/Qwen2.5-3B-Instruct") # or target Qwen 2B/3B repo
    data_dir = os.environ.get("DATA_DIR", "./data")
    output_dir = os.environ.get("OUTPUT_DIR", "./output")
    
    print(f"=== Starting Fine-Tuning on {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'} ===")
    print(f"Base Model: {model_id}")
    print(f"Data Dir: {data_dir}")

    # 1. Load Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # 2. 4-bit Quantization (QLoRA) for maximum memory efficiency & speed
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True
    )

    # 3. Load Model
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True
    )
    model = prepare_model_for_kbit_training(model)

    # 4. LoRA Configuration targeting Attention + MLP FeedForward layers
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj"
        ],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # 5. Load Dataset
    dataset = load_dataset("json", data_files={
        "train": os.path.join(data_dir, "train.jsonl"),
        "validation": os.path.join(data_dir, "valid.jsonl")
    })

    def format_chat(sample):
        # Format into standard chat template string
        text = tokenizer.apply_chat_template(sample["messages"], tokenize=False)
        return {"text": text}

    dataset = dataset.map(format_chat)

    # 6. Training Arguments
    training_args = SFTConfig(
        output_dir=output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        lr_scheduler_type="cosine",
        warmup_ratio=0.03,
        logging_steps=25,
        eval_strategy="steps",
        eval_steps=100,
        save_strategy="steps",
        save_steps=200,
        save_total_limit=2,
        bf16=True,
        max_seq_length=512,
        dataset_text_field="text",
        report_to="none"
    )

    # 7. Trainer
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset["train"],
        eval_dataset=dataset["validation"],
        peft_config=lora_config,
        args=training_args,
        tokenizer=tokenizer
    )

    print("\n--- Starting Training Run ---")
    trainer.train()

    # 8. Save Final Adapters
    final_adapter_path = os.path.join(output_dir, "final_lora_adapters")
    trainer.model.save_pretrained(final_adapter_path)
    tokenizer.save_pretrained(final_adapter_path)
    print(f"\nTraining Complete! Adapter saved to: {final_adapter_path}")

if __name__ == "__main__":
    main()

