# 🎬 Demo Guide

**Two demo versions available**: Standard and Comprehensive

---

## 🚀 Quick Start

### Prerequisites

```bash
# Set your Google AI API key
export GOOGLE_API_KEY="your-api-key-here"

# Install dependencies
uv sync
```

### Run Standard Demo (3 scenarios, ~5 minutes)

```bash
uv run python demo_agents.py
```

### Run Comprehensive Demo (6 scenarios, ~12 minutes)

```bash
uv run python demo_comprehensive.py
```

---

## 📋 Demo Comparison

| Feature            | Standard Demo    | Comprehensive Demo     |
|--------------------|------------------|------------------------|
| **Scenarios**      | 3                | 6                      |
| **Duration**       | ~5 minutes       | ~12 minutes            |
| **Output**         | Simple text      | Color-coded, formatted |
| **Metrics**        | Basic            | Detailed with summary  |
| **Tool Tracking**  | No               | Yes                    |
| **Agent Tracking** | Basic            | Comprehensive          |
| **Best For**       | Quick validation | Full presentation      |

---

## 🎯 Standard Demo (demo_agents.py)

### Scenarios Covered

1. **Homework Refusal** - Multi-factor behavior analysis
2. **Bedtime Routine** - Activity planning with materials
3. **Pattern Learning** - Analyzing session history

### What It Demonstrates

- ✅ Multi-agent orchestration
- ✅ Basic tool integration
- ✅ Retry handling
- ✅ Session management

### Expected Output

```
================================================================================
🤖 Neurodivergent Parenting Support Agent - ADK Demo
================================================================================
...
📋 SCENARIO 1: Homework Refusal Analysis
...
💬 Response:
[Coordinator provides comprehensive analysis...]
```

---

## 🌟 Comprehensive Demo (demo_comprehensive.py)

### Scenarios Covered

1. **Homework Refusal** - ADHD vs Age-Typical vs ASD
2. **Sensory Meltdown** - ASD sensory processing
3. **Bedtime Routine** - Structured activity planning
4. **Pattern Learning** - Memory agent analysis
5. **Impulsivity Assessment** - ADHD + Developmental expert
6. **Complex Multi-Factor** - ALL specialists working together

### What It Demonstrates

- ✅ All 5 specialist agents
- ✅ All 3 custom tools
- ✅ Multi-agent collaboration
- ✅ Pattern learning & memory
- ✅ Comprehensive metrics tracking
- ✅ Beautiful color-coded output
- ✅ Detailed performance analytics

### Expected Output

#### Scenario Execution

```
================================================================================
🤖 Neurodivergent Parenting Support Agent
================================================================================

System Architecture:
  🧠 Coordinator Agent (orchestrates everything)
  👥 5 Specialist Agents:
     • ADHD Expert - Executive function & attention
     • ASD Expert - Sensory processing & communication
     ...

📋 SCENARIO 1: Homework Refusal Analysis
--------------------------------------------------------------------------------
Parent's Question:
"My 8-year-old son refuses to start his homework..."

  🤔 parenting_coordinator analyzing...
  🔧 Using tool: _consult_adhd_expert
  🔧 Using tool: _consult_developmental_expert
  🔧 Using tool: _analyze_behavior_wrapper

💬 Coordinator Response:
[Comprehensive multi-agent analysis...]
```

#### Metrics Summary

```
📊 Demo Metrics Summary
--------------------------------------------------------------------------------

Overall Statistics:
  • Total Scenarios: 6
  • Successful: 6/6
  • Total Duration: 45.32s
  • Total Events: 156
  • Avg Events/Scenario: 26.0

Agents Activated:
  • parenting_coordinator: 6 scenarios
  • ADHD Specialist: 4 scenarios
  • ASD Specialist: 3 scenarios
  • Developmental Specialist: 3 scenarios
  • Memory Agent: 2 scenarios
  • Activity Planner: 2 scenarios

Tools Used:
  • _analyze_behavior_wrapper: 4 calls
  • _consult_adhd_expert: 4 calls
  • _consult_asd_expert: 3 calls
  • _consult_developmental_expert: 3 calls
  • _consult_memory_agent: 2 calls
  • _plan_activity_wrapper: 2 calls
```

---

## 🎨 Comprehensive Demo Features

### Color-Coded Output

- **Headers**: Purple/Bold
- **Info**: Blue
- **Success**: Green
- **Warnings**: Yellow
- **Errors**: Red
- **Thinking**: Cyan
- **Tool Calls**: Yellow

### Detailed Metrics

- Execution duration per scenario
- Event count tracking
- Agent activation tracking
- Tool usage statistics
- Success rate monitoring
- Error capture and reporting

### Smart Retry Handling

- Automatic retry on 429 errors
- Exponential backoff
- Rate limit detection
- User-friendly error messages
- Recovery suggestions

---

## 📊 What Each Scenario Demonstrates

### Scenario 1: Homework Refusal

**Specialists**: ADHD Expert + Developmental Expert
**Tools**: Behavior Classifier
**Shows**: Multi-factor behavioral analysis distinguishing ADHD from age-typical behavior

### Scenario 2: Sensory Meltdown

**Specialists**: ASD Expert
**Tools**: Behavior Classifier
**Shows**: Sensory processing analysis and environmental accommodation strategies

### Scenario 3: Bedtime Routine

**Specialists**: Activity Planner + Memory Agent
**Tools**: Activity Planner Tool
**Shows**: Structured activity generation with material integration

### Scenario 4: Pattern Learning

**Specialists**: Memory Agent
**Tools**: Pattern Analyzer Tool
**Shows**: Learning from session history and identifying successful patterns

### Scenario 5: Impulsivity

**Specialists**: ADHD Expert + Developmental Expert
**Tools**: Behavior Classifier
**Shows**: Distinguishing ADHD impulsivity from developmental stages

### Scenario 6: Complex Multi-Factor

**Specialists**: ALL 5 specialists
**Tools**: ALL 3 tools
**Shows**: Complete system orchestration for complex situations

---

## ⚠️ Troubleshooting

### Warning About Function Calls

**Message**: `Warning: there are non-text parts in the response: ['function_call']`

**Explanation**: This is **expected behavior**! It means the coordinator is successfully calling specialist tools. The
comprehensive demo handles this automatically.

**Fix**: Use `demo_comprehensive.py` which properly extracts text from responses.

### Rate Limit Errors (429)

**Message**: `RESOURCE_EXHAUSTED`

**Solutions**:

1. Wait 10-60 seconds between runs
2. Use the built-in retry logic (both demos have this)
3. Check quota at: https://ai.dev/usage?tab=rate-limit
4. Consider upgrading API plan for higher limits

### No API Key

**Message**: `GOOGLE_API_KEY environment variable not set`

**Solution**:

```bash
export GOOGLE_API_KEY="your-api-key-here"
```

---

## 🎯 Best Practices for Demo Presentation

### Before Running

1. ✅ Set API key environment variable
2. ✅ Check API quota has room for 6 scenarios
3. ✅ Close unnecessary terminal windows
4. ✅ Maximize terminal for best visibility

### During Demo

1. ✅ Use `demo_comprehensive.py` for full effect
2. ✅ Point out color-coded output
3. ✅ Highlight tool calls and agent thinking
4. ✅ Show metrics summary at end
5. ✅ Explain multi-agent orchestration

### Key Points to Emphasize

- **Architecture**: 1 coordinator + 5 specialists (hierarchical)
- **Tools**: 3 custom Pydantic-validated tools
- **Type Safety**: 100% typed with Pydantic v2
- **Best Practices**: 9.3/10 Python score
- **Production Ready**: Error handling, retries, metrics
- **Personalization**: Memory agent learns patterns

---

## 📝 Demo Script

### Opening (30 seconds)

> "I've built a multi-agent parenting support system for neurodivergent children.
> It uses 1 coordinator agent that orchestrates 5 specialist agents, each with
> domain expertise in ADHD, autism, child development, memory, and activity planning."

### During Scenarios (60 seconds each)

> "Watch how the coordinator intelligently routes questions to the right specialists.
> See the tool calls? That's the ADHD Expert being consulted. Now the Developmental Expert.
> The Behavior Classifier tool is analyzing whether this is ADHD, autism, or age-typical."

### Metrics Summary (30 seconds)

> "Here are the metrics. You can see all 5 agents were activated across 6 scenarios.
> The Behavior Classifier was used 4 times, Activity Planner twice. Average response
> time was 7-8 seconds per scenario with full multi-agent orchestration."

### Closing (30 seconds)

> "This demonstrates Day 1 (multi-agent), Day 2 (custom tools), and Day 3 (memory).
> The codebase follows Python best practices with 9.3/10 score: type hints, Pydantic v2,
> modern syntax, dependency injection, and comprehensive testing."

---

## 🚀 Next Steps After Demo

### For Development

```bash
# Run tests
uv run pytest tests/unit/ -v

# Check type safety
uv run ty check src/

# Check code quality
uv run ruff check src/
```

### For Submission

- ✅ All code in `src/capstone/`
- ✅ Demo scripts ready
- ✅ Tests passing (16/16)
- ✅ Documentation complete
- ✅ Best practices score: 9.3/10

---

## 📈 Performance Expectations

### Standard Demo

- **Duration**: 3-5 minutes
- **API Calls**: ~15-20
- **Success Rate**: >95%

### Comprehensive Demo

- **Duration**: 10-15 minutes
- **API Calls**: ~40-50
- **Success Rate**: >90%
- **Metrics**: Comprehensive tracking

### System Requirements

- **Python**: 3.12+
- **Memory**: ~100MB
- **Network**: Stable connection to Google AI API
- **Terminal**: Color support recommended

---

## 💡 Tips for Best Results

1. **Run comprehensive demo** for presentations
2. **Use wide terminal** (≥80 columns) for formatting
3. **Enable terminal colors** for visual impact
4. **Allow 15 minutes** for full comprehensive demo
5. **Have backup plan** for rate limits (show metrics from previous run)
6. **Highlight code quality** in discussion (Pydantic, types, DI)
7. **Explain AgentFactory** pattern (no global state)

---

**Questions?** Check `IMPROVEMENTS_IMPLEMENTED.md` for architecture details and `README.md` for project overview.
