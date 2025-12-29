#!/bin/bash

# Infrastructure tests - validate all infrastructure files

set -e

echo "=== Infrastructure Tests ==="
echo ""

TESTS_PASSED=0
TESTS_FAILED=0

# Test 1: Validate Dockerfile
echo "Test 1: Validating Dockerfile..."
if [ -f "Dockerfile" ]; then
    echo "  ✓ Dockerfile exists"
    ((TESTS_PASSED++))
else
    echo "  ✗ Dockerfile not found"
    ((TESTS_FAILED++))
fi
echo ""

# Test 2: Validate docker-compose.yml
echo "Test 2: Validating docker-compose.yml..."
if [ -f "docker-compose.yml" ]; then
    if command -v docker-compose &> /dev/null; then
        docker-compose config > /dev/null && echo "  ✓ docker-compose.yml is valid" && ((TESTS_PASSED++)) || { echo "  ✗ docker-compose.yml validation failed"; ((TESTS_FAILED++)); }
    else
        echo "  ⚠ docker-compose not installed, skipping validation"
    fi
else
    echo "  ✗ docker-compose.yml not found"
    ((TESTS_FAILED++))
fi
echo ""

# Test 3: Validate Terraform files
echo "Test 3: Validating Terraform files..."
if [ -d "terraform" ]; then
    if command -v terraform &> /dev/null; then
        cd terraform
        terraform init -upgrade > /dev/null 2>&1
        terraform validate > /dev/null && echo "  ✓ Terraform configuration is valid" && ((TESTS_PASSED++)) || { echo "  ✗ Terraform validation failed"; ((TESTS_FAILED++)); }
        cd ..
    else
        echo "  ⚠ Terraform not installed, skipping validation"
    fi
else
    echo "  ✗ Terraform directory not found"
    ((TESTS_FAILED++))
fi
echo ""

# Test 4: Validate Kubernetes manifests structure
echo "Test 4: Validating Kubernetes manifest structure..."
if [ -d "k8s-config" ] || [ -d "terraform/templates" ]; then
    echo "  ✓ Kubernetes configuration directory exists"
    ((TESTS_PASSED++))
else
    echo "  ✗ Kubernetes configuration directory not found"
    ((TESTS_FAILED++))
fi
echo ""

# Test 5: Check for required scripts
echo "Test 5: Checking for required scripts..."
REQUIRED_SCRIPTS=("scripts/docker_build.sh" "scripts/terraform_validate.sh" "scripts/k8s_deploy_test.sh" "scripts/ubuntu_checks.sh")
for script in "${REQUIRED_SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        echo "  ✓ $script exists"
        ((TESTS_PASSED++))
    else
        echo "  ✗ $script not found"
        ((TESTS_FAILED++))
    fi
done
echo ""

# Summary
echo "=== Test Summary ==="
echo "Tests Passed: $TESTS_PASSED"
echo "Tests Failed: $TESTS_FAILED"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo "✓ All infrastructure tests passed!"
    exit 0
else
    echo "✗ Some infrastructure tests failed"
    exit 1
fi
