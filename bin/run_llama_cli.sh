#!/bin/bash
# Add timeout to prevent hangs (30 minutes max)
timeout 1800 /opt/llama.cpp/build/bin/llama-cli "$@"