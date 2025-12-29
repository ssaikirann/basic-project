#!/bin/bash

# Terraform validation and testing script

set -e

echo "=== Terraform Validation and Testing ==="
echo ""

# Initialize Terraform
echo "1. Initializing Terraform..."
cd terraform || exit 1
terraform init -upgrade
echo "✓ Terraform initialized"
echo ""

# Validate Terraform configuration
echo "2. Validating Terraform configuration..."
terraform validate
echo "✓ Terraform configuration is valid"
echo ""

# Format check
echo "3. Checking Terraform formatting..."
terraform fmt -check -recursive . || terraform fmt -recursive .
echo "✓ Terraform formatting checked"
echo ""

# Plan the deployment
echo "4. Creating Terraform plan..."
terraform plan -out=tfplan
echo "✓ Terraform plan created"
echo ""

# Display the plan
echo "5. Terraform plan details:"
terraform show tfplan
echo ""

echo "=== Terraform validation completed successfully ==="
