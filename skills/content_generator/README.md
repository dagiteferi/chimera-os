# Skill: content_generator

**Skill ID:** `content_generator`  
**Version:** 1.0.0  
**Last Updated:** 2026-02-04  
**Traceability:** SRS Section 4.3 (FR 3.0-3.2), Task 1 Report Section 3.1 (Worker)

## Description

Generates multimodal content (text, images, video) using MCP Tools, ensuring character consistency and brand alignment. Used by Worker Agent to create social media posts, images, and videos for campaigns.

## Use Case

Worker Agent invokes this skill when:
- Task requires content generation (text, image, video, or multimodal)
- Campaign goals specify content creation
- Planner assigns content generation task

## Input Contract

See `input_schema.json` for full JSON Schema definition.

**Example Input:**
```json
{
  "skill_name": "content_generator",
  "parameters": {
    "content_type": "multimodal",
    "platform": "instagram",
    "topic": "Sustainable Fashion Trends",
    "persona_constraints": ["Witty", "Sustainability-focused", "Gen-Z Slang"],
    "character_reference_id": "agent-123-character-lora",
    "tier": "hero",
    "budget_limit_usdc": 25.00
  }
}
```

## Output Contract

See `output_schema.json` for full JSON Schema definition.

**Example Output:**
```json
{
  "content": {
    "text": "🔥 Sustainable fashion is the future! Check out these eco-friendly trends taking over Ethiopia! 🌱✨ #SustainableFashion #EthiopiaFashion",
    "image_url": "https://cdn.chimera.ai/generated/agent-123/image-456.jpg",
    "video_url": null,
    "platform": "instagram",
    "disclosure_level": "automated"
  },
  "metadata": {
    "generated_at": "2026-02-04T10:05:00Z",
    "generation_cost_usdc": 12.50,
    "character_consistency_score": 0.95,
    "brand_alignment_score": 0.91
  }
}
```

## MCP Dependencies

**Tools Used:**
- `mcp-server-ideogram.generate_image` (or `mcp-server-midjourney`)
- `mcp-server-runway.generate_video` (or `mcp-server-luma`)
- Native LLM (Gemini 3 Pro / Claude Opus) for text generation

**Reference:** SRS Section 4.3 (FR 3.0), `specs/technical.md` Section 1.4

## Implementation Notes

- Character consistency enforced via `character_reference_id` (LoRA)
- Tier-based video generation (Tier 1: Image-to-Video, Tier 2: Text-to-Video)
- Budget tracking via CFO Judge validation
- Judge validates character consistency before approval
