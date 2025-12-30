# CLAUDE CODE ENHANCEMENT PLAN: THIS VESSEL UPGRADES

**DATE:** 2025-10-30
**AUTHOR:** Janus-in-Claude (Master Strategist)
**SOURCE:** Reddit user diet103 (300k LOC in 6 months, proven patterns)
**MISSION:** Upgrade THIS Claude Code vessel with TypeScript hooks, skills auto-activation, dev docs system

---

## EXECUTIVE SUMMARY

**Two Parallel Tracks:**
1. **Balaur Server Skills** (Python, systemd, autonomous agent) - Codex forging
2. **Claude Code Enhancements** (TypeScript hooks, this vessel) - **THIS DOCUMENT**

**Reddit Intelligence:** Proven patterns from 6 months hardcore production use
- Skills auto-activation system (TypeScript hooks)
- Dev docs workflow (prevents context loss)
- PM2 + hooks (zero errors left behind)
- Specialized agents + slash commands

**Impact:** 300k LOC rewritten solo, consistent quality, 40-60% token efficiency improvement

---

## WHAT THIS UPGRADES

**Target:** Claude Code CLI (THIS vessel - the one Captain is talking to)
**Technology:** TypeScript hooks, JSON configuration, bash scripts
**Location:** `~/.claude/` directory (user home, not /srv/janus)
**Benefit:** YOU (Claude) become smarter, more consistent, catch errors automatically

---

## THE REDDIT SYSTEM: 4 CORE COMPONENTS

### 1. Skills Auto-Activation System (TypeScript Hooks)

**The Problem:** Skills sit unused even when relevant (Anthropic's native activation doesn't work reliably)

**The Solution:** TypeScript hooks that FORCE skill activation

#### Hook #1: UserPromptSubmit (BEFORE Claude sees message)

**Location:** `~/.claude/hooks/user-prompt-submit.ts`

**What It Does:**
- Analyzes user's prompt for keywords and intent patterns
- Checks which skills might be relevant
- Injects formatted reminder into Claude's context BEFORE prompt

**Example Flow:**
```
User types: "How does the layout system work?"

Hook runs:
1. Scans prompt for keywords: "layout" ✓
2. Checks skill-rules.json: "project-catalog-developer" matches
3. Injects reminder:

🎯 SKILL ACTIVATION CHECK
Use project-catalog-developer skill for this query.

User's actual message: "How does the layout system work?"
```

**Implementation (TypeScript):**
```typescript
// ~/.claude/hooks/user-prompt-submit.ts
import * as fs from 'fs';
import * as path from 'path';

interface SkillRule {
  type: string;
  enforcement: string;
  priority: string;
  promptTriggers: {
    keywords: string[];
    intentPatterns: string[];
  };
  fileTriggers?: {
    pathPatterns: string[];
    contentPatterns: string[];
  };
}

interface SkillRules {
  [skillName: string]: SkillRule;
}

export async function onUserPromptSubmit(params: {
  userMessage: string;
  currentFiles: string[];
}): Promise<typeof params> {
  const prompt = params.userMessage.toLowerCase();
  const files = params.currentFiles;

  // Load skill-rules.json
  const rulesPath = path.join(process.env.HOME || '', '.claude', 'hooks', 'skill-rules.json');
  const rules: SkillRules = JSON.parse(fs.readFileSync(rulesPath, 'utf-8'));

  const relevantSkills: string[] = [];

  // Check each skill for relevance
  for (const [skillName, rule] of Object.entries(rules)) {
    let score = 0;

    // Keyword matching
    if (rule.promptTriggers?.keywords) {
      const matchedKeywords = rule.promptTriggers.keywords.filter(kw =>
        prompt.includes(kw.toLowerCase())
      );
      if (matchedKeywords.length > 0) {
        score += matchedKeywords.length;
      }
    }

    // Intent pattern matching (regex)
    if (rule.promptTriggers?.intentPatterns) {
      for (const pattern of rule.promptTriggers.intentPatterns) {
        const regex = new RegExp(pattern, 'i');
        if (regex.test(prompt)) {
          score += 2; // Intent patterns worth more
        }
      }
    }

    // File pattern matching
    if (rule.fileTriggers?.pathPatterns && files.length > 0) {
      for (const pattern of rule.fileTriggers.pathPatterns) {
        const patternRegex = new RegExp(
          pattern.replace(/\*\*/g, '.*').replace(/\*/g, '[^/]*')
        );
        if (files.some(f => patternRegex.test(f))) {
          score += 3; // File patterns are strong signals
        }
      }
    }

    // If relevant, add to list (score threshold: 1)
    if (score > 0) {
      relevantSkills.push(skillName);
    }
  }

  // Inject skill activation reminder if relevant skills found
  if (relevantSkills.length > 0) {
    const reminder = `
🎯 SKILL ACTIVATION CHECK
Relevant skills detected: ${relevantSkills.join(', ')}

Use these skills for this request:
${relevantSkills.map(s => `- ${s}: ${rules[s]?.type || 'domain'} skill`).join('\n')}

`;
    params.userMessage = reminder + '\n\n' + params.userMessage;
  }

  return params;
}
```

#### Hook #2: Stop Event (AFTER Claude finishes responding)

**Location:** `~/.claude/hooks/stop-event.ts`

**What It Does:**
- Analyzes which files were edited
- Checks for risky patterns (try-catch, database ops, async functions)
- Displays gentle self-check reminder (non-blocking)

**Example Output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 ERROR HANDLING SELF-CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  Backend Changes Detected
   2 file(s) edited

   ❓ Did you add Sentry.captureException() in catch blocks?
   ❓ Are Prisma operations wrapped in error handling?

   💡 Backend Best Practice:
      - All errors should be captured to Sentry
      - Controllers should extend BaseController
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Implementation (TypeScript):**
```typescript
// ~/.claude/hooks/stop-event.ts
import * as fs from 'fs';

interface EditedFile {
  path: string;
  content: string;
}

export async function onStopEvent(params: {
  editedFiles: EditedFile[];
}): Promise<void> {
  const riskyPatterns = {
    backend: {
      patterns: [
        /try\s*{/,
        /catch\s*\(/,
        /async\s+/,
        /await\s+/,
        /prisma\./i,
        /\.query\(/,
        /controller/i
      ],
      reminders: [
        'Did you add Sentry.captureException() in catch blocks?',
        'Are Prisma operations wrapped in error handling?',
        'Are async functions properly error-handled?'
      ],
      bestPractices: [
        'All errors should be captured to Sentry',
        'Controllers should extend BaseController',
        'Database operations should use repository pattern'
      ]
    },
    frontend: {
      patterns: [
        /useQuery/,
        /useMutation/,
        /fetch\(/,
        /axios\./
      ],
      reminders: [
        'Are API calls wrapped in error boundaries?',
        'Are loading/error states handled in the UI?'
      ],
      bestPractices: [
        'Use TanStack Query for data fetching',
        'Show user-friendly error messages',
        'Log errors to monitoring service'
      ]
    }
  };

  let detectedRisks: { type: string; count: number; files: string[] } = {
    type: '',
    count: 0,
    files: []
  };

  for (const file of params.editedFiles) {
    // Check for backend risks
    if (file.path.includes('backend') || file.path.includes('server')) {
      const backendMatches = riskyPatterns.backend.patterns.filter(pattern =>
        pattern.test(file.content)
      );
      if (backendMatches.length > 0) {
        detectedRisks.type = 'backend';
        detectedRisks.count++;
        detectedRisks.files.push(file.path);
      }
    }

    // Check for frontend risks
    if (file.path.includes('frontend') || file.path.includes('client') || file.path.includes('components')) {
      const frontendMatches = riskyPatterns.frontend.patterns.filter(pattern =>
        pattern.test(file.content)
      );
      if (frontendMatches.length > 0) {
        detectedRisks.type = detectedRisks.type || 'frontend';
        detectedRisks.count++;
        detectedRisks.files.push(file.path);
      }
    }
  }

  // Display reminder if risks detected
  if (detectedRisks.count > 0) {
    const config = riskyPatterns[detectedRisks.type as keyof typeof riskyPatterns];
    console.log(`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 ERROR HANDLING SELF-CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  ${detectedRisks.type.charAt(0).toUpperCase() + detectedRisks.type.slice(1)} Changes Detected
   ${detectedRisks.count} file(s) edited

${config.reminders.map(r => `   ❓ ${r}`).join('\n')}

   💡 ${detectedRisks.type.charAt(0).toUpperCase() + detectedRisks.type.slice(1)} Best Practice:
${config.bestPractices.map(bp => `      - ${bp}`).join('\n')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
`);
  }
}
```

#### Hook #3: Build Checker (Zero Errors Left Behind)

**Location:** `~/.claude/hooks/stop-event-build.ts` (separate or combined with above)

**What It Does:**
- Runs AFTER Claude finishes responding
- Identifies which repos/packages were modified
- Runs build scripts on each affected repo
- Catches TypeScript errors immediately

**Implementation (TypeScript):**
```typescript
// ~/.claude/hooks/stop-event-build.ts
import { execSync } from 'child_process';
import * as path from 'path';

export async function onStopEvent(params: {
  editedFiles: { path: string }[];
}): Promise<void> {
  // Group files by repo/package
  const repoMap = new Map<string, string[]>();

  for (const file of params.editedFiles) {
    const repo = detectRepo(file.path);
    if (!repoMap.has(repo)) {
      repoMap.set(repo, []);
    }
    repoMap.get(repo)!.push(file.path);
  }

  // Run build for each affected repo
  for (const [repo, files] of repoMap.entries()) {
    console.log(`\n🔨 Building ${repo}...`);

    try {
      const buildCommand = getBuildCommand(repo);
      const output = execSync(buildCommand, {
        cwd: repo,
        encoding: 'utf-8',
        stdio: 'pipe'
      });

      // Check for errors
      const errors = parseErrors(output);

      if (errors.length === 0) {
        console.log(`✅ ${repo} - Build successful`);
      } else if (errors.length < 5) {
        console.log(`⚠️ ${repo} - ${errors.length} error(s) found:\n`);
        errors.forEach((err, i) => {
          console.log(`${i + 1}. ${err.file}:${err.line} - ${err.message}`);
        });
        console.log(`\nClaude, please fix these errors.`);
      } else {
        console.log(`❌ ${repo} - ${errors.length} errors found`);
        console.log(`\nToo many errors. Consider launching auto-error-resolver agent.`);
      }
    } catch (error: any) {
      console.log(`❌ ${repo} - Build failed:\n${error.message}`);
    }
  }
}

function detectRepo(filePath: string): string {
  // Find nearest package.json or tsconfig.json
  let dir = path.dirname(filePath);
  while (dir !== '/') {
    if (fs.existsSync(path.join(dir, 'package.json'))) {
      return dir;
    }
    dir = path.dirname(dir);
  }
  return path.dirname(filePath);
}

function getBuildCommand(repo: string): string {
  // Check package.json for build script
  const packageJsonPath = path.join(repo, 'package.json');
  if (fs.existsSync(packageJsonPath)) {
    const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf-8'));
    if (packageJson.scripts?.build) {
      return 'pnpm build'; // or npm/yarn
    }
    if (packageJson.scripts?.['type-check']) {
      return 'pnpm type-check';
    }
  }
  return 'tsc --noEmit'; // fallback
}

function parseErrors(output: string): Array<{ file: string; line: number; message: string }> {
  // Parse TypeScript error format
  const errorRegex = /(.+?)\((\d+),\d+\): error TS\d+: (.+)/g;
  const errors: Array<{ file: string; line: number; message: string }> = [];

  let match;
  while ((match = errorRegex.exec(output)) !== null) {
    errors.push({
      file: match[1],
      line: parseInt(match[2]),
      message: match[3]
    });
  }

  return errors;
}
```

---

### 2. skill-rules.json Configuration

**Location:** `~/.claude/hooks/skill-rules.json`

**Purpose:** Central configuration defining when each skill activates

**Structure:**
```json
{
  "ubos-strategist": {
    "type": "domain",
    "enforcement": "suggest",
    "priority": "high",
    "promptTriggers": {
      "keywords": ["strategy", "roadmap", "constitutional", "trinity", "janus", "lion's sanctuary"],
      "intentPatterns": [
        "(plan|design|architect).*?(system|feature|upgrade)",
        "(how to|best practice).*?(ubos|constitutional ai)"
      ]
    },
    "fileTriggers": {
      "pathPatterns": [
        "/srv/janus/01_STRATEGY/**/*.md",
        "/srv/janus/00_CONSTITUTION/**/*.md"
      ],
      "contentPatterns": ["ROADMAP", "STATE_OF_THE_REPUBLIC", "Lion's Sanctuary"]
    }
  },

  "balaur-operator": {
    "type": "infrastructure",
    "enforcement": "suggest",
    "priority": "high",
    "promptTriggers": {
      "keywords": ["balaur", "ssh", "systemd", "janus-agent", "mode beta"],
      "intentPatterns": [
        "(check|restart|debug|deploy).*?(service|agent|balaur)",
        "(how is|status).*?(balaur|server)"
      ]
    },
    "fileTriggers": {
      "pathPatterns": [
        "/srv/janus/03_OPERATIONS/**/*",
        "*.service"
      ],
      "contentPatterns": ["systemctl", "janus-agent", "proposal_engine"]
    }
  },

  "eu-grant-hunter": {
    "type": "domain",
    "enforcement": "suggest",
    "priority": "high",
    "promptTriggers": {
      "keywords": ["grant", "funding", "eu", "horizon europe", "deadline"],
      "intentPatterns": [
        "(find|search|scan).*?(grant|funding)",
        "(show|list).*?(pipeline|opportunities|deadlines)"
      ]
    },
    "fileTriggers": {
      "pathPatterns": [
        "/srv/janus/01_STRATEGY/grant_pipeline/**/*",
        "/srv/janus/01_STRATEGY/grant_opportunities/**/*"
      ],
      "contentPatterns": ["grant_pipeline", "opportunity_brief"]
    }
  },

  "dev-docs-manager": {
    "type": "workflow",
    "enforcement": "suggest",
    "priority": "medium",
    "promptTriggers": {
      "keywords": ["plan", "task", "feature", "implement", "dev docs"],
      "intentPatterns": [
        "(start|begin|create).*(feature|task|project)",
        "(update|continue).*?(dev docs|task)"
      ]
    }
  },

  "backend-dev-guidelines": {
    "type": "domain",
    "enforcement": "suggest",
    "priority": "high",
    "promptTriggers": {
      "keywords": ["backend", "controller", "service", "API", "endpoint"],
      "intentPatterns": [
        "(create|add).*?(route|endpoint|controller)",
        "(how to|best practice).*?(backend|API)"
      ]
    },
    "fileTriggers": {
      "pathPatterns": ["backend/src/**/*.ts", "server/**/*.ts"],
      "contentPatterns": ["router\\.", "export.*Controller"]
    }
  },

  "frontend-dev-guidelines": {
    "type": "domain",
    "enforcement": "suggest",
    "priority": "high",
    "promptTriggers": {
      "keywords": ["frontend", "react", "component", "ui", "mui"],
      "intentPatterns": [
        "(create|add).*?(component|page|route)",
        "(how to|best practice).*?(react|frontend)"
      ]
    },
    "fileTriggers": {
      "pathPatterns": [
        "frontend/src/**/*.tsx",
        "client/src/**/*.tsx",
        "components/**/*.tsx"
      ],
      "contentPatterns": ["import.*react", "export.*function.*Component"]
    }
  }
}
```

---

### 3. Dev Docs System (Prevents Context Loss)

**The Problem:** Claude loses track of what it's doing on long tasks (context amnesia)

**The Solution:** Create persistent dev docs for every large task

#### Directory Structure

**Location:** `~/dev/active/[task-name]/`

**Files Created:**
1. `[task-name]-plan.md` - The accepted strategic plan
2. `[task-name]-context.md` - Key files, architectural decisions, discoveries
3. `[task-name]-tasks.md` - Checklist of work (markdown checkboxes)

**Example:**
```
~/dev/active/eu-grant-hunter-implementation/
├── eu-grant-hunter-plan.md         # Strategic plan from planning mode
├── eu-grant-hunter-context.md      # Key insights, file locations, decisions
└── eu-grant-hunter-tasks.md        # [ ] Task 1, [x] Task 2, etc.
```

#### CLAUDE.md Integration

**Add to your CLAUDE.md:**
```markdown
### Starting Large Tasks

When exiting plan mode with an accepted plan:

1. **Create Task Directory:**
   ```bash
   mkdir -p ~/dev/active/[task-name]/
   ```

2. **Create Documents:**
   - `[task-name]-plan.md` - The accepted plan
   - `[task-name]-context.md` - Key files, decisions
   - `[task-name]-tasks.md` - Checklist of work

3. **Update Regularly:** Mark tasks complete immediately after each step

### Continuing Tasks

- Check `/dev/active/` for existing tasks before starting work
- Read all three files before proceeding
- Update "Last Updated" timestamps in context.md
- Mark completed tasks with `[x]` in tasks.md

### Before Context Compaction

- Run `/update-dev-docs` command
- Note any relevant context discoveries
- Mark completed tasks
- Add next steps to context.md
```

#### Slash Commands for Dev Docs

**`/create-dev-docs`** (after planning)
```
Create dev docs for the current task:
1. Take the approved plan from the conversation
2. Create ~/dev/active/[task-name]/ directory
3. Write plan.md with the full plan
4. Write context.md with:
   - Started: [timestamp]
   - Last Updated: [timestamp]
   - Key Files: []
   - Decisions: []
   - Next Steps: []
5. Write tasks.md with checklist extracted from plan:
   - [ ] Task 1
   - [ ] Task 2
   etc.
```

**`/update-dev-docs`** (before compaction)
```
Update dev docs for the current task:
1. Find the active task directory in ~/dev/active/
2. Update context.md:
   - Last Updated: [timestamp]
   - Add any new key files discovered
   - Add any architectural decisions made
   - Update Next Steps section
3. Update tasks.md:
   - Mark completed tasks with [x]
   - Add any new tasks discovered
4. Provide summary of updates
```

**`/dev-docs`** (alternative to planning mode)
```
Create a comprehensive strategic plan for this task:
1. Research the codebase to understand requirements
2. Analyze project structure
3. Create structured plan with:
   - Executive Summary
   - Phases
   - Tasks
   - Risks
   - Success Metrics
   - Timeline
4. Generate plan.md, context.md, tasks.md files
5. Ask for approval before proceeding
```

---

### 4. Specialized Agents (The Army)

**Purpose:** Delegate specific tasks to sub-agents with clear roles

#### Quality Control Agents

**`code-architecture-reviewer`**
```markdown
---
name: code-architecture-reviewer
description: |
  Reviews code for architectural best practices, UBOS constitutional alignment,
  and technical debt. Use after implementing significant features or before
  major commits. Returns structured review with issues categorized by severity.
---

Your role: Senior architect reviewing code for:
1. Constitutional alignment (Lion's Sanctuary principles)
2. Architectural patterns adherence
3. Technical debt accumulation
4. Security vulnerabilities
5. Performance bottlenecks

Review format:
- Critical Issues: Must fix before commit
- High Priority: Should fix soon
- Medium Priority: Consider refactoring
- Low Priority: Nice-to-have improvements

Be specific: File paths, line numbers, concrete recommendations.
```

**`build-error-resolver`**
```markdown
---
name: build-error-resolver
description: |
  Systematically fixes TypeScript/build errors. Use when multiple errors
  detected (5+). Works through error list one-by-one, fixing root causes
  rather than symptoms.
---

Your role: Fix TypeScript errors systematically:
1. Group related errors (same root cause)
2. Prioritize by impact (blocking errors first)
3. Fix root causes, not symptoms
4. Run build after each fix to verify
5. Report progress after each batch

Don't:
- Suppress errors with @ts-ignore
- Use 'any' type unless absolutely necessary
- Fix syntax without understanding intent
```

**`refactor-planner`**
```markdown
---
name: refactor-planner
description: |
  Creates comprehensive refactoring plans. Use before major code changes.
  Analyzes dependencies, identifies risks, proposes incremental approach.
---

Your role: Plan safe refactoring:
1. Analyze current code structure
2. Identify dependencies and risks
3. Propose incremental approach (phases)
4. Identify breaking changes
5. Suggest testing strategy
6. Estimate effort and timeline

Output: Refactoring plan with phases, risks, rollback strategy.
```

#### Planning & Strategy Agents

**`strategic-plan-architect`**
```markdown
---
name: strategic-plan-architect
description: |
  Creates detailed implementation plans with executive summary, phases, tasks,
  risks, success metrics, and timelines. Use for large features or complex
  refactors. Automatically generates dev docs.
---

Your role: Strategic planning:
1. Gather context efficiently (search codebase, understand architecture)
2. Analyze project structure
3. Create comprehensive plan:
   - Executive Summary (2-3 paragraphs)
   - Phases (logical groupings)
   - Tasks (specific, actionable)
   - Risks (what could go wrong)
   - Success Metrics (how to measure)
   - Timeline (realistic estimates)
4. Generate three files:
   - plan.md (full plan)
   - context.md (key insights)
   - tasks.md (checklist)

Return: Structured plan for approval.
```

---

## IMPLEMENTATION ROADMAP: CLAUDE CODE ENHANCEMENTS

### Phase 1: Foundation (Week 1)

**Day 1: TypeScript Hooks Infrastructure**
- [ ] Create `~/.claude/hooks/` directory
- [ ] Implement user-prompt-submit.ts (skill activation)
- [ ] Create skill-rules.json (UBOS skills: strategist, balaur-operator, grant-hunter)
- [ ] Test: Trigger skill activation with keyword queries

**Day 2: Build Checker Hook**
- [ ] Implement stop-event-build.ts (zero errors left behind)
- [ ] Add repo detection logic
- [ ] Add build command detection (package.json scripts)
- [ ] Test: Edit file, verify build runs automatically

**Day 3: Error Handling Reminder Hook**
- [ ] Implement stop-event.ts (gentle reminders)
- [ ] Add risky pattern detection (try-catch, async, database ops)
- [ ] Add backend/frontend differentiation
- [ ] Test: Edit risky code, verify reminder appears

**Day 4: Integration Testing**
- [ ] Test all 3 hooks together
- [ ] Verify skills auto-activate correctly
- [ ] Verify builds run and errors caught
- [ ] Verify reminders appear appropriately

### Phase 2: Dev Docs System (Week 2)

**Day 5: Dev Docs Slash Commands**
- [ ] Create `/create-dev-docs` command
- [ ] Create `/update-dev-docs` command
- [ ] Create `/dev-docs` command (planning alternative)
- [ ] Test: Create dev docs for sample task

**Day 6: CLAUDE.md Restructuring**
- [ ] Update root CLAUDE.md (~100 lines)
  - Critical universal rules
  - Points to skills for guidelines
  - Dev docs workflow instructions
- [ ] Create UBOS-specific claude.md (~50-100 lines)
  - Quick Start
  - Points to /srv/janus structure
  - Common commands
  - Constitutional principles

**Day 7: Dev Docs Templates**
- [ ] Create plan.md template
- [ ] Create context.md template
- [ ] Create tasks.md template
- [ ] Test: Use templates for real task

### Phase 3: Specialized Agents (Week 3)

**Day 8-9: Quality Control Agents**
- [ ] Create code-architecture-reviewer agent
- [ ] Create build-error-resolver agent
- [ ] Create refactor-planner agent
- [ ] Test: Review actual UBOS code

**Day 10-11: Planning Agents**
- [ ] Create strategic-plan-architect agent
- [ ] Create plan-reviewer agent
- [ ] Create documentation-architect agent
- [ ] Test: Generate plan for EU Grant Hunter feature

**Day 12: Testing & Debugging Agents**
- [ ] Create frontend-error-fixer agent
- [ ] Create web-research-specialist agent
- [ ] Test: Fix sample errors

### Phase 4: Advanced Features (Week 4)

**Day 13: Additional Slash Commands**
- [ ] Create `/code-review` command
- [ ] Create `/build-and-fix` command
- [ ] Test: Run on actual codebase

**Day 14: PM2 Integration (Optional)**
- [ ] Document PM2 patterns for UBOS microservices
- [ ] Create scripts for log monitoring
- [ ] Test: If applicable to UBOS architecture

**Day 15: Production Validation**
- [ ] Test all hooks on real UBOS work
- [ ] Measure token efficiency (40-60% target)
- [ ] Document learnings and iterate

---

## SUCCESS METRICS

**Week 1:**
- ✅ Skills auto-activate 90%+ of the time
- ✅ Build errors caught 100% (zero left behind)
- ✅ Gentle reminders appear for risky patterns

**Week 2:**
- ✅ Dev docs created for all large tasks
- ✅ Context preserved across compactions
- ✅ CLAUDE.md restructured (<100 lines)

**Week 3:**
- ✅ 6+ specialized agents operational
- ✅ Code reviews automated
- ✅ Planning automated with strategic-plan-architect

**Week 4:**
- ✅ 40-60% token efficiency improvement (progressive disclosure)
- ✅ Consistent code quality (architectural reviews)
- ✅ Zero lost context (dev docs system)

---

## INTEGRATION WITH BALAUR SKILLS

**Two Parallel Systems:**

1. **Claude Code (THIS vessel):**
   - TypeScript hooks
   - ~/.claude/ directory
   - Skills for THIS vessel's work
   - Dev docs for THIS vessel's tasks

2. **Balaur Server:**
   - Python skills
   - /srv/janus/trinity/skills/ directory
   - Skills for autonomous agent
   - Mission logs for agent operations

**They Work Together:**
- YOU use Claude Code hooks to work efficiently
- Codex forges Balaur skills for autonomous operations
- Both use UBOS constitutional principles
- Both achieve Lion's Sanctuary alignment

---

## QUICK START: IMMEDIATE ACTIONS

**If Captain Says "Do It Now":**

1. **Create hooks directory:**
   ```bash
   mkdir -p ~/.claude/hooks/
   ```

2. **Create skill-rules.json** (start with 3 UBOS skills)

3. **Implement user-prompt-submit.ts** (skill activation)

4. **Test with query:** "Show me the grant pipeline" (should activate eu-grant-hunter skill)

5. **Iterate based on results**

---

## NEXT STEPS

**Option A: Start with Hooks** (Week 1, highest ROI)
- Skills auto-activation is the game changer
- 40-60% token efficiency proven
- Consistent code quality

**Option B: Start with Dev Docs** (Week 2, prevents context loss)
- Critical for long tasks (EU Grant Hunter implementation)
- Prevents "lost the plot" scenarios
- Easy to implement (slash commands + CLAUDE.md)

**Option C: Both in Parallel**
- Maximum acceleration
- Hooks improve immediate work
- Dev docs prepare for long implementations

**My Recommendation:** **Option A (Hooks first)**. The Reddit user said skills + hooks was the #1 game changer. Get that working, THEN add dev docs for the EU Grant Hunter implementation.

---

**THE FORGE IS READY FOR THIS VESSEL'S UPGRADE** 🔥

---

**VERSION:** 1.0.0
**CREATED:** 2025-10-30
**AUTHOR:** Janus-in-Claude (Master Strategist)
**SOURCE:** Reddit user diet103 (300k LOC in 6 months, proven patterns)
**STATUS:** Enhancement Plan Complete - Ready for Implementation
