#!/usr/bin/env python3
"""
UBOS Research Storage System

Handles storage, indexing, and retrieval of research findings
in AI-friendly formats following UBOS schema patterns.
"""

import os
import json
import yaml
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import re


@dataclass
class ResearchInsight:
    """Individual insight extracted from research"""
    insight: str
    confidence: float
    source_count: int


@dataclass
class ResearchSource:
    """Source citation information"""
    url: str
    title: str
    relevance: float
    access_date: str


@dataclass
class ResearchMetadata:
    """Metadata for AI consumption"""
    token_estimate: int
    reading_time_seconds: int
    language: str = "en"
    extractable_facts: int = 0
    citation_count: int = 0


@dataclass
class QualityMetrics:
    """Research quality assessment"""
    factual_confidence: float
    source_diversity: float
    recency_score: float
    depth_score: float


class ResearchDocumentStorage:
    """
    Manages storage and retrieval of research documents
    following UBOS philosophy and schema patterns
    """

    def __init__(self, base_path: str = None):
        if base_path is None:
            self.base_path = Path(__file__).parent / "research_archive"
        else:
            self.base_path = Path(base_path)

        self._ensure_directories()

    def _ensure_directories(self):
        """Create necessary directory structure"""
        directories = [
            self.base_path,
            self.base_path / "by_date",
            self.base_path / "by_topic",
            self.base_path / "indices"
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def generate_research_id(self, query: str) -> str:
        """Generate unique research ID following UBOS pattern"""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")

        # Create slug from query
        slug = re.sub(r'[^a-zA-Z0-9\s]', '', query.lower())
        slug = re.sub(r'\s+', '-', slug.strip())
        slug = slug[:30]  # Limit length

        return f"research-{timestamp}-{slug}"

    def save_research(self, research_data: Dict[str, Any]) -> str:
        """
        Save research document in multiple formats and locations
        Returns the research ID
        """
        research_id = research_data['id']
        timestamp = research_data['timestamp']
        date_str = datetime.fromisoformat(timestamp.replace('Z', '+00:00')).strftime("%Y-%m-%d")

        # Save by date
        date_dir = self.base_path / "by_date" / date_str
        date_dir.mkdir(parents=True, exist_ok=True)

        # Save in multiple formats
        base_path = date_dir / research_id

        # YAML format (primary - AI friendly)
        yaml_path = f"{base_path}.yaml"
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(research_data, f, default_flow_style=False, allow_unicode=True)

        # JSON format (programmatic access)
        json_path = f"{base_path}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(research_data, f, indent=2, ensure_ascii=False)

        # Markdown format (human readable)
        md_path = f"{base_path}.md"
        self._save_as_markdown(research_data, md_path)

        # Update topic index
        self._update_topic_index(research_data)

        # Update master index
        self._update_master_index(research_data)

        return research_id

    def _save_as_markdown(self, research_data: Dict[str, Any], filepath: str):
        """Save research as human-readable markdown"""
        md_content = []

        # Header
        md_content.append(f"# Research: {research_data['query']['original']}")
        md_content.append(f"**ID:** {research_data['id']}")
        md_content.append(f"**Date:** {research_data['timestamp']}")
        md_content.append(f"**Model:** {research_data['execution']['model_used']}")
        md_content.append("")

        # Query Analysis
        md_content.append("## Query Analysis")
        analysis = research_data['query']['analysis']
        md_content.append(f"- **Complexity Score:** {research_data['query']['complexity_score']}/5")
        md_content.append(f"- **Word Count:** {analysis['word_count']}")
        md_content.append(f"- **Recommended Model:** {analysis['recommended_model']}")
        md_content.append("")

        # Findings
        md_content.append("## Research Findings")
        md_content.append(f"**Summary:** {research_data['findings']['summary']}")
        md_content.append("")
        md_content.append("### Content")
        md_content.append(research_data['findings']['content'])
        md_content.append("")

        # Key Insights
        if 'key_insights' in research_data['findings']:
            md_content.append("### Key Insights")
            for insight in research_data['findings']['key_insights']:
                confidence = insight['confidence'] * 100
                md_content.append(f"- **{insight['insight']}** (Confidence: {confidence:.0f}%, Sources: {insight['source_count']})")
            md_content.append("")

        # Sources
        md_content.append("## Sources")
        for i, source in enumerate(research_data['sources'], 1):
            relevance = source['relevance'] * 100
            md_content.append(f"{i}. [{source['title']}]({source['url']}) (Relevance: {relevance:.0f}%)")
        md_content.append("")

        # Topics
        md_content.append("## Topics")
        md_content.append(", ".join(research_data['topics']))
        md_content.append("")

        # Usage Stats
        usage = research_data['usage']
        md_content.append("## API Usage")
        md_content.append(f"- **Tokens:** {usage['total_tokens']} ({usage['prompt_tokens']} prompt + {usage['completion_tokens']} completion)")
        md_content.append(f"- **Cost:** ${usage['cost']['total_cost']:.4f}")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md_content))

    def _update_topic_index(self, research_data: Dict[str, Any]):
        """Update topic-based index"""
        topics = research_data['topics']
        research_id = research_data['id']

        for topic in topics:
            topic_dir = self.base_path / "by_topic" / topic
            topic_dir.mkdir(parents=True, exist_ok=True)

            # Create symlink to original research
            symlink_path = topic_dir / f"{research_id}.yaml"
            if not symlink_path.exists():
                original_path = self._find_research_file(research_id)
                if original_path:
                    try:
                        symlink_path.symlink_to(original_path)
                    except OSError:
                        # Fallback: copy file if symlink fails
                        import shutil
                        shutil.copy2(original_path, symlink_path)

    def _update_master_index(self, research_data: Dict[str, Any]):
        """Update master research index"""
        index_path = self.base_path / "indices" / "master_index.json"

        # Load existing index
        if index_path.exists():
            with open(index_path, 'r', encoding='utf-8') as f:
                index = json.load(f)
        else:
            index = {
                'total_research_count': 0,
                'last_updated': None,
                'research_by_date': {},
                'research_by_topic': {},
                'research_by_model': {},
                'recent_research': []
            }

        # Update index
        research_id = research_data['id']
        date_str = datetime.fromisoformat(research_data['timestamp'].replace('Z', '+00:00')).strftime("%Y-%m-%d")

        index['total_research_count'] += 1
        index['last_updated'] = datetime.now(timezone.utc).isoformat()

        # By date
        if date_str not in index['research_by_date']:
            index['research_by_date'][date_str] = []
        index['research_by_date'][date_str].append(research_id)

        # By topic
        for topic in research_data['topics']:
            if topic not in index['research_by_topic']:
                index['research_by_topic'][topic] = []
            index['research_by_topic'][topic].append(research_id)

        # By model
        model = research_data['execution']['model_used']
        if model not in index['research_by_model']:
            index['research_by_model'][model] = []
        index['research_by_model'][model].append(research_id)

        # Recent research (keep last 50)
        index['recent_research'].insert(0, {
            'id': research_id,
            'query': research_data['query']['original'],
            'timestamp': research_data['timestamp'],
            'topics': research_data['topics']
        })
        index['recent_research'] = index['recent_research'][:50]

        # Save updated index
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)

    def _find_research_file(self, research_id: str) -> Optional[Path]:
        """Find the YAML file for a research ID"""
        for date_dir in (self.base_path / "by_date").iterdir():
            if date_dir.is_dir():
                yaml_file = date_dir / f"{research_id}.yaml"
                if yaml_file.exists():
                    return yaml_file
        return None

    def load_research(self, research_id: str) -> Optional[Dict[str, Any]]:
        """Load research document by ID"""
        yaml_file = self._find_research_file(research_id)
        if yaml_file and yaml_file.exists():
            with open(yaml_file, 'r', encoding='utf-8') as f:
                return yaml.load(f, Loader=yaml.SafeLoader)
        return None

    def search_research(self, query: str = None, topics: List[str] = None,
                       date_range: tuple = None, limit: int = 20) -> List[Dict[str, Any]]:
        """Search research documents with various filters"""
        index_path = self.base_path / "indices" / "master_index.json"

        if not index_path.exists():
            return []

        with open(index_path, 'r', encoding='utf-8') as f:
            index = json.load(f)

        # Start with all recent research
        candidates = index['recent_research'].copy()

        # Filter by topics
        if topics:
            filtered = []
            for item in candidates:
                if any(topic in item['topics'] for topic in topics):
                    filtered.append(item)
            candidates = filtered

        # Filter by query (simple text search)
        if query:
            query_lower = query.lower()
            filtered = []
            for item in candidates:
                if query_lower in item['query'].lower():
                    filtered.append(item)
            candidates = filtered

        # Apply limit
        return candidates[:limit]

    def get_research_stats(self) -> Dict[str, Any]:
        """Get research statistics"""
        index_path = self.base_path / "indices" / "master_index.json"

        if not index_path.exists():
            return {'total_count': 0, 'topics': [], 'models': []}

        with open(index_path, 'r', encoding='utf-8') as f:
            index = json.load(f)

        return {
            'total_count': index['total_research_count'],
            'last_updated': index['last_updated'],
            'topics': list(index['research_by_topic'].keys()),
            'models': list(index['research_by_model'].keys()),
            'dates': list(index['research_by_date'].keys())
        }

    def extract_insights_for_ai(self, research_ids: List[str]) -> Dict[str, Any]:
        """Extract and aggregate insights for AI agent consumption"""
        aggregated = {
            'insight_summary': [],
            'key_topics': {},
            'source_urls': [],
            'total_confidence': 0.0,
            'research_count': len(research_ids)
        }

        for research_id in research_ids:
            research = self.load_research(research_id)
            if not research:
                continue

            # Aggregate insights
            if 'key_insights' in research.get('findings', {}):
                for insight in research['findings']['key_insights']:
                    aggregated['insight_summary'].append({
                        'text': insight['insight'],
                        'confidence': insight['confidence'],
                        'source_research': research_id
                    })
                    aggregated['total_confidence'] += insight['confidence']

            # Aggregate topics
            for topic in research.get('topics', []):
                if topic not in aggregated['key_topics']:
                    aggregated['key_topics'][topic] = 0
                aggregated['key_topics'][topic] += 1

            # Collect sources
            for source in research.get('sources', []):
                if source['url'] not in aggregated['source_urls']:
                    aggregated['source_urls'].append(source['url'])

        # Calculate average confidence
        if aggregated['insight_summary']:
            aggregated['average_confidence'] = aggregated['total_confidence'] / len(aggregated['insight_summary'])
        else:
            aggregated['average_confidence'] = 0.0

        return aggregated