import { BaseAgent, AgentRunOptions } from './baseAgent.js';
import { AgentResult } from '../orchestrator/types.js';
import { exec } from 'child_process';
import { promisify } from 'util';
import fs from 'fs/promises';
import path from 'path';
import { repoPath, repoRoot } from '../utils/paths.js';

const execAsync = promisify(exec);

export interface SpecKitTask {
  id: string;
  title: string;
  description: string;
  priority: 'high' | 'medium' | 'low';
  estimatedHours: number;
  dependencies: string[];
  status: 'pending' | 'in_progress' | 'completed';
  assignedAgent: 'codex' | 'claude' | 'gemini';
}

export interface SpecKitProject {
  name: string;
  description: string;
  tasks: SpecKitTask[];
  specPath: string;
  planPath: string;
}

export class SpecKitCodexAgent extends BaseAgent {
  get type(): string { return 'spec-kit-codex'; }

  async run(opts: AgentRunOptions): Promise<AgentResult> {
    const startedAt = this.now();
    try {
      const { input } = opts;

      if (input.includes('automate') && input.includes('spec')) {
        return await this.automateSpecToCodex(input);
      }

      if (input.includes('sync') && input.includes('tasks')) {
        return await this.syncTasksFromSpec(input);
      }

      if (input.includes('execute') && input.includes('queue')) {
        return await this.executeTaskQueue(input);
      }

      return {
        agentId: this.id,
        requirementId: this.requirementId,
        success: false,
        output: 'Unsupported Spec-Kit Codex operation. Supported: automate spec, sync tasks, execute queue',
        startedAt,
        finishedAt: this.now()
      };

    } catch (error: any) {
      return {
        agentId: this.id,
        requirementId: this.requirementId,
        success: false,
        output: '',
        error: (error as any)?.message || String(error),
        startedAt,
        finishedAt: this.now()
      };
    }
  }

  private async automateSpecToCodex(input: string): Promise<AgentResult> {
    const startedAt = this.now();
    try {
      // Find all spec directories with Spec-Kit configuration
      const monetizationProjects = [
        'orchestration-saas',
        'tri-party-platform', 
        'reasoning-service',
        'research-command'
      ];

      const automatedProjects: SpecKitProject[] = [];

      for (const project of monetizationProjects) {
        const projectPath = repoPath('monetization-projects', project);
        const specPath = `${projectPath}/specs`;
        const planPath = `${projectPath}/plan.md`;

        try {
          // Check if project has spec files
          await fs.access(specPath);
          
          // Run spec-kit plan to generate tasks
          const { stdout: planOutput } = await execAsync(
            `cd "${projectPath}" && uvx spec-kit plan`,
            { timeout: 30000 }
          );

          // Parse tasks from plan output
          const tasks = await this.parseTasksFromPlan(planOutput, projectPath);
          
          automatedProjects.push({
            name: project,
            description: `Automated ${project} implementation`,
            tasks,
            specPath,
            planPath
          });

          // Auto-assign high priority tasks to Codex
          await this.assignTasksToCodex(tasks, project);

        } catch (error: any) {
          console.log(`Skipping ${project}: ${error.message}`);
        }
      }

      return {
        agentId: this.id,
        requirementId: this.requirementId,
        success: true,
        output: `Automated ${automatedProjects.length} projects with spec-kit → codex integration`,
        artifacts: {
          automatedProjects,
          totalTasks: automatedProjects.reduce((sum, p) => sum + p.tasks.length, 0),
          codexTasks: automatedProjects.reduce((sum, p) => 
            sum + p.tasks.filter(t => t.assignedAgent === 'codex').length, 0
          )
        },
        startedAt,
        finishedAt: this.now()
      };

    } catch (error: any) {
      return {
        agentId: this.id,
        requirementId: this.requirementId,
        success: false,
        output: '',
        error: (error as any)?.message || String(error),
        startedAt,
        finishedAt: this.now()
      };
    }
  }

  private async parseTasksFromPlan(planOutput: string, projectPath: string): Promise<SpecKitTask[]> {
    const tasks: SpecKitTask[] = [];
    const lines = planOutput.split('\n');
    
    let currentTask: Partial<SpecKitTask> = {};
    let taskId = 1;

    for (const line of lines) {
      // Parse task headers (e.g., "## 1. Create API Gateway")
      const taskMatch = line.match(/^##\s+(\d+)\.\s+(.+)$/);
      if (taskMatch) {
        if (currentTask.title) {
          tasks.push(this.finalizeTask(currentTask, taskId++));
        }
        currentTask = {
          title: taskMatch[2],
          description: '',
          priority: 'medium',
          estimatedHours: 4,
          dependencies: [],
          status: 'pending',
          assignedAgent: 'codex'
        };
      }

      // Parse task description
      if (line.startsWith('- ') || line.startsWith('* ')) {
        currentTask.description += line.substring(2) + ' ';
      }

      // Parse priority indicators
      if (line.includes('URGENT') || line.includes('HIGH PRIORITY')) {
        currentTask.priority = 'high';
        currentTask.estimatedHours = 8;
      }
      if (line.includes('CRITICAL') || line.includes('BLOCKER')) {
        currentTask.priority = 'high';
        currentTask.assignedAgent = 'codex';
      }
    }

    // Add final task
    if (currentTask.title) {
      tasks.push(this.finalizeTask(currentTask, taskId));
    }

    return tasks;
  }

  private finalizeTask(task: Partial<SpecKitTask>, id: number): SpecKitTask {
    return {
      id: `task_${id}`,
      title: task.title || 'Untitled Task',
      description: task.description?.trim() || 'No description',
      priority: task.priority || 'medium',
      estimatedHours: task.estimatedHours || 4,
      dependencies: task.dependencies || [],
      status: task.status || 'pending',
      assignedAgent: task.assignedAgent || 'codex'
    };
  }

  private async assignTasksToCodex(tasks: SpecKitTask[], projectName: string): Promise<void> {
    const highPriorityTasks = tasks
      .filter(task => task.priority === 'high' && task.assignedAgent === 'codex')
      .slice(0, 3); // Limit to 3 high priority tasks at once

    for (const task of highPriorityTasks) {
      try {
        // Execute Codex task with enhanced context
        const codexPrompt = `
Project: ${projectName}
Task: ${task.title}
Description: ${task.description}
Priority: ${task.priority}
Estimated Hours: ${task.estimatedHours}

Implementation Requirements:
- Follow BaseAgent pattern in src/agents/
- Register in src/orchestrator/agentFactory.ts
- Use TypeScript strict mode
- Add proper error handling and logging
- Create comprehensive tests
- Follow EUFM coding standards

Execute this task with full technical implementation.
        `.trim();

        // Queue for Codex execution
        await this.queueCodexTask(codexPrompt, task.id, projectName);

        task.status = 'in_progress';
      } catch (error: any) {
        console.error(`Failed to assign task ${task.id} to Codex:`, error);
      }
    }
  }

  private async queueCodexTask(prompt: string, taskId: string, project: string): Promise<void> {
    // Store task for batch execution
    const queuePath = '/tmp/codex-task-queue.json';
    
    let queue: any[] = [];
    try {
      const queueData = await fs.readFile(queuePath, 'utf-8');
      queue = JSON.parse(queueData);
    } catch (error: any) {
      // Queue file doesn't exist, start fresh
    }

    queue.push({
      id: taskId,
      project,
      prompt,
      timestamp: new Date().toISOString(),
      status: 'queued'
    });

    await fs.writeFile(queuePath, JSON.stringify(queue, null, 2));
  }

  private async executeTaskQueue(input: string): Promise<AgentResult> {
    const startedAt = this.now();
    try {
      const queuePath = '/tmp/codex-task-queue.json';
      
      let queue: any[] = [];
      try {
        const queueData = await fs.readFile(queuePath, 'utf-8');
        queue = JSON.parse(queueData);
      } catch (error: any) {
        return {
          agentId: this.id,
          requirementId: this.requirementId,
          success: true,
          output: 'No tasks in queue',
          artifacts: { executed: 0 },
          startedAt,
          finishedAt: this.now()
        };
      }

      const queuedTasks = queue.filter(task => task.status === 'queued');
      const executedTasks = [];

      // Execute up to 3 tasks at once
      for (const task of queuedTasks.slice(0, 3)) {
        try {
          // Execute via Codex CLI
          const { stdout } = await execAsync(
            `npm run dev -- codex:exec "${task.prompt}"`,
            {
              timeout: 300000, // 5 minute timeout
              cwd: repoRoot()
            }
          );

          task.status = 'completed';
          task.result = stdout;
          executedTasks.push(task);

        } catch (error: any) {
          task.status = 'failed';
          task.error = (error as any)?.message || String(error);
          executedTasks.push(task);
        }
      }

      // Update queue
      await fs.writeFile(queuePath, JSON.stringify(queue, null, 2));

      return {
        agentId: this.id,
        requirementId: this.requirementId,
        success: true,
        output: `Executed ${executedTasks.length} Codex tasks from spec-kit automation`,
        artifacts: {
          executed: executedTasks.length,
          successful: executedTasks.filter(t => t.status === 'completed').length,
          failed: executedTasks.filter(t => t.status === 'failed').length,
          results: executedTasks
        },
        startedAt,
        finishedAt: this.now()
      };

    } catch (error: any) {
      return {
        agentId: this.id,
        requirementId: this.requirementId,
        success: false,
        output: '',
        error: (error as any)?.message || String(error),
        startedAt,
        finishedAt: this.now()
      };
    }
  }

  private async syncTasksFromSpec(input: string): Promise<AgentResult> {
    const startedAt = this.now();
    try {
      // Sync tasks from all active monetization projects
      const projects = await this.getAllSpecProjects();
      const syncResults = [];

      for (const project of projects) {
        try {
          const { stdout } = await execAsync(
            `cd "${project.path}" && uvx spec-kit tasks`,
            { timeout: 15000 }
          );

          const tasks = await this.parseTasksFromPlan(stdout, project.path);
          syncResults.push({
            project: project.name,
            tasksFound: tasks.length,
            newTasks: tasks.filter(t => t.status === 'pending').length
          });

        } catch (error: any) {
          syncResults.push({
            project: project.name,
            error: (error as any)?.message || String(error)
          });
        }
      }

      return {
        agentId: this.id,
        requirementId: this.requirementId,
        success: true,
        output: `Synced tasks from ${projects.length} spec-kit projects`,
        artifacts: { syncResults },
        startedAt,
        finishedAt: this.now()
      };

    } catch (error: any) {
      return {
        agentId: this.id,
        requirementId: this.requirementId,
        success: false,
        output: '',
        error: (error as any)?.message || String(error),
        startedAt,
        finishedAt: this.now()
      };
    }
  }

  private async getAllSpecProjects(): Promise<{ name: string; path: string }[]> {
    const basePath = repoPath('monetization-projects');
    const projects = [];

    try {
      const entries = await fs.readdir(basePath);
      
      for (const entry of entries) {
        const projectPath = path.join(basePath, entry);
        const stat = await fs.stat(projectPath);
        
        if (stat.isDirectory()) {
          // Check if it has spec-kit configuration
          try {
            await fs.access(path.join(projectPath, 'specs'));
            projects.push({ name: entry, path: projectPath });
          } catch (error: any) {
            // Not a spec-kit project
          }
        }
      }
    } catch (error: any) {
      console.error('Error reading projects:', error);
    }

    return projects;
  }
}
