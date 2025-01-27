# Azure AI Foundry Workshop

<div align="center">

[🤖Overview](#-overview) | [🚀Quick Start](#-quick-start) | [📦Prerequisites](#-prerequisites) | [⚙️Local Setup](#️-local-setup) | [📔Workshop Content](#-workshop-content) | [🧩Project Structure](#-project-structure) | [❓Support](#-support) | [🤝Contributing](#-contributing)

</div>

---

## 🤖 Overview

A hands-on workshop that guides you through building intelligent AI agents using Azure AI Foundry's SDK, with fun examples related to health and dietary advice. You will:
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
