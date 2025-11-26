# NeuroDiverAgents - Neurodivergent Parenting Support Agents

**Subtitle**: AI-powered multi-agent system helping parents understand and support children with ADHD and autism

**Track**: Agents for Good

---

## The Problem

Parents of neurodivergent children face daily challenges that can feel overwhelming:

- **Behavioral confusion**: Is this meltdown caused by ADHD executive function issues, autism sensory overload, or
  typical 8-year-old boundary testing?
- **Strategy paralysis**: With countless parenting tips online, which evidence-based approaches actually work for ADHD
  and autism?
- **Personalization gap**: Generic advice doesn't account for what works for THIS specific child
- **Expert access**: Specialist consultations are expensive and hard to schedule

These parents need accessible, personalized, evidence-based guidance available when challenging moments happen - not
weeks later at a therapy appointment.

---

## The Solution

The **Neurodivergent Parenting Support Agents** is a multi-agent AI system that acts like having five specialist experts
available 24/7:

```
                    Parenting Coordinator (Manager)
                              |
        +----------+----------+----------+----------+
        |          |          |          |          |
     ADHD       ASD      Developmental  Memory   Activity
     Expert    Expert      Expert       Agent    Planner
```

Each specialist focuses on their domain:

- **ADHD Expert**: Executive function, attention regulation, impulse control
- **ASD Expert**: Sensory processing, communication patterns, routine needs
- **Developmental Expert**: Age-appropriate expectations and milestones
- **Memory Agent**: Learns what works for THIS child across sessions
- **Activity Planner**: Creates structured plans with materials and timing

The **Coordinator** orchestrates these specialists, routing questions intelligently and synthesizing insights into
comprehensive, actionable guidance.

---

## ADK Capabilities Demonstrated

This project showcases **6+ capabilities** from the 5-Day AI Agents Intensive:

### Day 1: Multi-Agent Hierarchical System

- **1 Manager + 5 Specialists**: Coordinator delegates to appropriate experts based on question type
- **Agent-as-Tool Pattern**: Specialists wrapped as callable tools for the coordinator
- **Intelligent Routing**: Questions about sensory issues go to ASD Expert; executive function questions to ADHD Expert

### Day 2: Tools & Integration

- **GoogleSearchTool**: Evidence-based research from CHADD, CDC, Autism Speaks
- **3 Custom FunctionTools**:
    - `BehaviorClassifier`: Analyzes behaviors for ADHD/ASD/age-typical factors
    - `ActivityPlanner`: Creates structured activity plans with materials and timing
    - `PatternAnalyzer`: Learns from session history to identify what works

### Day 3: Memory & Context

- **Cross-Session Learning**: Memory Agent tracks successful strategies over time
- **Personalization**: Recommendations based on what worked for THIS child before
- **Pattern Recognition**: Identifies triggers and successful interventions

### Day 4: Session Management

- **InMemorySessionService**: Maintains conversation context
- **Session IDs**: Separate contexts for different scenarios
- **State Tracking**: Preserves conversation history within sessions

### Day 5: Production-Ready

- **Two-Layer Retry Strategy**: Agent-level + application-level retry handling
- **Rate Limit Handling**: Automatic backoff with jitter for 429 errors
- **Type Safety**: Strict Pydantic v2 models throughout (no `Dict[str, Any]`)

---

## Technical Excellence

The codebase follows production-grade Python best practices:

**Type-Safe Architecture**:

```python
class BehaviorAnalysis(BaseModel):
    adhd_factors: list[str]
    asd_factors: list[str]
    age_typical_factors: list[str]
    primary_driver: BehaviorFactor  # Enum, not string

    model_config = ConfigDict(strict=True, extra="forbid")
```

**Discriminated Unions for Results**:

```python
ToolResult = Union[ToolSuccess, ToolError]  # Never mixed success/error
```

**Dependency Injection**:

```python
def create_coordinator(agent_factory: AgentFactory | None = None) -> LlmAgent:
    factory = agent_factory or AgentFactory()  # Testable, no global state
```

---

## Demo Scenarios

The notebook demonstrates three real-world scenarios:

### Scenario 1: Homework Refusal Analysis

> "My 8-year-old refuses homework after school, gets frustrated, sometimes has meltdowns. Is this ADHD, autism, or just
> being 8?"

The system:

1. Coordinator routes to ADHD Expert, Developmental Expert, and potentially ASD Expert
2. BehaviorClassifier analyzes ADHD factors (task initiation, executive function) and ASD factors (transition
   difficulty, routine disruption)
3. GoogleSearch retrieves evidence-based strategies from CHADD and CDC
4. Coordinator synthesizes multi-perspective response

### Scenario 2: Bedtime Routine Planning

> "I need a structured bedtime routine. My son struggles with play-to-bed transitions. I have visual timers and fidget
> toys."

The system:

1. Activity Planner creates a complete structured plan
2. Includes materials list, environmental setup, step-by-step timing
3. Memory Agent recalls that visual timers worked well before
4. Provides success criteria and ADHD/ASD adaptations

### Scenario 3: Learning from History

> "Analyze what's worked for bedtime: Session 1 (visual timer = success), Session 2 (verbal only = failed), Session 3 (
> timer + sensory break = success)"

The system:

1. Memory Agent uses PatternAnalyzer tool
2. Identifies patterns: Visual timers 2/2 success, verbal reminders 0/1
3. Generates data-driven recommendations
4. ADHD/ASD experts explain WHY these patterns work neurologically

---

## Real-World Impact

**For Parents**:

- 24/7 access to specialist-quality guidance
- Personalized recommendations based on their child's history
- Understanding WHY behaviors happen, not just how to manage them
- Evidence-based strategies they can trust

**For Children**:

- Strategies tailored to how their brain works
- Understanding and acceptance (not punishment-focused)
- Consistent approaches across situations

**Societal Value**:

- 5-10 million children have ADHD in the US alone
- AI makes specialist knowledge accessible at scale
- Reduces family stress and improves parent-child relationships
- Earlier intervention before behaviors escalate

---

## Important Disclaimer

This is a **parenting support tool, NOT medical advice**. Always consult healthcare professionals for diagnoses,
treatment plans, and serious behavioral concerns.

---

## Links

- **Kaggle Notebook**: [Link to notebook]
- **GitHub Repository**: [https://github.com/marcuskbra/neuro-diver-agents](https://github.com/marcuskbra/neuro-diver-agents)
- **Demo Video**: [Optional - for bonus points]

---

## Acknowledgments

- Google & Kaggle for the ADK framework and Agents Intensive Course
- CHADD, Autism Speaks, and CDC for evidence-based resources
- Parents of neurodivergent children for inspiring this meaningful use case

---

*Built with care for neurodivergent children and their families*
