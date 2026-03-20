#!/bin/bash
# Creates and sets up the conda environment for the LiRI survey app

ENV_NAME="liri-survey"
PYTHON_VERSION="3.14"

echo "Creating conda environment '$ENV_NAME' with Python $PYTHON_VERSION..."
conda create -n "$ENV_NAME" python="$PYTHON_VERSION" -y

echo "Activating environment and installing dependencies..."
conda run -n "$ENV_NAME" pip install -r requirements.txt

echo ""
echo "Done! To run the app:"
echo "  conda activate $ENV_NAME"
echo "  streamlit run survey_app.py"
