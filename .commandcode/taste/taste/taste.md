# Taste
- When a config file is involved, prefers the assistant to hand back the complete, ready-to-paste file (whole file to replace) rather than snippets with "insert this above/below" instructions. Confidence: 0.6
- Dislikes vague, generic form error messages (e.g. "Please check the inputs and try again"); expects the actual validation error surfaced next to the offending field with that field highlighted. Confidence: 0.7
- Prefers confirmation/result screens compact and centered so the whole card fits in the viewport without page scrolling, rather than large headings and tall layouts. Confidence: 0.6
- Prefers plain white page backgrounds — avoid tinted canvas colors, decorative gradients, and background grid textures. Confidence: 0.55
- Wants styling change requests kept narrowly scoped: when asked to change one thing (e.g. the page background), leave the rest of the design — card colors, accents, surfaces — untouched. Confidence: 0.65
- Keep virtualenv directories (`.venv/`, `venv/`) out of git entirely — never committed or staged, always gitignored. Confidence: 0.65
- Prefers minimal, product-like cards: no price/fee metadata or extra footer rows in a selection card — just icon, title, and a short description, with a subtle arrow affordance. Confidence: 0.5
