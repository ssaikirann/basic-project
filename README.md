# Finance Tracker Application

A full-stack financial management system with CI/CD pipeline, containerization, and Kubernetes orchestration.

## 📋 Overview

This project demonstrates a complete modern DevOps and application development workflow with:

- **Application**: Python Flask web dashboard for finance tracking
- **Testing**: Comprehensive pytest test suite with coverage
- **CI/CD**: GitHub Actions with 8 automated stages
- **Containerization**: Docker with Docker Compose
- **Infrastructure**: Terraform for Kubernetes manifests
- **Orchestration**: Minikube Kubernetes deployment

## 🎯 Features

**Application Features**
- 💰 Expense tracking by category
- 📈 Investment portfolio management
- 📊 Interactive dashboard with charts
- 📱 Responsive web interface
- 💾 JSON-based data persistence

**DevOps Features**
- ✅ Automated testing with pytest
- 🔍 Code quality checks (Flake8, Pylint)
- 🐳 Docker containerization
- ☸️ Kubernetes (Minikube) deployment
- 🏗️ Infrastructure as Code (Terraform)
- 🔄 Full CI/CD automation

## 🚀 Quick Start

**Local Development:**
```bash
pip install -r requirements.txt
python app.py
```

**Docker:**
```bash
docker-compose up --build
```

**Kubernetes:**
```bash
cd terraform && terraform init && terraform apply
bash scripts/k8s_deploy_test.sh
```

## 🧪 Testing

```bash
pytest test_finance_tracker.py -v --cov=finance_tracker
bash scripts/infra_tests.sh
```

## 📊 8-Stage CI/CD Pipeline

1. System Checks - Ubuntu diagnostics
2. Build - Python environment setup
3. Test - pytest with coverage
4. Code Quality - Flake8 & Pylint
5. Infrastructure Tests - Validation
6. Docker Build - Build and push image
7. Kubernetes Deploy - Deploy to Minikube
8. Deployment Prep - Artifacts creation

## 📈 Technology Stack

Frontend: HTML5, CSS3, JavaScript, Chart.js
Backend: Python 3.10, Flask
Database: JSON files
Testing: pytest, pytest-cov
CI/CD: GitHub Actions
Container: Docker, Kubernetes
Infrastructure: Terraform

See [DASHBOARD.md](DASHBOARD.md) for detailed documentation.

## 📝 License

MIT License
