#!/bin/sh
set -e

if [ "$1" = "test" ]; then
    echo "[VATA INFRASTRUCTURE] Launching automated End-to-End Swarm Pipeline Test (MAP-001)..."
    python test_swarm_pipeline.py
else
    echo "[VATA INFRASTRUCTURE] Booting Core Kernel Command Center Interface..."
    exec python -m streamlit run app.py --server.port=8501 --server.address=0.0.0.0
fi
