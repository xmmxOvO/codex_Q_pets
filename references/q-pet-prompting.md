# Q Pet Prompting

Use this reference when turning real human portrait photos into a chibi Codex desktop pet.

## Identity Extraction

Extract only identity markers that survive at `192x208`:

- hair shape, length, color, and parting
- glasses, beard, mole, or other strong facial marker
- iconic clothing silhouette and color
- one accessory such as watch, necklace, hat, headphones, or bag
- overall energy: calm, playful, coach-like, scholarly, creator-like, focused

Avoid fragile details:

- tiny brand logos
- printed text
- complex jewelry
- realistic muscle definition
- subtle makeup
- photo lighting, lens distortion, or background context

## Base Prompt Pattern

Use this shape for the base job when the generated prompt needs reinforcement:

```text
Create one centered full-body Q-version Codex desktop pet sprite based on the attached real portrait photos.

Identity markers: <hair>, <glasses/accessories>, <outfit>, <body/energy>, <one small accessory>.
Style reference: <optional Q/chibi reference image role>.

Make the subject a cute chibi digital pet, not a realistic person. Compact body, oversized expressive head, friendly face, tiny limbs, thick dark pixel-style 1-2 px outline, visible stepped pixel edges, limited palette, flat cel shading.

Output one complete full-body sprite pose only on a perfectly flat pure #00FFFF chroma-key background. No scenery, text, labels, border, shadow, glow, detached effects, floor, checkerboard transparency, or extra props.
```

## Row Prompt Reinforcement

When a row drifts, prepend a short identity lock:

```text
Identity lock: same individual as the canonical base. Preserve the exact head shape, hair silhouette, glasses, face proportions, outfit, accessory side, palette, outline weight, and compact chibi proportions. Only change the pose for this animation row.
```

For portrait-based pets, keep each state simple:

- `idle`: blink and breathe only.
- `waving`: arm and hand pose only, no wave marks.
- `jumping`: body height and pose only, no shadows or dust.
- `failed`: slumped shoulders or attached tears only, no red X or floating symbols.
- `waiting`: subtle weight shift and blink.
- `running`: in-place busy energy, not literal travel.
- `review`: focused expression, head tilt, hand near chin; no new props.

## Visual Acceptance

Reject a generated row if:

- it looks like a different person from the base
- glasses, hair, or signature outfit disappear
- there are visible layout guide lines or boxes
- the character overlaps frame slots
- the background is not removable chroma key
- shadows, floor patches, text, scenery, or detached effects appear
- body parts are cropped

Prefer one clean, slightly less dynamic row over a flashy row that breaks the pet contract.
