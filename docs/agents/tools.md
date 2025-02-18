# AI Agent Tools in Azure AI Foundry 🛠️ 【†L3】

## Available Tools

### 1. File Search Tool 【†L4】
The File Search tool enables agents to search through document repositories using [Azure AI Search](https://learn.microsoft.com/azure/search/search-what-is-azure-search)'s vector capabilities.

```python
from azure.ai.projects.models import FileSearchTool

# Create agent with file search
agent = project_client.agents.create(
    name="health-advisor",
    tools=[FileSearchTool(name="document-search")]
)
```

### 2. Code Interpreter Tool 【†L5】
The Code Interpreter tool allows agents to execute Python code for data analysis and calculations. Learn more about [agent tools](https://learn.microsoft.com/azure/ai-services/agents/concepts/tools).

```python
from azure.ai.projects.models import CodeInterpreterTool

# Create agent with code interpreter
agent = project_client.agents.create(
    name="health-calculator",
    tools=[CodeInterpreterTool(name="python-calculator")]
)
```

### 3. Bing Grounding Tool 【†L6】
Ground agent responses in real-time web data using [Bing Search](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/bing-grounding).

```python
from azure.ai.projects.models import BingGroundingTool

# Create agent with Bing grounding
agent = project_client.agents.create(
    name="health-researcher",
    tools=[BingGroundingTool(name="web-search")]
)
```

## Tool Combinations
Agents can use multiple tools together for enhanced capabilities:

```python
# Create multi-tool agent
agent = project_client.agents.create(
    name="health-advisor-pro",
    tools=[
        FileSearchTool(name="document-search"),
        CodeInterpreterTool(name="python-calculator"),
        BingGroundingTool(name="web-search")
    ]
)
```

For implementation examples, see:
- [Code Interpreter Example](../2-notebooks/2-agent_service/2-code_interpreter.ipynb)
- [File Search Example](../2-notebooks/2-agent_service/3-file-search.ipynb)
- [Bing Grounding Example](../2-notebooks/2-agent_service/4-bing_grounding.ipynb)
