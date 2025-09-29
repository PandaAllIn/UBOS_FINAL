import { BaseAgent, type AgentRunOptions, type AgentContext } from './baseAgent.js';
import type { AgentResult, AgentSpec } from '../orchestrator/types.js';
import { MultiAgentCoordinator } from '../utils/multiAgentCoordinator.js';
import { MessageBus } from '../messaging/messageBus.js';

export interface CoordinationParams {
  agents: AgentSpec[];
  inputs: Record<string, string>; // requirementId -> input
  timeoutMs?: number;
  concurrency?: number;
  dryRun?: boolean;
}

/**
 * CoordinationAgent
 * An agent that coordinates multiple sub-agents using the MessageBus-based
 * MultiAgentCoordinator. It expects coordination parameters in ctx.shared.
 */
export class CoordinationAgent extends BaseAgent {
  get type() { return 'CoordinationAgent'; }

  async run(opts: AgentRunOptions, ctx?: AgentContext): Promise<AgentResult> {
    const startedAt = this.now();
    try {
      const params = (ctx?.shared || {}) as Partial<CoordinationParams>;
      if (!params.agents || !Array.isArray(params.agents) || params.agents.length === 0) {
        throw new Error('CoordinationAgent requires ctx.shared.agents: AgentSpec[]');
      }
      if (!params.inputs || typeof params.inputs !== 'object') {
        throw new Error('CoordinationAgent requires ctx.shared.inputs: Record<string,string>');
      }

      if (opts.dryRun) {
        return {
          agentId: this.id,
          requirementId: this.requirementId,
          success: true,
          output: `[Dry run] Would coordinate ${params.agents.length} agent(s).`,
          startedAt,
          finishedAt: this.now(),
          metadata: { coordinator: true, agents: params.agents.map((a) => a.type) },
        };
      }

      const bus = new MessageBus();
      const coordinator = new MultiAgentCoordinator(bus);
      coordinator.registerAgents(params.agents);
      const summary = await coordinator.execute({
        agents: params.agents,
        inputs: params.inputs,
        timeoutMs: params.timeoutMs ?? opts.timeoutMs,
        concurrency: params.concurrency,
        dryRun: params.dryRun ?? opts.dryRun,
      });

      const lines: string[] = [];
      lines.push(`Coordination complete: ${summary.results.length} result(s).`);
      lines.push(`Success: ${summary.success ? 'yes' : 'no'}`);
      for (const r of summary.results) {
        lines.push(`- ${r.agentId}/${r.requirementId}: ${r.success ? 'OK' : 'ERR'}`);
      }
      if (summary.errors.length) {
        lines.push('Errors:');
        summary.errors.forEach((e) => lines.push(`  - ${e}`));
      }

      return {
        agentId: this.id,
        requirementId: this.requirementId,
        success: summary.success,
        output: lines.join('\n'),
        artifacts: {
          results: summary.results,
          errors: summary.errors,
          taskId: summary.taskId,
        },
        startedAt,
        finishedAt: this.now(),
      };
    } catch (e: any) {
      const errMsg = e?.message || String(e);
      return {
        agentId: this.id,
        requirementId: this.requirementId,
        success: false,
        output: '',
        error: errMsg,
        startedAt,
        finishedAt: this.now(),
      };
    }
  }
}

