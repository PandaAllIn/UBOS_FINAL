#!/usr/bin/env python3
"""
UBOS Research CLI - Management interface for research archive

Commands for searching, retrieving, and managing stored research.
"""

import argparse
import json
import sys
from pathlib import Path
from research_storage import ResearchDocumentStorage


def list_research(storage: ResearchDocumentStorage, limit: int = 10):
    """List recent research documents"""
    recent = storage.search_research(limit=limit)

    if not recent:
        print("No research documents found.")
        return

    print(f"📚 Recent Research (showing {len(recent)} of {limit})")
    print("=" * 60)

    for item in recent:
        print(f"🔍 {item['id']}")
        print(f"   Query: {item['query']}")
        print(f"   Topics: {', '.join(item['topics'])}")
        print(f"   Date: {item['timestamp'][:10]}")
        print()


def search_research(storage: ResearchDocumentStorage, query: str = None,
                   topics: list = None, limit: int = 10):
    """Search research documents"""
    results = storage.search_research(query=query, topics=topics, limit=limit)

    if not results:
        print("No matching research found.")
        return

    print(f"🔎 Search Results (found {len(results)})")
    print("=" * 60)

    for item in results:
        print(f"🔍 {item['id']}")
        print(f"   Query: {item['query']}")
        print(f"   Topics: {', '.join(item['topics'])}")
        print(f"   Date: {item['timestamp'][:10]}")
        print()


def show_research(storage: ResearchDocumentStorage, research_id: str):
    """Show detailed research document"""
    research = storage.load_research(research_id)

    if not research:
        print(f"❌ Research '{research_id}' not found.")
        return

    print(f"📋 Research Details: {research_id}")
    print("=" * 80)
    print(f"Query: {research['query']['original']}")
    print(f"Model: {research['execution']['model_used']}")
    print(f"Complexity: {research['query']['complexity_score']}/5")
    print(f"Topics: {', '.join(research['topics'])}")
    print()

    print("🔍 FINDINGS:")
    print("-" * 40)
    print(research['findings']['content'][:500] + "..." if len(research['findings']['content']) > 500 else research['findings']['content'])
    print()

    if research['findings'].get('key_insights'):
        print("💡 KEY INSIGHTS:")
        print("-" * 40)
        for insight in research['findings']['key_insights']:
            confidence = insight['confidence'] * 100
            print(f"• {insight['insight']} (Confidence: {confidence:.0f}%)")
        print()

    print("📚 SOURCES:")
    print("-" * 40)
    for i, source in enumerate(research['sources'], 1):
        print(f"{i}. {source['url']}")
    print()


def show_stats(storage: ResearchDocumentStorage):
    """Show research archive statistics"""
    stats = storage.get_research_stats()

    print("📊 Research Archive Statistics")
    print("=" * 40)
    print(f"Total Research Documents: {stats['total_count']}")
    print(f"Last Updated: {stats.get('last_updated', 'Never')[:19] if stats.get('last_updated') else 'Never'}")
    print()

    if stats['topics']:
        print("📁 Topics:")
        for topic in sorted(stats['topics']):
            print(f"  • {topic}")
        print()

    if stats['models']:
        print("🤖 Models Used:")
        for model in sorted(stats['models']):
            print(f"  • {model}")
        print()


def export_insights(storage: ResearchDocumentStorage, topic: str = None, output_file: str = None):
    """Export aggregated insights for AI consumption"""
    # Search for research in the topic
    if topic:
        results = storage.search_research(topics=[topic], limit=50)
    else:
        results = storage.search_research(limit=50)

    if not results:
        print("No research found for insights extraction.")
        return

    research_ids = [item['id'] for item in results]
    insights = storage.extract_insights_for_ai(research_ids)

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(insights, f, indent=2, ensure_ascii=False)
        print(f"💾 Insights exported to {output_file}")
    else:
        print("🧠 Aggregated Insights")
        print("=" * 40)
        print(f"Research Count: {insights['research_count']}")
        print(f"Average Confidence: {insights['average_confidence']:.2f}")
        print()

        print("🔑 Key Topics:")
        for topic, count in sorted(insights['key_topics'].items(), key=lambda x: x[1], reverse=True):
            print(f"  • {topic}: {count} mentions")
        print()

        print("💡 Top Insights:")
        for insight in insights['insight_summary'][:5]:
            confidence = insight['confidence'] * 100
            print(f"  • {insight['text']} (Confidence: {confidence:.0f}%)")
        print()


def main():
    """CLI interface for research management"""
    parser = argparse.ArgumentParser(description="UBOS Research CLI - Manage research archive")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # List command
    list_parser = subparsers.add_parser('list', help='List recent research')
    list_parser.add_argument('--limit', type=int, default=10, help='Number of items to show')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search research documents')
    search_parser.add_argument('--query', help='Search query')
    search_parser.add_argument('--topics', nargs='+', help='Topics to filter by')
    search_parser.add_argument('--limit', type=int, default=10, help='Number of results')

    # Show command
    show_parser = subparsers.add_parser('show', help='Show detailed research')
    show_parser.add_argument('research_id', help='Research ID to display')

    # Stats command
    subparsers.add_parser('stats', help='Show archive statistics')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export insights for AI')
    export_parser.add_argument('--topic', help='Filter by topic')
    export_parser.add_argument('--output', help='Output file (JSON format)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Initialize storage
    storage = ResearchDocumentStorage()

    # Execute command
    if args.command == 'list':
        list_research(storage, args.limit)
    elif args.command == 'search':
        search_research(storage, args.query, args.topics, args.limit)
    elif args.command == 'show':
        show_research(storage, args.research_id)
    elif args.command == 'stats':
        show_stats(storage)
    elif args.command == 'export':
        export_insights(storage, args.topic, args.output)


if __name__ == "__main__":
    main()