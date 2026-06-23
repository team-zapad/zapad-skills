# Frontend & tooling

UI layer, client patterns, and code-quality tooling for the stack.

## TanStack Start / Router / Query

- File-based routes. Use `beforeLoad` for redirect-style gating and route context — **not** for security (see the auth reference: server functions are the boundary).
- Data comes from loaders + TanStack Query, both of which ship with Start. Don't add a separate data-fetching library.
- Server functions (`createServerFn`) are the only API layer. The client calls them like typed functions; there is no REST contract to maintain.

## MUI + Tailwind

- MUI for complex interactive components (data grids, date pickers, autocomplete, dialogs).
- Tailwind for layout and one-off styling.
- Don't fight MUI's Emotion runtime with Tailwind on the *same* element — pick one styling system per component.

## Forms — TanStack Form

- Pair with Zod validators. The same Zod schema that validates the server-function input also drives the form (see `data.md`, invariant #2) — define it once.

## Biome

- Single `biome.json`, one command for lint + format. Do **not** add ESLint or Prettier alongside it.

## Testing

- Vitest for units and server-function logic; Playwright for e2e including the auth round-trip.
- Test server functions directly — they are the security boundary, so they must be covered independently of the UI (see `auth.md`).
