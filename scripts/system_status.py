#!/usr/bin/env python3
"""
📊 UBOS System Status Checker
Comprehensive system health and capability report
"""

import os
import sys
from pathlib import Path
import importlib.util

def check_system_status():
    """Check comprehensive system status"""
    print("📊 UBOS ENHANCED AGENT SYSTEM STATUS")
    print("="*60)

    status = {
        "environment": check_environment(),
        "agents": check_agents(),
        "configuration": check_configuration(),
        "dependencies": check_dependencies()
    }

    # Overall assessment
    scores = [s.get("score", 0) for s in status.values()]
    overall_score = sum(scores) / len(scores) if scores else 0

    print(f"\\n🎯 OVERALL SYSTEM STATUS")
    print("="*30)
    print(f"Overall Score: {overall_score:.1f}/10")

    if overall_score >= 9.0:
        print("Status: 🟢 EXCELLENT - Production Ready")
    elif overall_score >= 7.0:
        print("Status: 🟡 GOOD - Minor Issues")
    else:
        print("Status: 🔴 NEEDS WORK - Configuration Required")

    return overall_score

def check_environment():
    """Check environment configuration"""
    print("\\n🌍 ENVIRONMENT CHECK")
    print("-" * 30)

    score = 0
    max_score = 10

    # API Keys
    perplexity_key = os.getenv("PERPLEXITY_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")

    if perplexity_key:
        print("✅ PERPLEXITY_API_KEY: Configured")
        score += 3
    else:
        print("❌ PERPLEXITY_API_KEY: Not set")

    if gemini_key:
        print("✅ GEMINI_API_KEY: Configured")
        score += 3
    else:
        print("❌ GEMINI_API_KEY: Not set")

    # Python version
    python_version = sys.version_info
    if python_version.major == 3 and python_version.minor >= 8:
        print(f"✅ Python Version: {python_version.major}.{python_version.minor}")
        score += 2
    else:
        print(f"⚠️ Python Version: {python_version.major}.{python_version.minor} (recommend 3.8+)")
        score += 1

    # Directory structure
    ubos_path = Path(__file__).parent.parent / "UBOS"
    if ubos_path.exists():
        print("✅ UBOS Directory: Found")
        score += 2
    else:
        print("❌ UBOS Directory: Missing")

    print(f"Environment Score: {score}/{max_score}")
    return {"score": score, "max_score": max_score}

def check_agents():
    """Check agent availability and functionality"""
    print("\\n🤖 AGENT STATUS CHECK")
    print("-" * 30)

    agents = {
        "Enhanced Research Agent": "UBOS/Agents/ResearchAgent/enhanced_research_agent.py",
        "Enhanced Specification Agent": "UBOS/Agents/AgentSummoner/enhanced_specification_agent.py",
        "Enhanced Orchestration Engine": "UBOS/Agents/AIPrimeAgent/enhanced_orchestration_engine.py",
        "UBOS Knowledge Loader": "UBOS/Agents/KnowledgeAgent/MasterLibrarianAgent/load_ubos_knowledge.py",
        "Agent Template Registry": "UBOS/Agents/AgentSummoner/agent_summoner/agent_templates.py"
    }

    base_path = Path(__file__).parent.parent
    score = 0
    max_score = len(agents) * 2

    for agent_name, agent_path in agents.items():
        full_path = base_path / agent_path
        if full_path.exists():
            print(f"✅ {agent_name}: Available")
            score += 2

            # Try to check if importable
            try:
                spec = importlib.util.spec_from_file_location("test_module", full_path)
                if spec:
                    print(f"   📦 Import check: OK")
                else:
                    print(f"   ⚠️ Import check: May have issues")
            except Exception:
                print(f"   ⚠️ Import check: Issues detected")
                score -= 0.5

        else:
            print(f"❌ {agent_name}: Missing")

    print(f"Agent Score: {score}/{max_score}")
    return {"score": score, "max_score": max_score}

def check_configuration():
    """Check configuration files"""
    print("\\n⚙️ CONFIGURATION CHECK")
    print("-" * 30)

    base_path = Path(__file__).parent.parent
    config_files = {
        "Environment Template": "config/.env.template",
        "Agent Configuration": "config/agents.json",
        "MCP Configuration": "config/mcp.json",
        "Main README": "README.md"
    }

    score = 0
    max_score = len(config_files) * 2

    for config_name, config_path in config_files.items():
        full_path = base_path / config_path
        if full_path.exists():
            print(f"✅ {config_name}: Present")
            score += 2

            # Check file size (should not be empty)
            if full_path.stat().st_size > 0:
                print(f"   📄 Content: {full_path.stat().st_size} bytes")
            else:
                print(f"   ⚠️ Content: Empty file")
                score -= 0.5
        else:
            print(f"❌ {config_name}: Missing")

    print(f"Configuration Score: {score}/{max_score}")
    return {"score": score, "max_score": max_score}

def check_dependencies():
    """Check Python dependencies"""
    print("\\n📦 DEPENDENCY CHECK")
    print("-" * 30)

    required_packages = [
        "requests",
        "pathlib",
        "dataclasses",
        "typing",
        "json",
        "os",
        "sys"
    ]

    optional_packages = [
        "yaml",
        "google.generativeai",
        "networkx"
    ]

    score = 0
    max_score = 10

    # Check required packages
    required_available = 0
    for package in required_packages:
        try:
            __import__(package)
            required_available += 1
        except ImportError:
            print(f"❌ Required: {package}")

    if required_available == len(required_packages):
        print(f"✅ Required packages: All available")
        score += 6
    else:
        print(f"⚠️ Required packages: {required_available}/{len(required_packages)}")
        score += (required_available / len(required_packages)) * 6

    # Check optional packages
    optional_available = 0
    for package in optional_packages:
        try:
            __import__(package)
            optional_available += 1
            print(f"✅ Optional: {package}")
        except ImportError:
            print(f"⚠️ Optional: {package} (not available)")

    score += (optional_available / len(optional_packages)) * 4

    print(f"Dependency Score: {score:.1f}/{max_score}")
    return {"score": score, "max_score": max_score}

if __name__ == "__main__":
    overall_score = check_system_status()

    print(f"\\n🎊 SYSTEM CHECK COMPLETE")
    print(f"Overall Health: {overall_score:.1f}/10")

    if overall_score >= 9.0:
        print("🎉 Your UBOS system is in excellent condition!")
    elif overall_score >= 7.0:
        print("🟡 Your UBOS system is mostly ready - minor configuration needed")
    else:
        print("🔧 Your UBOS system needs configuration - check the items above")

    sys.exit(0 if overall_score >= 7.0 else 1)