# NeuroDiverAgents Architecture

## System Overview

A hierarchical multi-agent AI system for supporting parents of neurodivergent children, built with type-safe Pydantic models and Google ADK integration.

---

## Complete Architecture Diagram

```mermaid
graph TB
    %% Styling
    classDef coordinator fill:#6366f1,stroke:#4f46e5,stroke-width:3px,color:#fff
    classDef specialist fill:#8b5cf6,stroke:#7c3aed,stroke-width:2px,color:#fff
    classDef tool fill:#10b981,stroke:#059669,stroke-width:2px,color:#fff
    classDef model fill:#f59e0b,stroke:#d97706,stroke-width:2px,color:#fff
    classDef infra fill:#64748b,stroke:#475569,stroke-width:2px,color:#fff
    classDef result fill:#ec4899,stroke:#db2777,stroke-width:2px,color:#fff

    %% User Input
    User[👨‍👩‍👧 Parent/Caregiver]

    %% Coordinator Layer
    Coordinator["🎯 Parenting Coordinator<br/>(Manager Agent)<br/>━━━━━━━━━━<br/>Orchestrates specialists<br/>Routes questions<br/>Synthesizes insights"]

    %% Specialist Agents
    ADHD["🧠 ADHD Expert<br/>━━━━━━━━━━<br/>Executive function<br/>Attention regulation"]
    ASD["🌈 ASD Expert<br/>━━━━━━━━━━<br/>Sensory processing<br/>Routine needs"]
    Dev["📊 Developmental Expert<br/>━━━━━━━━━━<br/>Age milestones<br/>Expectations"]
    Memory["💾 Memory Agent<br/>━━━━━━━━━━<br/>Pattern learning<br/>Personalization"]
    Activity["📅 Activity Planner<br/>━━━━━━━━━━<br/>Structured plans<br/>EF activities"]

    %% Custom Tools
    BehaviorTool["🔍 BehaviorClassifier<br/>━━━━━━━━━━<br/>ADHD/ASD/Age analysis<br/>Factor identification"]
    ActivityTool["🎨 ActivityPlanner<br/>━━━━━━━━━━<br/>Structured plans<br/>Age-appropriate"]
    PatternTool["📈 PatternAnalyzer<br/>━━━━━━━━━━<br/>Session history<br/>Personalized insights"]
    GoogleTool["🔎 GoogleSearchTool<br/>━━━━━━━━━━<br/>Research support<br/>Evidence-based"]

    %% Pydantic Models Layer
    subgraph Models["📦 Pydantic Model Layer (Type-Safe)"]
        BehaviorModel["behavior.py<br/>━━━━━━━━━━<br/>BehaviorInput<br/>BehaviorAnalysis<br/>BehaviorFactor enum"]
        ActivityModel["activity.py<br/>━━━━━━━━━━<br/>ActivityPlan<br/>ActivityRequest"]
        StrategyModel["strategy.py<br/>━━━━━━━━━━<br/>Strategy<br/>BehaviorResponse"]
        MemoryModel["memory.py<br/>━━━━━━━━━━<br/>SessionOutcome<br/>BehaviorPattern"]
        ResultModel["results.py<br/>━━━━━━━━━━<br/>ToolSuccess<br/>ToolError<br/>ToolResult"]
    end

    %% Infrastructure Layer
    subgraph Infrastructure["⚙️ Infrastructure Layer"]
        Factory["AgentFactory<br/>━━━━━━━━━━<br/>Agent caching<br/>Retry config"]
        Wrapper["Tool Wrappers<br/>━━━━━━━━━━<br/>ADK integration<br/>Type conversion"]
        Config["Configuration<br/>━━━━━━━━━━<br/>API keys<br/>Retry policies"]
    end

    %% Result Handling
    subgraph Results["🎭 Discriminated Union Pattern"]
        Success["✅ ToolSuccess<br/>success: Literal[True]<br/>data: T"]
        Error["❌ ToolError<br/>success: Literal[False]<br/>error_message: str"]
        Union["ToolResult = Success | Error<br/>━━━━━━━━━━<br/>Type-safe error handling"]
    end

    %% Connections - User to Coordinator
    User -->|Question| Coordinator

    %% Coordinator to Specialists (AgentTools)
    Coordinator -.->|Routes to| ADHD
    Coordinator -.->|Routes to| ASD
    Coordinator -.->|Routes to| Dev
    Coordinator -.->|Routes to| Memory
    Coordinator -.->|Routes to| Activity

    %% Specialists to Tools
    ADHD --> BehaviorTool
    ADHD --> GoogleTool
    ASD --> BehaviorTool
    ASD --> GoogleTool
    Dev --> GoogleTool
    Memory --> PatternTool
    Activity --> ActivityTool

    %% Tools to Models
    BehaviorTool --> BehaviorModel
    ActivityTool --> ActivityModel
    PatternTool --> MemoryModel
    BehaviorTool --> ResultModel
    ActivityTool --> ResultModel
    PatternTool --> ResultModel

    %% Infrastructure connections
    Factory -->|Creates| Coordinator
    Factory -->|Creates| ADHD
    Factory -->|Creates| ASD
    Factory -->|Creates| Dev
    Factory -->|Creates| Memory
    Factory -->|Creates| Activity

    Wrapper -->|Wraps| BehaviorTool
    Wrapper -->|Wraps| ActivityTool
    Wrapper -->|Wraps| PatternTool

    Config -->|Configures| Factory

    %% Result flow
    ResultModel --> Union
    Union --> Success
    Union --> Error

    %% Response flow
    ADHD -.->|Insights| Coordinator
    ASD -.->|Insights| Coordinator
    Dev -.->|Insights| Coordinator
    Memory -.->|Insights| Coordinator
    Activity -.->|Plans| Coordinator
    Coordinator -->|Synthesized Response| User

    %% Apply styles
    class Coordinator coordinator
    class ADHD,ASD,Dev,Memory,Activity specialist
    class BehaviorTool,ActivityTool,PatternTool,GoogleTool tool
    class BehaviorModel,ActivityModel,StrategyModel,MemoryModel,ResultModel model
    class Factory,Wrapper,Config infra
    class Success,Error,Union result
```

---

## Detailed Component Diagram

```mermaid
graph LR
    %% Styling
    classDef layer1 fill:#dbeafe,stroke:#3b82f6,stroke-width:2px
    classDef layer2 fill:#fce7f3,stroke:#ec4899,stroke-width:2px
    classDef layer3 fill:#dcfce7,stroke:#10b981,stroke-width:2px
    classDef layer4 fill:#fef3c7,stroke:#f59e0b,stroke-width:2px

    subgraph Layer1["🏗️ Layer 1: Models (Pure Data)"]
        M1[BehaviorInput<br/>BehaviorAnalysis<br/>BehaviorFactor]
        M2[ActivityPlan<br/>ActivityRequest]
        M3[SessionOutcome<br/>BehaviorPattern]
        M4[ToolSuccess<br/>ToolError<br/>ToolResult]
    end

    subgraph Layer2["🔧 Layer 2: Tools (Business Logic)"]
        T1[BehaviorClassifier<br/>━━━━━━━━━━<br/>Analyze behavior patterns]
        T2[ActivityPlanner<br/>━━━━━━━━━━<br/>Generate activities]
        T3[PatternAnalyzer<br/>━━━━━━━━━━<br/>Learn from history]
        T4[GoogleSearchTool<br/>━━━━━━━━━━<br/>Research support]
    end

    subgraph Layer3["🤖 Layer 3: Agents (Specialists)"]
        A1[ADHD Expert]
        A2[ASD Expert]
        A3[Developmental Expert]
        A4[Memory Agent]
        A5[Activity Planner]
    end

    subgraph Layer4["🎯 Layer 4: Orchestration"]
        O1[Parenting Coordinator<br/>━━━━━━━━━━<br/>Routes & synthesizes]
    end

    %% Layer connections
    M1 --> T1
    M2 --> T2
    M3 --> T3
    M4 -.->|Returns| T1
    M4 -.->|Returns| T2
    M4 -.->|Returns| T3

    T1 --> A1
    T1 --> A2
    T2 --> A5
    T3 --> A4
    T4 --> A1
    T4 --> A2
    T4 --> A3

    A1 --> O1
    A2 --> O1
    A3 --> O1
    A4 --> O1
    A5 --> O1

    %% Apply styles
    class M1,M2,M3,M4 layer1
    class T1,T2,T3,T4 layer2
    class A1,A2,A3,A4,A5 layer3
    class O1 layer4
```

---

## Type Safety Flow

```mermaid
sequenceDiagram
    participant User
    participant Coordinator
    participant ADHD as ADHD Expert
    participant Tool as BehaviorClassifier
    participant Model as Pydantic Models

    User->>Coordinator: "Child won't sit still for homework"

    Note over Coordinator: Routes to ADHD Expert
    Coordinator->>ADHD: Analyze behavior

    ADHD->>Tool: classify_behavior()
    Note over Tool: Validates input with Pydantic
    Tool->>Model: BehaviorInput.model_validate()
    Model-->>Tool: ✅ Validated

    Tool->>Tool: Analyze ADHD/ASD/Age factors
    Tool->>Model: BehaviorAnalysis.model_validate()
    Model-->>Tool: ✅ Validated

    alt Success
        Tool-->>ADHD: ToolSuccess(data=analysis)
        Note over Tool,ADHD: success: Literal[True]
    else Error
        Tool-->>ADHD: ToolError(error_message="...")
        Note over Tool,ADHD: success: Literal[False]
    end

    ADHD-->>Coordinator: Insights
    Coordinator-->>User: Synthesized response
```

---

## Data Flow Architecture

```mermaid
flowchart TD
    Start([👨‍👩‍👧 Parent Question]) --> Input[Parse Input]

    Input --> Validate{Pydantic<br/>Validation}
    Validate -->|Invalid| Error1[Return Validation Error]
    Validate -->|Valid| Route{Coordinator<br/>Routing}

    Route -->|ADHD-related| Agent1[ADHD Expert]
    Route -->|ASD-related| Agent2[ASD Expert]
    Route -->|Development| Agent3[Dev Expert]
    Route -->|Activities| Agent4[Activity Planner]
    Route -->|Patterns| Agent5[Memory Agent]

    Agent1 --> Tool1[BehaviorClassifier<br/>+ GoogleSearch]
    Agent2 --> Tool2[BehaviorClassifier<br/>+ GoogleSearch]
    Agent3 --> Tool3[GoogleSearch]
    Agent4 --> Tool4[ActivityPlanner]
    Agent5 --> Tool5[PatternAnalyzer]

    Tool1 --> Result1{ToolResult}
    Tool2 --> Result2{ToolResult}
    Tool3 --> Result3{ToolResult}
    Tool4 --> Result4{ToolResult}
    Tool5 --> Result5{ToolResult}

    Result1 -->|Success| Synth[Coordinator<br/>Synthesis]
    Result2 -->|Success| Synth
    Result3 -->|Success| Synth
    Result4 -->|Success| Synth
    Result5 -->|Success| Synth

    Result1 -->|Error| Error2[Error Handling]
    Result2 -->|Error| Error2
    Result3 -->|Error| Error2
    Result4 -->|Error| Error2
    Result5 -->|Error| Error2

    Error2 --> Synth

    Synth --> Response([📝 Parent Response])

    style Start fill:#dbeafe,stroke:#3b82f6
    style Response fill:#dcfce7,stroke:#10b981
    style Error1 fill:#fee2e2,stroke:#dc2626
    style Error2 fill:#fee2e2,stroke:#dc2626
    style Synth fill:#fef3c7,stroke:#f59e0b
```

---

## Key Architectural Decisions

### ✅ Type Safety Everywhere
- **Pydantic v2** for all data models
- **Discriminated unions** for result handling (ToolSuccess | ToolError)
- **ConfigDict** with strict validation
- **No `Dict[str, Any]`** - only typed models

### 🎯 Hierarchical Agent Design
- **Coordinator pattern** for orchestration
- **Specialist agents** with focused expertise
- **AgentTool integration** for delegation
- **Synthesis layer** for coherent responses

### 🔧 Clean Architecture Layers
1. **Models** - Pure data structures (Pydantic)
2. **Tools** - Business logic with custom implementations
3. **Agents** - Specialist knowledge domains
4. **Orchestration** - Coordination and routing

### 🛡️ Robustness Features
- **Retry configuration** for API calls
- **Error handling** via discriminated unions
- **Input validation** at every boundary
- **Agent caching** for performance

### 📊 Domain-Driven Design
- **BehaviorFactor enum** (ADHD, ASD, Age)
- **Clear domain models** (behavior, activity, strategy, memory)
- **Bounded contexts** per specialist
- **Ubiquitous language** in model naming

---

## Technology Stack

```mermaid
mindmap
  root((NeuroDiverAgents))
    AI Framework
      Google ADK
      Multi-Agent System
      AgentTools
    Type Safety
      Pydantic v2
      Python 3.12+
      Discriminated Unions
      Strict Validation
    Custom Tools
      BehaviorClassifier
      ActivityPlanner
      PatternAnalyzer
    Infrastructure
      AgentFactory
      Retry Logic
      Caching
      Tool Wrappers
    Domain Models
      Behavior Analysis
      Activity Planning
      Pattern Learning
      Session Memory
```

---

## Agent Communication Pattern

```mermaid
stateDiagram-v2
    [*] --> ReceiveQuestion

    ReceiveQuestion --> RouteToSpecialist: Coordinator analyzes

    RouteToSpecialist --> ADHDExpert: Executive function issue
    RouteToSpecialist --> ASDExpert: Sensory/routine issue
    RouteToSpecialist --> DevExpert: Milestone question
    RouteToSpecialist --> MemoryAgent: Pattern recognition
    RouteToSpecialist --> ActivityPlanner: Activity request

    ADHDExpert --> UseTool: BehaviorClassifier
    ASDExpert --> UseTool: BehaviorClassifier
    DevExpert --> UseTool: GoogleSearch
    MemoryAgent --> UseTool: PatternAnalyzer
    ActivityPlanner --> UseTool: ActivityPlanner

    UseTool --> ValidateInput: Pydantic validation
    ValidateInput --> ExecuteTool: Valid
    ValidateInput --> ReturnError: Invalid

    ExecuteTool --> ReturnSuccess: Success
    ExecuteTool --> ReturnError: Error

    ReturnSuccess --> SynthesizeResponse
    ReturnError --> SynthesizeResponse

    SynthesizeResponse --> [*]: Return to parent
```

---

## Deployment Architecture

```mermaid
C4Context
    title System Context - NeuroDiverAgents

    Person(parent, "Parent/Caregiver", "User seeking guidance")

    System_Boundary(neuroDiver, "NeuroDiverAgents") {
        Container(coordinator, "Parenting Coordinator", "Google ADK Agent", "Orchestrates specialist agents")
        Container(specialists, "Specialist Agents", "Google ADK Agents", "ADHD, ASD, Dev, Memory, Activity")
        Container(tools, "Custom Tools", "Pydantic Tools", "BehaviorClassifier, ActivityPlanner, PatternAnalyzer")
        Container(models, "Domain Models", "Pydantic v2", "Type-safe data structures")
    }

    System_Ext(google, "Google Search", "Research support")
    System_Ext(gemini, "Gemini AI", "LLM backend")

    Rel(parent, coordinator, "Asks question", "Natural language")
    Rel(coordinator, specialists, "Routes to", "AgentTools")
    Rel(specialists, tools, "Uses", "Function calls")
    Rel(tools, models, "Validates with", "Pydantic")
    Rel(tools, google, "Searches", "API")
    Rel(specialists, gemini, "Powered by", "LLM")
    Rel(coordinator, parent, "Returns", "Synthesized response")
```

---

## Summary

**NeuroDiverAgents** demonstrates enterprise-grade Python architecture:

- ✅ **Type-safe throughout** - Pydantic models with ConfigDict
- ✅ **Discriminated unions** - ToolSuccess | ToolError pattern
- ✅ **Layered architecture** - Models → Tools → Agents → Orchestration
- ✅ **Clean separation** - Business logic, infrastructure, domain models
- ✅ **Robust error handling** - Validation at boundaries, retry logic
- ✅ **Scalable design** - AgentFactory, caching, tool wrappers
- ✅ **Domain-driven** - Clear bounded contexts per specialist

**Perfect demonstration of modern Python best practices for AI systems.**
