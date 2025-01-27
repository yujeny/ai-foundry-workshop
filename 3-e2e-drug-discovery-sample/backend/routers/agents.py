from fastapi import APIRouter, HTTPException, File, UploadFile
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict, Any
import logging
import os
import json
import uuid
import pandas as pd
import numpy as np
from clients import project_client, chat_client, tracer, ensure_clients
from azure.ai.projects.models import BingGroundingTool, FunctionTool, CodeInterpreterTool, FilePurpose, ToolSet
from azure.core.exceptions import ResourceNotFoundError

# Configure logging
logger = logging.getLogger(__name__)

def serialize_tool_config(toolset: ToolSet) -> tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Serialize tool configuration into JSON-compatible format.
    
    Args:
        toolset (ToolSet): The toolset containing tools to serialize
        
    Returns:
        tuple[List[Dict[str, Any]], Dict[str, Any]]: Serialized tools and resources
    """
    logger.info(f"Serializing tool configuration for {len(toolset._tools)} tools")
    
    # Initialize lists and dicts for serialization
    tools = []
    resources = {
        "functions": [],
        "file_ids": [],
        "connection_id": os.getenv("spn_4o_BING_API_KEY")
    }
    
    # Process each tool
    for tool in toolset._tools:
        if isinstance(tool, BingGroundingTool):
            tools.append({
                "type": "bing_search",
                "name": "bing_search",
                "settings": {
                    "connection_id": os.getenv("spn_4o_BING_API_KEY"),
                    "search_parameters": {
                        "count": 5,
                        "textDecorations": True,
                        "textFormat": "HTML"
                    }
                }
            })
        elif isinstance(tool, FunctionTool):
            # Get functions from the tool
            functions = []
            for func in tool._functions:
                if not callable(func):
                    continue
                
                func_name = getattr(func, '__name__', str(func))
                func_doc = getattr(func, '__doc__', '') or ''
                
                functions.append({
                    "name": func_name,
                    "description": func_doc,
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                })
                resources["functions"].append(func_name)
            
            tools.append({
                "type": "function",
                "name": "function",
                "settings": {
                    "functions": functions
                }
            })
        elif isinstance(tool, CodeInterpreterTool):
            # Create code interpreter tool with proper settings
            tool_config = {
                "type": "code_interpreter",
                "name": "code_interpreter",
                "settings": {
                    "allowed_modules": [
                        "numpy", "pandas", "scipy",
                        "matplotlib", "sklearn", "statsmodels"
                    ]
                }
            }
            
            # Add file IDs if present
            if hasattr(tool, '_file_ids') and tool._file_ids:
                resources["file_ids"].extend(tool._file_ids)
            elif hasattr(tool, 'file_ids') and tool.file_ids:
                resources["file_ids"].extend(tool.file_ids)
            
            tools.append(tool_config)
    
    # Add debug logging
    logger.debug("Tool definitions:")
    logger.debug(json.dumps(tools, indent=2))
    logger.debug("Tool resources:")
    logger.debug(json.dumps(resources, indent=2))
    
    return tools, resources

# Cache for agents to avoid recreation
agent_cache: Dict[str, object] = {}

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(tags=["agents"])

class MoleculeAnalysisRequest(BaseModel):
    """Request model for molecule analysis."""
    smiles: str
    target_proteins: List[str]
    therapeutic_area: str

def analyze_molecule_properties(smiles: str, target_proteins: List[str]) -> dict:
    """
    Analyze molecular properties and predict interactions with target proteins.
    
    Args:
        smiles (str): SMILES representation of the molecule
        target_proteins (List[str]): List of target protein identifiers
    
    Returns:
        dict: Analysis results including molecular properties and predicted interactions
    """
    # Mock analysis for demonstration
    return {
        "molecular_weight": 342.4,
        "logP": 2.1,
        "h_bond_donors": 2,
        "h_bond_acceptors": 5,
        "predicted_binding_affinities": {
            protein: np.random.uniform(0.1, 0.9) 
            for protein in target_proteins
        }
    }

class LiteratureSearchRequest(BaseModel):
    """Request model for literature search."""
    query: str
    max_results: Optional[int] = 5
    include_clinical_trials: Optional[bool] = True

@router.post("/literature-search", tags=["agents"], summary="Search scientific literature using Bing grounding")
async def literature_search(request: LiteratureSearchRequest):
    """
    ### 📚 Literature Search Agent
    
    Uses Azure AI Agent's Bing grounding capability to search and analyze scientific literature
    about drug candidates and therapeutic targets.
    
    #### Real-world Applications
    - **Research Acceleration**: Quickly find relevant papers about similar compounds
    - **Competitive Analysis**: Track developments in specific therapeutic areas
    - **Validation**: Ground hypotheses in peer-reviewed research
    - **Safety Monitoring**: Stay updated on adverse effects and contraindications
    
    #### Azure AI Agent Usage
    - **Tool**: BingGroundingTool for literature search
    - **Capability**: Grounds responses in peer-reviewed publications
    - **Analysis**: Provides context-aware scientific analysis
    - **Validation**: Ensures findings are based on reliable sources
    
    ```mermaid
    sequenceDiagram
        participant Client
        participant Agent
        participant Bing
        Client->>Agent: Search Query
        Agent->>Bing: Ground Query
        Bing-->>Agent: Search Results
        Agent-->>Client: Analyzed Results
    ```
    
    Args:
        query (str): Search query about drug candidates or therapeutic targets
        
    Returns:
        dict: {
            "query": str,
            "summary": str,
            "agent_id": str
        }
        
    Example:
        ```python
        response = await literature_search("EGFR inhibitors in lung cancer")
        ```
    """
    with tracer.start_as_current_span("literature_search") as span:
        try:
            span.set_attribute("operation", "literature_search")
            logger.info(f"🔍 Starting literature search for: {request.query}")

            # Get or create agent from cache
            agent_type = "literature-search"
            if agent_type not in agent_cache:
                # Create tools configuration
                toolset = ToolSet()
                bing_tool = BingGroundingTool(
                    connection_id=os.getenv("spn_4o_BING_API_KEY")
                )
                toolset.add(bing_tool)

                try:
                    # Create agent with preview features enabled
                    agent = await project_client.agents.create_agent(
                        model=os.getenv('MODEL_DEPLOYMENT_NAME', os.getenv('spn_4o_model', 'gpt-4')),
                        instructions="""You are a scientific literature analysis agent specialized in drug discovery.
                        Analyze search results to extract key findings about drug candidates, mechanisms of action,
                        and clinical outcomes. Focus on recent peer-reviewed publications.""",
                        toolset=toolset,
                        headers={"x-ms-enable-preview": "true"}
                    )
                    agent_cache[agent_type] = agent
                except Exception as e:
                    logger.error(f"❌ Error creating {agent_type} agent: {str(e)}")
                    raise HTTPException(
                        status_code=500,
                        detail=f"Error creating {agent_type} agent: {str(e)}"
                    )
            
            agent = agent_cache[agent_type]
            
            # Start a conversation with the agent
            conversation = await chat_client.create_conversation(agent_id=agent.id)
            response = await conversation.send_message(
                f"""Search for recent scientific literature about: {request.query}
                Max Results: {request.max_results}
                Include Clinical Trials: {request.include_clinical_trials}
                
                Focus on drug development implications and summarize key findings.
                Provide references to support your analysis.
                
                Format your response as a JSON object with these fields:
                {
                    "query": "the search query",
                    "summary": "your analysis and findings",
                    "references": ["list of DOIs or citations"]
                }"""
            )
            
            logger.info("✅ Literature search complete")
            return {
                "query": request.query,
                "summary": response.message.content,
                "agent_id": agent.id
            }
            
        except Exception as e:
            logger.error(f"❌ Error in literature search: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error in literature search: {str(e)}"
            )

@router.post("/molecule-analysis", tags=["agents"], summary="Analyze molecular properties using function calling")
async def analyze_molecule(request: MoleculeAnalysisRequest):
    """
    ### 🧬 Molecule Analysis Agent
    
    Uses Azure AI Agent's function calling capability to analyze molecular properties
    and predict interactions with target proteins.
    
    #### Real-world Applications
    - **Drug Design**: Assess drug-like properties of new compounds
    - **Target Validation**: Predict protein-ligand interactions
    - **Safety Assessment**: Evaluate potential toxicity risks
    - **Lead Optimization**: Guide molecular modifications
    
    #### Azure AI Agent Usage
    - **Tool**: FunctionTool for property calculations
    - **Capability**: Calls custom analysis functions
    - **Integration**: Combines multiple property predictions
    - **Interpretation**: Provides scientific context for results
    
    ```mermaid
    sequenceDiagram
        participant Client
        participant Agent
        participant Functions
        Client->>Agent: Molecule Data
        Agent->>Functions: Analyze Properties
        Functions-->>Agent: Analysis Results
        Agent-->>Client: Interpreted Results
    ```
    
    Args:
        request (MoleculeAnalysisRequest): {
            "smiles": str,
            "target_proteins": List[str],
            "therapeutic_area": str
        }
        
    Returns:
        dict: {
            "molecule": str,
            "analysis": str,
            "agent_id": str
        }
        
    Example:
        ```python
        request = MoleculeAnalysisRequest(
            smiles="CC1=CC=C(C=C1)NC(=O)C2=CC=C(Cl)C=C2",
            target_proteins=["EGFR", "HER2"],
            therapeutic_area="Oncology"
        )
        response = await analyze_molecule(request)
        ```
    """
    with tracer.start_as_current_span("molecule_analysis") as span:
        try:
            span.set_attribute("operation", "molecule_analysis")
            logger.info(f"🧪 Analyzing molecule: {request.smiles}")

            # Get or create agent from cache
            agent_type = "molecule-analysis"
            if agent_type not in agent_cache:
                # Create tools configuration
                toolset = ToolSet()
                bing_tool = BingGroundingTool(
                    connection_id=os.getenv("spn_4o_BING_API_KEY")
                )
                function_tool = FunctionTool(
                    functions=[analyze_molecule_properties]
                )
                toolset.add(bing_tool)
                toolset.add(function_tool)

                try:
                    agent = await project_client.agents.create_agent(
                        model=os.getenv('MODEL_DEPLOYMENT_NAME', os.getenv('spn_4o_model', 'gpt-4')),
                        instructions="""You are a molecular analysis agent specialized in drug discovery.
                        Analyze molecular properties and protein interactions to assess drug candidate potential.
                        Provide detailed scientific explanations of your findings.""",
                        toolset=toolset,
                        headers={"x-ms-enable-preview": "true"}
                    )
                    agent_cache[agent_type] = agent
                except Exception as e:
                    logger.error(f"❌ Error creating {agent_type} agent: {str(e)}")
                    raise HTTPException(
                        status_code=500,
                        detail=f"Error creating {agent_type} agent: {str(e)}"
                    )
            
            agent = agent_cache[agent_type]
            
            # Start a conversation with the agent
            conversation = await chat_client.create_conversation(agent_id=agent.id)
            response = await conversation.send_message(
                f"""Analyze this molecule:
                SMILES: {request.smiles}
                Target Proteins: {', '.join(request.target_proteins)}
                Therapeutic Area: {request.therapeutic_area}
                
                Provide a detailed analysis of its drug-like properties and potential interactions.
                
                Format your response as a JSON object with these fields:
                {
                    "molecule": "SMILES string",
                    "analysis": {
                        "binding_predictions": {"protein": score},
                        "drug_likeness": score,
                        "safety_assessment": "description"
                    }
                }"""
            )
            
            logger.info("✅ Molecule analysis complete")
            return {
                "molecule": request.smiles,
                "analysis": response.message.content,
                "agent_id": agent.id
            }
            
        except Exception as e:
            logger.error(f"❌ Error in molecule analysis: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error in molecule analysis: {str(e)}"
            )

@router.post("/data-analysis", tags=["agents"], summary="Analyze clinical trial data using code interpreter")
async def analyze_trial_data(file: UploadFile = File(...)):
    """
    ### 📊 Clinical Trial Data Analysis Agent
    
    Uses Azure AI Agent's code interpreter capability to analyze and visualize
    clinical trial data, extracting insights and patterns.
    
    #### Real-world Applications
    - **Trial Monitoring**: Track patient outcomes and safety signals
    - **Efficacy Analysis**: Evaluate drug performance metrics
    - **Patient Stratification**: Identify responder subgroups
    - **Regulatory Reporting**: Generate compliance documentation
    
    #### Azure AI Agent Usage
    - **Tool**: CodeInterpreterTool for data analysis
    - **Capability**: Processes complex trial datasets
    - **Visualization**: Creates insightful plots automatically
    - **Statistics**: Performs advanced statistical analyses
    
    ```mermaid
    sequenceDiagram
        participant Client
        participant Agent
        participant CodeInterpreter
        Client->>Agent: Trial Data
        Agent->>CodeInterpreter: Process Data
        CodeInterpreter-->>Agent: Analysis & Plots
        Agent-->>Client: Insights
    ```
    
    Args:
        file (UploadFile): CSV file containing clinical trial data
        
    Returns:
        dict: {
            "filename": str,
            "analysis": str,
            "agent_id": str
        }
        
    Example:
        ```python
        with open("trial_data.csv", "rb") as f:
            file = UploadFile(f)
            response = await analyze_trial_data(file)
        ```
    """
    with tracer.start_as_current_span("trial_data_analysis") as span:
        try:
            span.set_attribute("operation", "trial_data_analysis")
            logger.info("📈 Starting trial data analysis")

            # Upload file for code interpreter
            file_content = await file.read()
            try:
                # Create a temporary file
                temp_file_path = f"/tmp/{file.filename}"
                with open(temp_file_path, "wb") as f:
                    f.write(file_content)
                
                # Create tools configuration
                toolset = ToolSet()
                code_tool = CodeInterpreterTool()
                toolset.add(code_tool)
                
                # Store file content in memory for code interpreter
                with open(temp_file_path, "rb") as f:
                    file_content = f.read()
                    file_id = f"file_{uuid.uuid4()}"
                    
                # Create agent with proper tool configuration
                toolset = ToolSet()
                code_tool = CodeInterpreterTool(
                    file_ids=[{
                        "id": file_id,
                        "name": file.filename,
                        "content": file_content.decode('utf-8') if isinstance(file_content, bytes) else file_content
                    }]
                )
                toolset.add(code_tool)
                
                # Clean up
                os.remove(temp_file_path)
            except Exception as e:
                logger.error(f"❌ Error uploading file: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Error uploading file: {str(e)}"
                )

            # Create agent with proper tool configuration
            agent = await project_client.agents.create_agent(
                model=os.getenv('MODEL_DEPLOYMENT_NAME', os.getenv('spn_4o_model', 'gpt-4')),
                instructions="""You are a clinical trial data analysis agent.
                Analyze trial data to extract insights about drug efficacy, safety profiles,
                and patient outcomes. Create visualizations to support your findings.""",
                toolset=toolset,
                headers={"x-ms-enable-preview": "true"}
            )
            
            # Start a conversation with the agent
            conversation = await chat_client.create_conversation(agent_id=agent.id)
            response = await conversation.send_message(
                f"""Analyze the clinical trial data in {file.filename}.
                1. Create summary statistics of key metrics
                2. Generate visualizations of important trends
                3. Identify any significant patterns or concerns
                4. Provide recommendations based on the analysis
                
                Format your response as a JSON object with these fields:
                {
                    "filename": "name of analyzed file",
                    "analysis": {
                        "correlations": {"metric": value},
                        "summary": "key findings",
                        "recommendations": ["list of recommendations"]
                    }
                }"""
            )
            
            logger.info("✅ Trial data analysis complete")
            return {
                "filename": file.filename,
                "analysis": response.message.content,
                "agent_id": agent.id
            }
            
        except Exception as e:
            logger.error(f"❌ Error in trial data analysis: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error in trial data analysis: {str(e)}"
            )


class ManufacturingOptRequest(BaseModel):
    """Request model for manufacturing optimization."""
    drug_candidate: str
    batch_size_range: List[int]
    raw_materials: dict
    production_constraints: Optional[dict] = {}

def optimize_manufacturing(
    drug_candidate: str,
    batch_sizes: List[int],
    materials: dict,
    constraints: dict
) -> dict:
    """
    Optimize manufacturing parameters for a drug candidate.
    
    Args:
        drug_candidate (str): Name/ID of the drug candidate
        batch_sizes (List[int]): Possible batch size options
        materials (dict): Available raw materials and quantities
        constraints (dict): Production line constraints
    
    Returns:
        dict: Optimized manufacturing parameters
    """
    # Mock optimization for demonstration
    return {
        "batch_size": np.random.choice(batch_sizes),
        "line_allocation": f"Line-{np.random.randint(1, 5)}",
        "estimated_unit_cost": round(np.random.uniform(1.5, 5.0), 2),
        "production_efficiency": round(np.random.uniform(0.75, 0.95), 2),
        "material_utilization": {
            material: round(np.random.uniform(0.8, 0.99), 2)
            for material in materials.keys()
        }
    }

async def process_manufacturing_opt_request(request: ManufacturingOptRequest) -> dict:
    """Process a manufacturing optimization request using Azure AI agents."""
    # Create tools configuration
    toolset = ToolSet()
    code_tool = CodeInterpreterTool()
    function_tool = FunctionTool(
        functions=[optimize_manufacturing]
    )
    toolset.add(code_tool)
    toolset.add(function_tool)

    # Create agent
    agent = await project_client.agents.create_agent(
        model=os.getenv('MODEL_DEPLOYMENT_NAME', os.getenv('spn_4o_model', 'gpt-4')),
        instructions="""You are a manufacturing optimization expert.
        Use the code interpreter to solve linear programming problems
        and optimize production schedules. Consider constraints and
        validate solutions using the provided functions.""",
        toolset=toolset,
        headers={"x-ms-enable-preview": "true"}
    )

    # Start conversation
    conversation = await chat_client.create_conversation(agent_id=agent.id)
    response = await conversation.send_message(
        f"""Optimize manufacturing schedule:
        Drug: {request.drug_candidate}
        Batch Sizes: {request.batch_size_range}
        Raw Materials: {json.dumps(request.raw_materials)}
        Constraints: {json.dumps(request.production_constraints)}
        
        1. Use linear programming to optimize batch size
        2. Consider raw material constraints
        3. Validate against production constraints
        
        Format response as JSON:
        {{
            "optimized_schedule": {{
                "batch_size": int,
                "line_allocation": str,
                "estimated_unit_cost": float
            }}
        }}"""
    )

    return {
        "optimized_schedule": json.loads(response.message.content)["optimized_schedule"],
        "agent_id": agent.id
    }

@router.post("/manufacturing-opt", tags=["agents"], summary="Optimize manufacturing process")
async def optimize_production(request: ManufacturingOptRequest):
    """
    ### 🏭 Manufacturing Optimization Agent
    
    Uses Azure AI Agent's code interpreter and function calling capabilities
    to optimize drug manufacturing processes.
    
    #### Real-world Applications
    - **Cost Optimization**: Minimize production costs
    - **Resource Planning**: Optimize material utilization
    - **Capacity Planning**: Balance production lines
    - **Supply Chain**: Coordinate material availability
    
    #### Azure AI Agent Usage
    - **Tool**: Code interpreter for simulation
    - **Capability**: Linear programming optimization
    - **Integration**: Production scheduling algorithms
    - **Analysis**: Cost-benefit trade-off analysis
    
    ```mermaid
    sequenceDiagram
        participant Client
        participant Agent
        participant Optimizer
        Client->>Agent: Production Data
        Agent->>Optimizer: Run Simulation
        Optimizer-->>Agent: Optimal Parameters
        Agent-->>Client: Schedule & Costs
    ```
    
    Args:
        request (ManufacturingOptRequest): {
            "drug_candidate": str,
            "batch_size_range": List[int],
            "raw_materials": dict,
            "production_constraints": dict
        }
        
    Returns:
        dict: {
            "optimized_schedule": dict,
            "agent_id": str
        }
        
    Example:
        ```python
        request = ManufacturingOptRequest(
            drug_candidate="DRUG123",
            batch_size_range=[1000, 2000, 5000],
            raw_materials={"API": 1000, "Excipient": 5000},
            production_constraints={"max_daily_batches": 3}
        )
        response = await optimize_production(request)
        ```
    """
    with tracer.start_as_current_span("manufacturing_optimization") as span:
        try:
            span.set_attribute("operation", "manufacturing_optimization")
            logger.info(f"🏭 Optimizing production for: {request.drug_candidate}")

            # Get or create agent from cache
            agent_type = "manufacturing-opt"
            if agent_type not in agent_cache:
                # Create tools configuration
                toolset = ToolSet()
                code_tool = CodeInterpreterTool()
                function_tool = FunctionTool(
                    functions=[optimize_manufacturing]
                )
                toolset.add(code_tool)
                toolset.add(function_tool)

                try:
                    agent = await project_client.agents.create_agent(
                        model=os.getenv('MODEL_DEPLOYMENT_NAME', os.getenv('spn_4o_model', 'gpt-4')),
                        instructions="""You are a manufacturing optimization agent.
                        Use simulation and optimization techniques to determine the most
                        efficient production parameters while considering costs, capacity,
                        and material constraints.""",
                        toolset=toolset,
                        headers={"x-ms-enable-preview": "true"}
                    )
                    agent_cache[agent_type] = agent
                except Exception as e:
                    logger.error(f"❌ Error creating {agent_type} agent: {str(e)}")
                    raise HTTPException(
                        status_code=500,
                        detail=f"Error creating {agent_type} agent: {str(e)}"
                    )
            
            agent = agent_cache[agent_type]
            
            # Start a conversation with the agent
            conversation = await chat_client.create_conversation(agent_id=agent.id)
            response = await conversation.send_message(
                f"""Optimize manufacturing process:
                Drug Candidate: {request.drug_candidate}
                Batch Size Options: {request.batch_size_range}
                Available Materials: {request.raw_materials}
                Production Constraints: {request.production_constraints}
                
                1. Run production simulation
                2. Optimize batch sizes and line allocation
                3. Calculate costs and efficiency metrics
                4. Provide detailed recommendations
                
                Format your response as a JSON object with these fields:
                {{
                    "optimized_schedule": {{
                        "batch_size": integer,
                        "line_allocation": "factory name",
                        "estimated_unit_cost": float
                    }}
                }}"""
            )
            
            logger.info("✅ Manufacturing optimization complete")
            optimization_results = optimize_manufacturing(
                request.drug_candidate,
                request.batch_size_range,
                request.raw_materials,
                request.production_constraints
            )
            
            # Parse the agent's response
            try:
                agent_response = json.loads(response.message.content)
                # Use the agent's response if valid, otherwise use optimization results
                schedule = agent_response.get("optimized_schedule", {
                    "batch_size": optimization_results["batch_size"],
                    "line_allocation": optimization_results["line_allocation"],
                    "estimated_unit_cost": optimization_results["estimated_unit_cost"]
                })
            except json.JSONDecodeError:
                # Fallback to optimization results if agent response isn't valid JSON
                schedule = {
                    "batch_size": optimization_results["batch_size"],
                    "line_allocation": optimization_results["line_allocation"],
                    "estimated_unit_cost": optimization_results["estimated_unit_cost"]
                }
            
            return {
                "optimized_schedule": schedule,
                "agent_id": agent.id
            }
            
        except Exception as e:
            logger.error(f"❌ Error in manufacturing optimization: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error in manufacturing optimization: {str(e)}"
            )


class PrecisionMedRequest(BaseModel):
    """Request model for precision medicine analysis."""
    patient_id: str
    genetic_markers: dict
    medical_history: dict
    current_medications: Optional[List[str]] = []

def analyze_genomic_compatibility(
    genetic_markers: dict,
    medical_history: dict,
    medications: List[str]
) -> dict:
    """
    Analyze genomic compatibility and predict treatment outcomes.
    
    Args:
        genetic_markers (dict): Patient's genetic markers and variants
        medical_history (dict): Patient's medical history and conditions
        medications (List[str]): Current medications
    
    Returns:
        dict: Personalized treatment analysis
    """
    # Mock analysis for demonstration
    return {
        "drug_compatibility_score": round(np.random.uniform(0.7, 0.99), 2),
        "predicted_response": round(np.random.uniform(0.6, 0.95), 2),
        "genetic_risk_factors": [
            f"Variant-{i}" for i in range(1, np.random.randint(1, 4))
        ],
        "metabolizer_status": np.random.choice([
            "Poor", "Intermediate", "Normal", "Rapid", "Ultra-rapid"
        ])
    }

async def process_precision_med_request(request: PrecisionMedRequest) -> dict:
    """Process a precision medicine request using Azure AI agents."""
    # Create tools configuration
    toolset = ToolSet()
    bing_tool = BingGroundingTool(
        connection_id=os.getenv("spn_4o_BING_API_KEY")
    )
    function_tool = FunctionTool(
        functions=[analyze_genomic_compatibility]
    )
    toolset.add(bing_tool)
    toolset.add(function_tool)

    # Create agent
    agent = await project_client.agents.create_agent(
        model=os.getenv('MODEL_DEPLOYMENT_NAME', os.getenv('spn_4o_model', 'gpt-4')),
        instructions="""You are a precision medicine expert.
        Analyze genetic markers and medical history to provide
        personalized treatment recommendations. Use Bing to
        ground recommendations in recent research.""",
        toolset=toolset,
        headers={"x-ms-enable-preview": "true"}
    )

    # Start conversation
    conversation = await chat_client.create_conversation(agent_id=agent.id)
    response = await conversation.send_message(
        f"""Analyze patient data for personalized treatment:
        Patient ID: {request.patient_id}
        Genetic Markers: {json.dumps(request.genetic_markers)}
        Medical History: {json.dumps(request.medical_history)}
        Current Medications: {', '.join(request.current_medications)}
        
        1. Analyze genomic compatibility
        2. Check recent literature for evidence
        3. Generate personalized recommendations
        
        Format response as JSON:
        {{
            "patient_id": str,
            "custom_dosage": str,
            "predicted_outcome": float,
            "recommended_followups": [str]
        }}"""
    )

    return json.loads(response.message.content) | {"agent_id": agent.id}

@router.post("/precision-med", tags=["agents"], summary="Generate personalized treatment recommendations")
async def precision_medicine(request: PrecisionMedRequest):
    """
    ### 🧬 Precision Medicine Agent
    
    Uses Azure AI Agent's capabilities to analyze patient genomic data
    and provide personalized treatment recommendations.
    
    #### Real-world Applications
    - **Treatment Optimization**: Personalize drug selection
    - **Risk Assessment**: Identify genetic contraindications
    - **Dosage Adjustment**: Account for metabolizer status
    - **Outcome Prediction**: Estimate treatment efficacy
    
    #### Azure AI Agent Usage
    - **Tool**: Combines Bing grounding and function calling
    - **Capability**: Genomic analysis and literature review
    - **Integration**: Clinical guidelines and genetic markers
    - **Assessment**: Treatment response prediction
    
    ```mermaid
    sequenceDiagram
        participant Client
        participant Agent
        participant Tools
        Client->>Agent: Patient Data
        Agent->>Tools: Analyze & Research
        Tools-->>Agent: Compatibility
        Agent-->>Client: Recommendations
    ```
    
    Args:
        request (PrecisionMedRequest): {
            "patient_id": str,
            "genetic_markers": dict,
            "medical_history": dict,
            "current_medications": List[str]
        }
        
    Returns:
        dict: {
            "custom_dosage": str,
            "predicted_outcome": float,
            "recommended_followups": List[str],
            "agent_id": str
        }
        
    Example:
        ```python
        request = PrecisionMedRequest(
            patient_id="PAT007",
            genetic_markers={"CYP2D6": "UM", "TPMT": "*1/*3"},
            medical_history={"conditions": ["Hypertension"]},
            current_medications=["Metoprolol"]
        )
        response = await precision_medicine(request)
        ```
    """
    with tracer.start_as_current_span("precision_medicine") as span:
        try:
            span.set_attribute("operation", "precision_medicine")
            logger.info(f"🧬 Analyzing precision medicine for patient: {request.patient_id}")

            # Get or create agent from cache
            agent_type = "precision-med"
            if agent_type not in agent_cache:
                # Create tools configuration
                toolset = ToolSet()
                bing_tool = BingGroundingTool(
                    connection_id=os.getenv("spn_4o_BING_API_KEY")
                )
                function_tool = FunctionTool(
                    functions=[analyze_genomic_compatibility]
                )
                toolset.add(bing_tool)
                toolset.add(function_tool)

                try:
                    agent = await project_client.agents.create_agent(
                        model=os.getenv('MODEL_DEPLOYMENT_NAME', os.getenv('spn_4o_model', 'gpt-4')),
                        instructions="""You are a precision medicine analysis agent.
                        Evaluate patient genomic data and medical history to provide
                        personalized treatment recommendations. Consider genetic markers,
                        drug interactions, and potential adverse effects.""",
                        toolset=toolset,
                        headers={"x-ms-enable-preview": "true"}
                    )
                    agent_cache[agent_type] = agent
                except Exception as e:
                    logger.error(f"❌ Error creating {agent_type} agent: {str(e)}")
                    raise HTTPException(
                        status_code=500,
                        detail=f"Error creating {agent_type} agent: {str(e)}"
                    )
            
            agent = agent_cache[agent_type]
            
            # Start a conversation with the agent
            conversation = await chat_client.create_conversation(agent_id=agent.id)
            response = await conversation.send_message(
                f"""Analyze patient data for precision medicine:
                Patient ID: {request.patient_id}
                Genetic Markers: {request.genetic_markers}
                Medical History: {request.medical_history}
                Current Medications: {request.current_medications}
                
                1. Research genetic variants and their implications
                2. Analyze drug-gene interactions
                3. Calculate compatibility scores
                4. Provide personalized recommendations
                
                Format your response as a JSON object with these fields:
                {{
                    "patient_id": "patient identifier",
                    "custom_dosage": "dosage recommendation",
                    "predicted_outcome": float between 0 and 1,
                    "recommended_followups": ["list of followup actions"]
                }}"""
            )
            
            logger.info("✅ Precision medicine analysis complete")
            analysis_results = analyze_genomic_compatibility(
                request.genetic_markers,
                request.medical_history,
                request.current_medications
            )
            
            # Calculate custom dosage based on metabolizer status
            base_dose = 120  # mg
            dose_adjustment = {
                "Poor": 0.5,        # 50% reduction
                "Intermediate": 0.75,  # 25% reduction
                "Normal": 1.0,      # Standard dose
                "Rapid": 1.25,      # 25% increase
                "Ultra-rapid": 1.5  # 50% increase
            }
            adjusted_dose = base_dose * dose_adjustment[analysis_results["metabolizer_status"]]
            
            # Parse the agent's response
            try:
                agent_response = json.loads(response.message.content)
                # Use the agent's response if valid, otherwise use analysis results
                result = {
                    "patient_id": agent_response.get("patient_id", request.patient_id),
                    "custom_dosage": agent_response.get("custom_dosage", f"{int(adjusted_dose)} mg daily"),
                    "predicted_outcome": agent_response.get("predicted_outcome", analysis_results["predicted_response"]),
                    "recommended_followups": agent_response.get("recommended_followups", [
                        "Monthly biomarker profiling",
                        f"Monitor {', '.join(analysis_results['genetic_risk_factors'])}",
                        f"Adjust dose based on {analysis_results['metabolizer_status']} metabolizer status"
                    ]),
                    "agent_id": agent.id
                }
            except json.JSONDecodeError:
                # Fallback to analysis results if agent response isn't valid JSON
                result = {
                    "patient_id": request.patient_id,
                    "custom_dosage": f"{int(adjusted_dose)} mg daily",
                    "predicted_outcome": analysis_results["predicted_response"],
                    "recommended_followups": [
                        "Monthly biomarker profiling",
                        f"Monitor {', '.join(analysis_results['genetic_risk_factors'])}",
                        f"Adjust dose based on {analysis_results['metabolizer_status']} metabolizer status"
                    ],
                    "agent_id": agent.id
                }
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error in precision medicine analysis: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error in precision medicine analysis: {str(e)}"
            )


class DigitalTwinRequest(BaseModel):
    """Request model for digital twin clinical simulation."""
    molecule_parameters: dict
    target_population: dict
    simulation_config: Optional[dict] = {}

def run_clinical_simulation(
    molecule_params: dict,
    population_data: dict,
    config: dict
) -> dict:
    """
    Run a digital twin simulation for clinical trial outcomes.
    
    Args:
        molecule_params (dict): Drug molecule parameters
        population_data (dict): Target population characteristics
        config (dict): Simulation configuration
    
    Returns:
        dict: Simulation results and metrics
    """
    # Mock simulation for demonstration
    population_size = np.random.randint(5000, 15000)
    return {
        "population_size": population_size,
        "toxicity_scores": {
            "mean": round(np.random.uniform(0.05, 0.2), 3),
            "std": round(np.random.uniform(0.01, 0.05), 3)
        },
        "efficacy_metrics": {
            "response_rate": round(np.random.uniform(0.4, 0.8), 2),
            "survival_gain": f"{np.random.randint(3, 12)} months"
        },
        "adverse_events": {
            "mild": round(np.random.uniform(0.1, 0.3), 2),
            "moderate": round(np.random.uniform(0.05, 0.15), 2),
            "severe": round(np.random.uniform(0.01, 0.05), 2)
        }
    }

async def process_digital_twin_request(request: DigitalTwinRequest) -> dict:
    """Process a digital twin simulation request using Azure AI agents."""
    # Create tools configuration
    toolset = ToolSet()
    code_tool = CodeInterpreterTool()
    function_tool = FunctionTool(
        functions=[run_clinical_simulation]
    )
    toolset.add(code_tool)
    toolset.add(function_tool)

    # Create agent
    agent = await project_client.agents.create_agent(
        model=os.getenv('MODEL_DEPLOYMENT_NAME', os.getenv('spn_4o_model', 'gpt-4')),
        instructions="""You are a clinical simulation expert.
        Use the code interpreter to run population-level simulations
        and analyze outcomes. Process results using provided functions
        to generate meaningful insights.""",
        toolset=toolset,
        headers={"x-ms-enable-preview": "true"}
    )

    # Start conversation
    conversation = await chat_client.create_conversation(agent_id=agent.id)
    response = await conversation.send_message(
        f"""Run digital twin simulation:
        Molecule Parameters: {json.dumps(request.molecule_parameters)}
        Target Population: {json.dumps(request.target_population)}
        Simulation Config: {json.dumps(request.simulation_config)}
        
        1. Generate virtual population
        2. Run PK/PD simulation
        3. Analyze outcomes and safety
        
        Format response as JSON:
        {{
            "simulated_population_size": int,
            "mean_toxicity_score": float,
            "average_survival_gain": str
        }}"""
    )

    return json.loads(response.message.content) | {"agent_id": agent.id}

@router.post("/digital-twin-sim", tags=["agents"], summary="Simulate clinical trial outcomes")
async def digital_twin_simulation(request: DigitalTwinRequest):
    """
    ### 🔬 Digital Twin Clinical Simulation Agent
    
    Uses Azure AI Agent's capabilities to simulate patient populations
    as digital twins for Phase I clinical trials.
    
    #### Real-world Applications
    - **Trial Design**: Optimize protocol parameters
    - **Risk Assessment**: Predict adverse events
    - **Patient Selection**: Define inclusion criteria
    - **Outcome Prediction**: Estimate efficacy metrics
    
    #### Azure AI Agent Usage
    - **Tool**: Code interpreter for PK/PD modeling
    - **Capability**: Population-level simulations
    - **Integration**: Clinical trial parameters
    - **Analysis**: Statistical outcome metrics
    
    ```mermaid
    sequenceDiagram
        participant Client
        participant Agent
        participant Simulator
        Client->>Agent: Trial Parameters
        Agent->>Simulator: Run Models
        Simulator-->>Agent: Results
        Agent-->>Client: Insights
    ```
    
    Args:
        request (DigitalTwinRequest): {
            "molecule_parameters": dict,
            "target_population": dict,
            "simulation_config": dict
        }
        
    Returns:
        dict: {
            "simulated_population_size": int,
            "mean_toxicity_score": float,
            "average_survival_gain": str,
            "agent_id": str
        }
        
    Example:
        ```python
        request = DigitalTwinRequest(
            molecule_parameters={
                "half_life": "24h",
                "bioavailability": 0.85
            },
            target_population={
                "age_range": [18, 65],
                "conditions": ["Type2Diabetes"]
            }
        )
        response = await digital_twin_simulation(request)
        ```
    """
    with tracer.start_as_current_span("digital_twin_simulation") as span:
        try:
            span.set_attribute("operation", "digital_twin_simulation")
            logger.info("🔬 Running digital twin simulation")

            # Get or create agent from cache
            agent_type = "digital-twin-sim"
            if agent_type not in agent_cache:
                # Create tools configuration
                toolset = ToolSet()
                code_tool = CodeInterpreterTool()
                function_tool = FunctionTool(
                    functions=[run_clinical_simulation]
                )
                toolset.add(code_tool)
                toolset.add(function_tool)

                try:
                    agent = await project_client.agents.create_agent(
                        model=os.getenv('MODEL_DEPLOYMENT_NAME', os.getenv('spn_4o_model', 'gpt-4')),
                        instructions="""You are a clinical trial simulation expert.
                        Use PK/PD modeling and statistical analysis to simulate
                        patient populations and predict trial outcomes. Consider
                        patient characteristics, drug properties, and trial design.""",
                        toolset=toolset,
                        headers={"x-ms-enable-preview": "true"}
                    )
                    agent_cache[agent_type] = agent
                except Exception as e:
                    logger.error(f"❌ Error creating {agent_type} agent: {str(e)}")
                    raise HTTPException(
                        status_code=500,
                        detail=f"Error creating {agent_type} agent: {str(e)}"
                    )
            
            agent = agent_cache[agent_type]
            
            # Start a conversation with the agent
            conversation = await chat_client.create_conversation(agent_id=agent.id)
            response = await conversation.send_message(
                f"""Simulate clinical trial outcomes:
                Molecule Parameters: {request.molecule_parameters}
                Target Population: {request.target_population}
                Simulation Config: {request.simulation_config}
                
                1. Run PK/PD simulations
                2. Generate virtual patient cohorts
                3. Calculate outcome metrics
                4. Analyze safety and efficacy
                
                Format your response as a JSON object with these fields:
                {{
                    "simulated_population_size": integer,
                    "mean_toxicity_score": float between 0 and 1,
                    "average_survival_gain": "duration in months",
                    "detailed_metrics": {{
                        "efficacy_by_subgroup": {{
                            "subgroup_name": float (efficacy score)
                        }},
                        "adverse_events": {{
                            "event_type": float (frequency)
                        }}
                    }}
                }}"""
            )
            
            logger.info("✅ Digital twin simulation complete")
            simulation_results = run_clinical_simulation(
                request.molecule_parameters,
                request.target_population,
                request.simulation_config
            )
            
            # Parse the agent's response
            try:
                agent_response = json.loads(response.message.content)
                # Use the agent's response if valid, otherwise use simulation results
                result = {
                    "simulated_population_size": agent_response.get("simulated_population_size", simulation_results["population_size"]),
                    "mean_toxicity_score": agent_response.get("mean_toxicity_score", simulation_results["toxicity_scores"]["mean"]),
                    "average_survival_gain": agent_response.get("average_survival_gain", simulation_results["efficacy_metrics"]["survival_gain"]),
                    "agent_id": agent.id
                }
            except json.JSONDecodeError:
                # Fallback to simulation results if agent response isn't valid JSON
                result = {
                    "simulated_population_size": simulation_results["population_size"],
                    "mean_toxicity_score": simulation_results["toxicity_scores"]["mean"],
                    "average_survival_gain": simulation_results["efficacy_metrics"]["survival_gain"],
                    "agent_id": agent.id
                }
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error in digital twin simulation: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error in digital twin simulation: {str(e)}"
            )


class DrugRepurposeRequest(BaseModel):
    """Request model for drug repurposing analysis."""
    molecule_id: str
    new_indication: str
    current_indications: Optional[List[str]] = []

def calculate_repurposing_score(molecule_id: str, target_disease: str) -> dict:
    """
    Calculate repurposing potential score for a molecule against a new indication.
    
    Args:
        molecule_id (str): Identifier for the existing drug molecule
        target_disease (str): New disease indication to evaluate
    
    Returns:
        dict: Repurposing analysis results including confidence scores
    """
    # Mock analysis for demonstration - ensure confidence is between 0.5 and 1.0
    confidence = np.random.uniform(0.5, 1.0)
    return {
        "disease": target_disease,
        "confidence": confidence,
        "supporting_sources": [
            f"DOI:10.1234/repurpose-{molecule_id}",
            f"DOI:10.5678/mechanism-{confidence:.2f}"
        ]
    }

async def process_drug_repurpose_request(request: DrugRepurposeRequest) -> dict:
    """Process a drug repurposing request using Azure AI agents."""
    # Create tools configuration
    toolset = ToolSet()
    bing_tool = BingGroundingTool(
        connection_id=os.getenv("spn_4o_BING_API_KEY")
    )
    function_tool = FunctionTool(
        functions=[calculate_repurposing_score]
    )
    toolset.add(bing_tool)
    toolset.add(function_tool)

    # Create agent
    agent = await project_client.agents.create_agent(
        model=os.getenv('MODEL_DEPLOYMENT_NAME', os.getenv('spn_4o_model', 'gpt-4')),
        instructions="""You are a drug repurposing expert.
        Leverage the Bing grounding tool to find recent research
        about reusing a known compound for a new indication.
        Then run any local function(s) to estimate feasibility.""",
        toolset=toolset,
        headers={"x-ms-enable-preview": "true"}
    )

    # Start conversation
    conversation = await chat_client.create_conversation(agent_id=agent.id)
    response = await conversation.send_message(
        f"""Analyze repurposing potential:
        Molecule ID: {request.molecule_id}
        Current Indications: {', '.join(request.current_indications)}
        Proposed New Indication: {request.new_indication}
        
        1. Search for recent research about this molecule and similar compounds
        2. Calculate repurposing score
        3. Provide evidence-based recommendations
        
        Format response as JSON:
        {{
            "repurposing_opportunities": [
                {{
                    "disease": "disease name",
                    "confidence": 0.0-1.0,
                    "supporting_sources": ["DOI references"]
                }}
            ]
        }}"""
    )

    return {
        "repurposing_opportunities": json.loads(response.message.content)["repurposing_opportunities"],
        "agent_id": agent.id
    }

@router.post("/drug-repurpose", tags=["agents"], summary="Analyze drug repurposing opportunities")
async def drug_repurpose(request: DrugRepurposeRequest):
    """
    ### 💊 Drug Repurposing Agent
    
    Uses Azure AI Agent's capabilities to evaluate opportunities for repurposing
    existing drugs for new therapeutic indications.
    
    #### Real-world Applications
    - **Cost Reduction**: Leverage existing safety data
    - **Time Savings**: Accelerate development timeline
    - **Risk Mitigation**: Build on known safety profiles
    - **Market Expansion**: Identify new therapeutic areas
    
    #### Azure AI Agent Usage
    - **Tool**: Combines Bing grounding and function calling
    - **Capability**: Literature analysis and similarity scoring
    - **Integration**: Merges historical data with new research
    - **Assessment**: Evaluates feasibility and potential
    
    ```mermaid
    sequenceDiagram
        participant Client
        participant Agent
        participant Tools
        Client->>Agent: Drug & New Indication
        Agent->>Tools: Literature & Analysis
        Tools-->>Agent: Feasibility Score
        Agent-->>Client: Recommendations
    ```
    
    Args:
        request (DrugRepurposeRequest): {
            "molecule_id": str,
            "new_indication": str,
            "current_indications": List[str]
        }
        
    Returns:
        dict: {
            "repurposing_opportunities": List[dict],
            "agent_id": str
        }
        
    Example:
        ```python
        request = DrugRepurposeRequest(
            molecule_id="DRUG123",
            new_indication="RareAutoimmuneXYZ",
            current_indications=["Arthritis", "Lupus"]
        )
        response = await drug_repurpose(request)
        ```
    """
    with tracer.start_as_current_span("drug_repurpose") as span:
        try:
            span.set_attribute("operation", "drug_repurpose")
            logger.info(f"🔄 Analyzing repurposing potential for molecule: {request.molecule_id}")

            # Get or create agent from cache
            agent_type = "drug-repurpose"
            if agent_type not in agent_cache:
                # Create tools configuration
                toolset = ToolSet()
                
                # Add Bing grounding tool with connection ID
                bing_tool = BingGroundingTool(
                    connection_id=os.getenv("spn_4o_BING_API_KEY")
                )
                toolset.add(bing_tool)
                
                # Add function tool with proper configuration
                function_tool = FunctionTool(
                    functions=[calculate_repurposing_score]
                )
                toolset.add(function_tool)

                try:
                    agent = await project_client.agents.create_agent(
                        model=os.getenv('MODEL_DEPLOYMENT_NAME', os.getenv('spn_4o_model', 'gpt-4')),
                        instructions="""You are a drug repurposing analysis agent.
                        Evaluate the potential of existing drugs for new therapeutic indications
                        by analyzing scientific literature and calculating similarity scores.
                        Consider mechanism of action, safety profiles, and development feasibility.""",
                        toolset=toolset,
                        headers={"x-ms-enable-preview": "true"}
                    )
                    agent_cache[agent_type] = agent
                except Exception as e:
                    logger.error(f"❌ Error creating {agent_type} agent: {str(e)}")
                    raise HTTPException(
                        status_code=500,
                        detail=f"Error creating {agent_type} agent: {str(e)}"
                    )
            
            agent = agent_cache[agent_type]
            
            # Start a conversation with the agent
            conversation = await chat_client.create_conversation(agent_id=agent.id)
            response = await conversation.send_message(
                f"""Analyze repurposing potential:
                Molecule ID: {request.molecule_id}
                Current Indications: {', '.join(request.current_indications)}
                Proposed New Indication: {request.new_indication}
                
                1. Search for relevant literature about similar repurposing cases
                2. Calculate repurposing feasibility scores
                3. Provide detailed recommendations with supporting evidence
                
                Format your response as a JSON object with these fields:
                {{
                    "repurposing_opportunities": [
                        {{
                            "disease": "disease name",
                            "confidence": 0.0 to 1.0,
                            "supporting_sources": ["DOI or citation"]
                        }}
                    ]
                }}"""
            )
            
            logger.info("✅ Drug repurposing analysis complete")
            # Parse the agent's response
            try:
                agent_response = json.loads(response.message.content)
                if "repurposing_opportunities" not in agent_response:
                    # If agent response doesn't have the right format, calculate it directly
                    analysis_result = calculate_repurposing_score(
                        request.molecule_id,
                        request.new_indication
                    )
                    agent_response = {
                        "repurposing_opportunities": [analysis_result]
                    }
                
                # Add agent_id to response
                agent_response["agent_id"] = agent.id
                result = agent_response
                
            except json.JSONDecodeError:
                # Fallback to direct calculation if agent response isn't valid JSON
                analysis_result = calculate_repurposing_score(
                    request.molecule_id,
                    request.new_indication
                )
                result = {
                    "repurposing_opportunities": [analysis_result],
                    "agent_id": agent.id
                }
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error in drug repurposing analysis: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error in drug repurposing analysis: {str(e)}"
            )
