#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Load environment variables if .env exists
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Deployment script for Terraform AWS infrastructure
echo "🚀 Starting Terraform deployment..."
echo "📁 Working directory: $(pwd)"

# Step 1: Initialize Terraform
echo "📦 Initializing Terraform..."
terraform init

# Step 2: Format Terraform files
echo "🎨 Formatting Terraform files..."
terraform fmt

# Step 3: Validate configuration
echo "✅ Validating Terraform configuration..."
terraform validate

# Step 4: Plan the deployment
echo "📋 Planning Terraform deployment..."
terraform plan -out=tfplan

# Step 5: Apply the plan (uncomment to auto-approve)
echo "🏗️  Applying Terraform plan..."
terraform apply tfplan
