# UBOS Master Librarian Agent - Comprehensive Specification

## Project Overview

The Master Librarian Agent is the foundational knowledge consultant for the UBOS AI ecosystem. It serves as the central repository of wisdom from all UBOS books and provides philosophical guidance to ensure all AI decisions align with UBOS principles.

## Scope Statement

- **Included**: Parsing and normalising UBOS book content; maintaining the knowledge graph; running philosophical and strategic analyses; responding to consultation requests; generating visual knowledge representations; surfacing UBOS-aligned recommendations.
- **Excluded**: Task orchestration, research execution, implementation planning, or triggering downstream agents. Those responsibilities remain with the AI Prime Agent and other specialised agents that consume the Master Librarian’s guidance.


## Core Purpose

This agent acts as the "UBOS wisdom keeper" that:
- Maintains comprehensive knowledge of all 4 UBOS books
- Recognizes patterns and interconnections between concepts
- Provides philosophical consultation to the AI Prime Agent
- Ensures UBOS alignment in all system decisions
- Generates visual knowledge graphs and relationship maps

## Functional Requirements

### FR-1: Knowledge Ingestion System
**Description**: Automatically ingest and process all UBOS book content
**Priority**: High
**Acceptance Criteria**:
- Parse all YAML files from SystemFundamentals/Books/
- Extract concepts, principles, practices, and quotes
- Maintain source references and metadata
- Validate data against UBOS schema
- Handle incremental updates to book content

### FR-2: Knowledge Graph Construction
**Description**: Build and maintain a comprehensive knowledge graph
**Priority**: High
**Acceptance Criteria**:
- Create nodes for all UBOS concepts
- Build semantic relationships between concepts
- Support relationship types: builds_on, enables, conflicts_with, requires, synergizes_with
- Calculate concept importance and centrality measures
- Enable graph traversal and querying

### FR-3: Pattern Recognition Engine
**Description**: Identify patterns and connections across all books
**Priority**: High
**Acceptance Criteria**:
- Analyze cross-book concept relationships
- Detect conflicting or synergistic principles
- Identify concept dependencies and prerequisites
- Generate strategic pathway recommendations
- Update patterns based on new knowledge

### FR-4: Philosophy Consultation Interface
**Description**: Provide UBOS-aligned guidance to other agents
**Priority**: High
**Acceptance Criteria**:
- Accept task descriptions and context from AI Prime Agent
- Analyze tasks through UBOS philosophical lens
- Return structured recommendations with confidence scores
- Identify relevant principles and practices
- Flag potential conflicts with UBOS philosophy

### FR-5: Visual Knowledge Representation
**Description**: Generate visual diagrams of knowledge structures
**Priority**: Medium
**Acceptance Criteria**:
- Create Mermaid diagrams of concept relationships
- Generate strategic pathway visualizations
- Support interactive graph exploration
- Update diagrams based on knowledge changes
- Export diagrams in multiple formats

### FR-6: API Interface
**Description**: Expose knowledge services via REST API
**Priority**: High
**Acceptance Criteria**:
- Provide consultation endpoints for AI Prime Agent
- Support knowledge graph queries
- Enable concept search and retrieval
- Return structured JSON responses
- Handle concurrent requests efficiently

## Non-Functional Requirements

### NFR-1: Performance
- Response time < 500ms for simple consultations
- Handle up to 100 concurrent consultation requests
- Memory usage < 2GB for full knowledge base
- Support knowledge base of 10,000+ concepts

### NFR-2: Reliability
- 99.9% uptime availability
- Graceful degradation under high load
- Automatic recovery from failures
- Data consistency guarantees

### NFR-3: Scalability
- Horizontal scaling support
- Efficient graph traversal algorithms
- Lazy loading for large datasets
- Caching for frequently accessed data

### NFR-4: Security
- API key authentication
- Input validation and sanitization
- Secure storage of sensitive data
- Rate limiting and abuse prevention

## Technical Architecture

### Core Components

#### 1. Knowledge Ingestion Service
```python
class UBOSKnowledgeIngester:
    def ingest_books(self) -> None
    def parse_yaml_content(self, file_path: str) -> Dict
    def extract_concepts(self, content: Dict) -> List[Concept]
    def validate_schema(self, data: Dict) -> bool
```

#### 2. Graph Management System
```python
class UBOSKnowledgeGraph:
    def add_concept(self, concept: Concept) -> None
    def add_relationship(self, source: str, target: str, relation_type: str) -> None
    def query_concepts(self, filters: Dict) -> List[Concept]
    def get_relationships(self, concept_id: str) -> List[Relationship]
    def calculate_centrality(self) -> Dict[str, float]
```

#### 3. Pattern Recognition Engine
```python
class UBOSPatternEngine:
    def analyze_cross_book_patterns(self) -> List[Pattern]
    def detect_conflicts(self) -> List[Conflict]
    def identify_dependencies(self) -> List[Dependency]
    def generate_pathways(self, goal: str) -> List[Pathway]
```

#### 4. Philosophy Consultant
```python
class UBOSPhilosophyConsultant:
    def consult(self, task: str, context: Dict) -> ConsultationResult
    def analyze_alignment(self, proposal: str) -> AlignmentScore
    def recommend_principles(self, scenario: str) -> List[Principle]
    def identify_conflicts(self, proposal: str) -> List[Conflict]
```

#### 5. Visualization Generator
```python
class UBOSVisualizationGenerator:
    def generate_concept_diagram(self, concept_id: str) -> str
    def create_pathway_diagram(self, pathway: Pathway) -> str
    def build_relationship_map(self, filters: Dict) -> str
    def export_diagram(self, diagram: str, format: str) -> bytes
```

### Data Models

#### Concept
```python
@dataclass
class Concept:
    id: str
    title: str
    description: str
    book_source: str
    chapter: str
    concept_type: ConceptType  # principle, practice, framework, quote
    topics: List[str]
    source_refs: List[str]
    confidence: float
    metadata: Dict[str, Any]
```

#### Relationship
```python
@dataclass
class Relationship:
    source_id: str
    target_id: str
    relationship_type: RelationshipType
    confidence: float
    evidence: List[str]
    metadata: Dict[str, Any]
```

#### ConsultationResult
```python
@dataclass
class ConsultationResult:
    alignment_score: float
    relevant_principles: List[Principle]
    recommended_approaches: List[str]
    potential_conflicts: List[str]
    confidence: float
    reasoning: str
    follow_up_questions: List[str]
```

## API Specification

### Consultation Endpoints

#### POST /api/v1/consult
**Description**: Get UBOS-aligned guidance for a task
**Request Body**:
```json
{
    "task": "string",
    "context": {
        "user_background": "string",
        "project_type": "string",
        "constraints": ["string"]
    },
    "priority": "high|medium|low"
}
```
**Response**:
```json
{
    "consultation_id": "string",
    "alignment_score": 0.95,
    "relevant_principles": [
        {
            "id": "principle-01-blueprint-thinking",
            "title": "Blueprint Thinking",
            "relevance": 0.9,
            "application": "string"
        }
    ],
    "recommended_approaches": ["string"],
    "potential_conflicts": ["string"],
    "confidence": 0.87,
    "reasoning": "string",
    "follow_up_questions": ["string"]
}
```

### Knowledge Graph Endpoints

#### GET /api/v1/concepts
**Description**: Query concepts by various filters
**Query Parameters**:
- `topic`: Filter by topic
- `book`: Filter by source book
- `type`: Filter by concept type
- `search`: Text search in titles/descriptions

#### GET /api/v1/concepts/{id}
**Description**: Get detailed information about a specific concept

#### GET /api/v1/concepts/{id}/relationships
**Description**: Get all relationships for a concept

#### GET /api/v1/graph/visualize
**Description**: Generate Mermaid diagram for knowledge graph subset

## Development Roadmap

### Phase 1: Core Foundation (Week 1-2)
- [ ] Set up development environment
- [ ] Implement YAML ingestion system
- [ ] Create basic knowledge graph structure
- [ ] Build concept and relationship models
- [ ] Create simple consultation interface

### Phase 2: AI Integration (Week 3-4)
- [ ] Integrate Google Gemini 2.5 Pro API
- [ ] Implement pattern recognition algorithms
- [ ] Build philosophy consultation logic
- [ ] Add confidence scoring system
- [ ] Create basic API endpoints

### Phase 3: Advanced Features (Week 5-6)
- [ ] Implement Mermaid diagram generation
- [ ] Add graph traversal optimizations
- [ ] Build caching system
- [ ] Create batch processing capabilities
- [ ] Implement real-time updates

### Phase 4: Production Ready (Week 7-8)
- [ ] Add comprehensive error handling
- [ ] Implement security measures
- [ ] Create monitoring and logging
- [ ] Add performance optimizations
- [ ] Write comprehensive tests

## Testing Strategy

### Unit Tests
- YAML parsing and validation
- Graph construction and queries
- Pattern recognition algorithms
- API endpoint functionality
- Gemini API integration

### Integration Tests
- End-to-end consultation workflows
- Knowledge graph accuracy validation
- Cross-component communication
- Database persistence
- External API interactions

### Performance Tests
- Load testing with large knowledge bases
- Concurrent consultation handling
- Memory usage profiling
- Response time optimization
- Scalability validation

## Deployment Strategy

### Development Environment
- Local Python environment
- NetworkX for graph management
- SQLite for development database
- Flask development server
- Local file-based storage

### Staging Environment
- Docker containerization
- Neo4j graph database
- Redis for caching
- Nginx load balancer
- Cloud storage integration

### Production Environment
- Kubernetes orchestration
- Managed graph database service
- Distributed caching
- API gateway
- Monitoring and alerting

## Success Metrics

### Knowledge Coverage
- **Target**: 95% of UBOS concepts captured accurately
- **Measurement**: Manual validation against source books
- **Timeline**: End of Phase 2

### Consultation Quality
- **Target**: 85% alignment score accuracy
- **Measurement**: Human expert validation
- **Timeline**: End of Phase 3

### Performance
- **Target**: <500ms average response time
- **Measurement**: Automated performance tests
- **Timeline**: End of Phase 4

### Integration Success
- **Target**: Seamless AI Prime Agent integration
- **Measurement**: End-to-end workflow tests
- **Timeline**: End of Phase 4

## Risk Mitigation

### Technical Risks
- **Gemini API rate limits**: Implement caching and request optimization
- **Knowledge graph complexity**: Use efficient algorithms and indexing
- **Data consistency**: Implement validation and backup procedures

### Business Risks
- **Changing requirements**: Maintain flexible architecture
- **Resource constraints**: Prioritize core functionality
- **Integration challenges**: Create robust API interfaces

## Appendix A: Interface & Implementation Details

### A.1 Data Model Contracts
| Entity | Description | Required Fields | Optional Fields |
|--------|-------------|-----------------|-----------------|
| `Concept` | Canonical knowledge record for ideas, practices, quotes, frameworks, or meta-principles. | `id`, `title`, `type` (`principle`\|`practice`\|`framework`\|`quote`\|`metaphor`\|`checklist`), `description`, `topics[]`, `source_refs[]` | `one_liner`, `actions[]`, `related_ids[]`, `metadata` (difficulty, reading_time, etc.) |
| `Relationship` | Directed edge linking two concepts in the knowledge graph. | `source_id`, `target_id`, `relationship_type` (`builds_on`\|`enables`\|`conflicts_with`\|`requires`\|`synergizes_with`), `confidence` (0.0–1.0) | `description`, `evidence_refs[]`, `metadata` |
| `ConsultationRequest` | Payload AI Prime submits when seeking guidance. | `task_id`, `summary`, `context[]`, `objectives[]` | `constraints[]`, `preferred_topics[]`, `metadata` |
| `ConsultationResult` | Response returned to AI Prime. | `task_id`, `recommendations[]`, `key_concepts[]`, `confidence`, `ubos_alignment_notes` | `mermaid_diagram`, `follow_up_actions[]`, `warnings[]` |

### A.2 Relationship Inference Heuristics
- **Explicit Links**: Respect `related_ids` inside YAML files (highest confidence).
- **Chapter Co-occurrence**: Shared chapter/topic membership implies `synergizes_with` (confidence scaled by frequency).
- **Practice → Principle**: Practices citing principle IDs map to `enables` edges.
- **Framework Structure**: Framework sections listing prerequisites create `requires` edges.
- **Quote Attribution**: Quotes referencing a concept generate `builds_on` edges.
- **Manual Overrides**: Provide curated CSV/YAML overrides that supersede heuristics.
- **Conflict Detection**: Detect opposing recommendations (keywords/human curation) to emit `conflicts_with` edges with conservative confidence.

### A.3 Gemini 2.5 Pro Integration
- **Client Wrapper**: Provide `generate_consultation(prompt, context)` with exponential backoff (2s, 4s, 8s) and max 3 retries.
- **Prompt Composition**: Include task summary, extracted concepts, graph insights, UBOS principles, and required output format.
- **Failure Modes**: On quota exhaustion or timeout (>20s), return partial results with `warnings[]` and flag `confidence` ≤ 0.4.
- **Response Contract**: Expect JSON containing `analysis`, `recommended_concepts`, `strategic_guidance`, `risks`, `next_steps`.
- **Caching**: Cache recent consultations by task hash to reduce duplicate Gemini calls.

### A.4 API Contract
| Method | Route | Description | Request | Response |
|--------|-------|-------------|---------|----------|
| `GET` | `/concepts/{id}` | Fetch a single concept. | Path `id` | Concept schema |
| `GET` | `/concepts` | Filter concepts by topic/type/search. | Query `topic`, `type`, `q`, `page`, `page_size` | Paginated concepts |
| `POST` | `/consult` | Run a UBOS consultation. | `ConsultationRequest` | `ConsultationResult` |
| `GET` | `/graph/path` | Shortest path between two concepts. | Query `source_id`, `target_id`, `max_depth` | Path nodes + edges |
| `GET` | `/graph/neighbors/{id}` | Adjacent concepts with relationship metadata. | Path `id`, optional `relationship_type` | Neighbor list |
| `POST` | `/graph/diagram` | Generate Mermaid diagram for given concept IDs. | `{ "concept_ids": [], "style": {...} }` | Mermaid code + rendered URL |

### A.5 Testing Expectations
- **Ingestion**: Verify parsing of valid YAML, graceful handling of missing fields, and incremental update scenarios.
- **Graph**: Confirm edge counts from heuristics/manual overrides, centrality calculations, and persistence.
- **Consultation**: Mock Gemini responses to ensure UBOS notes and concept references are present; cover timeout/partial data cases.
- **API**: Contract tests for each endpoint, including schema validation, pagination, and rate-limit errors.
- **Integration**: End-to-end test for “task → consultation → diagram → knowledge update”.
- **Regression**: Snapshot knowledge graph metrics to detect drift.

### A.6 Operational Integration Flow
- **Mermaid Agent**: Trigger diagram generation after successful consultations and on explicit `/graph/diagram` calls; attach diagram metadata to consultation results.
- **Context7 MCP**: Invoked when Gemini flags missing technical documentation or when clients set `needs_context=true`; cache retrieved docs per task.
- **Research Agent**: Optional context blocks may accompany consultation requests; annotate responses to distinguish internal vs external insights.
- **Monitoring**: Emit structured logs for consultation decisions, Gemini usage, MCP lookups, and graph updates to feed feedback loops.

## Conclusion

The Master Librarian Agent will serve as the philosophical foundation of the UBOS AI ecosystem, ensuring all decisions align with the core principles from the books. Its comprehensive knowledge graph and consultation capabilities will enable intelligent, UBOS-aligned AI agent orchestration.
