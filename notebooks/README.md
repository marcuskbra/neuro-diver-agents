# Kaggle Notebooks

This directory contains Jupyter notebooks for demonstrating the Neurodivergent Parenting Support Agent system.

## 📓 Available Notebooks

### `kaggle_capstone_self_contained.ipynb` (Recommended for Submission)

**Purpose**: Fully self-contained notebook for Kaggle Agents Intensive Capstone submission.

**Key Feature**: All source code is embedded using `%%writefile` cells - **no external file uploads required!**

### `kaggle_capstone_demo.ipynb`

**Purpose**: Development version of the notebook (requires separate source file upload).

---

## 🚀 Quick Start for Kaggle Submission

### Option A: Self-Contained Notebook (Recommended)

1. Run `./prepare_for_kaggle.sh` to generate the self-contained notebook
2. Go to [Kaggle Notebooks](https://www.kaggle.com/code)
3. Click "New Notebook"
4. File → Upload Notebook → Select `kaggle_capstone_self_contained.ipynb`
5. Add `GOOGLE_API_KEY` as a Kaggle secret (Add-ons → Secrets)
6. Enable internet access (Settings → Internet → On)
7. Click "Run All"

**That's it!** The notebook creates all source files automatically.

### Option B: Manual Setup (Alternative)

If you prefer to upload source files separately:

1. Create a new Kaggle notebook
2. Upload `src/` directory as a dataset
3. Extract in notebook: `!unzip /kaggle/input/your-dataset/src.zip -d /kaggle/working/`
4. Upload `kaggle_capstone_demo.ipynb`
5. Configure API key and run

---

## 📦 Generating the Self-Contained Notebook

```bash
cd notebooks/
./prepare_for_kaggle.sh
```

This runs `make_self_contained.py` which:
- Reads all Python files from `src/capstone/`
- Injects them as `%%writefile` cells into the notebook
- Creates `kaggle_capstone_self_contained.ipynb`

---

## ⚙️ Configure API Key

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
