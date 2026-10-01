# Captain ETA — Design notes

A working tool for operators and masters, not a showcase. Every element must earn its place.

## Principles
- **Data first.** Numbers are the product: monospaced (IBM Plex Mono), tabular, right-aligned in tables.
- **One accent.** Navy blue (`#0b4f8c` light / `#6ea6dd` dark) for primary action and focus only. Amber is reserved for estimated values.
- **No decoration.** No gradients, glows, glass, emojis or animated flourishes. Flat surfaces, 1px borders, 8px card radius, 5px control radius.
- **Plain language.** Industry terms (ETD, ETA, LT, sea margin, WP/AGW), sentence case, no marketing copy.
- **Light and dark.** Follows the OS setting; toggle stored per browser. Dark mode is for bridge/night use — low contrast surfaces, no bright fills.

## Type
- UI: IBM Plex Sans 14px, 500/600 for labels and headings.
- Figures: IBM Plex Mono.

## Layout
- Desktop: inputs (Voyage, Route, Bunkers) left; sticky summary right; passage schedule full width below.
- ≤980px: single column. ≤640px: route rows wrap into two lines.
