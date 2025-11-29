# Deployment Guide

This guide covers deploying the NeuroDiverAgents system for both Kaggle notebook submission and production Cloud Run deployment.

---

## Kaggle Notebook Deployment

### Prerequisites

1. Kaggle account with notebook access
2. Google AI API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### Step 1: Set Up Kaggle Secrets

1. Go to your Kaggle account settings
2. Navigate to **Account** > **API** section
3. Click **Add Secret**
4. Add your API key:
   - **Label**: `GOOGLE_API_KEY`
   - **Value**: Your Google AI API key

### Step 2: Upload the Project

**Option A: Use the Self-Contained Notebook**

The easiest approach is to use the self-contained notebook that includes all code inline:

```bash
# Generate the self-contained notebook
python make_self_contained.py

# Upload: notebooks/kaggle_capstone_self_contained.ipynb
```

**Option B: Upload as Dataset + Notebook**

1. Create a new Kaggle dataset with the `src/` directory
2. Import the notebook and reference the dataset
3. Install dependencies in the first cell

### Step 3: Configure Notebook Settings

In your Kaggle notebook settings:

1. **Enable Internet Access**: Required for Google AI API calls
2. **Enable GPU** (optional): Not required, but may improve performance
3. **Attach Secrets**: Enable the `GOOGLE_API_KEY` secret

### Step 4: Run the Notebook

```python
# First cell - Setup (if using Option B)
import sys
sys.path.insert(0, '/kaggle/input/your-dataset-name/src')

# Load API key from Kaggle secrets
from kaggle_secrets import UserSecretsClient
user_secrets = UserSecretsClient()
import os
os.environ['GOOGLE_API_KEY'] = user_secrets.get_secret("GOOGLE_API_KEY")
```

### Submission Checklist

- [ ] All cells execute without errors
- [ ] API key loaded from secrets (not hardcoded!)
- [ ] Internet access enabled
- [ ] Output cells show agent responses
- [ ] Markdown explanations are clear

---

## Cloud Run Deployment

Deploy the agent system as a scalable API service on Google Cloud Run.

### Prerequisites

1. Google Cloud account with billing enabled
2. `gcloud` CLI installed and authenticated
3. Docker installed locally

### Project Structure for Deployment

```
deployment/
├── Dockerfile
├── main.py              # FastAPI application
├── requirements.txt
└── .env.example
```

### Step 1: Create the FastAPI Application

Create `deployment/main.py`:

```python
"""FastAPI application for NeuroDiverAgents."""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Import your agents
from google.adk.agents import ParallelAgent, SequentialAgent

from capstone.agents import (
    create_adhd_expert,
    create_asd_expert,
    create_developmental_expert,
)
from capstone.infrastructure.agent_factory import AgentFactory


class QueryRequest(BaseModel):
    """Request model for agent queries."""

    query: str = Field(..., min_length=10, max_length=2000)
    use_parallel: bool = Field(default=True, description="Use parallel expert consultation")


class QueryResponse(BaseModel):
    """Response model for agent queries."""

    response: str
    agents_consulted: list[str]


# Application lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources on startup."""
    # Validate API key is present
    if not os.environ.get("GOOGLE_API_KEY"):
        raise RuntimeError("GOOGLE_API_KEY environment variable required")

    # Pre-initialize agent factory
    app.state.factory = AgentFactory()
    yield
    # Cleanup
    app.state.factory.clear_cache()


app = FastAPI(
    title="NeuroDiverAgents API",
    description="AI-powered support for parents of neurodivergent children",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health_check():
    """Health check endpoint for Cloud Run."""
    return {"status": "healthy"}


@app.post("/query", response_model=QueryResponse)
async def query_agents(request: QueryRequest):
    """Query the agent system."""
    try:
        factory: AgentFactory = app.state.factory

        if request.use_parallel:
            # Use ParallelAgent for concurrent consultation
            panel = ParallelAgent(
                name="parallel_expert_panel",
                description="Consults experts in parallel",
                sub_agents=[
                    factory.get_adhd_expert(),
                    factory.get_asd_expert(),
                    factory.get_developmental_expert(),
                ],
            )
            agents_used = ["adhd_expert", "asd_expert", "developmental_expert"]
        else:
            # Use SequentialAgent for structured analysis
            panel = SequentialAgent(
                name="behavior_analysis_pipeline",
                description="Sequential behavior analysis pipeline",
                sub_agents=[
                    factory.get_adhd_expert(),
                    factory.get_asd_expert(),
                    factory.get_developmental_expert(),
                ],
            )
            agents_used = ["behavior_analysis_pipeline"]

        # Execute query (placeholder - integrate with actual ADK runner)
        response_text = f"Query processed: {request.query}"

        return QueryResponse(
            response=response_text,
            agents_consulted=agents_used,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/agents")
async def list_agents():
    """List available agents and their capabilities."""
    return {
        "agents": [
            {
                "name": "adhd_expert",
                "description": "ADHD specialist with executive function focus",
                "tools": ["GoogleSearch", "BehaviorClassifier"],
            },
            {
                "name": "asd_expert",
                "description": "ASD specialist with sensory processing focus",
                "tools": ["GoogleSearch", "BehaviorClassifier"],
            },
            {
                "name": "developmental_expert",
                "description": "Child development specialist",
                "tools": ["GoogleSearch"],
            },
        ],
        "orchestration_patterns": [
            {
                "name": "parallel_expert_panel",
                "description": "Consult all experts simultaneously",
            },
            {
                "name": "research_pipeline",
                "description": "Sequential Research -> Analyze -> Synthesize",
            },
        ],
    }
```

### Step 2: Create Dockerfile

Create `deployment/Dockerfile`:

```dockerfile
# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY deployment/main.py .

# Set Python path
ENV PYTHONPATH=/app/src

# Cloud Run sets PORT environment variable
ENV PORT=8080

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### Step 3: Create Requirements

Create `deployment/requirements.txt`:

```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
google-adk>=0.1.0
```

### Step 4: Deploy to Cloud Run

```bash
# Set your project ID
export PROJECT_ID=your-project-id
export REGION=us-central1
export SERVICE_NAME=neurodiveragents

# Build and push container
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
    --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --set-env-vars GOOGLE_API_KEY=your-api-key \
    --memory 1Gi \
    --cpu 1 \
    --min-instances 0 \
    --max-instances 10
```

### Step 5: Configure Secret Manager (Recommended)

For production, use Secret Manager instead of environment variables:

```bash
# Create secret
echo -n "your-api-key" | gcloud secrets create google-api-key --data-file=-

# Grant Cloud Run access
gcloud secrets add-iam-policy-binding google-api-key \
    --member serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com \
    --role roles/secretmanager.secretAccessor

# Deploy with secret reference
gcloud run deploy $SERVICE_NAME \
    --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
    --platform managed \
    --region $REGION \
    --set-secrets GOOGLE_API_KEY=google-api-key:latest
```

### API Usage Examples

Once deployed, use the API:

```bash
# Health check
curl https://your-service-url/health

# Query agents (parallel mode)
curl -X POST https://your-service-url/query \
    -H "Content-Type: application/json" \
    -d '{"query": "My 8-year-old has trouble transitioning between activities", "use_parallel": true}'

# Query agents (sequential mode)
curl -X POST https://your-service-url/query \
    -H "Content-Type: application/json" \
    -d '{"query": "Analyze bedtime routine challenges", "use_parallel": false}'

# List available agents
curl https://your-service-url/agents
```

---

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google AI API key for Gemini models | Yes |
| `PORT` | Server port (Cloud Run sets automatically) | No (default: 8080) |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | No (default: INFO) |

---

## Monitoring and Logging

### Cloud Run Logging

View logs in Google Cloud Console or via CLI:

```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=$SERVICE_NAME" --limit 50
```

### Metrics to Monitor

1. **Request Latency**: Agent responses should complete within 30s
2. **Error Rate**: Monitor for API errors and agent failures
3. **Cold Start Time**: First request after scale-to-zero may be slower
4. **Memory Usage**: Monitor if approaching 1Gi limit

### Alerting

Set up alerts for:
- Error rate > 5%
- Latency p95 > 30s
- Memory usage > 80%

---

## Security Considerations

1. **API Key Protection**: Never commit API keys to source control
2. **Authentication**: Consider adding API key authentication for production
3. **Rate Limiting**: Implement rate limiting to prevent abuse
4. **Input Validation**: All inputs validated via Pydantic models
5. **CORS**: Configure CORS appropriately for your frontend

### Adding Authentication

```python
from fastapi import Security
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

@app.post("/query")
async def query_agents(
    request: QueryRequest,
    api_key: str = Security(api_key_header),
):
    if api_key != os.environ.get("CLIENT_API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API key")
    # ... rest of implementation
```

---

## Cost Optimization

### Cloud Run Pricing

- **CPU**: $0.00002400 per vCPU-second
- **Memory**: $0.00000250 per GiB-second
- **Requests**: $0.40 per million requests

### Optimization Tips

1. **Scale to Zero**: Use `--min-instances 0` for cost savings
2. **Right-size Resources**: Start with 1 CPU, 1Gi memory
3. **Concurrency**: Set `--concurrency 80` for efficient instance usage
4. **Cold Start Trade-off**: Balance cost vs latency with min instances

### Estimated Monthly Cost

For ~10,000 requests/month with 30s average response:
- CPU: ~$0.72
- Memory: ~$0.75
- Requests: ~$0.004
- **Total**: ~$1.50/month

---

## Troubleshooting

### Common Issues

**API Key Not Found**
```
Error: GOOGLE_API_KEY environment variable required
Solution: Ensure secret is properly configured and accessible
```

**Import Errors**
```
Error: ModuleNotFoundError: No module named 'capstone'
Solution: Check PYTHONPATH includes /app/src in Dockerfile
```

**Timeout Errors**
```
Error: Request timeout after 60s
Solution: Increase Cloud Run timeout or optimize agent queries
```

**Memory Errors**
```
Error: Container killed due to memory limit
Solution: Increase --memory allocation or optimize agent memory usage
```

### Debug Mode

Enable debug logging for troubleshooting:

```bash
gcloud run deploy $SERVICE_NAME \
    --set-env-vars LOG_LEVEL=DEBUG
```
