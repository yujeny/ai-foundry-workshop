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

3. **Configure environment**:
   ```bash
   cp .env.local .env
   ```
   Update `.env` with your Azure AI Foundry values:
   - `PROJECT_CONNECTION_STRING`: Your project connection string from Azure ML workspace
   - `MODEL_DEPLOYMENT_NAME`: Your model deployment name
   - `EMBEDDING_MODEL_DEPLOYMENT_NAME`: Your embedding model deployment name
   - `TENANT_ID`: Your tenant ID from Azure portal
   - `BING_CONNECTION_NAME`: Your Bing search connection name
   - `SERVERLESS_MODEL_NAME`: Your serverless model name

   > **Note**: The model specified in `MODEL_DEPLOYMENT_NAME` must be supported by Azure AI Agents Service or Assistants API. See [supported models](https://learn.microsoft.com/en-us/azure/ai-services/agents/concepts/model-region-support?tabs=python#azure-openai-models) for details.

4. **Install dependencies**:
   ```bash
   # Install core Azure AI SDKs
   pip install azure-identity azure-ai-projects azure-ai-inference azure-ai-evaluation azure-ai-contentsafety azure-monitor-opentelemetry

   # Install additional requirements
   pip install -r requirements.txt
   ```

5. **Start Jupyter**:
   ```bash
   jupyter notebook
   ```

6. **Follow the Learning Path**:
    1. **Introduction** (`docs/1-introduction/`)
       - `1-authentication.ipynb`: Set up your Azure credentials
       - `2-environment_setup.ipynb`: Configure your environment
       - `3-quick_start.ipynb`: Learn basic operations

    2. **Main Workshop** (`docs/2-notebooks/`)
       - Chat Completion & RAG (`1-chat_completion/`)
       - Agent Development (`2-agent_service/`)
       - Quality Attributes (`3-quality_attributes/`)

---

## 📦 Prerequisites

- Python 3.10+
- Azure subscription with access to Azure AI Foundry
- Deployment of a model and AI Search connection configured in Azure AI Foundry
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

### 1. Introduction (`docs/1-introduction/`)
- Azure authentication and setup
- Environment configuration
- Quick start with AI Foundry
- Core concepts and SDKs

### 2. Chat Completion & RAG (`docs/2-notebooks/1-chat_completion/`)
- Basic chat completion
- Embeddings and vector search
- RAG for health knowledge
- Advanced models (Phi-4)

### 3. Agent Development (`docs/2-notebooks/2-agent_service/`)
- Health Advisor Agent basics
- Code interpreter for health metrics
- File search capabilities
- Bing grounding for medical info
- AI Search integration
- Azure Functions deployment

### 4. Quality Attributes (`docs/2-notebooks/3-quality_attributes/`)
- Observability setup
- Performance monitoring
- Agent evaluation
- Health advice safety checks

---

## 🧩 Project Structure

```
azure-ai-foundry-workshop/
├── docs/
│   ├── 1-introduction/
│   │   ├── 1-authentication.ipynb
│   │   ├── 2-environment_setup.ipynb
│   │   └── 3-quick_start.ipynb
│   ├── 2-notebooks/
│   │   ├── 1-chat_completion/
│   │   │   ├── 1-basic-chat-completion.ipynb
│   │   │   ├── 2-embeddings.ipynb
│   │   │   ├── 3-basic-rag.ipynb
│   │   │   └── 4-phi-4.ipynb
│   │   ├── 2-agent_service/
│   │   │   ├── 1-basics.ipynb
│   │   │   ├── 2-code_interpreter.ipynb
│   │   │   ├── 3-file-search.ipynb
│   │   │   ├── 4-bing_grounding.ipynb
│   │   │   ├── 5-agents-aisearch.ipynb
│   │   │   └── 6-agents-az-functions.ipynb
│   │   └── 3-quality_attributes/
│   │       ├── 1-Observability.ipynb
│   │       └── 2-evaluation.ipynb
│   ├── agents/
│   ├── evaluation/
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
