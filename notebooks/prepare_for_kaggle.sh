#!/bin/bash
# prepare_for_kaggle.sh - Package project for Kaggle upload

set -e  # Exit on error

echo "📦 Preparing project for Kaggle submission..."

# Create output directory
OUTPUT_DIR="kaggle_upload"
mkdir -p "$OUTPUT_DIR"

echo "📁 Copying source files..."

# Copy src directory
cp -r ../src "$OUTPUT_DIR/"

# Copy notebook
cp kaggle_capstone_demo.ipynb "$OUTPUT_DIR/"

# Copy essential documentation
cp ../README.md "$OUTPUT_DIR/"
cp ../RETRY_STRATEGY.md "$OUTPUT_DIR/"

# Create requirements.txt for Kaggle
cat > "$OUTPUT_DIR/requirements.txt" << EOF
google-genai>=0.2.0
google-adk>=0.1.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
EOF

# Create archive
echo "🗜️ Creating archive..."
cd "$OUTPUT_DIR"
zip -r ../kaggle_upload.zip . -x "*.pyc" -x "__pycache__/*" -x ".DS_Store"
cd ..

echo "✅ Package created: kaggle_upload.zip"
echo ""
echo "📋 Next steps:"
echo "1. Go to Kaggle Notebooks: https://www.kaggle.com/code"
echo "2. Click 'New Notebook'"
echo "3. Upload kaggle_upload.zip as a dataset"
echo "4. Extract in notebook: !unzip /kaggle/input/your-dataset/kaggle_upload.zip -d /kaggle/working/"
echo "5. Add GOOGLE_API_KEY as a Kaggle secret"
echo "6. Enable internet access in notebook settings"
echo "7. Open kaggle_capstone_demo.ipynb and run all cells"
echo ""
echo "📚 See notebooks/README.md for detailed instructions"
