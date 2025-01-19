# Azure AI Foundry Workshop

<div align="center">

[🤖Overview](#-overview) | [🚀Quick Start](#-quick-start) | [📦Prerequisites](#-prerequisites) | [⚙️Local Setup](#️-local-setup) | [📔Workshop Content](#-workshop-content) | [🧩Project Structure](#-project-structure) | [❓Support](#-support) | [🤝Contributing](#-contributing)

</div>

---

## 🤖 Overview

A hands-on workshop that guides you through building intelligent AI agents using Azure AI Foundry's SDK, with examples ranging from customer service to health and dietary advice. You will:
- Learn Azure AI Foundry fundamentals
- Set up authentication and project configuration
- Deploy and test AI models
- Build AI agents (customer service and health advisor examples)
- Implement health calculations and dietary planning
- Evaluate agent performance with safety checks

> **Duration**: 2-4 hours  
> **Focus**: Hands-on exercises, interactive notebooks, practical examples

---

## 🚀 Quick Start

1. **Clone the repo**:
   ```bash
   git clone https://github.com/Azure/azure-ai-foundry-workshop.git
   cd azure-ai-foundry-workshop
   ```

2. **Create & activate a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   # Install core Azure AI SDKs
   pip install azure-identity azure-ai-projects azure-ai-inference azure-ai-evaluation azure-ai-contentsafety azure-monitor-opentelemetry

   # Install additional requirements
   pip install -r requirements.txt
   ```

4. **Start Jupyter**:
   ```bash
   jupyter notebook
   ```

5. **Follow the Learning Path**:
   1. **Introduction** (`introduction/`)
      - `0-authentication.ipynb`: Set up your Azure credentials
      - `1-project_setup.ipynb`: Configure your AI Foundry project
      - `2-quick_start.ipynb`: Learn basic operations

   2. **Main Workshop** (after completing introduction)
      - Building Agents
      - Model Deployment
      - Evaluation
      - Advanced Features

---

## 📦 Prerequisites

- Python 3.10+
- Azure subscription with access to Azure AI Foundry
- Basic Python knowledge
- Azure CLI
- Git

### Setting Up Azure CLI
```bash
# Install Azure CLI (Ubuntu)
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login and set subscription
az login
az account set --subscription <YOUR_SUBSCRIPTION_ID>
```

---

## ⚙️ Local Setup

1. **Verify Python Version**:
   ```bash
   python --version  # Should be 3.10 or higher
   ```

2. **Create & activate virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   - Copy `.env.example` to `.env`
   - Update with your Azure credentials

5. **Start Jupyter**:
   ```bash
   jupyter notebook
   ```

---

## 📔 Workshop Content

### 1. Introduction
- Authentication setup
- Project configuration
- Quick start guide
- Basic concepts

### 2. Building Agents
- Agent design principles
- Implementation strategies
  - Customer Service Agent
  - Health Advisor Agent
    - BMI calculations
    - Dietary planning
    - Nutritional guidance
- Testing and deployment
- Content safety checks
- Best practices

### 3. Model Deployment
- Available models
- Deployment options
- Configuration
- Performance tuning

### 4. Evaluation
- Metrics and monitoring
- Performance analysis
- Optimization techniques
- Continuous improvement

---

## 🧩 Project Structure

```
azure-ai-foundry-workshop/
├── 1-introduction/
│   ├── 1-authentication/
│   ├── 2-environment/
│   └── 3-quick_startup/
├── 2-notebooks/
│   ├── sdk_tutorials/
│   │   ├── sdk_projects_tutorial/
│   │   ├── sdk_inference_tutorial/
│   │   ├── sdk_evaluation_tutorial/
│   │   ├── sdk_contentsafety_tutorial/
│   │   ├── sdk_monitoring_tutorial/
│   │   └── sdk_identity_tutorial/
│   ├── agent_tutorials/
│   │   ├── agent_basics_tutorial/
│   │   ├── agent_code_interpreter_tutorial/
│   │   └── agent_file_search_tutorial/
│   ├── project_setup/
│   ├── model_management/
│   │   ├── available_models/
│   │   ├── model_deployment/
│   │   └── model_testing/
│   └── evaluation/
│       ├── monitoring_analysis/
│       └── performance_metrics/
├── 3-e2e-health-advisor/
│   ├── backend/
│   ├── deploy/
│   └── frontend/
├── docs/
│   ├── agents/
│   ├── evaluation/
│   ├── introduction/
│   ├── models/
│   └── sdk/
├── .env
├── .env.local
└── requirements.txt
```

---

## ❓ Support

If you encounter issues:

1. **Check Prerequisites**:
   - Verify Python version
   - Confirm Azure CLI installation
   - Check environment variables

2. **Common Solutions**:
   - Restart Jupyter kernel
   - Reactivate virtual environment
   - Clear notebook output and restart

3. **Get Help**:
   - Check [Azure AI Foundry docs](https://learn.microsoft.com/azure/ai-foundry/)
   - Search open issues
   - Submit a new issue

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add tests for new features
- Update documentation
- Keep examples simple and clear

---

## Code of Conduct

This project follows the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).

---

## License

```
MIT License
Copyright (c) Microsoft
```

See [LICENSE.txt](LICENSE.txt) for details.

### Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft trademarks or logos must follow [Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks).
