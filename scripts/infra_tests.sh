#!/bin/bash

# Infrastructure tests - validate all infrastructure files

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
        if docker-compose config > /dev/null 2>&1; then
            echo "  ✓ docker-compose.yml is valid"
            ((TESTS_PASSED++))
        else
            echo "  ✗ docker-compose.yml validation failed"
            ((TESTS_FAILED++))
        fi
    else
        echo "  ⚠ docker-compose not installed, checking syntax manually"
        if grep -q "version:" docker-compose.yml && grep -q "services:" docker-compose.yml; then
            echo "  ✓ docker-compose.yml has required fields"
            ((TESTS_PASSED++))
        else
            echo "  ✗ docker-compose.yml missing required fields"
            ((TESTS_FAILED++))
        fi
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
        cd terraform || exit 1
        if terraform init -upgrade > /dev/null 2>&1; then
            if terraform validate > /dev/null 2>&1; then
                echo "  ✓ Terraform configuration is valid"
                ((TESTS_PASSED++))
            else
                echo "  ✗ Terraform validation failed"
                ((TESTS_FAILED++))
            fi
        else
            echo "  ✗ Terraform init failed"
            ((TESTS_FAILED++))
        fi
        cd .. || exit 1
    else
        echo "  ⚠ Terraform not installed, checking file structure"
        if [ -f "terraform/main.tf" ]; then
            echo "  ✓ Terraform files exist"
            ((TESTS_PASSED++))
        else
            echo "  ✗ Terraform files not found"
            ((TESTS_FAILED++))
        fi
    fi
else
    echo "  ✗ Terraform directory not found"
    ((TESTS_FAILED++))
fi
echo ""

# Test 4: Validate Kubernetes manifests structure
echo "Test 4: Validating Kubernetes manifest structure..."
if [ -d "terraform/templates" ]; then
    TEMPLATE_COUNT=$(find terraform/templates -name "*.tpl" | wc -l)
    if [ "$TEMPLATE_COUNT" -gt 0 ]; then
        echo "  ✓ Kubernetes templates found ($TEMPLATE_COUNT files)"
        ((TESTS_PASSED++))
    else
        echo "  ✗ No Kubernetes templates found"
        ((TESTS_FAILED++))
    fi
elif [ -d "k8s-config" ]; then
    YAML_COUNT=$(find k8s-config -name "*.yaml" | wc -l)
    if [ "$YAML_COUNT" -gt 0 ]; then
        echo "  ✓ Kubernetes manifests found ($YAML_COUNT files)"
        ((TESTS_PASSED++))
    else
        echo "  ✗ No Kubernetes manifests found"
        ((TESTS_FAILED++))
    fi
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
        if [ -x "$script" ]; then
            echo "  ✓ $script exists and is executable"
            ((TESTS_PASSED++))
        else
            echo "  ⚠ $script exists but not executable"
            chmod +x "$script"
            ((TESTS_PASSED++))
        fi
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
