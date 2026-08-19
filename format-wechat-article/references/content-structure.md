# Content Structure

Convert the source into a small semantic model before styling it.

## Node Types

| Node | Use | Guardrail |
|---|---|---|
| title | Article headline | Exactly one; preserve wording |
| standfirst | Short opening summary or lead | Derive only when the user allows copy editing |
| section | Numbered or named major section | Preserve order and numbering |
| paragraph | Main explanation | Split only at semantic boundaries |
| list | Parallel items, causes, steps, examples | Do not convert unrelated prose into a list |
| quote | Source quotations or core thesis | Preserve attribution and wording |
| definition | A term and concise explanation | Use only for genuine concepts |
| process | Ordered mechanism or workflow | Keep causality and sequence explicit |
| callout | Key point, warning, example, or takeaway | Limit to roughly one per section |
| figure | Supplied image plus optional caption | Place near the first relevant discussion |
| conclusion | Closing synthesis or action | Preserve the article's final intent |

## Analysis Pass

1. Record the exact title and heading hierarchy.
2. Mark paragraphs that define a term, explain a mechanism, enumerate causes, or warn about a limitation.
3. Match each supplied image by visible subject, not filename order alone.
4. Decide which passages deserve a visual component. Most paragraphs should remain normal reading text.
5. Check that every source block appears exactly once in the layout plan.

## Image Placement

- Use the strongest overview image after the lead or before the first major section.
- Place process diagrams immediately before or after the process explanation.
- Place RAG, verification, or safety imagery near hallucination or reliability sections.
- Place tool/context imagery near prompt, context, Agent, or retrieval discussions.
- Avoid stacking multiple wide images without explanatory text between them.
- Use captions for interpretation or source credit, not to repeat the heading.

## Preservation Check

Before delivery, compare source and layout in order. Confirm:

- no heading, paragraph, list item, quotation, caveat, or conclusion disappeared;
- no factual statement was strengthened, weakened, or newly attributed;
- highlighted pull quotes are exact source text unless labeled as an editorial summary;
- typography changes do not imply a new hierarchy or meaning.

