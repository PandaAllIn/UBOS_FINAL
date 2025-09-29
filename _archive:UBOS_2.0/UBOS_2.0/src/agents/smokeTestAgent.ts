import { BaseAgent, AgentRunOptions, AgentContext } from './baseAgent.js';
import { AgentResult } from '../orchestrator/types.js';

export class SmokeTestAgent extends BaseAgent {
  get type() { return 'SmokeTestAgent'; }

  async run(opts: AgentRunOptions, _ctx?: AgentContext): Promise<AgentResult> {
    const startedAt = this.now();
    try {
      return {
        agentId: this.id,
        requirementId: this.requirementId,
        success: true,
        output: `SmokeTestAgent OK: ${opts.input || 'no input'}`,
        startedAt,
        finishedAt: this.now()
      };
    } catch (e: any) {
      return {
        agentId: this.id,
        requirementId: this.requirementId,
        success: false,
        output: '',
        error: e?.message || String(e),
        startedAt,
        finishedAt: this.now()
      };
    }
  }
}



