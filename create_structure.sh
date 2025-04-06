#!/bin/bash

# Root directory
ROOT="/home/oscar/Documents/VSCode/VisionHireAI"

# Create directory structure
mkdir -p "$ROOT"/{agents,api,ui,db,utils}

# Create Python files
touch "$ROOT"/agents/{jd_analyzer.py,cv_extractor.py,match_scorer.py,shortlister.py,scheduler.py}
touch "$ROOT"/api/main.py
touch "$ROOT"/ui/dashboard.py
touch "$ROOT"/db/candidates.db
touch "$ROOT"/utils/{text_utils.py,emailer.py}
touch "$ROOT"/requirements.txt

echo "✅ Project structure created at $ROOT"
