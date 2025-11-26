#!/bin/bash
# prepare_for_kaggle.sh - Prepare self-contained notebook for Kaggle submission

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📦 Preparing self-contained notebook for Kaggle submission..."

# Step 1: Generate self-contained notebook
echo ""
echo "🔧 Step 1: Generating self-contained notebook..."
python make_self_contained.py

# Step 2: Verify the notebook was created
if [ ! -f "kaggle_capstone_self_contained.ipynb" ]; then
    echo "❌ Error: Failed to generate self-contained notebook"
    exit 1
fi

echo ""
echo "✅ Self-contained notebook created: kaggle_capstone_self_contained.ipynb"
echo ""
echo "📋 Submission Instructions:"
echo ""
echo "1. Go to Kaggle Notebooks: https://www.kaggle.com/code"
echo "2. Click 'New Notebook'"
echo "3. File → Upload Notebook → Select 'kaggle_capstone_self_contained.ipynb'"
echo "4. Add GOOGLE_API_KEY as a Kaggle secret (Add-ons → Secrets)"
echo "5. Enable internet access (Settings → Internet → On)"
echo "6. Click 'Run All' to execute the complete demonstration"
echo ""
echo "💡 The notebook is fully self-contained - no additional file uploads needed!"
echo ""
echo "📁 Files for submission:"
echo "   - notebooks/kaggle_capstone_self_contained.ipynb (main submission)"
echo "   - KAGGLE_SUBMISSION_WRITEUP.md (competition writeup)"
echo ""
echo "🔗 GitHub Repository: https://github.com/marcuskbra/neuro-diver-agents"
