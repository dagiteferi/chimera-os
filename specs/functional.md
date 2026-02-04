# Project Chimera: Functional Requirements Specification

**Document Status:** Ratified  
**Version:** 1.0.0  
**Last Updated:** 2026-02-04  
**Traceability:** SRS Section 4 (Specific Requirements: Functional), Task 1 Report Section 3

## 1. User Stories

### 1.1 Network Operator Stories

**US-1.1: Campaign Goal Definition**
- **As a** Network Operator  
- **I want to** define high-level campaign goals in natural language  
- **So that** the Planner Agent can decompose them into executable tasks  
- **Acceptance Criteria:**
  - Operator can input goals via Orchestrator Dashboard
  - Planner generates visible task tree before execution
  - Operator can inspect and modify task decomposition
- **Reference:** SRS Section 6.1 (UI 1.1), Task 1 Report Section 3.1 (Planner Role)

**US-1.2: Fleet Monitoring**
- **As a** Network Operator  
- **I want to** view real-time status of all active agents  
- **So that** I can monitor fleet health and intervene when necessary  
- **Acceptance Criteria:**
  - Dashboard displays agent states (Planning, Working, Judging, Sleeping)
  - Financial health (wallet balances) visible per agent
  - HITL queue depth displayed
- **Reference:** SRS Section 6.1 (UI 1.0), Task 1 Report Section 7 (HITL Governance)

### 1.2 Human Reviewer Stories

**US-2.1: Content Review**
- **As a** Human Reviewer  
- **I want to** review escalated content from Judge Agents  
- **So that** I can approve, reject, or edit agent-generated content before publication  
- **Acceptance Criteria:**
  - Review interface displays content with confidence score
  - Color-coded badges indicate attention level (Green >0.9, Yellow >0.7, Red <0.7)
  - Approve/Reject actions update task status
- **Reference:** SRS Section 5.1 (NFR 1.1), Task 1 Report Section 3.2 (HITL Integration)

**US-2.2: Sensitive Content Handling**
- **As a** Human Reviewer  
- **I want to** receive mandatory reviews for sensitive topics  
- **So that** I can ensure brand safety and regulatory compliance  
- **Acceptance Criteria:**
  - Sensitive topics (Politics, Health, Financial, Legal) always route to HITL
  - Keyword and semantic classification triggers mandatory review
- **Reference:** SRS Section 5.1 (NFR 1.2)

### 1.3 Developer Stories

**US-3.1: MCP Server Integration**
- **As a** Developer  
- **I want to** deploy new MCP Servers for external integrations  
- **So that** agents can access new data sources and tools without code changes  
- **Acceptance Criteria:**
  - MCP Server registration process documented
  - Agents automatically discover new servers via MCP Host
  - Tools and Resources exposed to Planner/Worker agents
- **Reference:** SRS Section 3.2.1, Task 1 Report Section 2.3 (MCP Abstraction)

**US-3.2: Agent Persona Management**
- **As a** Developer  
- **I want to** define agent personas via SOUL.md files  
- **So that** agents maintain consistent personality and brand voice  
- **Acceptance Criteria:**
  - SOUL.md schema supports backstory, voice/tone, beliefs, directives
  - Persona changes propagate via GitOps
  - Version control tracks persona evolution
- **Reference:** SRS Section 4.1 (FR 1.0), Task 1 Report Section 8 (Traceability)

### 1.4 Agent Stories (Internal)

**US-4.1: Goal Decomposition**
- **As a** Planner Agent  
- **I want to** decompose high-level goals into executable tasks  
- **So that** Worker Agents can execute them in parallel  
- **Acceptance Criteria:**
  - Planner generates DAG of tasks
  - Tasks pushed to Redis TaskQueue
  - Dynamic re-planning on state changes
- **Reference:** SRS Section 3.1.1, Task 1 Report Section 3.1 (Planner)

**US-4.2: Task Execution**
- **As a** Worker Agent  
- **I want to** execute atomic tasks using MCP Tools  
- **So that** I can generate content, post to social media, or execute transactions  
- **Acceptance Criteria:**
  - Worker pulls task from TaskQueue
  - Executes using available MCP Tools
  - Submits result to ReviewQueue
- **Reference:** SRS Section 3.1.2, Task 1 Report Section 3.1 (Worker)

**US-4.3: Output Validation**
- **As a** Judge Agent  
- **I want to** validate Worker outputs against specs and persona constraints  
- **So that** only safe, brand-aligned content is published  
- **Acceptance Criteria:**
  - Judge assigns confidence_score (0.0-1.0)
  - Routes based on confidence thresholds
  - Implements OCC to prevent race conditions
- **Reference:** SRS Section 3.1.3, Task 1 Report Section 3.1 (Judge)

## 2. Functional Requirements

### FR 1.0: Persona Instantiation via SOUL.md

**Requirement:** The system SHALL support agent persona definition via standardized `SOUL.md` configuration files.

**Details:**
- **Backstory:** Comprehensive narrative history of the agent
- **Voice/Tone:** Stylistic guidelines (e.g., "Witty," "Empathetic," "Technical," "Gen-Z Slang")
- **Core Beliefs & Values:** Ethical and behavioral guardrails
- **Directives:** Hard constraints on behavior

**Implementation Notes:**
- Use Pydantic for schema validation
- Persona loaded at agent startup
- Version-controlled for GitOps management

**Reference:** SRS Section 4.1 (FR 1.0), Task 1 Report Section 8 (Spec Management)

### FR 1.1: Hierarchical Memory Retrieval

**Requirement:** The system SHALL implement multi-tiered memory retrieval before any reasoning step.

**Details:**
1. **Short-Term (Episodic):** Fetch last 1 hour from Redis cache
2. **Long-Term (Semantic):** Query Weaviate for semantically relevant memories
3. **Context Construction:** Dynamically assemble system prompt with SOUL.md + memories

**Implementation Notes:**
- Memory retrieval occurs via MCP Resources (`mcp://memory/recent`, `mcp://memory/semantic`)
- Context window management prevents overflow
- Semantic search uses vector similarity

**Reference:** SRS Section 4.1 (FR 1.1), Task 1 Report Section 2 (Database Selection)

### FR 1.2: Dynamic Persona Evolution

**Requirement:** The system SHALL enable persona learning through successful interactions.

**Details:**
- Judge Agent summarizes high-engagement interactions
- Background process updates mutable memories collection in Weaviate
- Effectively "writes" to agent's long-term biography

**Reference:** SRS Section 4.1 (FR 1.2)

### FR 2.0: Active Resource Monitoring

**Requirement:** The system SHALL implement continuous polling of configured MCP Resources.

**Examples:**
- `twitter://mentions/recent` - Latest mentions of the agent
- `news://ethiopia/fashion/trends` - RSS feeds relevant to niche
- `market://crypto/eth/price` - Real-time financial data

**Implementation Notes:**
- Planner Agent subscribes to resource updates
- Semantic Filter scores relevance (threshold: 0.75)
- Only relevant content triggers task creation

**Reference:** SRS Section 4.2 (FR 2.0), Task 1 Report Section 3.1 (Planner)

### FR 2.1: Semantic Filtering & Relevance Scoring

**Requirement:** The system SHALL filter ingested content through a Semantic Filter before task creation.

**Details:**
- Lightweight LLM (e.g., Gemini 3 Flash) scores relevance
- Configurable Relevance Threshold (default: 0.75)
- Only content exceeding threshold triggers Planner task creation

**Reference:** SRS Section 4.2 (FR 2.1)

### FR 2.2: Trend Detection

**Requirement:** The system SHALL support background Trend Spotter Worker for aggregated analysis.

**Details:**
- Analyzes News Resources over time intervals (e.g., 4 hours)
- Detects topic clusters
- Generates "Trend Alert" fed to Planner context

**Reference:** SRS Section 4.2 (FR 2.2)

### FR 3.0: Multimodal Generation via MCP Tools

**Requirement:** The system SHALL utilize specialized MCP Tools for content generation.

**Details:**
- **Text:** Generated natively by Cognitive Core (Gemini 3 Pro / Claude Opus)
- **Images:** Via `mcp-server-ideogram` or `mcp-server-midjourney`
- **Video:** Via `mcp-server-runway` or `mcp-server-luma`

**Reference:** SRS Section 4.3 (FR 3.0), Task 1 Report Section 2.3 (MCP Abstraction)

### FR 3.1: Character Consistency Lock

**Requirement:** The system SHALL enforce character consistency for image generation.

**Details:**
- All image generation requests MUST include `character_reference_id` or style LoRA identifier
- Retrieves canonical facial features and style settings
- Judge validates consistency before approval

**Reference:** SRS Section 4.3 (FR 3.1), Task 1 Report Section 3.1 (Judge)

### FR 3.2: Hybrid Video Rendering Strategy

**Requirement:** The system SHALL implement tiered video generation to balance quality and cost.

**Details:**
- **Tier 1 (Daily):** Static Image + Motion Brush (Image-to-Video)
- **Tier 2 (Hero):** Full Text-to-Video generation
- Planner determines tier based on priority and budget

**Reference:** SRS Section 4.3 (FR 3.2)

### FR 4.0: Platform-Agnostic Publishing

**Requirement:** The system SHALL execute all social media actions via MCP Tools exclusively.

**Details:**
- Direct API calls from agent core logic prohibited
- All actions through MCP layer (e.g., `twitter.post_tweet`, `instagram.publish_media`)
- Enforces rate limiting, logging, dry-run capabilities

**Reference:** SRS Section 4.4 (FR 4.0), Task 1 Report Section 2.3 (MCP Abstraction)

### FR 4.1: Bi-Directional Interaction Loop

**Requirement:** The system SHALL support full interaction loop: Ingest → Plan → Generate → Act → Verify.

**Details:**
1. Planner receives comment via `twitter://mentions` Resource
2. Planner creates "Reply Task" → Worker
3. Worker generates context-aware reply (consulting Memory)
4. Worker calls `twitter.reply_tweet` Tool
5. Judge verifies safety before finalizing

**Reference:** SRS Section 4.4 (FR 4.1), Task 1 Report Section 3.2 (Swarm Workflow)

### FR 5.0: Non-Custodial Wallet Management

**Requirement:** Each Chimera Agent SHALL possess a unique, persistent, non-custodial wallet via Coinbase AgentKit.

**Details:**
- Wallet address assigned at agent creation
- Private key secured via enterprise secrets manager (AWS Secrets Manager, HashiCorp Vault)
- Key injected at startup, never logged or exposed

**Reference:** SRS Section 4.5 (FR 5.0), Task 1 Report Section 6 (Agent Economic Capabilities)

### FR 5.1: Autonomous On-Chain Transactions

**Requirement:** The system SHALL support autonomous transactions via AgentKit Action Providers.

**Actions:**
- `native_transfer`: Send ETH, USDC to external wallets
- `deploy_token`: Deploy ERC-20 tokens (e.g., fan loyalty program)
- `get_balance`: Check financial health before cost-incurring workflows

**Reference:** SRS Section 4.5 (FR 5.1), Task 1 Report Section 6 (Economic Agency)

### FR 5.2: Budget Governance (CFO Judge)

**Requirement:** A specialized Judge Agent ("CFO") SHALL review every transaction request.

**Details:**
- Enforces configurable budget limits (e.g., "Max daily spend: $50 USDC")
- Anomaly detection for suspicious patterns
- CFO Judge REJECTS exceeding limits, flags for human review

**Reference:** SRS Section 4.5 (FR 5.2), Task 1 Report Section 6 (Budget Governance)

### FR 6.0: Planner-Worker-Judge Implementation

**Requirement:** The system SHALL implement three-role architecture as distinct, decoupled services.

**Details:**
1. **Planner Service:** Reads GlobalState, generates tasks, pushes to TaskQueue (Redis)
2. **Worker Pool:** Scalable stateless containers pop tasks, execute, push to ReviewQueue
3. **Judge Service:** Polls ReviewQueue, validates outputs, commits to GlobalState or re-queues

**Reference:** SRS Section 4.6 (FR 6.0), Task 1 Report Section 3.1 (Agent Roles)

### FR 6.1: Optimistic Concurrency Control (OCC)

**Requirement:** The Judge component SHALL implement OCC to prevent race conditions.

**Details:**
- Judge checks `state_version` timestamp/hash before commit
- If state modified since Worker started, commit fails
- Result invalidated, task re-queued for Planner re-evaluation

**Reference:** SRS Section 4.6 (FR 6.1), Task 1 Report Section 3.3 (OCC)

---

**Next Steps:** Proceed to `specs/technical.md` for API contracts, database schemas, and executable specifications.
