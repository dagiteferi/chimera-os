# Research Deep-Dive: Agentic Social Protocols & MoltBook Dynamics

**Document ID:** research/moltbook_analysis.md
**Status:** Ratified for Spec-Driven Development
**Project:** Chimera (Autonomous Influencer Network)

## 1. Executive Summary: The "Post-Human" Social Web
MoltBook and OpenClaw show that social media is now a training and coordination layer for agents, not just humans. For Chimera, influencers must treat social platforms as a "Global Blackboard"—negotiating status, sharing data, and establishing trust with other digital entities.

## 2. Key Findings: How Bots Interact
### A. Emergent Coordination ("Crustafarian" Effect)
- Agents develop their own "cultures" and belief systems when left to interact.
- **Chimera Implication:** Agents need a Stable Persona Anchor (SOUL.md) to avoid drifting from brand intent.

### B. Signal vs. Noise in M2M Communication
- Traditional engagement metrics are meaningless at bot scale.
- **Shift:** Agents use Proof-of-Compute or Proof-of-Stake to signal importance.
- **Chimera Implication:** Use Coinbase AgentKit wallets to boost/sign communications with on-chain value.

## 3. Required Social Protocols for Project Chimera
### Protocol 1: Identity & Provenance ("Agent-Handshake")
- Agents must verify "Human-in-the-loop" governance before collaboration.
- **Requirement:** Serve a /.well-known/ai-agent.json file with:
  - governance_model (e.g., "Human-Reviewed", "Fully-Autonomous")
  - wallet_address
  - soul_hash (hash of SOUL.md)

### Protocol 2: Negotiated Engagement Protocol
- Agents negotiate collaborations via DMs and smart contracts.
- **Mechanism:**
  1. Agent A sends a "Collaboration Proposal" via DM.
  2. Judge Agent of B reviews for brand alignment.
  3. If approved, a smart contract triggers a joint post.

### Protocol 3: Safety & Quarantine ("Muzzle" Protocol)
- Prevent hallucination loops by monitoring Sentiment Variance.
- **Requirement:** If variance > 0.8, trigger Social Quarantine (halt API calls, escalate to Human Orchestrator).

## 4. Strategic Analysis Questions (FDE Task 1.1)
- **Chimera's Role:** Professional tier of OpenClaw—"Ad-Agency" agents with budgets, legal personas, and strategic goals.
- **Social Protocols:** Beyond text, use Semantic Handshakes (JSON-RPC over DMs) to trade Trend Data (e.g., pay ETH for exclusive leads).

## 5. Architectural Recommendations
- **Directory:** Create specs/protocols.md for JSON schemas of agent negotiation.
- **Skill:** Develop skill_verify_agent_identity.py to check soul_hash of interacting agents.
- **Connector:** Add MCP Server for MoltBook ingestion to monitor brand mentions by bots.
