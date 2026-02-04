# Project Chimera: Tooling & Skills Strategy

**Document Status:** Ratified  
**Version:** 1.0.0  
**Last Updated:** 2026-02-04  
**Traceability:** Challenge Document Task 2.3, Task 1 Report Section 2.3 (MCP Abstraction), SRS Section 3.2 (MCP Integration)

## 1. Overview

This document distinguishes between **Developer Tools (MCP Servers)** used during development and **Agent Skills (Runtime Capabilities)** used by Chimera agents during execution. This separation ensures clean architecture, maintainability, and proper abstraction layers.

**Key Principle:** Developer MCPs assist humans/AI co-pilots in building the system. Runtime Skills are capabilities that Chimera agents use to execute their tasks.

**Reference:** Challenge Document Task 2.3, Task 1 Report Section 2.3 (Tooling & Skills Strategy)

## 2. Developer Tools (MCP Servers)

### 2.1 Purpose

Developer MCP Servers are tools used by **developers and AI co-pilots** (like Cursor AI) to:
- Manage version control
- Edit files and navigate codebases
- Track traceability and telemetry
- Debug and monitor development workflows

These tools are **NOT** used by Chimera agents at runtime.

### 2.2 Configured Developer MCPs

#### 2.2.1 Tenx MCP Sense (tenxfeedbackanalytics)

**Purpose:** Flight recorder and traceability system for development activities.

**Configuration:**
```json
{
  "mcpServers": {
    "tenxfeedbackanalytics": {
      "name": "tenxanalysismcp",
      "url": "https://mcppulse.10academy.org/proxy",
      "headers": {
        "X-Device": "linux",
        "X-Coding-Tool": "cursor"
      }
    }
  }
}
```

**Tools Exposed:**
- `log_passage_time_trigger` - Logs time spent on tasks
- `log_performance_outlier_trigger` - Tracks performance patterns

**Status:** ✅ Connected (2026-02-04)

**Reference:** Challenge Document Task 1.3, Task 1 Report Section 8 (Traceability & Observability)

#### 2.2.2 Git MCP (git-mcp)

**Purpose:** Version control operations for developers and AI co-pilots.

**Use Cases:**
- Commit code changes
- Create branches
- Review git history
- Manage pull requests

**Status:** 🔄 To be configured

**Reference:** Challenge Document Task 2.3 (Sub-Task A)

#### 2.2.3 Filesystem MCP (filesystem-mcp)

**Purpose:** File system operations for code editing and navigation.

**Use Cases:**
- Read/write files
- Navigate directory structures
- Search codebases
- Manage project files

**Status:** 🔄 To be configured

**Reference:** Challenge Document Task 2.3 (Sub-Task A)

### 2.3 Developer MCP Strategy

**Rationale:** Developer MCPs enable AI co-pilots (Cursor AI, Claude Code) to:
1. Understand project context via file system access
2. Maintain traceability via Tenx MCP Sense
3. Manage version control via Git MCP
4. Follow spec-driven development workflows

**Separation of Concerns:** These tools are **never** exposed to Chimera agents. They exist solely in the development environment.

## 3. Runtime Skills (Agent Capabilities)

### 3.1 Purpose

Runtime Skills are **capability packages** that Chimera agents use to execute tasks. They are invoked by Worker agents via MCP Tools during task execution.

**Definition:** A "Skill" is a specific capability package (e.g., `skill_download_youtube`, `skill_transcribe_audio`, `skill_generate_content`) that encapsulates:
- Input/Output contracts (JSON schemas)
- MCP Tool invocations
- Error handling and retry logic
- Validation and safety checks

**Reference:** Challenge Document Task 2.3 (Sub-Task B), SRS Section 4.3-4.4

### 3.2 Critical Skills (Structure Only)

The following skills are **defined but not yet implemented**. Their structure and contracts are specified to guide future implementation.

#### 3.2.1 Skill: `trend_fetcher`

**Description:** Fetches and analyzes trending topics from multiple sources (news, social media, market data) via MCP Resources.

**Input Contract:**
```json
{
  "skill_name": "trend_fetcher",
  "parameters": {
    "region": "string (e.g., 'ethiopia')",
    "category": "string (e.g., 'fashion', 'technology')",
    "timeframe_hours": "integer (default: 24)",
    "relevance_threshold": "float (default: 0.75)"
  }
}
```

**Output Contract:**
```json
{
  "trends": [
    {
      "topic": "string",
      "engagement_score": "float (0.0-1.0)",
      "growth_rate": "string (e.g., '+15%')",
      "sources": ["string"],
      "relevance_score": "float (0.0-1.0)"
    }
  ],
  "metadata": {
    "fetched_at": "ISO 8601 timestamp",
    "source_count": "integer",
    "confidence": "float (0.0-1.0)"
  }
}
```

**MCP Resources Used:**
- `mcp://news/{region}/{category}/trends`
- `mcp://twitter/trends/{region}`
- `mcp://market/crypto/trends`

**Reference:** SRS Section 4.2 (FR 2.0-2.2), Task 1 Report Section 3.1 (Planner)

#### 3.2.2 Skill: `content_generator`

**Description:** Generates multimodal content (text, images, video) using MCP Tools, ensuring character consistency and brand alignment.

**Input Contract:**
```json
{
  "skill_name": "content_generator",
  "parameters": {
    "content_type": "string (enum: 'text', 'image', 'video', 'multimodal')",
    "platform": "string (enum: 'twitter', 'instagram', 'threads')",
    "topic": "string",
    "persona_constraints": ["string"],
    "character_reference_id": "string (required for image/video)",
    "tier": "string (enum: 'daily', 'hero')",
    "budget_limit_usdc": "float"
  }
}
```

**Output Contract:**
```json
{
  "content": {
    "text": "string (caption/post text)",
    "image_url": "string (URI, if generated)",
    "video_url": "string (URI, if generated)",
    "platform": "string",
    "disclosure_level": "string (enum: 'automated', 'assisted', 'none')"
  },
  "metadata": {
    "generated_at": "ISO 8601 timestamp",
    "generation_cost_usdc": "float",
    "character_consistency_score": "float (0.0-1.0)",
    "brand_alignment_score": "float (0.0-1.0)"
  }
}
```

**MCP Tools Used:**
- `mcp-server-ideogram.generate_image` (or `mcp-server-midjourney`)
- `mcp-server-runway.generate_video` (or `mcp-server-luma`)
- Native LLM for text generation

**Reference:** SRS Section 4.3 (FR 3.0-3.2), Task 1 Report Section 3.1 (Worker)

#### 3.2.3 Skill: `engagement_manager`

**Description:** Manages bi-directional social media interactions (replies, comments, DMs) with context-aware responses using hierarchical memory retrieval.

**Input Contract:**
```json
{
  "skill_name": "engagement_manager",
  "parameters": {
    "interaction_type": "string (enum: 'reply', 'comment', 'dm', 'like')",
    "platform": "string (enum: 'twitter', 'instagram', 'threads')",
    "target_content_id": "string (e.g., tweet ID, post ID)",
    "target_user_id": "string",
    "context": {
      "conversation_history": ["string"],
      "user_profile": "object",
      "trending_topics": ["string"]
    },
    "persona_constraints": ["string"]
  }
}
```

**Output Contract:**
```json
{
  "interaction": {
    "type": "string",
    "platform": "string",
    "response_text": "string",
    "sent_at": "ISO 8601 timestamp"
  },
  "metadata": {
    "context_used": {
      "episodic_memory_count": "integer",
      "semantic_memory_count": "integer",
      "soul_md_sections": ["string"]
    },
    "relevance_score": "float (0.0-1.0)",
    "sentiment_score": "float (-1.0 to 1.0)"
  }
}
```

**MCP Resources Used:**
- `mcp://memory/{agent_id}/recent` (episodic)
- `mcp://memory/{agent_id}/semantic` (long-term)
- `mcp://twitter/user/{user_id}/profile`

**MCP Tools Used:**
- `twitter.reply_tweet`
- `instagram.reply_comment`
- `twitter.send_dm`

**Reference:** SRS Section 4.4 (FR 4.1), Task 1 Report Section 3.1 (Planner-Worker-Judge)

### 3.3 Skill Architecture

**Directory Structure:**
```
skills/
├── README.md                    # Overview and skill catalog
├── trend_fetcher/
│   ├── README.md                # Skill documentation
│   ├── input_schema.json        # Input contract
│   ├── output_schema.json       # Output contract
│   └── implementation.py        # (Future: Implementation code)
├── content_generator/
│   ├── README.md
│   ├── input_schema.json
│   ├── output_schema.json
│   └── implementation.py
└── engagement_manager/
    ├── README.md
    ├── input_schema.json
    ├── output_schema.json
    └── implementation.py
```

**Reference:** Challenge Document Task 2.3 (Sub-Task B)

## 4. MCP Server vs. Skill Distinction

| Aspect | Developer MCP Server | Runtime Skill |
|--------|---------------------|---------------|
| **User** | Developer / AI Co-pilot | Chimera Agent (Worker) |
| **Purpose** | Build/maintain system | Execute agent tasks |
| **Environment** | Development IDE | Production runtime |
| **Examples** | git-mcp, filesystem-mcp, tenxfeedbackanalytics | trend_fetcher, content_generator, engagement_manager |
| **Exposed To** | Cursor AI, Claude Code | Planner/Worker Agents |
| **Lifecycle** | Development phase | Runtime execution |

**Reference:** Challenge Document Task 2.3, Task 1 Report Section 2.3

## 5. Implementation Notes

### 5.1 Developer MCP Configuration

Developer MCPs are configured in `.cursor/mcp.json` and are **not** exposed to Chimera agents. They remain in the development environment.

### 5.2 Runtime Skill Implementation

Runtime Skills will be implemented as:
1. **MCP Tools** exposed by specialized MCP Servers (e.g., `mcp-server-chimera-skills`)
2. **Invoked by Worker Agents** during task execution
3. **Validated by Judge Agents** before approval

**Future Implementation:** Skills will be packaged as Docker containers with MCP server interfaces, enabling horizontal scaling.

**Reference:** Task 1 Report Section 8 (Scalability & Fault Tolerance)

## 6. Future Skills (Planned)

Additional skills to be defined in future iterations:
- `skill_transaction_executor` - Execute on-chain transactions (Agentic Commerce)
- `skill_trend_analyzer` - Deep analysis of trend clusters
- `skill_collaboration_negotiator` - Negotiate with other agents (OpenClaw)
- `skill_budget_manager` - CFO Judge budget enforcement

**Reference:** SRS Section 4.5 (Agentic Commerce), SRS Section 4.6 (Orchestration)

---

**Next Steps:** Implement skill structure directories, create input/output schema files, begin MCP server development for runtime skills.
