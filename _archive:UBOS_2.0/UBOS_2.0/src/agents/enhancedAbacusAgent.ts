import { BaseAgent, AgentRunOptions, AgentContext } from './baseAgent.js';
import { AgentResult } from '../orchestrator/types.js';
import { 
  EnhancedPerplexityResearch, 
  ResearchQuery, 
  runEnhancedPerplexityResearch,
  conductDeepResearch 
} from '../tools/enhancedPerplexityResearch.js';

interface ResearchTaskOptions {
  depth?: 'quick' | 'comprehensive' | 'deep';
  domain?: string;
  sources?: 'academic' | 'commercial' | 'mixed';
  followUp?: boolean;
  saveResults?: boolean;
}

export class EnhancedAbacusAgent extends BaseAgent {
  private researcher: EnhancedPerplexityResearch;

  constructor(id: string, requirementId: string) {
    super(id, requirementId);
    this.researcher = new EnhancedPerplexityResearch();
  }

  get type() { return 'EnhancedAbacusAgent'; }

  async run(opts: AgentRunOptions, ctx?: AgentContext): Promise<AgentResult> {
    const startedAt = this.now();

    try {
      if (opts.dryRun) {
        return {
          agentId: this.id,
          requirementId: this.requirementId,
          success: true,
          output: '[Dry run] EnhancedAbacusAgent would conduct comprehensive research with cost tracking and structured results.',
          startedAt,
          finishedAt: this.now()
        };
      }

      const taskOptions = this.parseTaskOptions(opts.input, ctx);
      const researchResult = await this.conductResearch(opts.input, taskOptions);

      return {
        agentId: this.id,
        requirementId: this.requirementId,
        success: true,
        output: researchResult.output,
        startedAt,
        finishedAt: this.now(),
        metadata: {
          researchCost: researchResult.cost,
          confidence: researchResult.confidence,
          tokensUsed: researchResult.tokensUsed,
          researchId: researchResult.researchId
        }
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

  private parseTaskOptions(input: string, ctx?: AgentContext): ResearchTaskOptions {
    const inputLower = input.toLowerCase();
    
    // Determine research depth
    let depth: 'quick' | 'comprehensive' | 'deep' = 'comprehensive';
    if (inputLower.includes('quick') || inputLower.includes('brief')) {
      depth = 'quick';
    } else if (inputLower.includes('deep') || inputLower.includes('detailed') || inputLower.includes('thorough')) {
      depth = 'deep';
    }

    // Determine domain
    let domain: string | undefined;
    const domainKeywords = {
      'eu_funding': ['eu fund', 'european fund', 'horizon', 'grant', 'h2020', 'h2025'],
      'biotechnology': ['biotech', 'biology', 'pharmaceutical', 'drug', 'therapeutic'],
      'agriculture': ['agriculture', 'farming', 'plant', 'crop', 'xylella'],
      'chemistry': ['chemistry', 'chemical', 'compound', 'synthesis', 'phosphinic'],
      'research_methods': ['research method', 'methodology', 'analysis', 'study design'],
      'market_analysis': ['market', 'competition', 'industry', 'commercial'],
      'regulatory': ['regulation', 'regulatory', 'compliance', 'approval', 'efsa']
    };

    for (const [domainKey, keywords] of Object.entries(domainKeywords)) {
      if (keywords.some(keyword => inputLower.includes(keyword))) {
        domain = domainKey;
        break;
      }
    }

    // Determine sources preference
    let sources: 'academic' | 'commercial' | 'mixed' = 'mixed';
    if (inputLower.includes('academic') || inputLower.includes('peer review') || inputLower.includes('journal')) {
      sources = 'academic';
    } else if (inputLower.includes('commercial') || inputLower.includes('industry') || inputLower.includes('market')) {
      sources = 'commercial';
    }

    // Check for follow-up request
    const followUp = inputLower.includes('follow up') || inputLower.includes('more detail') || depth === 'deep';

    // Context overrides
    const contextOptions = ctx?.shared?.researchOptions as ResearchTaskOptions || {};

    return {
      depth: contextOptions.depth || depth,
      domain: contextOptions.domain || domain,
      sources: contextOptions.sources || sources,
      followUp: contextOptions.followUp !== undefined ? contextOptions.followUp : followUp,
      saveResults: contextOptions.saveResults !== undefined ? contextOptions.saveResults : true
    };
  }

  private async conductResearch(input: string, options: ResearchTaskOptions) {
    const query = this.buildResearchQuery(input, options);

    if (options.followUp && options.depth === 'deep') {
      // Use deep research with follow-ups
      const followUpQueries = this.generateFollowUpQueries(input, options.domain);
      const result = await conductDeepResearch(query, options.domain || 'general', followUpQueries);
      
      return {
        output: this.formatDeepResearchOutput(result, input),
        cost: result.totalCost,
        confidence: result.primary.confidence,
        tokensUsed: result.primary.tokensUsed + (result.followUps?.reduce((sum, f) => sum + f.tokensUsed, 0) || 0),
        researchId: result.primary.queryId
      };
    } else {
      // Standard research
      const researchQuery: ResearchQuery = {
        query,
        domain: options.domain,
        researchDepth: options.depth,
        sources: options.sources
      };

      const result = await this.researcher.conductResearch(researchQuery);
      
      return {
        output: this.formatStandardResearchOutput(result, input),
        cost: result.costUSD,
        confidence: result.confidence,
        tokensUsed: result.tokensUsed,
        researchId: result.queryId
      };
    }
  }

  private buildResearchQuery(input: string, options: ResearchTaskOptions): string {
    // Enhance the input query based on context
    let enhancedQuery = input;

    // Add domain context if available
    if (options.domain) {
      const domainContexts = {
        'eu_funding': 'in the context of European Union funding, grants, and Horizon Europe programs',
        'biotechnology': 'in the biotechnology and pharmaceutical industry',
        'agriculture': 'in agricultural applications and plant health',
        'chemistry': 'in chemistry and chemical synthesis',
        'market_analysis': 'from a market analysis and competitive intelligence perspective',
        'regulatory': 'regarding regulatory requirements and compliance'
      };

      const context = domainContexts[options.domain as keyof typeof domainContexts];
      if (context) {
        enhancedQuery = `${input} ${context}`;
      }
    }

    // Add depth-specific instructions
    if (options.depth === 'deep') {
      enhancedQuery += '. Please provide comprehensive technical details, current market status, key players, recent developments, and future outlook.';
    } else if (options.depth === 'quick') {
      enhancedQuery += '. Please provide a concise overview with key facts and current status.';
    }

    return enhancedQuery;
  }

  private generateFollowUpQueries(input: string, domain?: string): string[] {
    const baseQuery = input.toLowerCase();
    const followUps: string[] = [];

    // Generate contextual follow-up questions
    if (baseQuery.includes('market') || domain === 'market_analysis') {
      followUps.push(`What are the key competitors and market size for ${input}?`);
      followUps.push(`What are the latest market trends and forecasts related to ${input}?`);
    }

    if (baseQuery.includes('regulation') || domain === 'regulatory') {
      followUps.push(`What are the regulatory requirements and approval processes for ${input}?`);
      followUps.push(`What recent regulatory changes affect ${input}?`);
    }

    if (baseQuery.includes('research') || baseQuery.includes('study')) {
      followUps.push(`What are the most recent research developments in ${input}?`);
      followUps.push(`What are the main research gaps and challenges in ${input}?`);
    }

    if (domain === 'eu_funding') {
      followUps.push(`What EU funding opportunities are available for ${input}?`);
      followUps.push(`What are successful case studies of EU-funded projects in ${input}?`);
    }

    // If no specific follow-ups generated, create generic ones
    if (followUps.length === 0) {
      followUps.push(`What are the current trends and developments in ${input}?`);
      followUps.push(`What are the main challenges and opportunities in ${input}?`);
    }

    return followUps.slice(0, 2); // Limit to 2 follow-ups to control costs
  }

  private formatStandardResearchOutput(result: any, originalInput: string): string {
    const confidence = Math.round(result.confidence * 100);
    const cost = result.costUSD.toFixed(4);

    return `
🔍 RESEARCH COMPLETED: ${originalInput}
Research ID: ${result.queryId}
Confidence: ${confidence}% | Cost: $${cost} | Tokens: ${result.tokensUsed}

${result.response}

📊 RESEARCH METADATA:
• Processing Time: ${result.processingTimeMs}ms
• Sources Found: ${result.sources?.length || 0}
• Research Quality: ${confidence >= 80 ? 'High' : confidence >= 60 ? 'Medium' : 'Standard'}

${result.sources && result.sources.length > 0 ? `
📚 KEY SOURCES:
${result.sources.slice(0, 5).map((s: string) => `• ${s}`).join('\n')}
` : ''}

💡 Research saved for future reference: logs/research_data/perplexity/research_${result.queryId}.*
`;
  }

  private formatDeepResearchOutput(result: any, originalInput: string): string {
    return `
🔬 DEEP RESEARCH COMPLETED: ${originalInput}
Primary Research ID: ${result.primary.queryId}
Total Cost: $${result.totalCost.toFixed(4)}
Follow-up Queries: ${result.followUps?.length || 0}

${result.synthesis}

📈 RESEARCH SUMMARY:
• Primary Confidence: ${Math.round(result.primary.confidence * 100)}%
• Total Processing: Multi-stage analysis
• Comprehensive Coverage: ${result.followUps ? 'Yes' : 'Basic'}

💎 This deep research provides comprehensive insights beyond standard queries.
Full research files available in: logs/research_data/perplexity/

🎯 NEXT STEPS:
1. Review detailed findings in research files
2. Consider follow-up research on specific aspects
3. Apply insights to your project planning
`;
  }

  // Method for getting research history - useful for context
  async getRecentResearch(limit: number = 5): Promise<any[]> {
    return await this.researcher.getResearchHistory(limit);
  }

  // Method for getting research costs - useful for budget tracking
  async getResearchCosts(days: number = 30): Promise<number> {
    return await this.researcher.getTotalResearchCost(days);
  }

  // Method for research analysis and recommendations
  async analyzeResearchNeeds(projectDescription: string): Promise<{
    recommendedQueries: string[];
    estimatedCost: number;
    researchStrategy: string;
  }> {
    // This could be enhanced with AI-powered analysis
    const queries: string[] = [];
    const desc = projectDescription.toLowerCase();

    // Generate research recommendations based on project content
    if (desc.includes('market')) {
      queries.push(`Market analysis and competitive landscape for ${projectDescription}`);
      queries.push(`Market size and growth projections for ${projectDescription}`);
    }

    if (desc.includes('regulation') || desc.includes('approval')) {
      queries.push(`Regulatory requirements and approval processes for ${projectDescription}`);
    }

    if (desc.includes('technology') || desc.includes('innovation')) {
      queries.push(`Latest technological developments in ${projectDescription}`);
      queries.push(`Innovation trends and emerging technologies in ${projectDescription}`);
    }

    if (desc.includes('funding') || desc.includes('grant')) {
      queries.push(`EU funding opportunities for ${projectDescription}`);
      queries.push(`Successful funding case studies similar to ${projectDescription}`);
    }

    // Estimate costs (based on comprehensive research for each query)
    const estimatedCost = queries.length * 0.015; // Approximate cost per comprehensive query

    const researchStrategy = `
RECOMMENDED RESEARCH STRATEGY for: ${projectDescription}

1. Primary Research Queries: ${queries.length}
2. Estimated Total Cost: $${estimatedCost.toFixed(3)}
3. Research Depth: Comprehensive with selective deep dives
4. Timeline: ${Math.ceil(queries.length * 2)} minutes for sequential execution

Strategy:
• Start with market and competitive analysis
• Follow with regulatory and technical research
• Conclude with funding and opportunity identification
• Use deep research for the most critical aspects

This analysis will provide comprehensive coverage while optimizing for cost-effectiveness.
`;

    return {
      recommendedQueries: queries,
      estimatedCost,
      researchStrategy
    };
  }
}

