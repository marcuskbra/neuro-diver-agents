# API Reference

Complete API documentation for the NeuroDiverAgents capstone project.

---

## Table of Contents

- [Models](#models)
    - [Behavior Models](#behavior-models)
    - [Activity Models](#activity-models)
    - [Memory Models](#memory-models)
    - [Strategy Models](#strategy-models)
    - [Result Models](#result-models)
- [Tools](#tools)
    - [Behavior Classifier](#behavior-classifier)
    - [Activity Planner](#activity-planner)
    - [Pattern Analyzer](#pattern-analyzer)
- [Agents](#agents)
    - [Coordinator](#coordinator)
    - [Specialist Factory](#specialist-factory)
    - [Agent Factory](#agent-factory)

---

## Models

All models use Pydantic v2 with strict validation, type safety, and immutability where appropriate.

### Behavior Models

**Module**: `capstone.models.behavior`

#### Enums

##### `BehaviorFactor`

Behavioral factor categories for classification.

```python
class BehaviorFactor(str, Enum):
    ADHD = "adhd"
    ASD = "asd"
    AGE_TYPICAL = "age_typical"
    COMBINED = "combined"
```

##### `TimeOfDay`

Time periods for behavior tracking.

```python
class TimeOfDay(str, Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    BEDTIME = "bedtime"
```

##### `ActivityType`

Types of activities for context.

```python
class ActivityType(str, Enum):
    SCHOOL = "school"
    HOMEWORK = "homework"
    PLAY = "play"
    TRANSITIONS = "transitions"
    MEALS = "meals"
    BEDTIME_ROUTINE = "bedtime_routine"
    HYGIENE = "hygiene"
```

#### Classes

##### `BehaviorInput`

Input model for behavior analysis.

| Field           | Type           | Constraints      | Description                 |
|-----------------|----------------|------------------|-----------------------------|
| `description`   | `str`          | min=10, max=1000 | Description of the behavior |
| `time_of_day`   | `TimeOfDay`    | required         | When the behavior occurred  |
| `activity_type` | `ActivityType` | required         | Type of activity            |
| `context`       | `str`          | min=5, max=500   | Additional context          |

**Example:**

```python
from capstone.models.behavior import BehaviorInput, TimeOfDay, ActivityType

behavior = BehaviorInput(
    description="Child struggles to start homework, keeps getting distracted",
    time_of_day=TimeOfDay.AFTERNOON,
    activity_type=ActivityType.HOMEWORK,
    context="After school, quiet room, no screens nearby"
)
```

##### `BehaviorAnalysis`

Result of behavior classification (immutable).

| Field                 | Type             | Description                     |
|-----------------------|------------------|---------------------------------|
| `adhd_factors`        | `list[str]`      | Identified ADHD-related factors |
| `asd_factors`         | `list[str]`      | Identified ASD-related factors  |
| `age_typical_factors` | `list[str]`      | Age-typical behavioral factors  |
| `primary_driver`      | `BehaviorFactor` | Primary behavioral driver       |

---

### Activity Models

**Module**: `capstone.models.activity`

#### Enums

##### `ActivityGoal`

Activity goal categories.

```python
class ActivityGoal(str, Enum):
    ENGAGEMENT = "engagement"
    EXECUTIVE_FUNCTION = "executive_function"
    TRANSITION_SUPPORT = "transition_support"
    HOMEWORK_SUPPORT = "homework_support"
```

#### Classes

##### `ActivityRequest`

Request for activity planning.

| Field                 | Type           | Constraints | Description           |
|-----------------------|----------------|-------------|-----------------------|
| `goal`                | `ActivityGoal` | required    | Goal of the activity  |
| `duration_minutes`    | `int`          | 5-120       | Duration in minutes   |
| `available_materials` | `list[str]`    | optional    | Available materials   |
| `specific_needs`      | `str \| None`  | max=500     | Specific requirements |

**Example:**

```python
from capstone.models.activity import ActivityRequest, ActivityGoal

request = ActivityRequest(
    goal=ActivityGoal.HOMEWORK_SUPPORT,
    duration_minutes=30,
    available_materials=["timer", "fidget toys"],
    specific_needs="Child has difficulty with math"
)
```

##### `ActivityPlan`

Complete activity plan with preparation details.

| Field                 | Type           | Constraints    | Description              |
|-----------------------|----------------|----------------|--------------------------|
| `name`                | `str`          | min=5, max=100 | Activity name            |
| `goal`                | `ActivityGoal` | required       | Activity goal            |
| `materials`           | `list[str]`    | min=1          | Required materials       |
| `environmental_setup` | `str`          | min=10         | Setup instructions       |
| `duration_minutes`    | `int`          | 5-120          | Duration in minutes      |
| `structure`           | `list[str]`    | min=1          | Step-by-step structure   |
| `success_criteria`    | `list[str]`    | min=1          | Success indicators       |
| `adaptations`         | `list[str]`    | optional       | Adaptation strategies    |
| `from_memory`         | `str \| None`  | optional       | Past successful patterns |

---

### Memory Models

**Module**: `capstone.models.memory`

#### Classes

##### `SessionOutcome`

Outcome of a strategy application.

| Field           | Type       | Constraints    | Description                     |
|-----------------|------------|----------------|---------------------------------|
| `strategy_used` | `str`      | min=5          | Strategy that was applied       |
| `worked`        | `bool`     | required       | Whether strategy was successful |
| `notes`         | `str`      | min=5, max=500 | Observation notes               |
| `timestamp`     | `datetime` | auto           | When the session occurred       |

**Example:**

```python
from capstone.models.memory import SessionOutcome

outcome = SessionOutcome(
    strategy_used="Visual timer with 5-minute warnings",
    worked=True,
    notes="Child responded well to countdown, minimal resistance"
)
```

##### `BehaviorPattern`

Identified behavioral pattern (immutable).

| Field                     | Type        | Constraints | Description             |
|---------------------------|-------------|-------------|-------------------------|
| `behavior_type`           | `str`       | min=3       | Type of behavior        |
| `common_triggers`         | `list[str]` | optional    | Common triggers         |
| `successful_strategies`   | `list[str]` | optional    | What works              |
| `unsuccessful_approaches` | `list[str]` | optional    | What doesn't work       |
| `frequency_count`         | `int`       | ≥0          | Success frequency       |
| `sessions_analyzed`       | `int`       | ≥1          | Total sessions analyzed |

**Validation:** `frequency_count` cannot exceed `sessions_analyzed`.

---

### Strategy Models

**Module**: `capstone.models.strategy`

#### Classes

##### `Strategy`

Individual strategy recommendation (immutable).

| Field                | Type        | Constraints     | Description          |
|----------------------|-------------|-----------------|----------------------|
| `title`              | `str`       | min=5, max=100  | Strategy title       |
| `description`        | `str`       | min=10, max=500 | Detailed description |
| `rationale`          | `str`       | min=10, max=300 | Why this works       |
| `success_indicators` | `list[str]` | min=1           | Success indicators   |

##### `BehaviorResponse`

Complete behavioral analysis response (immutable).

| Field                  | Type               | Constraints     | Description               |
|------------------------|--------------------|-----------------|---------------------------|
| `acknowledgment`       | `str`              | min=10, max=200 | Empathetic acknowledgment |
| `analysis`             | `BehaviorAnalysis` | required        | Behavioral analysis       |
| `strategies`           | `list[Strategy]`   | 1-5             | Recommended strategies    |
| `proactive_suggestion` | `str \| None`      | max=300         | Proactive tip             |
| `disclaimer`           | `Literal[...]`     | fixed           | Medical disclaimer        |

---

### Result Models

**Module**: `capstone.models.results`

#### Type Alias

```python
ToolResult = ToolSuccess | ToolError
```

#### Classes

##### `ToolSuccess`

Successful tool execution result (immutable).

| Field     | Type             | Description   |
|-----------|------------------|---------------|
| `success` | `Literal[True]`  | Always `True` |
| `data`    | `dict[str, ...]` | Result data   |

**Type-Safe Accessors:**

```python
result.get_str("key", default="")  # Get string value
result.get_int("key", default=0)  # Get integer value
result.get_float("key", default=0.0)  # Get float value
result.get_bool("key", default=False)  # Get boolean value
result.get_list("key", default=[])  # Get list value
```

##### `ToolError`

Tool execution error (immutable).

| Field           | Type             | Constraints    | Description            |
|-----------------|------------------|----------------|------------------------|
| `success`       | `Literal[False]` | Always `False` |
| `error_code`    | `str`            | min=1          | Error code identifier  |
| `error_message` | `str`            | min=1          | Human-readable message |

#### Type Guards

```python
from capstone.models.results import is_success, is_error, ToolResult


def handle_result(result: ToolResult) -> str:
    if is_success(result):  # Narrows type to ToolSuccess
        return result.get_str("message")
    else:  # Narrows type to ToolError
        return f"Error: {result.error_message}"
```

---

## Tools

All tools return `ToolResult` (discriminated union of `ToolSuccess | ToolError`).

### Behavior Classifier

**Module**: `capstone.tools.behavior_classifier`

#### `classify_behavior()`

Classify behavior into ADHD/ASD/age-typical factors.

```python
def classify_behavior(behavior_input: BehaviorInput) -> ToolResult:
    """
    Classify behavior into ADHD/ASD/age-typical factors.

    Args:
        behavior_input: Validated behavior input with description and context

    Returns:
        ToolResult: Success with classification or Error with details
    """
```

**Success Data Keys:**

- `adhd_factors`: `list[str]` - Identified ADHD factors
- `asd_factors`: `list[str]` - Identified ASD factors
- `age_typical_factors`: `list[str]` - Age-typical factors
- `primary_driver`: `str` - Primary behavioral driver

**Error Codes:**

- `CLASSIFICATION_ERROR` - General classification failure

**Example:**

```python
from capstone.tools.behavior_classifier import classify_behavior
from capstone.models.behavior import BehaviorInput, TimeOfDay, ActivityType
from capstone.models.results import is_success

behavior = BehaviorInput(
    description="Child can't focus on homework, keeps looking around",
    time_of_day=TimeOfDay.AFTERNOON,
    activity_type=ActivityType.HOMEWORK,
    context="Quiet room after school"
)

result = classify_behavior(behavior)

if is_success(result):
    print(f"Primary driver: {result.get_str('primary_driver')}")
    print(f"ADHD factors: {result.get_list('adhd_factors')}")
```

---

### Activity Planner

**Module**: `capstone.tools.activity_planner`

#### `get_activity_plan()`

Get structured activity plan based on goal.

```python
def get_activity_plan(request: ActivityRequest) -> ToolResult:
    """
    Get structured activity plan based on goal.

    Args:
        request: Validated activity request with goal and constraints

    Returns:
        ToolResult: Success with ActivityPlan or Error if goal not found
    """
```

**Success Data Keys:**

- `name`: `str` - Activity name
- `goal`: `str` - Activity goal
- `materials`: `list[str]` - Required materials
- `setup`: `str` - Environmental setup instructions
- `duration`: `int` - Duration in minutes
- `structure`: `list[str]` - Step-by-step structure
- `success_criteria`: `list[str]` - Success indicators
- `adaptations`: `list[str]` - Adaptation strategies

**Error Codes:**

- `INVALID_GOAL` - Unsupported activity goal
- `PLANNING_ERROR` - General planning failure

**Example:**

```python
from capstone.tools.activity_planner import get_activity_plan
from capstone.models.activity import ActivityRequest, ActivityGoal
from capstone.models.results import is_success

request = ActivityRequest(
    goal=ActivityGoal.EXECUTIVE_FUNCTION,
    duration_minutes=15
)

result = get_activity_plan(request)

if is_success(result):
    print(f"Activity: {result.get_str('name')}")
    print(f"Materials: {result.get_list('materials')}")
```

---

### Pattern Analyzer

**Module**: `capstone.tools.pattern_analyzer`

#### `analyze_patterns()`

Analyze behavioral patterns from session history.

```python
def analyze_patterns(
        session_history: list[SessionOutcome],
        behavior_type: str,
) -> ToolResult:
    """
    Analyze behavioral patterns from session history.

    Args:
        session_history: List of validated session outcomes
        behavior_type: Type of behavior to analyze (e.g., "bedtime", "homework")

    Returns:
        ToolResult: Success with BehaviorPattern or Error if insufficient data
    """
```

**Success Data Keys:**

- `behavior_type`: `str` - Type of behavior analyzed
- `common_triggers`: `list[str]` - Identified triggers
- `successful_strategies`: `list[str]` - What works
- `unsuccessful_approaches`: `list[str]` - What doesn't work
- `frequency`: `int` - Success frequency count
- `sessions`: `int` - Total sessions analyzed

**Error Codes:**

- `INSUFFICIENT_DATA` - Need at least 1 session
- `NO_MATCHING_SESSIONS` - No sessions found for behavior type
- `ANALYSIS_ERROR` - General analysis failure

**Example:**

```python
from capstone.tools.pattern_analyzer import analyze_patterns
from capstone.models.memory import SessionOutcome
from capstone.models.results import is_success

history = [
    SessionOutcome(
        strategy_used="Visual timer for bedtime",
        worked=True,
        notes="Child responded well, minimal resistance"
    ),
    SessionOutcome(
        strategy_used="Verbal countdown for bedtime",
        worked=False,
        notes="Screen time before bed caused issues"
    )
]

result = analyze_patterns(history, "bedtime")

if is_success(result):
    print(f"Successful strategies: {result.get_list('successful_strategies')}")
    print(f"Triggers: {result.get_list('common_triggers')}")
```

---

## Agents

### Coordinator

**Module**: `capstone.agents.coordinator`

#### `create_coordinator()`

Create the parenting coordinator agent that orchestrates all specialists.

```python
def create_coordinator(agent_factory: AgentFactory | None = None) -> LlmAgent:
    """
    Create parenting coordinator agent with dependency injection.

    This agent orchestrates 5 specialist agents:
    1. ADHD Expert - Executive function and attention challenges
    2. ASD Expert - Sensory processing and communication patterns
    3. Developmental Expert - Age-appropriate expectations
    4. Memory Agent - Pattern learning from past experiences
    5. Activity Planner - Structured activity recommendations

    Args:
        agent_factory: Optional AgentFactory for dependency injection.
                      If None, creates a new factory instance.

    Returns:
        Configured LlmAgent coordinator instance.
    """
```

**Tools Available to Coordinator:**

- `_consult_adhd_expert(question: str)` - Consult ADHD specialist
- `_consult_asd_expert(question: str)` - Consult ASD specialist
- `_consult_developmental_expert(question: str)` - Consult developmental specialist
- `_consult_memory_agent(question: str)` - Consult memory agent
- `_consult_activity_planner(question: str)` - Consult activity planner
- `_analyze_behavior_wrapper(...)` - Direct behavior analysis
- `_plan_activity_wrapper(...)` - Direct activity planning
- `_analyze_patterns_wrapper(...)` - Direct pattern analysis

**Example:**

```python
from capstone.agents.coordinator import create_coordinator
from capstone.infrastructure.agent_factory import AgentFactory

# With dependency injection
factory = AgentFactory()
coordinator = create_coordinator(agent_factory=factory)

# Or use default factory
coordinator = create_coordinator()
```

---

### Specialist Factory

**Module**: `capstone.agents.specialist_factory`

Functions for creating individual specialist agents.

#### `create_adhd_expert()`

Create ADHD specialist agent with executive function expertise.

#### `create_asd_expert()`

Create ASD specialist agent with sensory processing expertise.

#### `create_developmental_expert()`

Create developmental specialist with age-appropriate expectations.

#### `create_memory_agent()`

Create memory agent for pattern learning.

#### `create_activity_planner_agent()`

Create activity planning specialist.

#### `create_agent_by_type()`

Create any specialist agent by type name.

```python
def create_agent_by_type(agent_type: AgentType) -> LlmAgent:
    """
    Create a specialist agent by type.

    Args:
        agent_type: One of "adhd_expert", "asd_expert", "developmental_expert",
                   "memory_agent", "activity_planner_agent"

    Returns:
        Configured LlmAgent instance.
    """
```

---

### Agent Factory

**Module**: `capstone.infrastructure.agent_factory`

#### `AgentFactory`

Factory class for creating and caching specialist agents.

```python
class AgentFactory:
    """
    Factory for creating specialist agents with caching.

    Implements the Factory pattern with built-in caching to avoid
    recreating agents during a session.
    """

    def get_adhd_expert(self) -> LlmAgent: ...

    def get_asd_expert(self) -> LlmAgent: ...

    def get_developmental_expert(self) -> LlmAgent: ...

    def get_memory_agent(self, tools: list) -> LlmAgent: ...

    def get_activity_planner_agent(self, tools: list) -> LlmAgent: ...
```

**Example:**

```python
from capstone.infrastructure.agent_factory import AgentFactory

factory = AgentFactory()

# First call creates agent
adhd_expert = factory.get_adhd_expert()

# Second call returns cached instance
same_expert = factory.get_adhd_expert()

assert adhd_expert is same_expert  # True - same instance
```

---

## Type Safety Patterns

### Discriminated Unions

All tools return `ToolResult = ToolSuccess | ToolError`:

```python
from capstone.models.results import ToolResult, is_success, is_error


def process_result(result: ToolResult) -> str:
    if is_success(result):
        # Type narrowed to ToolSuccess
        return result.get_str("data")
    else:
        # Type narrowed to ToolError
        return f"Error {result.error_code}: {result.error_message}"
```

### Pydantic ConfigDict

All models use consistent configuration:

```python
model_config = ConfigDict(
    validate_assignment=True,  # Validate on attribute changes
    strict=True,  # No type coercion
    extra="forbid",  # No extra fields
    frozen=True,  # Immutable (where appropriate)
)
```

### Enums Over Strings

Always use enums for categorical data:

```python
# Good
activity_type: ActivityType = ActivityType.HOMEWORK

# Bad - avoid string literals
activity_type: str = "homework"  # No type safety!
```

---

## Error Handling

### Error Code Reference

| Code                   | Tool                | Description                    |
|------------------------|---------------------|--------------------------------|
| `CLASSIFICATION_ERROR` | behavior_classifier | General classification failure |
| `INVALID_GOAL`         | activity_planner    | Unsupported activity goal      |
| `PLANNING_ERROR`       | activity_planner    | General planning failure       |
| `INSUFFICIENT_DATA`    | pattern_analyzer    | Need at least 1 session        |
| `NO_MATCHING_SESSIONS` | pattern_analyzer    | No sessions for behavior type  |
| `ANALYSIS_ERROR`       | pattern_analyzer    | General analysis failure       |

### Best Practices

```python
from capstone.models.results import ToolResult, is_success, ToolError


def safe_operation(result: ToolResult) -> str:
    match result:
        case _ if is_success(result):
            return f"Success: {result.data}"
        case ToolError(error_code="INSUFFICIENT_DATA"):
            return "Need more session data"
        case ToolError(error_code=code, error_message=msg):
            return f"Error [{code}]: {msg}"
```
