#!/bin/bash

# UBOS Codex CLI with API Key Authentication
# This script sets up Codex CLI to use API key authentication instead of subscription

# Set your OpenAI API key
export OPENAI_API_KEY="your_openai_api_key_here"

# Change to UBOS project directory
cd /Users/apple/Desktop/UBOS_FINAL

# Run Codex CLI with the provided arguments
codex "$@"
