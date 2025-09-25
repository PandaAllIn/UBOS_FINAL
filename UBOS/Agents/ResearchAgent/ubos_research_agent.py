#!/usr/bin/env python3
"""
UBOS Research Agent - Perplexity Sonar API Integration

A CLI research agent that embodies UBOS philosophy:
- Pause before response (query analysis)
- Systems over willpower (structured approach)
- Strategic thinking (optimal model selection)

Usage:
    python ubos_research_agent.py quick "AI agent trends"
    python ubos_research_agent.py deep "knowledge graph architectures"
    python ubos_research_agent.py reason "compare agent frameworks"
    python ubos_research_agent.py --model sonar-pro "complex analysis"
"""

import argparse
import json
import sys
import time
from typing import Dict, Any, Optional, List
import requests
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timezone
import re
import os
from pathlib import Path

# Add the script's directory to the Python path to ensure local imports work
sys.path.append(str(Path(__file__).parent))

from research_storage import ResearchDocumentStorage, ResearchInsight, ResearchSource, ResearchMetadata, QualityMetrics


class SonarModel(Enum):
    """Available Sonar models with their characteristics"""
    SONAR = "sonar"
    SONAR_PRO = "sonar-pro"
    SONAR_REASONING = "sonar-reasoning"
    SONAR_REASONING_PRO = "sonar-reasoning-pro"
    SONAR_DEEP_RESEARCH = "sonar-deep-research"


@dataclass
class ResearchConfig:
    """Configuration for research requests"""
    api_key: str = ""
    base_url: str = "https://api.perplexity.ai"
    max_tokens: int = 4000
    temperature: float = 0.2
    top_p: float = 0.9

    def __post_init__(self):
        if not self.api_key:
            self.api_key = os.getenv("PERPLEXITY_API_KEY", "")


class QueryComplexityAnalyzer:
    """Analyzes query complexity following UBOS pause-before-response principle"""

    @staticmethod
    def analyze(query: str) -> Dict[str, Any]:
        """Analyze query complexity to select optimal model"""
        # Pause: Analyze before responding
        time.sleep(0.1)  # Brief pause for analysis

        words = len(query.split())
        has_complex_terms = any(term in query.lower() for term in [
            'compare', 'analyze', 'evaluate', 'pros and cons', 'research',
            'comprehensive', 'detailed', 'strategic', 'architecture'
        ])
        has_reasoning_terms = any(term in query.lower() for term in [
            'why', 'how', 'explain', 'reason', 'logic', 'cause', 'effect'
        ])

        complexity_score = 0
        if words > 10: complexity_score += 1
        if has_complex_terms: complexity_score += 2
        if has_reasoning_terms: complexity_score += 1
        if '?' in query and words > 15: complexity_score += 1

        return {
            'score': complexity_score,
            'word_count': words,
            'has_complex_terms': has_complex_terms,
            'has_reasoning_terms': has_reasoning_terms,
            'recommended_model': QueryComplexityAnalyzer._recommend_model(complexity_score, has_reasoning_terms).value
        }

    @staticmethod
    def _recommend_model(score: int, has_reasoning: bool) -> SonarModel:
        """Select optimal model based on complexity analysis"""
        if has_reasoning and score >= 3:
            return SonarModel.SONAR_REASONING_PRO
        elif has_reasoning:
            return SonarModel.SONAR_REASONING
        elif score >= 4:
            return SonarModel.SONAR_DEEP_RESEARCH
        elif score >= 2:
            return SonarModel.SONAR_PRO
        else:
            return SonarModel.SONAR


class UBOSResearchAgent:
    """
    Main research agent implementing UBOS principles:
    - Strategic model selection
    - Structured response patterns
    - Error handling with grace
    """

    def __init__(self, config: Optional[ResearchConfig] = None):
        self.config = config or ResearchConfig()
        if not self.config.api_key:
            raise ValueError("PERPLEXITY_API_KEY is not set. Please set it in your environment and try again.")
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.config.api_key}',
            'Content-Type': 'application/json'
        })
        self.storage = ResearchDocumentStorage()

    def research(self, query: str, model: Optional[str] = None,
                format_output: str = "text", depth: str = "medium") -> Dict[str, Any]:
        """
        Main research method following UBOS methodology:
        1. Pause: Analyze query complexity
        2. Plan: Select optimal approach
        3. Execute: Make API call with error handling
        4. Respond: Format output appropriately
        """

        # Step 1: Pause and analyze (UBOS principle)
        print("🔍 Analyzing query complexity...")
        analysis = QueryComplexityAnalyzer.analyze(query)

        # Step 2: Strategic model selection
        selected_model = model or analysis['recommended_model']
        print(f"📊 Complexity score: {analysis['score']}/5")
        print(f"🤖 Selected model: {selected_model}")

        # Step 3: Execute research with error handling
        try:
            result = self._execute_api_call(query, selected_model, depth)

            # Step 4: Format and save response
            formatted_result = self._format_response(result, format_output, analysis)

            # Step 5: Save research artifacts for future use
            research_doc = self._create_research_document(query, result, analysis, selected_model, depth)
            research_id = self.storage.save_research(research_doc)

            # Add research ID to result for reference
            if isinstance(formatted_result, dict):
                formatted_result['research_id'] = research_id
            else:
                print(f"💾 Research saved as: {research_id}")

            return formatted_result

        except Exception as e:
            return self._handle_error(e, query, selected_model)

    def _execute_api_call(self, query: str, model: str, depth: str) -> Dict[str, Any]:
        """Execute the Perplexity API call with proper parameters"""

        # Prepare system prompt based on depth
        system_prompts = {
            "quick": "Provide a concise, accurate answer with key sources.",
            "medium": "Provide a comprehensive answer with analysis and multiple sources.",
            "deep": "Provide an exhaustive analysis with detailed sourcing and multiple perspectives."
        }

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompts.get(depth, system_prompts["medium"])
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "top_p": self.config.top_p,
            "return_citations": True,
            "return_images": False
        }

        print("⚡ Executing research query...")
        response = self.session.post(
            f"{self.config.base_url}/chat/completions",
            json=payload,
            timeout=30
        )
        response.raise_for_status()

        return response.json()

    def _format_response(self, api_response: Dict[str, Any],
                        format_output: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Format the API response according to requested format"""

        content = api_response['choices'][0]['message']['content']
        citations = api_response.get('citations', [])

        result = {
            'query_analysis': analysis,
            'content': content,
            'citations': citations,
            'model_used': api_response.get('model', 'unknown'),
            'usage': api_response.get('usage', {}),
            'timestamp': time.time()
        }

        if format_output == "json":
            return result
        elif format_output == "yaml":
            import yaml
            return yaml.dump(result, default_flow_style=False)
        else:
            # Human-readable text format
            return self._format_text_output(result)

    def _format_text_output(self, result: Dict[str, Any]) -> str:
        """Format result as human-readable text"""
        output = []
        output.append("="*80)
        output.append("🧠 UBOS RESEARCH AGENT RESULTS")
        output.append("="*80)
        output.append(f"Model Used: {result['model_used']}")
        output.append(f"Complexity Score: {result['query_analysis']['score']}/5")
        output.append("")
        output.append("📋 RESEARCH FINDINGS:")
        output.append("-"*40)
        output.append(result['content'])

        if result['citations']:
            output.append("")
            output.append("📚 SOURCES:")
            output.append("-"*40)
            for i, citation in enumerate(result['citations'], 1):
                output.append(f"{i}. {citation}")

        if result['usage']:
            output.append("")
            output.append("📊 API USAGE:")
            output.append("-"*40)
            for key, value in result['usage'].items():
                output.append(f"{key}: {value}")

        output.append("="*80)
        return "\n".join(output)

    def _handle_error(self, error: Exception, query: str, model: str) -> Dict[str, Any]:
        """Handle errors gracefully following UBOS resilience principles"""
        error_result = {
            'error': True,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'query': query,
            'attempted_model': model,
            'timestamp': time.time(),
            'suggestions': []
        }

        # Provide helpful suggestions based on error type
        if "401" in str(error) or "authentication" in str(error).lower():
            error_result['suggestions'].append("Check API key configuration")
        elif "429" in str(error) or "rate limit" in str(error).lower():
            error_result['suggestions'].append("Wait before retrying - rate limit exceeded")
        elif "timeout" in str(error).lower():
            error_result['suggestions'].append("Try again - network timeout occurred")
        else:
            error_result['suggestions'].append("Check network connection and try again")

        return error_result

    def _create_research_document(self, query: str, api_response: Dict[str, Any],
                                analysis: Dict[str, Any], model: str, depth: str) -> Dict[str, Any]:
        """Create a research document following UBOS schema"""
        research_id = self.storage.generate_research_id(query)
        timestamp = datetime.now(timezone.utc).isoformat()

        content = api_response['choices'][0]['message']['content']
        citations = api_response.get('citations', [])

        # Extract key insights from content
        insights = self._extract_insights(content, len(citations))

        # Process sources
        sources = []
        for i, citation in enumerate(citations):
            sources.append({
                'url': citation,
                'title': f"Source {i+1}",
                'relevance': 0.8,  # Default relevance
                'access_date': timestamp.split('T')[0]
            })

        # Determine topics from query and content
        topics = self._extract_topics(query, content)

        # Calculate quality metrics
        quality = self._calculate_quality_metrics(content, citations, analysis)

        # Create the research document
        research_doc = {
            'id': research_id,
            'timestamp': timestamp,
            'agent_version': "1.0.0",
            'query': {
                'original': query,
                'complexity_score': analysis['score'],
                'analysis': analysis
            },
            'execution': {
                'model_used': model,
                'depth': depth,
                'search_mode': 'medium',  # Default
                'duration_seconds': 0  # Could be measured
            },
            'findings': {
                'summary': self._generate_summary(content),
                'content': content,
                'key_insights': insights
            },
            'sources': sources,
            'topics': topics,
            'usage': api_response.get('usage', {}),
            'metadata': {
                'token_estimate': len(content.split()) * 1.3,  # Rough estimate
                'reading_time_seconds': len(content.split()) * 0.5,  # Rough estimate
                'language': 'en',
                'extractable_facts': len(insights),
                'citation_count': len(citations)
            },
            'quality': quality,
            'related_research': [],  # Could be populated later
            'agent_notes': {
                'follow_up_queries': self._suggest_follow_ups(query, content),
                'applications': [
                    {
                        'context': 'knowledge_agent',
                        'use_case': 'Pattern recognition and knowledge integration'
                    },
                    {
                        'context': 'specification_agent',
                        'use_case': 'Informed requirement gathering'
                    }
                ]
            }
        }

        return research_doc

    def _extract_insights(self, content: str, source_count: int) -> List[Dict[str, Any]]:
        """Extract key insights from research content"""
        insights = []

        # Simple extraction - look for key patterns
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line and (line.startswith('•') or line.startswith('-') or line.startswith('*')):
                insight_text = line.lstrip('•-* ').strip()
                if len(insight_text) > 20:  # Meaningful insights
                    insights.append({
                        'insight': insight_text,
                        'confidence': 0.7 + (source_count * 0.05),  # Higher confidence with more sources
                        'source_count': source_count
                    })

        # Limit to top insights
        return insights[:5]

    def _extract_topics(self, query: str, content: str) -> List[str]:
        """Extract relevant topics from query and content"""
        topic_keywords = {
            'ai_agents': ['agent', 'ai agent', 'artificial intelligence', 'machine learning'],
            'architecture': ['architecture', 'design', 'structure', 'framework'],
            'knowledge_management': ['knowledge', 'information', 'data', 'knowledge base'],
            'research': ['research', 'analysis', 'study', 'investigation'],
            'technology': ['technology', 'tech', 'software', 'system'],
            'strategy': ['strategy', 'strategic', 'planning', 'approach'],
            'implementation': ['implementation', 'development', 'building', 'coding']
        }

        text_to_analyze = f"{query} {content}".lower()
        detected_topics = []

        for topic, keywords in topic_keywords.items():
            if any(keyword in text_to_analyze for keyword in keywords):
                detected_topics.append(topic)

        return detected_topics[:5]  # Limit topics

    def _generate_summary(self, content: str) -> str:
        """Generate a one-liner summary"""
        sentences = content.split('.')
        if sentences:
            return sentences[0].strip() + '.'
        return "Research findings on requested topic."

    def _calculate_quality_metrics(self, content: str, citations: List[str], analysis: Dict[str, Any]) -> Dict[str, float]:
        """Calculate quality metrics for the research"""
        return {
            'factual_confidence': min(0.9, 0.5 + len(citations) * 0.1),
            'source_diversity': min(1.0, len(set(citations)) / max(len(citations), 1)),
            'recency_score': 0.8,  # Assuming recent sources
            'depth_score': analysis['score'] / 5.0
        }

    def _suggest_follow_ups(self, original_query: str, content: str) -> List[str]:
        """Suggest follow-up research queries"""
        follow_ups = []

        if 'compare' in original_query.lower():
            follow_ups.append(f"Best practices for implementing {original_query.split()[-1]}")
        elif 'best practices' in original_query.lower():
            follow_ups.append(f"Common pitfalls in {original_query.replace('best practices', '').strip()}")
        else:
            follow_ups.append(f"Implementation guide for {original_query}")
            follow_ups.append(f"Case studies of {original_query}")

        return follow_ups[:3]


def main():
    """CLI interface for UBOS Research Agent"""
    parser = argparse.ArgumentParser(description="UBOS Research Agent - Strategic Intelligence Gathering")

    parser.add_argument('command', choices=['quick', 'deep', 'reason', 'pro'],
                       help='Research depth/type')
    parser.add_argument('query', help='Research query')
    parser.add_argument('--model', choices=[m.value for m in SonarModel],
                       help='Force specific Sonar model')
    parser.add_argument('--format', choices=['text', 'json', 'yaml'],
                       default='text', help='Output format')
    parser.add_argument('--depth', choices=['quick', 'medium', 'deep'],
                       default='medium', help='Research depth')

    args = parser.parse_args()

    # Initialize agent
    agent = UBOSResearchAgent()

    # Map command to model if not explicitly specified
    command_model_map = {
        'quick': SonarModel.SONAR.value,
        'deep': SonarModel.SONAR_DEEP_RESEARCH.value,
        'reason': SonarModel.SONAR_REASONING.value,
        'pro': SonarModel.SONAR_PRO.value
    }

    model = args.model or command_model_map.get(args.command)

    # Execute research
    print("🚀 UBOS Research Agent Starting...")
    print(f"Query: {args.query}")
    print("-" * 60)

    result = agent.research(
        query=args.query,
        model=model,
        format_output=args.format,
        depth=args.depth
    )

    # Output result
    if isinstance(result, dict) and result.get('error'):
        print("❌ Error occurred:")
        print(f"Type: {result['error_type']}")
        print(f"Message: {result['error_message']}")
        if result['suggestions']:
            print("Suggestions:")
            for suggestion in result['suggestions']:
                print(f"  • {suggestion}")
        sys.exit(1)
    else:
        if args.format == 'text':
            print(result)
        else:
            print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()