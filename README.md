<div align="center">

# Azure AI Foundry Workshop

[🤖Overview](#-overview) | [🚀Quick Start](#-quick-start) | [📦Prerequisites](#-prerequisites) | [⚙️Local Setup](#️-local-setup) | [📔Workshop Docs](#-workshop-documentation) | [🧩Project Structure](#-project-structure) | [❓Support](#-support) | [🤝Contributing](#-contributing)

</div>

---

## 🤖 Overview

A hands-on workshop that guides you through building an intelligent customer service agent using Azure AI Foundry’s SDK, Agents Service, and Evaluations. You will:
- Set up the Azure AI Foundry environment
- Deploy and test AI models
- Build a customer service AI agent
- Evaluate agent performance

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
   pip install -r requirements.txt
   ```

4. **Generate workshop notebooks**:
   ```bash
   # Bash (Linux/macOS)
   for script in notebooks/create_*.py; do
       python "$script"
   done

   python validate_notebooks.py
   ```

   ```powershell
   # PowerShell (Windows)
   Get-ChildItem notebooks/create_*.py | ForEach-Object {
       python $_
   }

   python validate_notebooks.py
   ```

5. **Start Jupyter**:
   ```bash
   jupyter notebook
   ```
   Open the generated notebooks in the `building_agent` directory, starting with `project_setup/project_setup.ipynb`.

---

## 📦 Prerequisites

- Python 3.10+
- Azure subscription with access to Azure AI Foundry
- Basic Python knowledge
- Azure CLI installed
- Git

Make sure you’ve installed and logged in to the Azure CLI:
```bash
# (Ubuntu)
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

az login
az account set --subscription <YOUR_SUBSCRIPTION_ID>
```

---

## ⚙️ Local Setup

In more detail:

1. **Create & activate a virtual environment**  
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate & validate notebooks**  
   ```bash
   for script in notebooks/create_*.py; do
       python "$script"
   done

   python validate_notebooks.py
   ```

4. **Run notebooks**  
   ```bash
   jupyter notebook
   ```
   - Navigate to `building_agent/`  
   - Start with `project_setup/project_setup.ipynb` and proceed in the recommended order

---

## 📔 Workshop Documentation

### Local Development

1. **Install docs dependencies** (if not already done):
   ```bash
   pip install -r requirements.txt
   ```
2. **Serve docs locally**:
   ```bash
   mkdocs serve
   ```
3. Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser to view the docs.

### Build for Deployment

1. **Build the docs**:
   ```bash
   mkdocs build
   ```
2. The compiled site is in the `site` directory, ready to be served.

---

## 🧩 Project Structure

<details>
  <summary><strong>azure-ai-foundry-workshop/</strong></summary>
  <pre>
azure-ai-foundry-workshop/
├── building_agent/
│   ├── README.md
│   ├── requirements.txt
│   └── your_agent_module.py
├── docs/
│   ├── agents/
│   │   ├── deploy-test.md
│   │   ├── design.md
│   │   ├── implementation.md
│   │   ├── intro.md
│   │   └── service.md
│   ├── assets/
│   │   └── overrides/
│   │       └── index.html
│   ├── evaluation/
│   │   ├── agent.md
│   │   ├── intro.md
│   │   ├── monitoring.md
│   │   └── setup.md
│   ├── introduction/
│   │   ├── ai-foundry.md
│   │   ├── ai-studio.md
│   │   ├── index.md
│   │   └── overview.md
│   ├── models/
│   │   ├── deploying.md
│   │   ├── listing.md
│   │   └── testing.md
│   ├── sdk/
│   │   ├── aiprojectclient.md
│   │   ├── authentication.md
│   │   └── installation.md
│   ├── conclusion.md
│   └── index.md
├── notebooks/
│   ├── create_agent_design_notebook.py
│   ├── create_agent_implementation_notebook.py
│   ├── create_agent_intro_notebook.py
│   ├── create_agent_service_notebook.py
│   ├── create_agent_testing_notebook.py
│   ├── create_aiprojectclient_notebook.py
│   ├── create_auth_notebook.py
│   ├── create_available_models_notebook.py
│   ├── create_conclusion_notebook.py
│   ├── create_environment_notebook.py
│   ├── create_evaluation_intro_notebook.py
│   ├── create_model_deployment_notebook.py
│   ├── create_model_testing_notebook.py
│   ├── create_monitoring_analysis_notebook.py
│   ├── create_performance_metrics_notebook.py
│   ├── create_project_setup_notebook.py
│   ├── create_quickstart_notebook.py
│   ├── create_test_notebook.py
│   └── validate_notebook.py
├── mkdocs.yml
├── README.md
├── requirements.txt
└── validate_notebooks.py
  </pre>
</details>

---

## ❓ Support

If you run into problems:
1. Verify prerequisites and environment variables
2. Check [Azure AI Foundry docs](https://learn.microsoft.com/azure/ai-foundry/)
3. Confirm you have the required Python packages installed
4. Search open issues or submit a new one in this repo

---

## 🤝 Contributing

Contributions and suggestions are welcome! Please submit a Pull Request for any improvements.

---

## Code of Conduct

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). See the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) for details.

---

## License

```
MIT License

Copyright (c) Microsoft
```

See the [LICENSE.txt](LICENSE.txt) file for more details.

### Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft trademarks or logos must follow [Microsoft’s Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks). Third-party trademarks or logos are subject to those third-parties’ policies.
