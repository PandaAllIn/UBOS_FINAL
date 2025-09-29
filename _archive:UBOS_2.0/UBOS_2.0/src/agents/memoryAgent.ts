import { BaseAgent, AgentRunOptions, AgentContext } from './baseAgent.js';
import { AgentResult } from '../orchestrator/types.js';
import { loadKnowledgeBase, toContext, findNotesByQuery } from '../memory/memoryLoader.js';

export class MemoryAgent extends BaseAgent {
  get type() { return 'MemoryAgent'; }
  async run(opts: AgentRunOptions, _ctx?: AgentContext): Promise<AgentResult> {
    const startedAt = this.now();
    try {
      const notes = await loadKnowledgeBase();
      const results = findNotesByQuery(notes, opts.input);
      const context = toContext(results, { maxBytes: 8000 });
      const output = results.length
        ? `Found ${results.length} related notes. Context preview:\n\n${context}`
        : 'No direct matches in knowledge base.';
      return { agentId: this.id, requirementId: this.requirementId, success: true, output, startedAt, finishedAt: this.now(), artifacts: { matched: results.map(r => ({ path: r.path, title: r.title })) } };
    } catch (e: any) {
      return { agentId: this.id, requirementId: this.requirementId, success: false, output: '', error: e?.message || String(e), startedAt, finishedAt: this.now() };
    }
  }
}

