import { BaseAgent, AgentRunOptions, AgentContext } from './baseAgent.js';
import { AgentResult } from '../orchestrator/types.js';
import { runPerplexityTest } from '../tools/perplexity_sonar.js';
import { trackLLMUsage } from '../analytics/autoTracker.js';
import { promises as fs } from 'fs';
import path from 'path';

interface AgentSummoningRequest {
  taskDescription: string;
  domain?: string;
  complexity?: number;
  budget?: number;
  requirements?: string[];
}

interface AgentDiscoveryResult {
  agentName: string;
  provider: string;
  capabilities: string[];
  cost: string;
  integrationComplexity: 'low' | 'medium' | 'high';
  recommendation: 'optimal' | 'suitable' | 'not_recommended';
  reasoning: string;
}

interface AgentSummoningResult {
  taskId: string;
  discoveredAgents: AgentDiscoveryResult[];
  recommendations: string[];
  implementationPlan: string;
  estimatedCost: number;
  confidence: number;
}

export class AgentSummonerAgent extends BaseAgent {
  get type() { return 'AgentSummonerAgent'; }
  
  private async saveResult(result: AgentSummoningResult): Promise<void> {
    const baseDir = 'logs/agent_summoner';
    await fs.mkdir(baseDir, { recursive: true });
    const filename = `summoning_${Date.now()}.json`;
    await fs.writeFile(
      path.join(baseDir, filename),
      JSON.stringify(result, null, 2)
    );
  }

  async run(opts: AgentRunOptions, ctx?: AgentContext): Promise<AgentResult> {
    const startedAt = this.now();
    
    try {
      if (opts.dryRun) {
        return {
          agentId: this.id,
          requirementId: this.requirementId,
          success: true,
          output: '[Dry run] AgentSummoner would research optimal agents for the task.',
          startedAt,
          finishedAt: this.now()
        };
      }

      const request = this.parseRequest(opts.input);
      const result = await this.summonOptimalAgents(request);
      
      await this.saveResult(result);
      
      const summary = this.formatSummary(result);
      
      return {
        agentId: this.id,
        requirementId: this.requirementId,
        success: true,
        output: summary,
        startedAt,
        finishedAt: this.now(),
        metadata: { summoningResult: result }
      };

    } catch (error: any) {
      return {
        agentId: this.id,
        requirementId: this.requirementId,
        success: false,
        output: '',
        error: error?.message || String(error),
        startedAt,
        finishedAt: this.now()
      };
    }
  }

  private parseRequest(input: string): AgentSummoningRequest {
    // Simple parsing - could be enhanced with NLP
    return {
      taskDescription: input,
      domain: this.extractDomain(input),
      complexity: this.assessComplexity(input),
      requirements: this.extractRequirements(input)
    };
  }

  private extractDomain(input: string): string {
    const domainKeywords = {
      'research': ['research', 'study', 'analyze', 'investigate'],
      'development': ['build', 'create', 'develop', 'implement'],
      'analysis': ['analyze', 'evaluate', 'assess', 'review'],
      'automation': ['automate', 'schedule', 'monitor', 'track']
    };

    const inputLower = input.toLowerCase();
    for (const [domain, keywords] of Object.entries(domainKeywords)) {
      if (keywords.some(keyword => inputLower.includes(keyword))) {
        return domain;
      }
    }
    return 'general';
  }

  private assessComplexity(input: string): number {
    const complexityIndicators = [
      'integrate', 'coordinate', 'multiple', 'complex', 'advanced',
      'real-time', 'continuous', 'comprehensive', 'sophisticated'
    ];
    
    const inputLower = input.toLowerCase();
    const matchCount = complexityIndicators.filter(indicator => 
      inputLower.includes(indicator)
    ).length;
    
    return Math.min(10, Math.max(1, matchCount + 3));
  }

  private extractRequirements(input: string): string[] {
    const requirements: string[] = [];
    const inputLower = input.toLowerCase();
    
    if (inputLower.includes('real-time') || inputLower.includes('live')) {
      requirements.push('real-time-capability');
    }
    if (inputLower.includes('research') || inputLower.includes('data')) {
      requirements.push('research-capability');
    }
    if (inputLower.includes('automat') || inputLower.includes('schedul')) {
      requirements.push('automation-capability');
    }
    if (inputLower.includes('integrat') || inputLower.includes('api')) {
      requirements.push('integration-capability');
    }
    
    return requirements;
  }

  private async summonOptimalAgents(request: AgentSummoningRequest): Promise<AgentSummoningResult> {
    const taskId = `task_${Date.now()}`;
    
    // Step 1: Agent Discovery Research
    const discoveryPrompt = this.buildDiscoveryPrompt(request);
    const discoveryResearch = await runPerplexityTest(discoveryPrompt);
    
    // Step 2: Agent Evaluation Research
    const evaluationPrompt = this.buildEvaluationPrompt(request, discoveryResearch);
    const evaluationResearch = await runPerplexityTest(evaluationPrompt);
    
    // Step 3: Implementation Research
    const implementationPrompt = this.buildImplementationPrompt(request);
    const implementationResearch = await runPerplexityTest(implementationPrompt);
    
    // Parse results and create structured recommendations
    const result: AgentSummoningResult = {
      taskId,
      discoveredAgents: await this.parseDiscoveredAgents(discoveryResearch),
      recommendations: this.parseRecommendations(evaluationResearch),
      implementationPlan: implementationResearch,
      estimatedCost: this.estimateCost(request),
      confidence: this.calculateConfidence(discoveryResearch, evaluationResearch)
    };
    
    return result;
  }

  private buildDiscoveryPrompt(request: AgentSummoningRequest): string {
    return `Task: Discover and research AI agents, tools, and services optimal for this specific requirement:

TASK DESCRIPTION: "${request.taskDescription}"
DOMAIN: ${request.domain}
COMPLEXITY: ${request.complexity}/10
REQUIREMENTS: ${request.requirements?.join(', ') || 'None specified'}

Please research and identify:
1. Specialized AI agents or services available in 2024-2025 for this domain
2. Commercial platforms, APIs, and tools that could handle this task
3. Open-source solutions and frameworks
4. Academic or research-based tools
5. Emerging technologies relevant to this requirement

For each discovered solution, provide:
- Name and provider
- Core capabilities
- API availability
- Pricing model (if known)
- Integration complexity
- Performance benchmarks (if available)

Focus on current, available solutions that could be implemented within 30 days.`;
  }

  private buildEvaluationPrompt(request: AgentSummoningRequest, discoveryResults: string): string {
    return `Task: Evaluate and rank the discovered AI agents for this specific use case:

ORIGINAL TASK: "${request.taskDescription}"
DISCOVERED SOLUTIONS:
${discoveryResults}

Please provide detailed evaluation covering:
1. SUITABILITY: How well does each solution match the task requirements?
2. INTEGRATION: How easily can it be integrated into existing TypeScript/Node.js systems?
3. COST-EFFECTIVENESS: What are the actual costs vs value provided?
4. RELIABILITY: Track record, stability, and support quality
5. SCALABILITY: Can it handle growing demands?
6. IMPLEMENTATION TIME: How quickly can it be deployed?

Rank top 3 recommendations with specific reasoning for each choice.
Include implementation complexity assessment and potential risks.`;
  }

  private buildImplementationPrompt(request: AgentSummoningRequest): string {
    return `Task: Create implementation plan for integrating optimal agents:

TASK: "${request.taskDescription}"

Please provide:
1. Step-by-step implementation plan
2. Required API keys, credentials, and setup
3. Code integration points and architecture considerations
4. Testing and validation approach
5. Deployment and monitoring requirements
6. Potential challenges and mitigation strategies

Focus on practical, actionable steps for a TypeScript/Node.js environment with existing agent orchestration framework.`;
  }

  private async parseDiscoveredAgents(research: string): Promise<AgentDiscoveryResult[]> {
    // This would be enhanced with better parsing logic
    const agents: AgentDiscoveryResult[] = [];
    
    // Mock parsing for now - would implement proper text analysis
    const lines = research.split('\n');
    let currentAgent: Partial<AgentDiscoveryResult> = {};
    
    for (const line of lines) {
      if (line.includes('Name:') || line.includes('Agent:') || line.includes('Service:')) {
        if (currentAgent.agentName) {
          agents.push(currentAgent as AgentDiscoveryResult);
        }
        currentAgent = {
          agentName: line.replace(/.*(?:Name|Agent|Service):\s*/i, '').trim(),
          capabilities: [],
          recommendation: 'suitable'
        };
      }
      // Add more parsing logic here
    }
    
    return agents;
  }

  private parseRecommendations(research: string): string[] {
    const recommendations = research.split('\n')
      .filter(line => line.includes('recommend') || line.includes('suggest'))
      .map(line => line.trim())
      .filter(line => line.length > 20);
    
    return recommendations.slice(0, 5); // Top 5 recommendations
  }

  private estimateCost(request: AgentSummoningRequest): number {
    // Estimate based on complexity and domain
    const baseCost = 10; // $10 base
    const complexityMultiplier = (request.complexity || 5) / 10;
    const domainMultiplier = request.domain === 'research' ? 1.5 : 1.0;
    
    return baseCost * complexityMultiplier * domainMultiplier;
  }

  private calculateConfidence(discoveryResults: string, evaluationResults: string): number {
    // Simple confidence calculation based on result quality
    const discoveryLength = discoveryResults.length;
    const evaluationLength = evaluationResults.length;
    
    const baseConfidence = 0.7;
    const lengthBonus = Math.min(0.2, (discoveryLength + evaluationLength) / 10000);
    
    return Math.min(0.95, baseConfidence + lengthBonus);
  }

  private formatSummary(result: AgentSummoningResult): string {
    const { discoveredAgents, recommendations, confidence, estimatedCost } = result;
    
    return `
🤖 AGENT SUMMONING COMPLETE
Task ID: ${result.taskId}
Confidence: ${Math.round(confidence * 100)}%
Estimated Integration Cost: $${estimatedCost}

📊 DISCOVERED AGENTS: ${discoveredAgents.length}
${discoveredAgents.slice(0, 3).map(agent => `
• ${agent.agentName}${agent.provider ? ` (${agent.provider})` : ''}
  Capabilities: ${agent.capabilities?.join(', ') || 'Multiple'}
  Recommendation: ${agent.recommendation?.toUpperCase()}
  ${agent.reasoning || 'Advanced AI capabilities'}
`).join('')}

💡 TOP RECOMMENDATIONS:
${recommendations.slice(0, 3).map((rec, i) => `${i + 1}. ${rec}`).join('\n')}

🛠️ NEXT STEPS:
1. Review detailed implementation plan in logs/agent_summoner/
2. Select optimal agent(s) based on your priorities
3. Proceed with integration using provided guidance

Full results saved to: logs/agent_summoner/summoning_${Date.now()}.json
`;
  }
}

