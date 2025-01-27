# Azure AI Foundry Workshop

<div align="center">

[📦Prerequisites](#-prerequisites) | [🚀Quick Start](#-quick-start) | [🤖Overview](#-overview) | [📔Workshop Content](#-workshop-content) | [🧩Project Structure](#-project-structure) | [❓Support](#-support) | [🤝Contributing](#-contributing)

</div>

---

## 📦 Prerequisites

Before starting the workshop, ensure you have:

- Python 3.10 or higher installed
- An active Azure subscription with access to Azure AI Foundry
- Azure CLI installed
- Git installed
- VS Code, GitHub Codespaces, or Jupyter Notebook environment
- Basic Python programming knowledge
- Model deployment and AI Search connection configured in Azure AI Foundry

---

## 🤖 Overview

A hands-on workshop that guides you through building intelligent apps and AI agents on top of Azure AI Foundry, with fun examples related to health and dietary advice. You will:
- Learn Azure AI Foundry fundamentals
- Set up authentication and project configuration
- Deploy and test AI models
- Build AI agents (health advisor examples)
- Implement health calculations and dietary planning
- Evaluate agent performance with safety checks

> **Duration**: 2-4 hours  
> **Focus**: Hands-on exercises, interactive notebooks, practical examples, end-to-end project

---

## 🚀 Quick Start

1. **Clone the repo**:
   ```bash
   git clone https://github.com/Azure/azure-ai-foundry-workshop.git
   cd azure-ai-foundry-workshop
   ```

2. **Install uv**:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Create & activate a virtual environment**:
   ```bash
   uv venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

4. **Set up Azure AI Foundry**:

   a. **Create Project and Deploy Resources**:
      1. Go to [Azure AI Foundry](https://ai.azure.com)
      2. Create a new AI Hub and Project using the AI Foundry Wizard
      3. Deploy required models:
         - GPT models(gpt-4o, gpt-4o-mini) for chat/completion (**set TPM to max** to avoid issues with Agents notebooks)
         - Embedding model for vector search
      4. Set up connections:
         - Configure Bing Search connection
         - Configure Azure AI Search connection
      5. Add your user account to the `Azure AI Developer` role from Azure AI Foundry Management Portal

   b. **Configure Environment Variables**:
      ```bash
      cp .env.example .env
      ```
      Update `.env` with your Azure AI Foundry values:
      - `PROJECT_CONNECTION_STRING`: Your project connection string from Azure ML workspace
      - `MODEL_DEPLOYMENT_NAME`: Your model deployment name
      - `EMBEDDING_MODEL_DEPLOYMENT_NAME`: Your embedding model deployment name
      - `TENANT_ID`: Your tenant ID from Azure portal
      - `BING_CONNECTION_NAME`: Your Bing search connection name
      - `SERVERLESS_MODEL_NAME`: Your serverless model name

      > **Note**: The model specified in `MODEL_DEPLOYMENT_NAME` must be supported by Azure AI Agents Service or Assistants API. See [supported models](https://learn.microsoft.com/en-us/azure/ai-services/agents/concepts/model-region-support?tabs=python#azure-openai-models) for details. For Grounding with Bing Search, you need to use `gpt-4o-mini` model.

5. **Install dependencies**:
   ```bash
   # Install core Azure AI SDKs
   uv pip install azure-identity azure-ai-projects azure-ai-inference azure-ai-evaluation azure-ai-contentsafety azure-monitor-opentelemetry

   # Install additional requirements
   uv pip install -r requirements.txt
   ```

6. **Start Jupyter**:
   ```bash
   jupyter notebook
   ```

7. **Follow the Learning Path**:
    1. **Introduction** (`1-introduction/`)
       - `1-authentication.ipynb`: Set up your Azure credentials
       - `2-environment_setup.ipynb`: Configure your environment
       - `3-quick_start.ipynb`: Learn basic operations

    2. **Main Workshop** (`2-notebooks/`)
       - Chat Completion & RAG (`1-chat_completion/`)
       - Agent Development (`2-agent_service/`)
       - Quality Attributes (`3-quality_attributes/`)

---

## 📔 Workshop Learning Path

Follow these notebooks in sequence to complete the workshop:

### 1. Introduction (`1-introduction/`)
| Notebook | Description |
|----------|-------------|
| [1. Authentication](1-introduction/1-authentication.ipynb) | Set up Azure credentials and access |
| [2. Environment Setup](1-introduction/2-environment_setup.ipynb) | Configure your development environment |
| [3. Quick Start](1-introduction/3-quick_start.ipynb) | Learn basic Azure AI Foundry operations |

### 2. Main Workshop (`2-notebooks/`)
| Topic | Notebooks |
|-------|-----------|
| **Chat Completion & RAG** | • [Chat Completion & RaG](2-notebooks/1-chat_completion/) |
| **Agent Development** | • [Agent Development](2-notebooks/2-agent_service/) |
| **Quality Attributes** | • [Observability & Evaluations](2-notebooks/3-quality_attributes/) |

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on how to:
- Submit bug reports and feature requests
- Submit pull requests
- Follow our coding standards
- Participate in code reviews

---

## ❓ Support

If you need help or have questions:
- Open an issue in this repository
- Contact Azure support
- Visit [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry)

---

<div align="center">
© 2024 Microsoft Corporation. All rights reserved.
</div>



