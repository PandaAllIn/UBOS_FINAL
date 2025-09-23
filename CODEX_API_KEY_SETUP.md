# Codex CLI API Key Authentication Setup

This guide shows how to configure Codex CLI to use API key authentication instead of a ChatGPT subscription account.

## Quick Setup

### Option 1: Use the provided script
```bash
# Make the script executable (already done)
chmod +x codex_with_api_key.sh

# Use Codex CLI with API key authentication
./codex_with_api_key.sh "your prompt here"

# Or run interactively
./codex_with_api_key.sh
```

### Option 2: Manual setup
```bash
# Set the API key environment variable
export OPENAI_API_KEY="your_openai_api_key_here"

# Navigate to your project directory
cd /Users/apple/Desktop/UBOS_FINAL

# Run Codex CLI
codex
```

## Important Notes

1. **API Key Security**: Never commit your API key to version control. Consider using a `.env` file or environment variable management.

2. **Usage Limits**: The API key has usage limits. If you hit limits, you may need to:
   - Wait for the limit to reset
   - Upgrade your OpenAI plan
   - Use a different API key

3. **Logout First**: If you previously used Codex CLI with a subscription account, run `codex logout` first to clear stored credentials.

## Integration with UBOS Agents

This setup aligns with the UBOS agent architecture pattern:

```python
# Example for future Implementation Agent
class CodexConfig:
    api_key: str = ""
    base_url: str = "https://api.openai.com/v1"
    
    def __post_init__(self):
        if not self.api_key:
            self.api_key = os.getenv("OPENAI_API_KEY", "")
```

## Troubleshooting

- **Authentication Issues**: Ensure the API key is correctly set and valid
- **Usage Limits**: Check your OpenAI account for usage limits
- **Directory Issues**: Run Codex CLI from a trusted directory (like your project root)

## Next Steps

1. Test the setup with a simple command
2. Integrate with your UBOS Implementation Agent
3. Consider adding this to your agent configuration system
