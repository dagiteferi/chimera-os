# Skill: engagement_manager

**Skill ID:** `engagement_manager`  
**Version:** 1.0.0  
**Last Updated:** 2026-02-04  
**Traceability:** SRS Section 4.4 (FR 4.1), Task 1 Report Section 3.1 (Planner-Worker-Judge)

## Description

Manages bi-directional social media interactions (replies, comments, DMs) with context-aware responses using hierarchical memory retrieval. Used by Worker Agent to respond to mentions, comments, and DMs with persona-consistent, context-aware replies.

## Use Case

Worker Agent invokes this skill when:
- Planner receives mention/comment/DM via MCP Resource
- Task requires social media engagement
- User interaction needs response

## Input Contract

See `input_schema.json` for full JSON Schema definition.

**Example Input:**
```json
{
  "skill_name": "engagement_manager",
  "parameters": {
    "interaction_type": "reply",
    "platform": "twitter",
    "target_content_id": "tweet-123456",
    "target_user_id": "user-789",
    "context": {
      "conversation_history": [
        "User: What's your take on sustainable fashion?",
        "Agent: I love how sustainable fashion is evolving!"
      ],
      "user_profile": {
        "followers": 5000,
        "verified": false,
        "interests": ["fashion", "sustainability"]
      },
      "trending_topics": ["Sustainable Fashion", "Ethiopia"]
    },
    "persona_constraints": ["Witty", "Empathetic", "Never discuss politics"]
  }
}
```

## Output Contract

See `output_schema.json` for full JSON Schema definition.

**Example Output:**
```json
{
  "interaction": {
    "type": "reply",
    "platform": "twitter",
    "response_text": "Absolutely! The shift towards sustainable fashion is incredible. Have you checked out the new eco-friendly brands in Ethiopia? 🌱",
    "sent_at": "2026-02-04T10:10:00Z"
  },
  "metadata": {
    "context_used": {
      "episodic_memory_count": 3,
      "semantic_memory_count": 5,
      "soul_md_sections": ["backstory", "voice_traits", "core_beliefs"]
    },
    "relevance_score": 0.88,
    "sentiment_score": 0.75
  }
}
```

## MCP Dependencies

**Resources Used:**
- `mcp://memory/{agent_id}/recent` (episodic, last 1 hour from Redis)
- `mcp://memory/{agent_id}/semantic` (long-term, Weaviate vector search)
- `mcp://twitter/user/{user_id}/profile`

**Tools Used:**
- `twitter.reply_tweet`
- `instagram.reply_comment`
- `twitter.send_dm`

**Reference:** SRS Section 4.1 (FR 1.1), `specs/technical.md` Section 3

## Implementation Notes

- Hierarchical memory retrieval: episodic (Redis) + semantic (Weaviate)
- Context assembly includes SOUL.md sections, conversation history, user profile
- Sentiment analysis for appropriate tone
- Relevance scoring for Judge validation
- Judge verifies safety and brand alignment before tool execution
