#!/usr/bin/env bash
set -e

# ==============================================================================
# Google Cloud Run (Jobs with GPU) Deployment Script
# ==============================================================================
# Prerequisites:
# 1. gcloud CLI installed and authenticated (`gcloud auth login`)
# 2. Project ID set: `gcloud config set project <YOUR_PROJECT_ID>`
# 3. Artifact Registry repository created for Docker images.
# ==============================================================================

PROJECT_ID=$(gcloud config get-value project 2>/dev/null || echo "your-project-id")
REGION="us-central1"
IMAGE_NAME="gcr.io/${PROJECT_ID}/qwen-finetune:latest"
JOB_NAME="qwen-12k-finetune-job"

echo "=== 1. Building Container Image ==="
docker build -t ${IMAGE_NAME} .

echo "=== 2. Pushing Container Image to Google Container Registry ==="
docker push ${IMAGE_NAME}

echo "=== 3. Creating / Updating Cloud Run Job with NVIDIA L4 GPU ==="
# Cloud Run Jobs with GPU requires:
# --gpu 1 (Nvidia L4)
# --gpu-type nvidia-l4
# --cpu 4 / --memory 16Gi
gcloud beta run jobs create ${JOB_NAME} \
    --image=${IMAGE_NAME} \
    --region=${REGION} \
    --gpu=1 \
    --gpu-type=nvidia-l4 \
    --cpu=4 \
    --memory=16Gi \
    --max-retries=0 \
    --task-timeout=7200s \
    || gcloud beta run jobs update ${JOB_NAME} \
    --image=${IMAGE_NAME} \
    --region=${REGION} \
    --gpu=1 \
    --gpu-type=nvidia-l4 \
    --cpu=4 \
    --memory=16Gi \
    --task-timeout=7200s

echo "=== 4. Executing Cloud Run Training Job ==="
gcloud beta run jobs execute ${JOB_NAME} --region=${REGION} --wait

echo "=== Cloud Run Training Job Completed! ==="

