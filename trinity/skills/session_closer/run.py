#!/usr/bin/env python3
"""
Session Closer - Intelligent session analysis and context management
Designed by Gemini CLI, implemented for Trinity coordination
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

class SessionCloser:
    def __init__(self, config_path="/srv/janus/trinity/skills/session_closer/config.json"):
        with open(config_path) as f:
            self.config = json.load(f)

    def analyze_with_gemini(self, prompt):
        """Use Gemini CLI for analysis"""
        cmd = [self.config["analysis_cli"], prompt]
        result = subprocess.run(cmd, capture_output=True, text=True)
        # Filter out error lines, keep only actual response
        lines = result.stdout.split('\n')
        response = '\n'.join(line for line in lines if not line.startswith('Error') and not line.startswith('[Routing]') and not line.startswith('Loaded'))
        return response.strip()

    def close_session(self, conversation_summary):
        """Main session closer function"""
        timestamp = datetime.utcnow().isoformat()

        # 1. Analyze conversation
        print("🔍 Analyzing session...")
        analysis = self.analyze_conversation(conversation_summary)

        # 2. Update context files
        print("📝 Updating context files...")
        for agent, path in self.config["context_files"].items():
            self.update_context_file(path, analysis, timestamp)

        # 3. Create git commit if enabled
        if self.config["enable_git_commit"]:
            print("💾 Creating git commit...")
            self.create_commit(analysis, timestamp)

        print("✅ Session closed successfully")
        return analysis

    def analyze_conversation(self, summary):
        """Extract structured insights from conversation"""
        prompt = f"""Analyze this session and extract:
1. Brief summary (2-3 sentences)
2. Key decisions made
3. Next steps

Session: {summary}

Format as JSON with keys: summary, decisions (array), next_steps (array)
"""
        response = self.analyze_with_gemini(prompt)

        # Try to parse JSON, fallback to structured text
        try:
            return json.loads(response)
        except:
            return {
                "summary": response[:500],
                "decisions": ["See full log for details"],
                "next_steps": ["Continue from where session ended"]
            }

    def update_context_file(self, file_path, analysis, timestamp):
        """Append session analysis to context file"""
        content = f"""
---
## Session Closer: {timestamp}

**Summary:**
{analysis.get('summary', 'N/A')}

**Key Decisions:**
{chr(10).join(f"- {d}" for d in analysis.get('decisions', []))}

**Next Steps:**
{chr(10).join(f"- {n}" for n in analysis.get('next_steps', []))}

---

"""
        with open(file_path, 'a') as f:
            f.write(content)

    def create_commit(self, analysis, timestamp):
        """Create git commit with session summary"""
        repo = self.config["git_repo"]
        files = list(self.config["context_files"].values())

        # Git add
        for file in files:
            subprocess.run(["git", "-C", repo, "add", file], check=False)

        # Git commit
        message = f"""Session closer: {timestamp}

{analysis.get('summary', 'Session analysis')}

🤖 Generated with Session Closer
Co-Authored-By: Trinity <trinity@janus.ai>"""

        subprocess.run(
            ["git", "-C", repo, "commit", "-m", message],
            check=False
        )

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 run.py '<session summary>'")
        sys.exit(1)

    closer = SessionCloser()
    summary = sys.argv[1]
    closer.close_session(summary)

if __name__ == "__main__":
    main()
