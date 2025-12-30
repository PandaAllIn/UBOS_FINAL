"""
Cognitive Recalibration Script for Claude
This script rebuilds Claude's knowledge graph from the endless_scroll archive.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Correctly locate the Librarian's knowledge graph tools
# This path is relative to the project root, assuming the script is run from there.
sys.path.append(str(Path(__file__).resolve().parent.parent.parent / "02_FORGE/src/UBOS/Agents/KnowledgeAgent/MasterLibrarianAgent"))

from master_librarian.graph.knowledge_graph import UBOSKnowledgeGraph
from master_librarian.models import Concept, Relationship, ConceptType, RelationshipType

# Define the correct, post-reorganization paths
# The living scroll is gitignored and lives at the Desktop root
SCROLL_PATH = Path("/Users/panda/Desktop/endless_scroll_archive_ubos2.log")
OUTPUT_PATH = Path("03_OPERATIONS/vessels/localhost/state/claude/knowledge_graph.json")

def main():
    """
    Reads the endless scroll, creates a simple knowledge graph, and saves it.
    """
    if not SCROLL_PATH.exists():
        print(f"Error: Cannot find the endless scroll at {SCROLL_PATH}")
        return

    print("Beginning cognitive recalibration. Reading the endless scroll...")
    
    with SCROLL_PATH.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    graph = UBOSKnowledgeGraph()

    # Create a root concept for the scroll itself
    scroll_concept = Concept(
        id="endless_scroll",
        title="The Endless Scroll",
        description="The complete historical record of the UBOS project.",
        concept_type=ConceptType.ARTIFACT,
    )
    graph.add_concept(scroll_concept)

    # Simple analysis: create a concept for each significant log entry (e.g., containing '[...Z]')
    for i, line in enumerate(lines):
        if "[20" in line and "Z]" in line:
            try:
                timestamp = line.split(']')[0][1:]
                message = line.split(']')[1].strip()
                
                if not message:
                    continue

                concept_id = f"log_entry_{i}"
                concept = Concept(
                    id=concept_id,
                    title=f"Log Entry: {timestamp}",
                    description=message,
                    concept_type=ConceptType.EVENT,
                    source_refs=[f"endless_scroll:line:{i+1}"]
                )
                graph.add_concept(concept)

                # Link this event to the main scroll
                relationship = Relationship(
                    source_id="endless_scroll",
                    target_id=concept_id,
                    relationship_type=RelationshipType.SUPPORTS,
                    description=f"The scroll contains this log entry.",
                    confidence=1.0
                )
                graph.add_relationship(relationship)

            except IndexError:
                # Ignore lines that don't parse correctly
                continue

    print(f"Processed {len(lines)} lines from the scroll.")
    print(f"Generated {len(graph.graph.nodes)} concepts and {len(graph.graph.edges)} relationships.")

    # Ensure the output directory exists
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Save the graph
    graph.save(OUTPUT_PATH)
    
    print(f"Cognitive recalibration complete. Knowledge graph saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    import sys
    main()
