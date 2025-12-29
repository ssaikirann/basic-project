#!/bin/bash

# Kubernetes deployment testing script

set -e

echo "=== Kubernetes Deployment Testing ==="
echo ""

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "kubectl not found. Installing minikube kubectl..."
    minikube kubectl -- version
    KUBECTL="minikube kubectl --"
else
    KUBECTL="kubectl"
fi

echo "1. Checking Kubernetes cluster status..."
$KUBECTL cluster-info
echo "✓ Kubernetes cluster is accessible"
echo ""

# Create test namespace
TEST_NS="finance-tracker-test"
echo "2. Creating test namespace: $TEST_NS"
$KUBECTL create namespace $TEST_NS --dry-run=client -o yaml | $KUBECTL apply -f -
echo "✓ Test namespace created"
echo ""

# Apply Kubernetes manifests
echo "3. Applying Kubernetes manifests..."
for manifest in k8s-config/*.yaml; do
    if [ -f "$manifest" ]; then
        echo "  Applying: $manifest"
        $KUBECTL apply -f "$manifest" --namespace=$TEST_NS
    fi
done
echo "✓ Kubernetes manifests applied"
echo ""

# Verify deployments
echo "4. Verifying deployments..."
$KUBECTL get deployments -n finance-tracker
echo ""

echo "5. Verifying services..."
$KUBECTL get services -n finance-tracker
echo ""

# Check pod status
echo "6. Checking pod status..."
$KUBECTL get pods -n finance-tracker -o wide
echo ""

# Wait for deployment to be ready
echo "7. Waiting for deployment to be ready..."
$KUBECTL rollout status deployment/finance-tracker -n finance-tracker --timeout=5m || true
echo ""

# Get deployment details
echo "8. Deployment details:"
$KUBECTL describe deployment finance-tracker -n finance-tracker || true
echo ""

echo "=== Kubernetes deployment testing completed ==="
