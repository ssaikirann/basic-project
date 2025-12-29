#!/bin/bash

# Docker build, test, and push script

set -e

echo "=== Docker Build, Test, and Push ==="
echo ""

# Configuration
DOCKER_REGISTRY=${DOCKER_REGISTRY:-"ghcr.io"}
DOCKER_USERNAME=${DOCKER_USERNAME:-"ssaikirann"}
DOCKER_IMAGE_NAME="finance-tracker"
DOCKER_IMAGE_TAG=${DOCKER_IMAGE_TAG:-"latest"}
FULL_IMAGE_NAME="${DOCKER_REGISTRY}/${DOCKER_USERNAME}/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"

echo "Building Docker image: $FULL_IMAGE_NAME"
echo ""

# Build Docker image
echo "1. Building Docker image..."
docker build -t "$FULL_IMAGE_NAME" -t "${DOCKER_REGISTRY}/${DOCKER_USERNAME}/${DOCKER_IMAGE_NAME}:latest" .
echo "✓ Docker image built successfully"
echo ""

# Test Docker image
echo "2. Testing Docker image..."
echo "  - Checking image size..."
docker images | grep "$DOCKER_IMAGE_NAME"
echo ""

echo "  - Running container test..."
docker run --rm "$FULL_IMAGE_NAME" python -c "import finance_tracker; print('✓ Finance Tracker imported successfully')"
echo "✓ Docker image test passed"
echo ""

# Display image info
echo "3. Docker image information:"
docker inspect "$FULL_IMAGE_NAME" | python -m json.tool | head -50
echo ""

echo "=== Docker build and test completed successfully ==="
echo "Image: $FULL_IMAGE_NAME"
