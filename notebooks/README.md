# Kaggle Notebooks

This directory contains Jupyter notebooks for demonstrating the Neurodivergent Parenting Support Agent system.

## 📓 Available Notebooks

### `kaggle_capstone_demo.ipynb`

**Purpose**: Complete demonstration of the multi-agent system for Kaggle Agents Intensive Capstone submission.

**Contents**:

1. Project overview and architecture explanation
2. Setup and installation instructions
3. API key configuration for Kaggle
4. Three interactive demo scenarios:
    - Scenario 1: Homework refusal behavioral analysis
    - Scenario 2: Bedtime routine activity planning
    - Scenario 3: Pattern learning from session history
5. Comprehensive capability showcase (6+ ADK features)
6. Results analysis and conclusions

**Requirements**:

- Google AI API key (get at: https://aistudio.google.com/app/apikey)
- Project source code uploaded to Kaggle notebook

---

## 🚀 Running on Kaggle

### Step 1: Create New Notebook

1. Go to [Kaggle Notebooks](https://www.kaggle.com/code)
2. Click "New Notebook"
3. Choose "Python" notebook type

### Step 2: Upload Project Files

You need to upload the `src/` directory to your Kaggle notebook:

**Option A: Direct Upload**

1. Create a new notebook
2. Click "Add Data" → "Upload" → "New Dataset"
3. Upload the entire `src/` directory as a zip file
4. Extract in the notebook: `!unzip /kaggle/input/your-dataset/src.zip -d /kaggle/working/`

**Option B: GitHub Integration**

1. Push your project to GitHub
2. In Kaggle notebook: "Add Data" → "GitHub"
3. Connect your repository
4. Copy files to working directory

**Required directory structure**:

```
/kaggle/working/
└── src/
    └── capstone/
        ├── models/
        │   ├── __init__.py
        │   ├── behavior.py
        │   ├── activity.py
        │   ├── strategy.py
        │   ├── memory.py
        │   └── results.py
        ├── tools/
        │   ├── __init__.py
        │   ├── behavior_classifier.py
        │   ├── activity_planner.py
        │   └── pattern_analyzer.py
        └── agents/
            ├── __init__.py
            ├── retry_config.py
            ├── adhd_expert.py
            ├── asd_expert.py
            ├── developmental_expert.py
            ├── memory_agent.py
            ├── activity_planner_agent.py
            └── coordinator.py
```

### Step 3: Configure API Key

**Recommended: Use Kaggle Secrets**

1. In your notebook, go to "Add-ons" → "Secrets"
2. Click "Add a new secret"
3. Name: `GOOGLE_API_KEY`
4. Value: Your Google AI API key
5. The notebook will automatically retrieve it

**Alternative: Set in Notebook**

```python
import os

os.environ['GOOGLE_API_KEY'] = "your-api-key-here"
```

### Step 4: Import Notebook

1. Download `kaggle_capstone_demo.ipynb` from this directory
2. In Kaggle: "File" → "Upload Notebook"
3. Select the downloaded `.ipynb` file
4. Enable internet access: Settings → Internet → On

### Step 5: Run the Notebook

Click "Run All" or execute cells sequentially to see the complete demonstration.

---

## 🧪 Running Locally

If you want to test the notebook locally before uploading to Kaggle:

```bash
# Install Jupyter
uv add --dev jupyter notebook

# Start Jupyter
uv run jupyter notebook

# Navigate to notebooks/kaggle_capstone_demo.ipynb
```

**Modifications needed for local execution:**

1. Remove the Kaggle secrets cell (use environment variable instead)
2. Update paths if your source directory is elsewhere
3. Ensure `GOOGLE_API_KEY` is set in your environment

---

## 📊 What Gets Demonstrated

### ADK Capabilities (6+)

| Capability                | Demonstration                                        |
|---------------------------|------------------------------------------------------|
| **Multi-agent hierarchy** | Manager + 5 specialist agents                        |
| **AgentTool pattern**     | Specialists wrapped as tools                         |
| **Custom FunctionTools**  | BehaviorClassifier, ActivityPlanner, PatternAnalyzer |
| **GoogleSearchTool**      | Evidence-based research integration                  |
| **Memory & learning**     | Pattern analysis from session history                |
| **Session management**    | State tracking with InMemorySessionService           |
| **Error handling**        | Two-layer retry strategy (ADK best practices)        |

### Type Safety Features

- ✅ No `Dict[str, Any]` for domain data
- ✅ Discriminated unions (Success | Error)
- ✅ Enums for constants
- ✅ Pydantic v2 strict validation
- ✅ Field constraints and validators

### Real-World Scenarios

1. **Behavioral Analysis**: Understanding if behavior is ADHD, ASD, or age-typical
2. **Activity Planning**: Creating structured routines with materials and timing
3. **Pattern Learning**: Identifying what strategies work for a specific child

---

## 🔍 Troubleshooting

### "Module not found: src.capstone"

**Problem**: Source files not in the correct location.

**Solution**: Ensure the `src/` directory is in `/kaggle/working/` (not `/kaggle/input/`)

```python
# Verify structure
!ls - la / kaggle / working / src / capstone /
```

### "GOOGLE_API_KEY not found"

**Problem**: API key not configured.

**Solution**: Add it as a Kaggle secret (recommended) or set it manually:

```python
import os

os.environ['GOOGLE_API_KEY'] = "your-key-here"
```

### "429 RESOURCE_EXHAUSTED errors"

**Problem**: Rate limits on free tier API.

**Solution**: The notebook includes automatic retry logic. If persistent:

1. Wait a few minutes between runs
2. Check quota at: https://ai.dev/usage?tab=rate-limit
3. Consider upgrading API plan

### "ImportError: cannot import name 'create_coordinator'"

**Problem**: `__init__.py` files missing or incorrect.

**Solution**: Ensure all `__init__.py` files export correctly:

```python
# src/capstone/agents/__init__.py should contain:
from .coordinator import create_coordinator
```

---

## 📝 Submission Checklist

Before submitting to Kaggle:

- [ ] Notebook runs without errors
- [ ] All 3 demo scenarios execute successfully
- [ ] API key configured via Kaggle secrets (not hardcoded)
- [ ] Internet access enabled in notebook settings
- [ ] Output cells show agent responses
- [ ] Markdown cells explain what's happening
- [ ] Architecture diagrams are visible
- [ ] Resource links are working
- [ ] Disclaimer is included

---

## 🎯 Evaluation Criteria

Your Kaggle Capstone will be evaluated on:

1. **ADK Capability Demonstration** (40%)
    - Multi-agent system
    - Tool integration
    - Memory/context
    - Session management

2. **Code Quality** (30%)
    - Type safety
    - Error handling
    - Documentation
    - Best practices

3. **Real-World Application** (20%)
    - Problem solving
    - User value
    - Practicality
    - Innovation

4. **Presentation** (10%)
    - Notebook clarity
    - Explanation quality
    - Visual elements
    - Professional polish

---

## 💡 Tips for Success

### Before Submission

1. **Test thoroughly**: Run the notebook multiple times to ensure consistency
2. **Check outputs**: Make sure all cells executed and show results
3. **Proofread**: Review markdown cells for typos and clarity
4. **Time management**: Account for API rate limits in demo timing
5. **Backup**: Save copies of your notebook regularly

### During Presentation

1. **Explain architecture**: Use the diagrams to walk through the system
2. **Highlight capabilities**: Point out each ADK feature being demonstrated
3. **Show real results**: Let the agents generate live responses
4. **Discuss design choices**: Why hierarchical? Why these specialists?
5. **Address limitations**: Be honest about free tier constraints

### After Submission

1. **Share on GitHub**: Make your code available for others to learn from
2. **Write a blog post**: Document your learning journey
3. **Join community**: Engage with other capstone participants
4. **Iterate**: Continue improving based on feedback

---

## 🔗 Resources

- [Kaggle Notebooks Documentation](https://www.kaggle.com/docs/notebooks)
- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Project Main README](../README.md)
- [Retry Strategy Documentation](../RETRY_STRATEGY.md)

---

## 📧 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review ADK documentation for API changes
3. Verify Google AI API key has not expired
4. Check Kaggle community forums for similar issues

---

**Good luck with your Capstone submission! 🎉**
